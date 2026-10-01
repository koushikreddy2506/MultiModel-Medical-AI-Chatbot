"""LLaVA, Whisper, and optional Google text-to-speech adapters."""

import tempfile
from pathlib import Path


MODEL_ID = "llava-hf/llava-1.5-7b-hf"


class LlavaVision:
    def __init__(self):
        import torch
        from transformers import AutoProcessor, BitsAndBytesConfig, LlavaForConditionalGeneration

        if not torch.cuda.is_available():
            raise RuntimeError(
                "LLaVA mode requires a CUDA-capable NVIDIA GPU. "
                "Use --demo to check the interface on this computer."
            )
        self.torch = torch
        self.processor = AutoProcessor.from_pretrained(MODEL_ID)
        self.model = LlavaForConditionalGeneration.from_pretrained(
            MODEL_ID,
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
            ),
            device_map="auto",
            dtype=torch.float16,
        )
        self.model.eval()

    def analyze(self, image_path, question):
        from PIL import Image

        # The model is a general vision-language model, not a medical device.
        conversation = [{
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": (
                    "Describe only what is visible. State uncertainty and do not give "
                    f"a diagnosis. Question: {question}"
                )},
            ],
        }]
        prompt = self.processor.apply_chat_template(conversation, add_generation_prompt=True)
        with Image.open(image_path) as source:
            image = source.convert("RGB")
        inputs = self.processor(text=prompt, images=image, return_tensors="pt")
        inputs = {key: value.to(self.model.device) for key, value in inputs.items()}
        if "pixel_values" in inputs:
            inputs["pixel_values"] = inputs["pixel_values"].to(self.torch.float16)
        with self.torch.inference_mode():
            generated = self.model.generate(**inputs, max_new_tokens=180, do_sample=False)
        new_tokens = generated[0, inputs["input_ids"].shape[1]:]
        answer = self.processor.decode(new_tokens, skip_special_tokens=True).strip()
        return answer.removeprefix("ASSISTANT:").strip() or "The model returned no answer."


class WhisperTranscriber:
    def __init__(self):
        import torch
        import whisper

        self.cuda = torch.cuda.is_available()
        self.model = whisper.load_model("base", device="cuda" if self.cuda else "cpu")

    def transcribe(self, audio_path):
        return self.model.transcribe(str(audio_path), fp16=self.cuda)["text"]


class GoogleSpeech:
    def synthesize(self, text):
        from gtts import gTTS

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as output:
            destination = Path(output.name)
        try:
            gTTS(text=text, lang="en").save(str(destination))
        except Exception:
            destination.unlink(missing_ok=True)
            raise
        return str(destination)


class DemoVision:
    def analyze(self, image_path, question):
        return (
            "DEMO MODE: The image and question reached the app. "
            "No model inference was performed. Start without --demo on a supported GPU."
        )


class DemoTranscriber:
    def transcribe(self, audio_path):
        return "[Demo mode: audio received; transcription was not performed]"
