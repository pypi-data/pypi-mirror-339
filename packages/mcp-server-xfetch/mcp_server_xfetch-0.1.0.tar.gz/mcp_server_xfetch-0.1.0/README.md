# XFetch MCP Server

[![PyPI version](https://badge.fury.io/py/mcp-server-xfetch.svg)](https://badge.fury.io/py/mcp-server-xfetch)
[![Python Versions](https://img.shields.io/pypi/pyversions/mcp-server-xfetch.svg)](https://pypi.org/project/mcp-server-xfetch/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Enhanced Model Context Protocol server for web content fetching (fetch on steroids). This server enables LLMs to retrieve and process content from any web pages, including those protected by Cloudflare and other security systems that regular fetch can't handle.

## Key Features

- 🚀 **Bypass Protection Systems**: Access content from websites protected by Cloudflare and other security systems
- 🌐 **JavaScript Rendering**: Fetch content from dynamic websites that require JavaScript execution
- 🎯 **CSS Selectors**: Extract specific content from web pages using CSS selectors
- ⏱️ **Dynamic Content Loading**: Wait for dynamic content to load before fetching
- 📝 **Markdown Conversion**: Automatically converts HTML to markdown for easier LLM consumption
- 🔄 **Chunked Reading**: Read long pages in chunks using start_index parameter

### Available Tools

- `xfetch` - Enhanced web content fetching tool with advanced capabilities
    - `url` (string, required): URL to fetch
    - `max_length` (integer, optional): Maximum number of characters to return (default: 5000)
    - `start_index` (integer, optional): Start content from this character index (default: 0)
    - `raw` (boolean, optional): Get raw content without markdown conversion (default: false)
    - `render` (boolean, optional): Enable JavaScript rendering for dynamic content (default: false)
    - `selector` (string, optional): CSS selector to extract specific content
    - `timeout` (integer, optional): Wait time in seconds for dynamic content loading (1-10 seconds)

### Prompts

- **xfetch**
  - Fetch a URL and extract its contents as markdown
  - Arguments:
    - `url` (string, required): URL to fetch
    - `render` (boolean, optional): Enable JavaScript rendering
    - `selector` (string, optional): CSS selector for content extraction
    - `timeout` (integer, optional): Dynamic content loading timeout

## Installation

### Using pip

```bash
pip install mcp-server-xfetch
```

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/), no specific installation is needed:

```bash
uvx mcp-server-xfetch
```

## Configuration

### Configure for Claude.app

Add to your Claude settings:

<details>
<summary>Using uvx (recommended)</summary>

```json
"mcpServers": {
  "xfetch": {
    "command": "uvx",
    "args": ["mcp-server-xfetch"]
  }
}
```
</details>

<details>
<summary>Using docker</summary>

```json
"mcpServers": {
  "xfetch": {
    "command": "docker",
    "args": ["run", "-i", "--rm", "mcp/xfetch"]
  }
}
```
</details>



### API Token

XFetch service offers two usage tiers:

#### Free Tier
The package includes a default API token that allows limited free usage. This is great for:
- Testing and evaluation
- Personal projects
- Small-scale non-commercial use

However, the free tier has rate limits and may have occasional stability issues.

#### Commercial/Production Use
For stable and reliable service, especially for:
- Commercial projects
- Production environments
- High-volume requests
- Guaranteed uptime and support

Visit [xfetch.ai](https://xfetch.ai) to:
1. Register for a commercial account
2. Get your dedicated API token
3. Access premium features and support

Once you have your token, you can set it up in one of these ways:

```bash
# Option 1: Environment variable (recommended)
export XFETCH_API_TOKEN=your_token_here
```

```bash
# Option 2: Command line argument
python -m mcp_server_xfetch --api-token=your_token_here
```

Or in your Claude configuration:
```json
"mcpServers": {
  "xfetch": {
    "command": "python",
    "args": ["-m", "mcp_server_xfetch", "--api-token=your_token_here"]
  }
}
```

## Examples

### Basic Usage
```python
# Simple fetch with markdown conversion
{
    "url": "https://example.com"
}
```

### JavaScript Rendering
```python
# Fetch from a dynamic website
{
    "url": "https://dynamic-site.com",
    "render": true,
    "timeout": 5  # Wait up to 5 seconds for content to load
}
```

### Content Extraction
```python
# Extract specific content using CSS selector
{
    "url": "https://news-site.com",
    "selector": "article.main-content",
    "render": true
}
```

### Reading Long Content
```python
# First request
{
    "url": "https://long-article.com",
    "max_length": 5000
}

# Continue reading from where it left off
{
    "url": "https://long-article.com",
    "start_index": 5000,
    "max_length": 5000
}
```

## Debugging

You can use the MCP inspector to debug the server:

```bash
npx @modelcontextprotocol/inspector uvx mcp-server-xfetch
```

## Contributing

We welcome contributions! Whether you want to add new features, fix bugs, or improve documentation, your help is appreciated.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: [xfetch.ai/docs](https://xfetch.ai/docs)
- Issues: [GitHub Issues](https://github.com/xfetchai/mcp-server-xfetch/issues)
- Email: xfetchai@gmail.com
