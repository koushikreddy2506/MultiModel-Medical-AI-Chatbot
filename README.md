# Medical Image Assistant

A comprehensive multimodal medical AI assistant designed to process medical images, typed queries, and audio interactions. It supports both local CPU execution and high-performance GPU-accelerated models (such as LLaVA), and integrates speech-to-text (**Whisper**) and text-to-speech (**gTTS**) capabilities for fully voice-controlled clinical or experimental workflows.

---

## Key Features

* **Multimodal Analysis:** Upload medical imagery alongside text or voice questions to receive descriptive AI insights.
* **Flexible Hardware Support:** Run via heavy GPU acceleration or lightweight CPU modes depending on available hardware resources.
* **Voice-Enabled Interface:** Complete integration with Whisper for speech transcription and gTTS for spoken responses.
* **Gradio Web UI:** Interactive browser-based graphical user interface for easy session handling and media uploading.
* **Built-in Self-Testing & Diagnostic Tools:** Quick command-line arguments to verify pipelines, checks, and interface functionality prior to model deployment.

---

## Project Architecture & Tech Stack

* **Core AI Models:** LLaVA (Large Language and Vision Assistant) for image/text reasoning.
* **Audio Processing:** OpenAI Whisper for speech-to-text recognition; Google Text-to-Speech (gTTS) for output audio synthesis.
* **Interface:** Gradio framework powering the local web application dashboard.
* **Environment:** Python virtual environment (`.venv`) with modular requirements setup for GPU (`requirements.txt`) and CPU (`requirements-cpu.txt`) configurations.

---

## Getting Started & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/koushikreddy2506/MultiModel-Medical-AI-Chatbot.git](https://github.com/koushikreddy2506/MultiModel-Medical-AI-Chatbot.git)
cd MultiModel-Medical-AI-Chatbot
2. Python Environment & DependenciesCreate and activate your virtual environment, then install requirements based on your hardware capabilities:For GPU-Accelerated Systems (Standard Setup):Bashpip install -r requirements.txt
For CPU-Only Systems:Bashpython -m pip install -r requirements-cpu.txt
Note: CPU-based requirements include packages for Whisper, packaged FFmpeg, and gTTS. Typed queries and image analysis will function normally even if voice features are bypassed.   3. VS Code Configuration   Open the repository folder in VS Code.   Select your workspace .venv interpreter by opening the command palette (Ctrl+Shift+P / Cmd+Shift+P) and choosing Python: Select Interpreter.   Use your configured debug setup or run commands directly from the integrated terminal.   Running the ApplicationChoose the launch mode that best matches your testing phase or hardware profile:   Bashpython app.py --demo       # Launches the UI interface check without loading heavy AI models
python app.py --cpu        # Runs real inference using a smaller model optimized for CPU
python app.py              # Runs full LLaVA inference (requires a compatible CUDA GPU)
Once running:Open your browser and navigate to http://127.0.0.1:7860.Upload a medical image, then type a question or record audio to submit.Note: The system requires an image upload alongside your input query to generate a contextual response.   Optional Public Tunneling   By default, the application runs securely and locally on your machine.   Pass --share to generate a temporary public Gradio link.   Alternatively, if your network restricts Gradio sharing, you can expose the local port using Cloudflare Tunnel:   Bashcloudflared tunnel --url [http://127.0.0.1:7860](http://127.0.0.1:7860)
⚠️ Security Warning: Public sharing exposes the endpoint to anyone with the URL. Avoid sending sensitive, real-world private medical data over public temporary links.Verification & Self-TestsYou can validate components and environment integrity before triggering large model downloads:Bashpython app.py --self-test
python app.py --check
--self-test: Exercises input pipelines with placeholder stand-ins to confirm text/voice loops and file handling. (Does not substitute for checking actual model weights inference).--check: Validates environment settings, dependencies, and hardware compatibility.Troubleshooting GuideSymptom / ErrorRecommended Action / ResolutionCUDA unavailableConfirm your NVIDIA driver installation and CUDA-enabled PyTorch package via python app.py --check, or switch to CPU mode using python app.py --cpu.Out of Memory (OOM) / Model Download FailsEnsure a stable internet connection and verify that your hardware meets the memory requirements for large 7B model execution.Audio Transcription IssuesVerify that imageio-ffmpeg is properly installed, or check that system ffmpeg is available in your system path (ffmpeg -version).Spoken Output FailsCheck your network status; gTTS requires an active internet connection to synthesize speech chunks.VS Code Terminal ErrorsEnsure you have explicitly activated or selected the .venv Python interpreter before executing script commands.
