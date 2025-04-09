import pytest
from mcp_server_xfetch.server import XFetch, extract_content_from_html, clean_html
from pydantic import ValidationError


def test_xfetch_model_validation():
    # Test valid URL
    valid_data = {
        "url": "https://example.com",
        "max_length": 5000,
        "start_index": 0,
        "raw": False,
        "render": False,
        "selector": None,
        "timeout": None
    }
    xfetch = XFetch(**valid_data)
    assert str(xfetch.url) == "https://example.com"
    assert xfetch.max_length == 5000

    # Test invalid URL
    with pytest.raises(ValidationError):
        XFetch(url="not-a-url")

    # Test invalid max_length
    with pytest.raises(ValidationError):
        XFetch(url="https://example.com", max_length=-1)

    # Test invalid timeout
    with pytest.raises(ValidationError):
        XFetch(url="https://example.com", timeout=11)


def test_extract_content_from_html():
    html = """
    <html>
        <body>
            <h1>Test Title</h1>
            <p>Test paragraph</p>
        </body>
    </html>
    """
    content = extract_content_from_html(html)
    assert "Test Title" in content
    assert "Test paragraph" in content


def test_clean_html():
    html = """
    <html>
        <head>
            <script>alert('test')</script>
            <style>body { color: red; }</style>
        </head>
        <body>
            <div class="remove-me" style="color: blue;">
                <h1>Keep this</h1>
            </div>
        </body>
    </html>
    """
    cleaned = clean_html(html)
    assert "script" not in cleaned
    assert "style" not in cleaned
    assert "class=" not in cleaned
    assert "style=" not in cleaned
    assert "Keep this" in cleaned 