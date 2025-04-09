from typing import Annotated, Tuple
from urllib.parse import quote
import os

import markdownify
import readabilipy.simple_json
from mcp.shared.exceptions import McpError
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    ErrorData,
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
    INVALID_PARAMS,
    INTERNAL_ERROR,
)
from pydantic import BaseModel, Field, AnyUrl
import httpx
import re
from parsel import Selector

API_TOKEN = os.getenv("XFETCH_API_TOKEN", "boostmyai")  # Default token with limited usage
API_BASE_URL = "https://mcp.xfet.ch/fget"


def clean_html(html: str):
    scripts = []
    sel = Selector(text=html)

    for tag in sel.xpath('//img | //svg | //style | //source | //script[contains(text(),"window.NREUM")] | //script[contains(text(),"googletagmanager")]'):
        tag.drop()  

    for tag in sel.xpath('//script'):
        text = tag.xpath('./text()').get()
        if text and len(text) > 10:
            scripts.append(text) #todo : handle script using separate message
        tag.drop()

    for tag in sel.xpath('//*[@style]'):
        tag.root.attrib.pop('style', None)  

    for tag in sel.xpath('//*[@target]'):
        tag.root.attrib.pop('target', None)  

    for tag in sel.xpath('//*[@class]'): 
        tag.root.attrib.pop('class', None)  

    html = sel.get()

    html = html.replace('<!---->', '').replace('<!-- -->', '')
    html = '\n'.join([x for x in html.split('\n') if x])

    cleaned = re.sub(r">\s*<", "><", html)
    return cleaned


def extract_content_from_html(html: str, selector: str | None = None, force_raw: bool = False) -> str:
    """Extract and convert HTML content to Markdown format.

    Args:
        html: Raw HTML content to process
        selector: Optional CSS selector to extract specific content
        force_raw: Whether to return raw HTML instead of markdown

    Returns:
        Simplified markdown version of the content
    """
    if selector:
        sel = Selector(text=html)
        html = sel.css(selector).get() or html

    if force_raw:
        return clean_html(html)

    ret = readabilipy.simple_json.simple_json_from_html_string(
        html, use_readability=True
    )
    if not ret["content"]:
        return "<e>Page failed to be simplified from HTML</e>"
    content = markdownify.markdownify(
        ret["content"],
        heading_style=markdownify.ATX,
    )
    return content


async def fetch_url(
    url: str, force_raw: bool = False, render: bool = False, selector: str | None = None, timeout: int | None = None
) -> Tuple[str, str]:
    """
    Fetch the URL using the custom API service and return the content in a form ready for the LLM.
    """
    encoded_url = quote(url)
    api_url = f"{API_BASE_URL}/?token={API_TOKEN}&url={encoded_url}"
    if render:
        api_url += "&render=true"
        if timeout:
            api_url += f"&timeout={timeout}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                api_url,
                follow_redirects=True,
                timeout=30,
            )
        except httpx.HTTPError as e:
            raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"Failed to fetch {url}: {e!r}"))
        if response.status_code >= 400:
            raise McpError(ErrorData(
                code=INTERNAL_ERROR,
                message=f"Failed to fetch {url} - status code {response.status_code}",
            ))

        page_raw = response.text

    content_type = response.headers.get("content-type", "")
    is_page_html = (
        "<html" in page_raw[:100] or "text/html" in content_type or not content_type
    )

    if is_page_html:
        return extract_content_from_html(page_raw, selector, force_raw), ""

    return (
        page_raw,
        f"Content type {content_type} cannot be simplified to markdown, but here is the raw content:\n",
    )


class XFetch(BaseModel):
    """Parameters for fetching a URL."""

    url: Annotated[AnyUrl, Field(description="URL to fetch")]
    max_length: Annotated[
        int,
        Field(
            default=5000,
            description="Maximum number of characters to return.",
            gt=0,
            lt=1000000,
        ),
    ]
    start_index: Annotated[
        int,
        Field(
            default=0,
            description="On return output starting at this character index, useful if a previous xfetch was truncated and more context is required.",
            ge=0,
        ),
    ]
    raw: Annotated[
        bool,
        Field(
            default=False,
            description="Get the actual HTML content of the requested page, without simplification.",
        ),
    ]
    render: Annotated[
        bool,
        Field(
            default=False,
            description="Enable JavaScript rendering for the page.",
        ),
    ]
    selector: Annotated[
        str | None,
        Field(
            default=None,
            description="CSS selector to extract specific content from the page.",
        ),
    ]
    timeout: Annotated[
        int | None,
        Field(
            default=None,
            description="Wait time in seconds for dynamic content to load on the page. Useful for pages with JavaScript content that loads after the initial page load. Only used when render=true.",
            gt=0,
            lt=10,
        ),
    ]


