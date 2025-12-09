# Claudio

MCP server for audio understanding via Gemini. Ask questions about audio files - describe music, transcribe lyrics, identify instruments, and more.

## What is this?

Claudio is an [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that gives AI assistants like Claude the ability to listen to and analyze audio files. It uses Google's Gemini API for audio understanding.

**This is not a standalone CLI tool.** It's a server that MCP clients (like Claude Code or Claude Desktop) connect to.

## Setup

### 1. Get a Gemini API Key

Get an API key at [Google AI Studio](https://aistudio.google.com/apikey).

### 2. Add to your MCP client

**Claude Code:**
```bash
claude mcp add claudio -e GEMINI_API_KEY=your-key -- uvx claudio
```

**Claude Desktop / Manual config:**

Add to your MCP config file:
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

### `listen_to_audio`

Start listening to an audio file and ask a question about it.

| Parameter | Type | Description |
|-----------|------|-------------|
| `file_path` | string | Absolute path to a local audio file |
| `question` | string | Your question about the audio (e.g., "Describe this music", "Transcribe the lyrics") |

Returns an answer and a session ID for follow-up questions.

### `ask_about_audio`

Ask a follow-up question about audio from an existing session.

| Parameter | Type | Description |
|-----------|------|-------------|
| `session_id` | string | Session ID from a previous `listen_to_audio` call |
| `question` | string | Your follow-up question |

## Supported Formats

WAV, MP3, AIFF, AAC, OGG, FLAC

Files under 20MB are sent inline; larger files are uploaded via Gemini's Files API.
