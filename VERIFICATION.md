# Verification record

Checked on 2026-10-01 in the local Windows workspace with Python 3.12.14.

| Check | Result |
| --- | --- |
| `python app.py --self-test` | Passed 5 pipeline tests. |
| `python -m compileall -q app.py medical_bot tests` | Passed. |
| `python app.py --demo` | Started the Gradio interface at `http://127.0.0.1:7860`; HTTP GET returned 200. |
| Gradio `/respond` with no inputs | Returned the expected input prompt. |
| Gradio `/respond` with a generated image and typed question | Returned the explicit `DEMO MODE` response. |
| `python app.py --check` | Gradio and Pillow installed; PyTorch, Transformers, bitsandbytes, Whisper, gTTS, and FFmpeg absent in this environment. |

The real LLaVA/Whisper/gTTS inference path was **not run** here. This machine has no accessible NVIDIA GPU, and downloading model weights and CUDA dependencies was outside this verification. The demo response is intentionally not a medical analysis.
