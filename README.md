## Very simple, yet powerful script for local compression of multiple images.

Requirements:
```pip install Pillow```

> [!IMPORTANT]
> compressor_v2_async -- a version of the code that has all previous features + asynchronously processing with the asyncio library + progress bar :).

> [!IMPORTANT]
> compressor_v1 -- a version of the code that recursively goes through all folders in the current directory, compresses images and overwrites them.

> [!IMPORTANT]
> compressor -- current version of the code iterates through all image files in a given directory, compresses them to a target size, and saves them in an output folder. It reduces image dimensions if needed and adjusts the quality to achieve compression while maintaining a minimum threshold for quality.

Just place all files (.png, .jpg, .jpeg) that you want to compress nearby the ```compressor.py``` and run it.

| 1.66 Mb  | 156 Kb  |
|---|---|
| ![00014-3936683554](https://github.com/user-attachments/assets/be2ee138-baa1-45e6-b698-0e78b5f033e2) | ![00014-3936683554](https://github.com/user-attachments/assets/2e36f7a1-01aa-4a32-a39a-6242244794de)|
