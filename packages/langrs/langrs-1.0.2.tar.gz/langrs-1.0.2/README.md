# LangRS 

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MohanadDiab/langrs/blob/main/examples/langrs.ipynb)
[![PyPI version](https://badge.fury.io/py/langrs.svg)](https://pypi.python.org/pypi/langrs)


<p align="center">
  <img src="https://raw.githubusercontent.com/MohanadDiab/langrs/main/assets/langrs_logo.png" alt="LangRS Logo" width="300"/>
</p>

**A python package that omptimizes zero-shot segmentation of aerial image based with GroundingDINO and Segment Anything Model (SAM)**

# Introduction

LangRS  is a Python package for remote sensing image segmentation, it is built on top of the [Segment-Geospatial](https://github.com/opengeos/segment-geospatial) package. It combines advanced techniques like bounding box detection, semantic segmentation, and outlier rejection to deliver precise and reliable segmentation of geospatial images.

## Citation
```bibtex
@article{DIAB2025100105,
title = {Optimizing zero-shot text-based segmentation of remote sensing imagery using SAM and Grounding DINO},
journal = {Artificial Intelligence in Geosciences},
volume = {6},
number = {1},
pages = {100105},
year = {2025},
issn = {2666-5441},
doi = {https://doi.org/10.1016/j.aiig.2025.100105},
url = {https://www.sciencedirect.com/science/article/pii/S2666544125000012},
author = {Mohanad Diab and Polychronis Kolokoussis and Maria Antonia Brovelli},
keywords = {Foundation models, Multi-modal models, Vision language models, Semantic segmentation, Segment anything model, Earth observation, Remote sensing},
}
```

## How it works 

<p align="center">
  <img src="https://raw.githubusercontent.com/MohanadDiab/langrs/main/assets/pres.gif" alt="Performance Comparison" width="600"/>
</p>

## 📊 Package Performance vs Ground Truth

<p align="center">
  <img src="https://raw.githubusercontent.com/MohanadDiab/langrs/main/assets/10.png" alt="Performance Comparison" width="600"/>
</p>

## 🔄 Direct Comparison with SAMGEO Package

<p align="center">
  <img src="https://raw.githubusercontent.com/MohanadDiab/langrs/main/assets/11.png" alt="Comparison with Older Package" width="600"/>
</p>


## Features

- **Bounding Box Detection:** Locate objects in remote sensing images with a sliding window approach.
- **Outlier Detection:** Apply various statistical and machine learning methods to filter out anomalies in the detected objects based on the area of the detected bounding boxes.
- **Non-Max Suppression** Applies NMS to the input bounding boxes, can reduce accuracy slightly, but greatly increases inference speed and lowers memory usage.
- **Area Calculation:** Compute and rank bounding boxes by their areas.
- **Image Segmentation:** Detect and extract objects based on text prompts using LangSAM.
---

## Installation


### Install LangRS with pip

```bash
pip install langrs
```


## Usage

Here is an example of how to use the `LangRS` class for remote sensing image segmentation:

```python
from langrs import LangRS

# The class accepts tif/ RGB images
text_input = "object.tif" 

# Path to the input remote sensing image
image_input = "path_to_your_tif_file"

# Initialize LangRS with the input image, text prompt, and output directory
langrs = LangRS(image_input, text_input, "output_folder")

# Detect bounding boxes using the sliding window approach with example parameters
bounding_boxes = langrs.generate_boxes(window_size=600, overlap=300, box_threshold=0.25, text_threshold=0.25)

# Apply outlier rejection to filter anomalous bounding boxes
# This will return a dict with the follwing keys:
# ['zscore', 'iqr', 'svm', 'svm_sgd', 'robust_covariance', 'lof', 'isolation_forest']
# The value of each key represent the boudning boxes from the previous step with the 
# outlier rejection method of the key's name applied to them
bboxes_filtered = langrs.outlier_rejection()

# Retreive certain bounding boxes 
bboxes_zscore = bboxes_filtered['zscore']

# Generate segmentation masks for the filtered bounding boxes of the provided key
masks = langrs.generate_masks(boxes=bounding_boxes)
# Or
masks = langrs.generate_masks(boxes=bboxes_zscore)
```

### Input Parameters for LangRS Methods

#### `LangRS` Initialization:
- `image`: Path to the input image.
- `prompt`: Text prompt for object detection.
- `output_path`: Directory to save output files.

#### `generate_boxes`:
- `window_size` (int): Size of each chunk for processing. Default is `500`.
- `overlap` (int): Overlap size between chunks. Default is `200`.
- `box_threshold` (float): Confidence threshold for box detection. Default is `0.5`.
- `text_threshold` (float): Confidence threshold for text detection. Default is `0.5`.

#### `outlier_rejection`:
Applies multiple outlier detection methods (e.g., Z-Score, IQR, SVM, LOF) to filter bounding boxes.

#### `generate_masks`:
- `boxes` (list[torch.tensor]): The input boxes, the model will segment what is inside these boxes only.
---

## Output

When the code runs, it generates the following outputs:
1. **Original Image with Bounding Boxes:** Shows the detected bounding boxes.
2. **Filtered Bounding Boxes:** Bounding boxes after applying outlier rejection.
3. **Segmentation Masks:** Overlays segmentation masks on the original image.
4. **Area Plot:** A scatter plot of bounding box areas to visualize distributions.

The results are saved in the specified `output` directory, organized with a timestamp to separate runs.

---

## Contributing

We welcome contributions! If you'd like to add features or fix bugs:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support

For any questions or issues, please open an issue on GitHub or contact the project maintainers.

