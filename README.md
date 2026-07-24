# Borehole Image Porosity Classifier

An automated, data-driven petrophysical tool designed to process, segment, and classify secondary porosity spaces from Borehole Image (BHI) logs. The script extracts features from raw `.dlis` files, handles sensor artifact interpolation, blends static and dynamic datasets, and groups structural features using advanced clustering techniques.

## 🚀 Key Features

*   **DLIS Parsing & Preprocessing:** Reads raw oilfield `.dlis` files to extract static (`BHI_STAT`), dynamic (`BHI_DYN`), and continuous depth log arrays.
*   **Sensor Gap Interpolation:** Automatically detects missing data channels and pads/sensor gaps, accurately reconstructing them using OpenCV’s Telea inpainting algorithm.
*   **Morphological Image Blending:** Harmonizes static and dynamic properties through a weighted (50/50) matrix summation followed by dual-pass `skimage` area-closing and area-opening routines.
*   **Geometric Feature Extraction:** Translates visual pore structures into quantifiable petrophysical dataframes (extracting Area, Aspect Ratio, Circularity, Orientation Tilt, Roundness, and Depth coordinates).
*   **Unsupervised Secondary Porosity Clustering:** Employs density-based spatial clustering (`HDBSCAN`) to automatically identify distinct porosity regimes and microstructural signatures.
*   **Automated Step-Plot Generation:** Exports high-resolution (`180 DPI`), 9-panel visual quality control slices mapping every processing step along the borehole index.

## 📦 Required Dependencies

Ensure you have the following packages installed before running the pipeline:

```bash
pip install dlisio numpy opencv-python pandas matplotlib scikit-image scikit-learn
```

## 🛠️ Step-by-Step Processing Pipeline

The script slices large-scale depth sequences into computational chunks to optimize memory and processing speed:

1. **Inpainting:** Reconstructs unmapped borehole pad gaps.
2. **Segmentation:** Generates a binary mask of potential pore structures using dynamic threshold bit-ranges.
3. **Property Engine:** Measures geometric parameters of labeled structural regions.
4. **Clustering Analysis:** Feeds dimensions into `HDBSCAN` to produce a unique, color-mapped classification matrix.
5. **QC Export:** Generates multi-panel horizontal comparison figures for every 1000 depth units.

## 📊 Pipeline Visual Layout Output

For every depth increment, the code saves a comprehensive 9-panel diagnostic plot tracking:
`Static BHI` ➡️ `Dynamic BHI` ➡️ `Interpolated Sets` ➡️ `Weighted Merge` ➡️ `Area Closing` ➡️ `Area Opening` ➡️ `Binary Filter` ➡️ `HDBSCAN Clusters`

## ⚠️ Internal Notice

🔒 **Confidentiality:** This repository is intended strictly for **internal use only**. Do not distribute, publish, or share data/code blocks externally without explicit organizational clearance.
