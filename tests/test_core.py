import tempfile
import unittest
from pathlib import Path

from medical_bot.core import NO_IMAGE, NO_INPUT, process_inputs


class FakeVision:
    def analyze(self, path, question):
        return f"analyzed {Path(path).name}: {question}"


class FakeTranscriber:
    def transcribe(self, path):
        return "spoken question"


class FakeSpeech:
    def synthesize(self, text):
        return "reply.mp3"


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.image = Path(self.temp.name) / "image.png"
        self.audio = Path(self.temp.name) / "voice.wav"
        self.image.write_bytes(b"image fixture")
        self.audio.write_bytes(b"audio fixture")
        self.vision = FakeVision()
        self.transcriber = FakeTranscriber()
        self.speech = FakeSpeech()

    def run_request(self, question="", audio=None, image=None, speak=False):
        return process_inputs(question, audio, image, speak,
                              self.vision, self.transcriber, self.speech)

    def test_no_input(self):
        self.assertEqual(self.run_request(), ("", NO_INPUT, None))

    def test_text_without_image(self):
        self.assertEqual(self.run_request(question="hello"), ("", NO_IMAGE, None))

    def test_image_and_typed_question(self):
        self.assertEqual(self.run_request(question="What is shown?", image=self.image),
                         ("", "analyzed image.png: What is shown?", None))

    def test_voice_image_and_speech(self):
        result = self.run_request(question="please", audio=self.audio,
                                  image=self.image, speak=True)
        self.assertEqual(result, ("spoken question",
                                  "analyzed image.png: please spoken question", "reply.mp3"))
        self.assertTrue(self.audio.exists())

    def test_missing_image(self):
        with self.assertRaisesRegex(ValueError, "Image file was not found"):
            self.run_request(image=Path(self.temp.name) / "missing.png")


if __name__ == "__main__":
    unittest.main()
