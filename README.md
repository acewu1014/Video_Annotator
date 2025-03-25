## Project Name: Video_Annotator
## Descriptions
When dealing with long videos, precisely annotating their content becomes challenging. Therefore, existing methods typically use off the shelf shot detection modules, such as Shot Detector or other AI-based models, to segment long videos into smaller shots for annotation. However, there is currently no well-suited annotation tool for handling such segmented data. To address this issue, we propose this project to facilitate the rapid annotation of videos.

## Environment Setup
1. **Create a virtual environment:**
    ```bash
    conda create -n kk_ui python=3.7
    conda activate kk_ui
    ```   

2. **Install dependecy:**
    ```bash
    pip install -r requirements.txt
    ```
    
    ```txt
    PyQt5 == 5.15.7
    ```
3. **Codec**
Since pyQt5 is not compactible with video in mp4 format, It's essential to install the K-Lite codec pack. [Codec download](https://codecguide.com/download_kl.htm)

## Data preperation
Before activate the UI, it's essential to preprocess the video. After preprocessing, we'll have the data as following
```
-ANY_FOLDER
    - 1.mp4
    - 1.json

```
### Json format
**Require columns:** index, boundary_timecode, boundary_frame, keywords, predictions
```jsonld
label.json
{"index": 0, "boundary_timecode": [0, 567], "boundary_frame": [0, 17], "keywords": ["XX", "XX"], "predictions": ["XX", "XX"]}
{"index": 1, "boundary_timecode": [568, 5670], "boundary_frame": [17, 222], "keywords": ["XX", "XX"], "predictions": ["XX", "XX"]}
...
{"index": 456, "boundary_timecode": [56800, 67800], "boundary_frame": [4599, 4700], "keywords": ["XX", "XX"], "predictions": ["XX", "XX"]}
```

Notice: the video and the label should share the same name.

## Start
CMD:
```
python start.py
```
## Shortcut
- Q: play/pause video.
- C: copy the previous shot info to the current one.
- R: recovery from the origin one.

## Other information
After annotating the video, if you open another video, it'll automatically save the label file. On the other hand, you should manually use SAVE_LABEL function. 