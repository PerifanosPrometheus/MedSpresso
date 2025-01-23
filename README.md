# MedSpresso

Extract structured information from clinical text using local LLMs.

## Features

- 🏥 Extract medications, diagnoses, and other clinical information
- 🚀 Uses Ollama for local LLM inference
- 🔒 Privacy-focused: all processing happens locally
- 🖥️ GPU acceleration support (Metal on Mac, CUDA on Linux)
- 📝 Customizable extraction prompts

## Installation

1. Install Ollama:
```bash
# On macOS
brew install ollama

# On Linux
curl -fsSL https://ollama.com/install.sh | sh
```

2. Install MedSpresso:
```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

1. Start Ollama:
```bash
ollama serve
```

2. Pull the model (in a new terminal):
```bash
ollama pull deepseek-r1:1.5b
```

3. List available models:
```bash
clinical-extract list-models
```

4. Run extraction:
```bash
clinical-extract extract \
    --input data/sample.txt \
    --model deepseek-r1:1.5b \
    --prompt-type medications \
    --format json
```

## Available Models

- `deepseek-r1:1.5b` - Fast, efficient model (recommended)
- `deepseek-r1:7b` - More accurate but slower
- `deepseek-r1:14b` - Best quality, requires more GPU memory

## Customization

You can customize extraction prompts in `prompts/extraction_prompts.yaml`:

```yaml
medications: |
  Extract medications from the following clinical text...

diagnoses: |
  Extract diagnoses from the following clinical text...
```

## Requirements

- Python 3.8+
- Ollama
- GPU recommended (Metal on Mac, CUDA on Linux)

## License

MIT
