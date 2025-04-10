# Element.fm MCP Server

This is the MCP server implementation for Element.fm, providing a command-line interface for interacting with the Element.fm API.

## Installation

You can install this package using pip:

```bash
pip install elementfm-mcp-server
```

## Configuration

Before using the server, you need to set up your API key as an environment variable:

```bash
export API_KEY=your_api_key_here
```

You can also optionally configure the frontend URL (defaults to https://app.element.fm):

```bash
export FRONTEND_ROOT_URL=https://your-custom-url.com
```

## Usage

Once installed, you can run the MCP server using:

```bash
elementfm-mcp stdio  # For standard I/O mode
# or
elementfm-mcp sse   # For Server-Sent Events mode
```

## Features

The MCP server provides the following functionality:

- Workspace management (create, list, get)
- Show management (create, list, get, update)
- Episode management (create, list, get, update, publish)
- AI features (transcription, chapter generation, show notes generation)
- Workspace invitations
- Recipient management
- Workspace search

## Development

To set up the development environment:

1. Clone the repository
2. Install dependencies: `pip install -e .`
3. Set up your API key as described in the Configuration section
4. Run the server in development mode: `python server.py stdio`

## License

MIT License