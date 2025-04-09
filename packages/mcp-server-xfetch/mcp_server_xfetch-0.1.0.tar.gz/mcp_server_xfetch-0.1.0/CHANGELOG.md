# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-04-08

### Added
- Initial release of XFetch
- Support for bypassing Cloudflare and other protection systems
- JavaScript rendering capability with timeout control
- CSS selector support for content extraction
- Dynamic content loading with configurable timeout
- Markdown conversion for HTML content
- Chunked reading support for long pages
- API token support for xfetch.ai service integration

### Changed
- Forked from original mcp-server-fetch
- Replaced direct HTTP requests with xfetch service
- Updated configuration to support new features
- Improved HTML cleaning and content extraction

### Removed
- Direct robots.txt handling (now handled by service)
- User-agent customization (now handled by service)
- Direct proxy support (now handled by service) 