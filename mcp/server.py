#!/usr/bin/env python3
"""Claudio - MCP server for audio understanding via Gemini."""

import os
import uuid
import mimetypes
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize MCP server
mcp = FastMCP("claudio")

# Session storage: session_id -> (chat_session, uploaded_file)
sessions: dict[str, tuple] = {}

# Supported audio MIME types
SUPPORTED_MIME_TYPES = {
    ".wav": "audio/wav",
    ".mp3": "audio/mp3",
    ".mpeg": "audio/mpeg",
    ".mpga": "audio/mpeg",
    ".aiff": "audio/aiff",
    ".aac": "audio/aac",
    ".ogg": "audio/ogg",
    ".flac": "audio/flac",
    ".m4a": "audio/m4a",
    ".webm": "audio/webm",
    ".pcm": "audio/pcm",
    ".mp4": "audio/mp4",
}

# 20MB threshold for inline vs Files API
INLINE_SIZE_LIMIT = 20 * 1024 * 1024


def get_mime_type(file_path: str) -> str | None:
    """Get MIME type for an audio file."""
    ext = Path(file_path).suffix.lower()
    return SUPPORTED_MIME_TYPES.get(ext)


def generate_session_id() -> str:
    """Generate a short unique session ID."""
    return uuid.uuid4().hex[:8]


@mcp.tool()
async def listen_to_audio(file_path: str, question: str) -> str:
    """
    Start listening to an audio file and ask a question about it.
    Returns an answer along with a session_id for follow-up questions.

    Args:
        file_path: Path to a local audio file (mp3, wav, flac, etc.)
        question: Your question about the audio (e.g., "Describe this music",
                  "What instruments are playing?", "Transcribe the lyrics")
    """
    # Validate file exists
    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        return f"Error: File not found: {file_path}"

    # Get MIME type
    mime_type = get_mime_type(str(path))
    if not mime_type:
        supported = ", ".join(SUPPORTED_MIME_TYPES.keys())
        return f"Error: Unsupported audio format. Supported formats: {supported}"

    try:
        # Read audio file
        audio_bytes = path.read_bytes()
        file_size = len(audio_bytes)

        # Upload to Gemini
        if file_size > INLINE_SIZE_LIMIT:
            # Use Files API for large files
            uploaded_file = client.files.upload(
                file=path,
                config={"mime_type": mime_type}
            )
            audio_part = uploaded_file
        else:
            # Use inline data for smaller files
            audio_part = types.Part.from_bytes(
                data=audio_bytes,
                mime_type=mime_type
            )
            uploaded_file = None

        # Create chat session with audio context
        chat = client.chats.create(
            model="gemini-3-pro-preview",
            history=[
                types.Content(
                    role="user",
                    parts=[
                        audio_part,
                        types.Part.from_text(text="I'm sharing an audio file with you. Please listen to it carefully so you can answer questions about it.")
                    ]
                ),
                types.Content(
                    role="model",
                    parts=[types.Part.from_text(text="I've received and listened to the audio file. I'm ready to answer any questions you have about it - whether about the music, instruments, lyrics, mood, or any other aspects of the audio.")]
                )
            ]
        )

        # Send the actual question
        response = chat.send_message(question)
        answer = response.text

        # Store session
        session_id = generate_session_id()
        sessions[session_id] = (chat, uploaded_file)

        return f"{answer}\n\n---\nSession ID: {session_id}\n(Use this ID with ask_about_audio for follow-up questions)"

    except Exception as e:
        return f"Error communicating with Gemini: {str(e)}"


@mcp.tool()
async def ask_about_audio(session_id: str, question: str) -> str:
    """
    Ask a follow-up question about audio from an existing session.

    Args:
        session_id: Session ID from a previous listen_to_audio call
        question: Your follow-up question about the audio
    """
    if session_id not in sessions:
        return f"Error: Session '{session_id}' not found. Use listen_to_audio first to start a new session."

    try:
        chat, _ = sessions[session_id]
        response = chat.send_message(question)
        return response.text

    except Exception as e:
        return f"Error communicating with Gemini: {str(e)}"


if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "stdio")

    if transport == "http":
        # Hosted mode: HTTP transport for remote access
        # Set HOST=0.0.0.0 and PORT via environment variables
        mcp.run(transport="streamable-http")
    else:
        # Local mode: stdio transport (default)
        mcp.run()
