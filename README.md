# Claudio

MCP server for audio understanding via Gemini. Ask questions about audio files - describe music, transcribe lyrics, identify instruments, and more.

## Installation

```bash
uvx claudio
```

Or with Claude Code:

```bash
claude mcp add claudio -e GEMINI_API_KEY=your-key -- uvx claudio
```

## Configuration

Set the `GEMINI_API_KEY` environment variable. Get one at [Google AI Studio](https://aistudio.google.com/apikey).

### Claude Desktop / Claude Code

Add to your MCP config:

```json
{
  "mcpServers": {
    "claudio": {
      "command": "uvx",
      "args": ["claudio"],
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

Supports: WAV, MP3, AIFF, AAC, OGG, FLAC