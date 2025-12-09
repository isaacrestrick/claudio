# Claudio

Helping Claude Opus 4.5 hear the music.

MCP server for audio understanding via Google Gemini. Ask questions about audio files - describe music, transcribe lyrics, identify instruments, and more.

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A Google Gemini API key

## Quick Start

### 1. Get a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a new API key
3. Copy the key

### 2. Set Up the Environment

```bash
cd mcp

# Create .env file with your API key
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Install dependencies with uv
uv sync
```

### 3. Run the Server (Standalone Test)

```bash
cd mcp
uv run server.py
```

The server communicates via stdio, so you won't see output - it's waiting for MCP messages.

### 4. Configure Claude Code

Add to your Claude Code MCP config (`~/.claude/mcp.json` or project `.mcp.json`):

```json
{
  "mcpServers": {
    "claudio": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/claudio/mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```

Replace `/path/to/claudio/mcp` with the actual absolute path to the `mcp` directory.

### 5. Restart Claude Code

After updating the config, restart Claude Code to load the new MCP server.

## Usage

Once configured, you can ask Claude Code to analyze audio files:

```
Listen to ~/Music/song.mp3 and describe the genre and mood
```

```
What instruments are playing in this track?
```

```
Transcribe the lyrics from this audio file
```

### Available Tools

| Tool | Description |
|------|-------------|
| `listen_to_audio` | Start a new session with an audio file and ask a question |
| `ask_about_audio` | Ask follow-up questions using a session ID |

### Supported Audio Formats

- MP3 (`.mp3`)
- WAV (`.wav`)
- FLAC (`.flac`)
- AAC (`.aac`)
- OGG (`.ogg`)
- M4A (`.m4a`)
- WebM (`.webm`)
- AIFF (`.aiff`)
- MP4 audio (`.mp4`)

### Session Follow-ups

When you analyze an audio file, you get a session ID. Use it for follow-up questions:

```
First call returns: "Session ID: abc12345"

Then ask: "Using session abc12345, what's the tempo of that song?"
```

## File Size Handling

- Files under 20MB: Sent inline with the request
- Files over 20MB: Uploaded via Gemini Files API (expires after 48 hours)

## Troubleshooting

### "GEMINI_API_KEY not set"

Make sure your `.env` file exists in the `mcp/` directory and contains your API key.

### Server won't start

1. Check that `uv` is installed: `uv --version`
2. Ensure dependencies are installed: `cd mcp && uv sync`
3. Verify the path in your MCP config is correct

### Session not found

Sessions are stored in memory. They're lost when:
- The MCP server restarts
- Claude Code restarts
- Your terminal session ends

Just start a new session with `listen_to_audio`.

## Architecture

```
claudio/
├── mcp/
│   ├── server.py      # MCP server implementation
│   ├── pyproject.toml # Dependencies
│   ├── .env           # API key (create this)
│   └── .venv/         # Virtual environment (auto-created)
├── .mcp.json          # Example MCP config
└── README.md
```
