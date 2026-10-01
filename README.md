# Medical Image Assistant

A VS Code ready version of the [original Colab notebook](https://colab.research.google.com/drive/1Q4tLQC8f0Rl3CDY-Iva_TXYcTl7D_LXC?usp=sharing). It accepts a typed or spoken question and an uploaded image. The real mode uses the notebook's LLaVA 1.5 7B model for image responses, Whisper Base for speech transcription, and optional gTTS for a spoken reply. The original notebook is preserved in [`notebooks/original_colab.ipynb`](notebooks/original_colab.ipynb) with its previous outputs removed.

**Research demo only.** LLaVA is a general vision model. Its descriptions can be wrong. Do not use this app for diagnosis, treatment, or medical decisions.

## Requirements

- Python 3.10–3.12, Git, and VS Code with the Python extension.
- For **real image analysis**: a supported NVIDIA GPU with enough VRAM for a 4-bit 7B model, CUDA-enabled PyTorch, and internet access on first run to download model weights. The model download is several GB. GPU capacity and performance vary; this repository does not bundle weights.
- For **speech transcription**: [FFmpeg](https://github.com/openai/whisper#setup) installed and on `PATH`. Whisper Base is downloaded on first use. Text plus image works without FFmpeg.
- For **spoken replies**: internet access to Google's text-to-speech service. Leave the checkbox off for local text responses.

The `--demo` mode checks the web interface and input flow without loading AI models. It clearly labels its output as a demo and does not infer from the image or transcribe audio.

## Setup in VS Code

Open the `medical-ai-assistant` folder in VS Code, open a terminal, and run:

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

For real mode, install the CUDA PyTorch build matching your system using the command from the [official PyTorch selector](https://pytorch.org/get-started/locally/). Then install the app dependencies:

```bash
python -m pip install -r requirements.txt
python app.py --check
```

Select the `.venv` interpreter in VS Code using **Python: Select Interpreter**. Use **Run and Debug** with one of the included launch configurations, or run the commands below in the integrated terminal.

## Run

```bash
python app.py --demo       # interface check, no AI inference
python app.py              # real LLaVA inference, requires supported GPU
```

Open <http://127.0.0.1:7860>. Enter a question or record audio, upload an image, and submit. A question without an image produces a request to upload one. The app binds only to the local computer and does not create a public Gradio share link.

### Verify without downloading models

```bash
python app.py --self-test
python app.py --check
```

`--self-test` runs the input pipeline with local stand-ins. It checks text and voice paths, missing files, and that uploaded audio is not deleted. It does **not** prove that LLaVA, Whisper, or gTTS inference runs on your machine. Run the real app with a sample image and audio to verify those paths after setup.

## What changed from Colab

- Moved `pip` and `apt-get` commands to project setup; there are no notebook shell commands in the app.
- Loads LLaVA once when real mode starts and loads Whisper only when audio is used.
- Added the typed question field described by the original UI, which the notebook did not actually provide.
- Leaves Gradio upload files alone; Gradio manages its temporary files.
- Makes voice reply optional because gTTS sends the response text to Google and needs internet.
- Uses deterministic generation and asks the general model to describe visible details and uncertainty.
- Disabled the notebook's `share=True` public URL.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `CUDA unavailable` | Verify an NVIDIA GPU and a CUDA-enabled PyTorch install with `python app.py --check`. Use `--demo` to check the UI on a CPU computer. |
| Model download or out of memory | Ensure internet access and sufficient GPU memory; this is a large 7B model. |
| Audio transcription fails | Install FFmpeg and confirm `ffmpeg -version` works in the same terminal. |
| Spoken reply fails | Disable spoken reply or restore internet access; gTTS is an online service. |
| VS Code uses the wrong Python | Select the `.venv` interpreter, then reopen the terminal. |

## Push to GitHub

This workspace already has an initial commit on `main`. To push it, create an empty GitHub repository and run:

```bash
git remote add origin https://github.com/YOUR-USER/YOUR-REPO.git
git push -u origin main
```

If you use the ZIP instead, extract it into a new folder and first create the local commit:

```bash
git init
git add .
git commit -m "Convert Colab medical assistant to local app"
git branch -M main
git remote add origin https://github.com/YOUR-USER/YOUR-REPO.git
git push -u origin main
```

Replace the remote URL with the URL of a repository you created on GitHub. Do not commit `.venv`, model caches, or private medical images.

## References

- [LLaVA model documentation](https://huggingface.co/docs/transformers/model_doc/llava)
- [Bitsandbytes installation and GPU support](https://huggingface.co/docs/bitsandbytes/installation)
- [Whisper installation and FFmpeg](https://github.com/openai/whisper#setup)
