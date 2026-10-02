# Medical Image Assistant

A multimodal medical AI assistant built to process images, typed queries, and audio interactions locally or using GPU-accelerated models (such as LLaVA). It integrates speech-to-text (Whisper) and text-to-speech (gTTS) capabilities for complete voice-controlled interactions.

---

## Getting Started

### 1. Installation

For a standard setup with GPU support:
```bash
pip install -r requirements.txt
For a CPU-only computer, install the smaller image model and packages instead:Bashpython -m pip install -r requirements-cpu.txt
python app.py --cpu
Note: The CPU requirements also install Whisper, packaged FFmpeg, and gTTS for voice controls. Typed questions and image responses can still be used without these optional voice features.2. VS Code SetupSelect the .venv interpreter in VS Code using Python: Select Interpreter.Use Run and Debug with one of the included launch configurations, or run the commands below directly in the integrated terminal.RunExecute the application based on your setup:Bashpython app.py --demo       # Interface check, no AI inference
python app.py --cpu        # Real image response with smaller CPU model
python app.py              # Real LLaVA inference, requires supported GPU
Open http://127.0.0.1:7860 in your browser.Enter a question (or record audio), upload an image, and submit.Note: Submitting a question without an image will prompt you to upload one.Public Sharing (Optional)By default, the application runs locally only.Add --share to attempt generating a temporary public Gradio URL.If your network blocks Gradio sharing, an installed Cloudflare Tunnel can expose the running local app:Bashcloudflared tunnel --url [http://127.0.0.1:7860](http://127.0.0.1:7860)
⚠️ Warning: Anyone with a public link can submit images and text to your computer. Keep private medical records off public links. The URL stops working when the application or tunnel stops; neither option provides permanent hosting.Verify Without Downloading ModelsRun self-tests and validation checks prior to full model downloads:Bashpython app.py --self-test
python app.py --check
--self-test: Runs the input pipeline with local stand-ins to check text and voice paths, verify missing files, and ensure uploaded audio is not deleted. (Note: This does not prove that LLaVA, Whisper, or gTTS inference runs successfully on your machine).Run the real app with a sample image and audio to verify actual model paths after initial setup.TroubleshootingSymptomCheck / SolutionCUDA unavailableVerify your NVIDIA GPU and CUDA-enabled PyTorch installation using python app.py --check, or run the app via python app.py --cpu.Model download or Out of MemoryEnsure stable internet access and sufficient GPU memory (this is a large 7B model).Audio transcription failsCheck that imageio-ffmpeg is installed, or install system FFmpeg and confirm ffmpeg -version functions properly.Spoken reply failsDisable spoken replies or restore your internet connection (gTTS relies on an online service).VS Code uses the wrong PythonSelect the .venv interpreter explicitly, then reopen your terminal.
- [SmolVLM 256M model card](https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct)
- [Bitsandbytes installation and GPU support](https://huggingface.co/docs/bitsandbytes/installation)
- [Whisper installation and FFmpeg](https://github.com/openai/whisper#setup)
