import io
import os
from typing import Any, Optional

from groq import Groq, GroqError


class GroqWhisperClient:
    """
    A client for interacting with the Groq API for Whisper audio transcriptions.

    Handles API key management, different input types (bytes, stream, file),
    and provides methods for transcription.
    """
    DEFAULT_MODEL = "whisper-large-v3"
    DEFAULT_RESPONSE_FORMAT = "verbose_json" # Options: json, text, srt, verbose_json, vtt

    def __init__(self, api_key: Optional[str] = None, groq_client: Optional[Groq] = None) -> None:
        """
        Initializes the GroqWhisperClient.

        Args:
            api_key: The Groq API key. If not provided, attempts to read from
                     the GROQ_API_KEY environment variable.
            groq_client: An optional pre-configured Groq client instance.
                         If provided, the api_key argument is ignored.

        Raises:
            ValueError: If neither api_key nor GROQ_API_KEY env var is found,
                        and no groq_client is provided.
        """
        if groq_client:
            self.client = groq_client
        else:
            resolved_api_key = api_key or os.getenv("GROQ_API_KEY")
            if not resolved_api_key:
                raise ValueError("Groq API key must be provided either via the 'api_key' argument "
                                 "or the GROQ_API_KEY environment variable.")
            self.client = Groq(api_key=resolved_api_key)

    def _transcribe(self, file_tuple: tuple[str, bytes], model: str, response_format: str, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """
        Internal helper method for making the transcription API call.

        Args:
            file_tuple: A tuple containing (filename, file_bytes).
            model: The Whisper model to use.
            response_format: The desired response format.
            **kwargs: Additional parameters for the Groq API call (e.g., prompt, temperature).

        Returns:
            A dictionary containing the transcription result from the Groq API.

        Raises:
            GroqError: If the API call fails.
        """
        try:
            # Ensure timestamp_granularities is a list if provided
            if "timestamp_granularities" in kwargs and isinstance(kwargs["timestamp_granularities"], str):
                kwargs["timestamp_granularities"] = [kwargs["timestamp_granularities"]]

            transcription = self.client.audio.transcriptions.create(
                file=file_tuple,
                model=model,
                response_format=response_format,
                **kwargs
            )
            # Assuming the response object has a model_dump() method (common in Pydantic v2+)
            # or dict() for older Pydantic/other objects. Fallback to returning the object itself.
            if hasattr(transcription, 'model_dump'):
                return transcription.model_dump()
            elif hasattr(transcription, 'dict'):
                return transcription.dict()
            else:
                # If it's not a Pydantic model or similar, it might be dict-like already
                # This might need adjustment based on the actual type returned by groq-python
                return dict(transcription)
        except GroqError as e:
            # Consider logging the error here
            print(f"Groq API error during transcription: {e}")
            raise # Re-raise the exception for the caller to handle
        except Exception as e:
            # Catch other unexpected errors during the API call
            print(f"An unexpected error occurred during transcription: {e}")
            raise


    def transcribe_bytes(self, audio_bytes: bytes, filename: str = "audio.mp3", model: Optional[str] = None, response_format: Optional[str] = None,
    **kwargs: dict[str, Any]) -> dict[str, Any]:
        """
        Transcribes audio provided as bytes.

        Args:
            audio_bytes: The audio data as bytes.
            filename: The filename to associate with the bytes (required by Groq API).
                      Defaults to "audio.mp3".
            model: The Whisper model to use (e.g., 'whisper-large-v3').
                   Defaults to the class default (DEFAULT_MODEL).
            response_format: The desired response format (e.g., 'verbose_json').
                             Defaults to the class default (DEFAULT_RESPONSE_FORMAT).
            **kwargs: Additional parameters for the Groq API call (e.g., prompt,
                      temperature, language, timestamp_granularities=['word']).

        Returns:
            A dictionary containing the transcription result.

        Raises:
            GroqError: If the API call fails.
            ValueError: If input arguments are invalid.
        """
        if not isinstance(audio_bytes, bytes):
            raise ValueError("audio_bytes must be of type bytes.")
        if not filename:
             raise ValueError("filename cannot be empty.")

        effective_model = model or self.DEFAULT_MODEL
        effective_response_format = response_format or self.DEFAULT_RESPONSE_FORMAT

        return self._transcribe(
            file_tuple=(filename, audio_bytes),
            model=effective_model,
            response_format=effective_response_format,
            **kwargs
        )

    def transcribe_stream(self, audio_stream: io.BytesIO, filename: str = "audio.mp3", model: Optional[str] = None,
    response_format: Optional[str] = None, **kwargs: dict[str, Any]) -> dict[str, Any]:
         """
         Transcribes audio provided as a BytesIO stream.

         The stream will be read to its end. Consider stream position if reusing.

         Args:
            audio_stream: The audio data as a BytesIO stream.
            filename: The filename to associate with the stream data. Defaults to "audio.mp3".
            model: The Whisper model to use. Defaults to the class default.
            response_format: The desired response format. Defaults to the class default.
            **kwargs: Additional parameters for the Groq API call.

        Returns:
            A dictionary containing the transcription result.

        Raises:
            GroqError: If the API call fails.
            ValueError: If input arguments are invalid.
            TypeError: If audio_stream is not a BytesIO object.
         """
         if not isinstance(audio_stream, io.BytesIO):
             raise TypeError("audio_stream must be an instance of io.BytesIO.")
         if not filename:
             raise ValueError("filename cannot be empty.")

         # Consider adding stream position handling if necessary, e.g.:
         # original_position = audio_stream.tell()
         # audio_stream.seek(0)
         audio_bytes = audio_stream.read()
         # audio_stream.seek(original_position) # Restore position if needed elsewhere

         effective_model = model or self.DEFAULT_MODEL
         effective_response_format = response_format or self.DEFAULT_RESPONSE_FORMAT

         return self._transcribe(
             file_tuple=(filename, audio_bytes),
             model=effective_model,
             response_format=effective_response_format,
             **kwargs
         )

    def transcribe_file(self, file_path: str, model: Optional[str] = None, response_format: Optional[str] = None, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """
        Transcribes audio from a local file path.

        Args:
            file_path: The path to the audio file.
            model: The Whisper model to use. Defaults to the class default.
            response_format: The desired response format. Defaults to the class default.
            **kwargs: Additional parameters for the Groq API call.

        Returns:
            A dictionary containing the transcription result.

        Raises:
            FileNotFoundError: If the file does not exist at file_path.
            GroqError: If the API call fails.
            ValueError: If file_path is empty.
        """
        if not file_path:
            raise ValueError("file_path cannot be empty.")

        effective_model = model or self.DEFAULT_MODEL
        effective_response_format = response_format or self.DEFAULT_RESPONSE_FORMAT
        filename = os.path.basename(file_path)
        if not filename:
             raise ValueError(f"Could not determine filename from path: {file_path}")

        try:
            with open(file_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
                return self._transcribe(
                    file_tuple=(filename, audio_bytes),
                    model=effective_model,
                    response_format=effective_response_format,
                    **kwargs
                )
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            raise
        except OSError as e:
            print(f"Error reading file at {file_path}: {e}")
            raise # Re-raise IO errors
