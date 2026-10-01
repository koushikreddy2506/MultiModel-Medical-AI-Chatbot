"""Run the medical image assistant in VS Code or from a terminal."""

import argparse
import importlib.util
import shutil
import sys
import unittest
from pathlib import Path

from medical_bot.core import process_inputs


def check_environment():
    print(f"Python: {sys.version.split()[0]}")
    for module in ("gradio", "torch", "transformers", "bitsandbytes", "whisper", "gtts", "PIL"):
        print(f"{module}: {'installed' if importlib.util.find_spec(module) else 'missing'}")
    print(f"ffmpeg: {shutil.which('ffmpeg') or 'missing'}")
    if importlib.util.find_spec("torch"):
        import torch
        print(f"CUDA: {'available' if torch.cuda.is_available() else 'unavailable'}")


def run_self_test():
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).parent / "tests"))
    return unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()


def build_interface(demo=False):
    import gradio as gr

    from medical_bot.services import (
        DemoTranscriber,
        DemoVision,
        GoogleSpeech,
        LlavaVision,
        WhisperTranscriber,
    )

    vision = DemoVision() if demo else LlavaVision()
    # Load Whisper only when an audio request is submitted.
    transcriber = DemoTranscriber() if demo else None
    speech = GoogleSpeech()

    def respond(question, audio_path, image_path, speak):
        nonlocal transcriber
        try:
            if audio_path and transcriber is None:
                transcriber = WhisperTranscriber()
            return process_inputs(
                question, audio_path, image_path, speak and not demo,
                vision, transcriber, speech,
            )
        except Exception as exc:
            raise gr.Error(str(exc)) from exc

    return gr.Interface(
        fn=respond,
        inputs=[
            gr.Textbox(label="Question (optional)", placeholder="What is visible in this image?"),
            gr.Audio(sources=["microphone", "upload"], type="filepath", label="Voice question (optional)"),
            gr.Image(type="filepath", label="Image"),
            gr.Checkbox(value=False, label="Generate spoken reply (requires internet)"),
        ],
        outputs=[
            gr.Textbox(label="Transcript"),
            gr.Textbox(label="Response"),
            gr.Audio(label="Spoken reply"),
        ],
        title="Medical Image Assistant" + (" — Demo Mode" if demo else ""),
        description=(
            "Research demonstration only. Descriptions may be incorrect. "
            "Do not use this app to diagnose, treat, or make medical decisions."
        ),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="launch without loading AI models")
    parser.add_argument("--check", action="store_true", help="report local prerequisites")
    parser.add_argument("--self-test", action="store_true", help="run dependency-free pipeline tests")
    parser.add_argument("--port", type=int, default=7860)
    args = parser.parse_args()
    if args.check:
        check_environment()
        return 0
    if args.self_test:
        return 0 if run_self_test() else 1
    try:
        build_interface(args.demo).launch(server_name="127.0.0.1", server_port=args.port, share=False)
    except (ImportError, RuntimeError) as exc:
        print(f"Cannot start: {exc}", file=sys.stderr)
        print("Run: python app.py --check", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
