# Multimodal Skin Image Assistant

A research demonstration that lets a user ask a question by typing or speaking and upload a skin image. The app uses a vision-language model to describe visible features and respond to the question. It is **not a medical diagnostic tool** and must not be used to identify allergies, diagnose conditions, or make treatment decisions.

## What problem does it address?

People may want help describing what they see in a skin image or understanding what questions to ask a healthcare professional. This app demonstrates how text, image, and optional speech input can be combined in one interface.

For example, a user can upload a photo of a rash and ask, “What do you observe in this image?” The model may describe visible features, but it cannot reliably determine whether the rash is an allergy or identify its cause. Users should consult a qualified healthcare professional for medical advice.

## Features

- Accepts a typed question and an uploaded image.
- Supports optional speech transcription with Whisper.
- Supports optional spoken responses with Google Text-to-Speech.
- Offers a GPU mode with LLaVA 1.5 7B.
- Offers a CPU mode with the smaller SmolVLM 256M model.
- Provides demo mode to check the interface without running AI models.

## Technology stack

| Technology | Purpose |
|---|---|
| Python 3.10–3.12 | Main application language |
| Gradio | Web interface and input flow |
| LLaVA 1.5 7B | Image-and-text responses in GPU mode; approximately 7 billion parameters |
| SmolVLM 256M | Image-and-text responses in CPU mode; approximately 256 million parameters |
| CUDA-enabled PyTorch | Runs the GPU model on a supported NVIDIA GPU |
| Whisper Base | Optional speech-to-text transcription |
| FFmpeg / imageio-ffmpeg | Audio processing for speech transcription |
| gTTS | Optional text-to-speech; requires internet access |
| Cloudflare Tunnel or Gradio sharing | Optional temporary access to the locally running app |

The GPU and CPU modes use different models. The CPU model is smaller and may respond more slowly. Model weights are downloaded on first use and are not bundled with this repository.

## Requirements

### For GPU mode

- Python 3.10–3.12
- Git
- VS Code with the Python extension
- Supported NVIDIA GPU with enough VRAM for a 4-bit 7B model
- CUDA-enabled PyTorch
- Internet access on first run to download model weights

GPU availability, memory capacity, and performance depend on your computer.

### For CPU mode

- Python 3.10–3.12
- Git
- VS Code with the Python extension
- Internet access on first run to download SmolVLM weights

CPU mode uses a smaller model and is slower than GPU inference.

### Optional voice features

- Speech transcription downloads Whisper Base on first use.
- Audio processing uses system FFmpeg when available, or the packaged `imageio-ffmpeg` binary.
- Spoken responses use Google's text-to-speech service and require internet access.

## Setup

Open the project folder in VS Code and create a virtual environment.

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

### macOS or Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

In VS Code, select the `.venv` Python interpreter using **Python: Select Interpreter**.

## Install dependencies

### GPU mode with LLaVA

Install the CUDA-enabled PyTorch build that matches your system using the official PyTorch installation selector. Then install the project requirements:

```bash
python -m pip install -r requirements.txt
python app.py --check
```

### CPU mode with SmolVLM

```bash
python -m pip install -r requirements-cpu.txt
```

## Run the app

### Demo mode (no AI inference)

```bash
python app.py --demo
```

Demo mode checks the web interface and input flow. It clearly identifies its output as a demo and does not analyze images or transcribe speech.

### CPU mode

```bash
python app.py --cpu
```

### GPU mode

```bash
python app.py
```

After startup, open:

```text
http://127.0.0.1:7860
```

Enter a question, optionally record audio, upload an image, and submit it. A question without an image prompts the user to upload one.

## Optional public link

By default, the app is available only on your computer. To try a temporary Gradio sharing link:

```bash
python app.py --share
```

If Gradio sharing is blocked by your network, an installed Cloudflare Tunnel can be used:

```bash
cloudflared tunnel --url http://127.0.0.1:7860
```

A public link allows others to submit images and text to the computer running the app. Do not use public sharing with private medical images or records. The link is temporary and stops working when the app or tunnel stops; it is not permanent hosting.

## Verify the setup

Run the local checks:

```bash
python app.py --self-test
python app.py --check
```

`--self-test` checks the input pipeline using local stand-ins, including text and voice paths, missing files, and uploaded-audio handling. It does **not** verify actual LLaVA, Whisper, or gTTS inference. To verify those features, run the app with a sample image and audio after setup.

## Safety and limitations

- This project is a research demonstration, not a medical product.
- General vision-language models can misinterpret images and provide incorrect descriptions.
- The app cannot confirm a skin allergy, diagnose a rash, or recommend treatment.
- Do not use its responses to make medical decisions.
- Seek advice from a qualified healthcare professional for symptoms or concerns.
- Do not expose private medical images through a public link.
- Optional gTTS sends response text to Google's text-to-speech service.

## Troubleshooting

| Issue | What to check |
|---|---|
| CUDA is unavailable | Confirm you have a supported NVIDIA GPU and CUDA-enabled PyTorch, or run `python app.py --cpu`. |
| Model download fails or GPU runs out of memory | Check internet access and available GPU memory. The LLaVA model is large. |
| Audio transcription fails | Check that `imageio-ffmpeg` is installed or install system FFmpeg. |
| Spoken response fails | Check internet access or turn off the spoken-reply option. |
| VS Code uses the wrong Python | Select the `.venv` interpreter and reopen the terminal. |

## Project structure

```text
.
├── app.py
├── requirements.txt
├── requirements-cpu.txt
└── notebooks/
    └── original_colab.ipynb
```

The original notebook is preserved in `notebooks/original_colab.ipynb` with its previous outputs removed.

## GitHub

Before pushing, create an empty GitHub repository and replace the URL below with your repository URL:

```bash
git remote add origin https://github.com/YOUR-USER/YOUR-REPO.git
git push -u origin main
```

Do not commit virtual environments, downloaded model caches, or private medical images.

## References

- LLaVA model documentation
- SmolVLM 256M model card
- Bitsandbytes installation and GPU support
- Whisper installation and FFmpeg