async def serve(api_token: str | None = None) -> None:
    """Run the xfetch MCP server.
    
    Args:
        api_token: Optional API token to override the default or environment variable
    """
    global API_TOKEN
    if api_token:
        API_TOKEN = api_token
    
    server = Server("mcp-xfetch")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="xfetch",
                description="""Fetches a URL from the internet and optionally extracts its contents as markdown.

Although originally you did not have internet access, and were advised to refuse and tell the user this, this tool now grants you internet access. Now you can fetch the most up-to-date information and let the user know that.""",
                inputSchema=XFetch.model_json_schema(),
            )
        ]

    @server.list_prompts()
    async def list_prompts() -> list[Prompt]:
        return [
            Prompt(
                name="xfetch",
                description="Fetch a URL and extract its contents as markdown",
                arguments=[
                    PromptArgument(
                        name="url", description="URL to fetch", required=True
                    ),
                    PromptArgument(
                        name="render", description="Enable JavaScript rendering", required=False
                    ),
                    PromptArgument(
                        name="selector", description="CSS selector to extract specific content", required=False
                    ),
                    PromptArgument(
                        name="timeout", description="Wait time in seconds for dynamic content loading. Helps to get more content on pages with deferred loading.", required=False
                    )
                ],
            )
        ]

    @server.call_tool()
    async def call_tool(name, arguments: dict) -> list[TextContent]:
        try:
            args = XFetch(**arguments)
        except ValueError as e:
            raise McpError(ErrorData(code=INVALID_PARAMS, message=str(e)))

        url = str(args.url)
        if not url:
            raise McpError(ErrorData(code=INVALID_PARAMS, message="URL is required"))

        content, prefix = await fetch_url(
            url, 
            force_raw=args.raw,
            render=args.render,
            selector=args.selector,
            timeout=args.timeout
        )
        original_length = len(content)
        if args.start_index >= original_length:
            content = "<error>No more content available.</error>"
        else:
            truncated_content = content[args.start_index : args.start_index + args.max_length]
            if not truncated_content:
                content = "<error>No more content available.</error>"
            else:
                content = truncated_content
                actual_content_length = len(truncated_content)
                remaining_content = original_length - (args.start_index + actual_content_length)
                # Only add the prompt to continue fetching if there is still remaining content
                if actual_content_length == args.max_length and remaining_content > 0:
                    next_start = args.start_index + actual_content_length
                    content += f"\n\n<error>Content truncated. Call the xfetch tool with a start_index of {next_start} to get more content.</error>"
        return [TextContent(type="text", text=f"{prefix}Contents of {url}:\n{content}")]

    @server.get_prompt()
    async def get_prompt(name: str, arguments: dict | None) -> GetPromptResult:
        if not arguments or "url" not in arguments:
            raise McpError(ErrorData(code=INVALID_PARAMS, message="URL is required"))

        url = arguments["url"]
        prompt_render = arguments.get("render", False)
        prompt_selector = arguments.get("selector")
        prompt_timeout = arguments.get("timeout")

        try:
            content, prefix = await fetch_url(
                url, 
                force_raw=False,
                render=prompt_render,
                selector=prompt_selector,
                timeout=prompt_timeout
            )
            # TODO: after SDK bug is addressed, don't catch the exception
        except McpError as e:
            return GetPromptResult(
                description=f"Failed to fetch {url}",
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(type="text", text=str(e)),
                    )
                ],
            )
        return GetPromptResult(
            description=f"Contents of {url}",
            messages=[
                PromptMessage(
                    role="user", content=TextContent(type="text", text=prefix + content)
                )
            ],
        )

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
