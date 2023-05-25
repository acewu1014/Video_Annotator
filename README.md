# Video_Annotator
## Requirement
Since pyQt5 is not compactible with video in mp4 format, It's essential to install the K-Lite codec pack. [Codec download](https://codecguide.com/download_kl.htm)

## Data preperation
Before activate the UI, it's essential to preprocess the video. After preprocessing, we'll have the data as following
```
-ANY_FOLDER
    - 1.mp4
    - 1.json

```
Notice: the video and the label should share the same name.

## Start
CMD:
```
python start.py
```
## Shortcut
Q: play/pause video.
C: copy the previous shot info to the current one.

## Other information
After annotating the video, if you open another video, it'll automatically save the label file. On the other hand, you should manually use SAVE_LABEL function. 