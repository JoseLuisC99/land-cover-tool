# Dataset for the project
For this project, we use [DeepGlobe Land Cover Classification Dataset](https://www.kaggle.com/datasets/balraj98/deepglobe-land-cover-classification-dataset) who introduces the challenge of automatic multi-class segmentation of land cover types:

## Data
- The training data for Land Cover Challenge contains 803 satellite imagery in RGB, size 2448x2448.
- The imagery has 50cm pixel resolution, collected by DigitalGlobe's satellite.
- The dataset contains 171 validation and 172 test images (but no masks).

## Labels
Each satellite image is paired with a mask image for land cover annotation. The mask is a RGB image with 7 classes of labels, using color-coding (R, G, B) as follows.
| Land type         | RGB           | Description                                           |
| :---------------- | :-----------: | :---------------------------------------------------- |
| Urban land        | (0,255,255)   | Man-made, built up areas with human artifacts.        |
| Agriculture land  | (255,255,0)   | Farmsor any planned plantation.                       |
| Rangeland         | (255,0,255)   | Any non-forest, non-farm, green land, grass.          |
| Forest land       | (0,255,0)     | Any land with x% tree crown density plus clearcuts.   |
| Water             | (0,0,255)     | Rivers, oceans, lakes, wetland, ponds.                |
| Barren land       | (255,255,255) | Mountain, land, rock, dessert, beach, no vegetation.  |
| Unknown           | (0,0,0)       | Clouds and others.                                    |

The original dataset (from kaggle) must be in the folder `data/v0.1`. For every version of the dataset, use the follow structure:
```
│ v1.0              <- Change the version number
│
├── content         <- Folder with the TFRecords
│   ├── test        <- Test samples (20%)
│   ├── train       <- Train samples (80%)
│   └── valid       <- Validation samples (20%)
|
└── metadata.csv    <- Metadata CSV with three columns: split, sat_path and mask_path
```