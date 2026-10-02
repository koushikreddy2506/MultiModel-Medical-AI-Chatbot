# Verification record

Checked on 2026-10-01 in the local Windows workspace with Python 3.12.14.

| Check | Result |
| --- | --- |
| `python app.py --self-test` | Passed 5 pipeline tests. |
| `python -m compileall -q app.py medical_bot tests` | Passed. |
| `python app.py --demo` | Started the Gradio interface at `http://127.0.0.1:7860`; HTTP GET returned 200. |
| Gradio `/respond` with no inputs | Returned the expected input prompt. |
| Gradio `/respond` with a generated image and typed question | Returned the explicit `DEMO MODE` response. |
| `python app.py --check` (initial) | Gradio and Pillow installed; PyTorch, Transformers, bitsandbytes, Whisper, gTTS, and FFmpeg absent before CPU setup. |
| CPU model load | SmolVLM 256M loaded from Hugging Face on this Windows CPU machine. |
| CPU image inference | A generated white image with a blue circle and the question “What shape and color is shown?” returned `A circle`. This confirms model inference ran, while showing that the answer can be incomplete. |
| Whisper audio path | Downloaded Whisper Base and processed a generated tone WAV through packaged FFmpeg without error; the transcript was empty, as expected for nonspeech audio. |
| gTTS audio path | Generated an MP3 from the nonpersonal phrase “This is a test.” |
| Temporary public tunnel | Cloudflare URL returned HTTP 200. An end-to-end request through it with a generated image and tone returned `Circle` and a spoken reply file. |
| `run-and-share.bat` | Executed the single-file Windows launcher. It installed/checked dependencies, started CPU mode on an available port, verified the tunnel, and printed a public URL. |

The LLaVA path was **not run** here because this machine has no accessible NVIDIA GPU. Whisper and gTTS were run with generated test data. The CPU image response is from a different small general vision model and is not a medical analysis. The tunnel URL is temporary and depends on this computer staying online.
