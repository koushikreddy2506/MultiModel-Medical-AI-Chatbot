# Medical Image Assistant

A VS Code ready version of the [original Colab notebook](https://colab.research.google.com/drive/1Q4tLQC8f0Rl3CDY-Iva_TXYcTl7D_LXC?usp=sharing). It accepts a typed or spoken question and an uploaded image. The default GPU mode uses the notebook's LLaVA 1.5 7B model. The `--cpu` mode uses the smaller SmolVLM 256M model for actual image responses on computers without a CUDA GPU. Whisper Base handles optional speech transcription, and gTTS can make an optional spoken reply. The original notebook is preserved in [`notebooks/original_colab.ipynb`](notebooks/original_colab.ipynb) with its previous outputs removed.

**Research demonstration only.** These are general vision models. Their descriptions can be wrong. Do not use this app for diagnosis, treatment, or medical decisions.

## Requirements

- Python 3.10–3.12, Git, and VS Code with the Python extension.
- For **LLaVA image analysis**: a supported NVIDIA GPU with enough VRAM for a 4-bit 7B model, CUDA-enabled PyTorch, and internet access on first run to download model weights. The model download is several GB. GPU capacity and performance vary; this repository does not bundle weights.
- For **CPU image responses**: install `requirements-cpu.txt` and run `--cpu`. This uses [SmolVLM 256M](https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct), a different, smaller model. It downloads its weights on first run and is slower on CPU.
- For **speech transcription**: Whisper Base is downloaded on first use. The app uses system [FFmpeg](https://github.com/openai/whisper#setup) when available, or the packaged `imageio-ffmpeg` binary.
- For **spoken replies**: internet access to Google's text-to-speech service. Leave the checkbox off for local text responses.

The `--demo` mode checks the web interface and input flow without loading AI models. It clearly labels its output as a demo and does not infer from the image or transcribe audio.

## Setup in VS Code

### One-click Windows launcher

Double-click [`run-and-share.bat`](run-and-share.bat), or run it in the VS Code terminal. It creates `.venv` if needed, installs the CPU app dependencies, starts the model, and prints a temporary public URL. It uses an installed `cloudflared` or downloads the official Windows binary into the ignored `.tools` folder. Keep the batch window open while using the link; press Enter in that window to stop the app and tunnel. First launch needs internet and can take several minutes to download model weights. Python 3.10–3.12 must already be installed.

The batch file starts the **SmolVLM CPU mode**. For the original 7B LLaVA mode on an NVIDIA GPU, follow the manual setup below.

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

For the original LLaVA mode, install the CUDA PyTorch build matching your system using the command from the [official PyTorch selector](https://pytorch.org/get-started/locally/). Then install all app dependencies:

```bash
python -m pip install -r requirements.txt
python app.py --check
```

For a CPU computer, install the smaller image model instead:

```bash
python -m pip install -r requirements-cpu.txt
python app.py --cpu
```

The CPU requirements also install Whisper, packaged FFmpeg, and gTTS for the voice controls. You can use typed questions and image responses without using those optional controls.

Select the `.venv` interpreter in VS Code using **Python: Select Interpreter**. Use **Run and Debug** with one of the included launch configurations, or run the commands below in the integrated terminal.

## Run

```bash
python app.py --demo       # interface check, no AI inference
python app.py --cpu        # real image response with smaller CPU model
python app.py              # real LLaVA inference, requires supported GPU
```

Open <http://127.0.0.1:7860>. Enter a question or record audio, upload an image, and submit. A question without an image produces a request to upload one. By default the app is local only. Add `--share` to attempt a temporary public Gradio URL. If your network blocks Gradio sharing, an installed [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/) can expose the running local app with `cloudflared tunnel --url http://127.0.0.1:7860`. Anyone with a public link can submit images and text to your computer. Keep private medical records off a public link. The URL stops working when the app or tunnel stops; neither option is permanent hosting.

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
- Made the notebook's public share URL opt-in with `--share`.
- Added a smaller CPU model path so image responses can run without CUDA.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `CUDA unavailable` | Verify an NVIDIA GPU and a CUDA-enabled PyTorch install with `python app.py --check`, or run `python app.py --cpu`. |
| Model download or out of memory | Ensure internet access and sufficient GPU memory; this is a large 7B model. |
| Audio transcription fails | Check that `imageio-ffmpeg` is installed, or install system FFmpeg and confirm `ffmpeg -version` works. |
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
- [SmolVLM 256M model card](https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct)
- [Bitsandbytes installation and GPU support](https://huggingface.co/docs/bitsandbytes/installation)
- [Whisper installation and FFmpeg](https://github.com/openai/whisper#setup)
