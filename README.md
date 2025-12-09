# Claudio

MCP server for audio understanding via Gemini. Ask questions about audio files - describe music, transcribe lyrics, identify instruments, and more.

## Usage

### Hosted (no setup required)

Add to your MCP config:

```json
{
  "mcpServers": {
    "claudio": {
      "url": "https://claudio.onrender.com/mcp"
    }
  }
}
```

### Local (bring your own API key)

1. Get a [Gemini API key](https://aistudio.google.com/apikey)
2. Configure MCP:

```json
{
  "mcpServers": {
    "claudio": {
      "command": "uv",
      "args": ["--directory", "/path/to/claudio/mcp", "run", "server.py"],
      "env": { "GEMINI_API_KEY": "your-key" }
    }
  }
}
```

## Tools

| Tool | Description |
|------|-------------|
| `listen_to_audio` | Analyze an audio file and ask a question |
| `ask_about_audio` | Follow-up questions using session ID |

Supports: MP3, WAV, FLAC, AAC, OGG, M4A, WebM, AIFF
