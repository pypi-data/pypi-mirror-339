# DiffusionLM: Large Language Models with Diffusion

[![PyPI version](https://badge.fury.io/py/diffusion-llm.svg)](https://badge.fury.io/py/diffusion-llm)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

DiffusionLM is a novel approach to language modeling that combines transformer architectures with diffusion processes for high-quality text generation. This package provides a flexible and efficient implementation of diffusion-based language models.

## Features

- **Advanced Architecture**
  - Transformer-based backbone with diffusion capabilities
  - Configurable model sizes (small, medium, large)
  - Time step conditioning
  - Attention mechanisms optimized for text

- **Multiple Generation Strategies**
  - Auto-regressive generation
  - Parallel generation
  - Confidence-based masking
  - Semi-autoregressive generation
  - Top-p (nucleus) sampling
  - Beam search

- **Training Features**
  - Distributed training support
  - Mixed precision training
  - Gradient checkpointing
  - Early stopping
  - Model checkpointing
  - Learning rate scheduling

- **Utilities**
  - Real-time token generation streaming
  - Model saving and loading
  - HuggingFace Hub integration
  - Comprehensive logging
  - Error handling

## Installation

```bash
pip install diffusion-llm
```

For development installation:

```bash
git clone https://github.com/codewithdark-git/PIP-DifffusionLM.git
cd PIP-DifffusionLM
pip install -e .
```

## Quick Start

```python
from diffusion_llm.utils import prepare_dataset
from transformers import AutoTokenizer
from diffusion_llm.model import DiffusionConfig, DiffusionLLM

# Load tokenizer and prepare dataset
tokenizer = AutoTokenizer.from_pretrained("gpt2")
train_dataset, val_dataset, _ = prepare_dataset(
    dataset_name="wikitext/wikitext-103-v1",
    tokenizer_name="gpt2"
)

# Initialize model
config = DiffusionConfig(
        vocab_size=len(tokenizer),
        max_position_embeddings=256,
        num_timesteps=50,
        pad_token_id=tokenizer.pad_token_id,
        mask_token_id=tokenizer.mask_token_id,
        # **config_kwargs
    )
    model = DiffusionLLM(config)


```

## Training

### Basic Training

```python
from diffusion_llm import trainer

train_model = trainer(
        model=model,
        train_dataset=train_dataset,
        val_dataset=val_dataset,
        batch_size=batch_size,
        num_epochs=num_epochs,
        learning_rate=learning_rate,
        num_timesteps=num_timesteps,
        save_path=save_dir,
        device=device,
    )
```

### Model Registry

```python
from diffusion_llm import registerANDpush

registerANDpush(
    model=trained_model,
    tokenizer=tokenizer,
    model_type="diffusionLM",
    repo_id="your-username/model-name"
)
```

## Error Handling

The package includes comprehensive error handling:

```python
from diffusion_llm import DiffusionLMError, handle_errors

@handle_errors()
def your_function():
    # Your code here
    pass
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Requirements

- Python ≥ 3.8
- PyTorch ≥ 1.9.0
- Transformers ≥ 4.21.0
- For full requirements, see `requirements.txt`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

```bibtex
@article{diffusionllm2025,
  title={DiffusionLM: Large Language Models with Diffusion},
  author={Dark Coder},
  journal={GitHub Repository},
  year={2025},
  publisher={GitHub},
  url={https://github.com/codewithdark-git/PIP-DifffusionLM}
}
```

## Contact

- GitHub: [@codewithdark-git](https://github.com/codewithdark-git)
- Email: codewithdark90@gmail.com
# PIP-DifffusionLM
