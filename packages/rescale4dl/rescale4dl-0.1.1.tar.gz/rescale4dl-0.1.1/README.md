# ReScale4DL: Balancing Pixel and Contextual Information for Enhanced Bioimage Segmentation

[![Python 3.8+](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<img src="https://raw.githubusercontent.com/HenriquesLab/ReScale4DL/refs/heads/main/.github/logo.png?token=GHSAT0AAAAAAC5PYSXBX34C76FL7KUWDO62Z7VHF5A" align="right" width="150"/>

A systematic approach for determining optimal image resolution in deep learning-based microscopy segmentation, balancing accuracy with acquisition/storage costs.

## Key Features
- **Resolution simulation**: Rescale images and their respective annotations (upsample and downsample)
- **Segmentation evaluation**: Compare performance across resolutions using:
  - Mean Intersection-over-Union (IoU)
  - Morphological features
  - Potential throughput
  - Personalised metrics
- **Visualization tools**: Generate comparative plots and sample outputs

## Installation

ReScale4DL is available as a Python package through pip. 
Activate your conda environment or create one and install it with `pip`:

```terminal
pip install rescale4dl
```

### Manual installation
Manual installation from using GitHub repository
```terminal
git clone https://github.com/HenriquesLab/ReScale4DL.git
cd rescale4dl
conda create -n rescale4dl "python<=3.12"
conda activate rescale4dl
python -m pip install .
```


## Usage

### 1. Image Rescaling
Notebook: `Rescale_Images.ipynb`

### 2. Segmentation Analysis 
Notebook: `Evaluate_Segmentation.ipynb`

### 3. Rescale and crop 
Notebook: `Rescale_Foundation_Models.ipynb`


## Contributing
We welcome contributions through:
- [Issue reporting](https://github.com/HenriquesLab/ReScale4D/issues)
- [Pull requests](https://github.com/HenriquesLab/ReScale4D/pulls)

## License
MIT License - See [LICENSE](LICENSE) for details

## Citation
If using this work in research, please cite:
```
@article{gferreira2025rescale4dl,
  title={ReScale4DL: Balancing Pixel and Contextual Information for Enhanced Bioimage Segmentation},
  author={Ferreira, Mariana G. and Saraiva, Bruno M. and Brito, Antonio D. and Pinho, Mariana G. and Henriques, Ricardo and G{\'o}mez-de-Mariscal, Estibaliz },
  journal={bioRxiv},
  year={2025},
  publisher = {Cold Spring Harbor Laboratory},
  URL = ,
  eprint = ,
}
```




