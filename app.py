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
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg and importlib.util.find_spec("imageio_ffmpeg"):
        ffmpeg = "packaged via imageio-ffmpeg"
    print(f"ffmpeg: {ffmpeg or 'missing'}")
    if importlib.util.find_spec("torch"):
        import torch
        print(f"CUDA: {'available' if torch.cuda.is_available() else 'unavailable'}")


def run_self_test():
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).parent / "tests"))
    return unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()


def build_interface(mode="gpu"):
    import gradio as gr

    from medical_bot.services import (
        CpuVision,
        DemoTranscriber,
        DemoVision,
        GoogleSpeech,
        LlavaVision,
        WhisperTranscriber,
    )

    vision = {"gpu": LlavaVision, "cpu": CpuVision, "demo": DemoVision}[mode]()
    # Load Whisper only when an audio request is submitted.
    transcriber = DemoTranscriber() if mode == "demo" else None
    speech = GoogleSpeech()

    def respond(question, audio_path, image_path, speak):
        nonlocal transcriber
        try:
            if audio_path and transcriber is None:
                transcriber = WhisperTranscriber()
            return process_inputs(
                question, audio_path, image_path, speak and mode != "demo",
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
        title="Medical Image Assistant" + (" — Demo Mode" if mode == "demo" else ""),
        description=(
            "Research demonstration only. Descriptions may be incorrect. "
            "Do not use this app to diagnose, treat, or make medical decisions."
        ),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--demo", action="store_true", help="launch without loading AI models")
    modes.add_argument("--cpu", action="store_true", help="use the smaller SmolVLM model on CPU")
    parser.add_argument("--check", action="store_true", help="report local prerequisites")
    parser.add_argument("--self-test", action="store_true", help="run dependency-free pipeline tests")
    parser.add_argument("--port", type=int, default=7860)
    parser.add_argument("--share", action="store_true", help="create a temporary public Gradio link")
    args = parser.parse_args()
    if args.check:
        check_environment()
        return 0
    if args.self_test:
        return 0 if run_self_test() else 1
    try:
        mode = "demo" if args.demo else "cpu" if args.cpu else "gpu"
        build_interface(mode).launch(server_name="127.0.0.1", server_port=args.port, share=args.share)
    except (ImportError, RuntimeError) as exc:
        print(f"Cannot start: {exc}", file=sys.stderr)
        print("Run: python app.py --check", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
