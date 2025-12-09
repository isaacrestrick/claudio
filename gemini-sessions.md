# Gemini Session Duration & Caching

## How Claudio Sessions Work

Claudio maintains sessions in two layers:

### 1. Local Session Storage (In-Memory)

Sessions are stored in a Python dictionary within the MCP server process:

```python
sessions: dict[str, tuple] = {}  # session_id -> (chat_session, uploaded_file)
```

**Duration:** Sessions persist as long as the MCP server process is running. When the server restarts, all sessions are lost.

### 2. Gemini Files API (For Large Audio Files)

For audio files >20MB, Claudio uploads them via Gemini's Files API.

**Duration:** Files uploaded via the Files API expire after **48 hours** automatically.

- Each file can be up to 2GB
- 20GB storage limit per project
- Files cannot be given a shorter TTL (this is a [known limitation](https://github.com/googleapis/python-genai/issues/1172))
- Files can be deleted programmatically before expiration

### 3. Gemini Chat History

Claudio uses Gemini's Chat API, which maintains conversation history client-side. The chat object stores all previous messages and sends them with each request.

**Duration:** The chat history persists as long as the local session exists (see #1 above).

## Gemini Context Caching (Not Used by Claudio)

For reference, Gemini also offers explicit context caching with different behavior:

| Feature | Default TTL | Configurable? | Min Tokens |
|---------|-------------|---------------|------------|
| Context Cache | 1 hour | Yes, no min/max bounds | 1,024 (2.5 Flash) / 4,096 (2.5 Pro) |
| Files API | 48 hours | No (can only delete early) | N/A |
| Implicit Cache | Automatic | No | N/A |

## Practical Implications

1. **Short-lived sessions:** If you restart Claude Code or the MCP server, your audio sessions are gone
2. **Re-upload needed:** For files uploaded via Files API, they'll expire after 48 hours
3. **No persistence:** Claudio doesn't persist sessions to disk - they're purely in-memory

## Sources

- [Gemini Files API Documentation](https://ai.google.dev/gemini-api/docs/files)
- [Gemini Context Caching](https://ai.google.dev/gemini-api/docs/caching)
- [Files API Reference](https://ai.google.dev/api/files)
