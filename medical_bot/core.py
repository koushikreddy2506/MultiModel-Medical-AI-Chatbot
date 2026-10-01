"""Input orchestration, independent of Gradio and model packages."""

from pathlib import Path


DEFAULT_QUESTION = "Describe what is visible in this image."
NO_INPUT = "Enter a question, record audio, or upload an image."
NO_IMAGE = "Please upload an image to analyze."


def process_inputs(question, audio_path, image_path, speak, vision, transcriber, speech):
    """Return (transcript, response, generated_audio_path) for one request."""
    question = (question or "").strip()
    transcript = ""
    if audio_path:
        if not Path(audio_path).is_file():
            raise ValueError("Audio file was not found. Please upload it again.")
        transcript = transcriber.transcribe(audio_path).strip()

    user_prompt = " ".join(part for part in (question, transcript) if part)
    if not image_path:
        response = NO_IMAGE if user_prompt else NO_INPUT
        return transcript, response, None
    if not Path(image_path).is_file():
        raise ValueError("Image file was not found. Please upload it again.")

    response = vision.analyze(image_path, user_prompt or DEFAULT_QUESTION)
    audio_reply = speech.synthesize(response) if speak and response else None
    return transcript, response, audio_reply
