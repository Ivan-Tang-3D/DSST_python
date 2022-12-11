# DSST_Python

## Requirements
- Python 3.7
- NumPy
- Numba (needed if you want to use the hog feature)
- OpenCV (ensure that you can import cv2 in python) need opencv-contrib-python and the version of opencv-python is 3.4.5.36

## How to run tracking

track with a given video:

```shell
python run.py --mode video
```

track with a stream from a camera:

```shell
python run.py --mode builtin_stream
```

or

```shell
python run.py --mode outer_stream
```
