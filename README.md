# Video Matching

## Step 0. Watch the demo :)
[![](http://img.youtube.com/vi/fO46zt5-JNs/0.jpg)](http://www.youtube.com/watch?v=fO46zt5-JNs "Video Matching")

## Step 1. Take a look at Jupyter notebooks
You can take a look at Jupyter notebooks in /jupyter_notebooks which contains color matching part and object matching part. They were wrote solely by me and the software is basically putting them together as a program with user interface. I also wrote comprehensive documentation/comments in those notebooks so you should have no problem understanding what I'm doing.

## Step 2. Get your video database and model resource

First, you should store a video database with jpg format and add that directory into `config.json`. 
The directory within `database_videos` should be like 
```angular2html
.
├── flowers
├── interview
├── movie
├── musicvideo
├── sports
├── starcraft
└── traffic
```
Each of the directory should include an audio file, and a list of images format with `FILENAME + FRAME_NUMBER.jpg`
For convenience, query video should be organized in a similar way, but it's also compatible with rgb files.

You need to add the directory of resource videos into `config.json`. 
Links to download database/query videos:
[Database](https://drive.google.com/file/d/1oHsvXNuoni_aVqi1qhY563X6TtmepSkE/view?usp=sharing)

[Query](https://drive.google.com/file/d/1rf8JRYKSG3UnGRKkoOCX10FGI0Z_UBrX/view?usp=sharing)

Another important configuration is the `resource` directory path. Since we will use yolo to detect objects, it's important to put an object detection model traning network under `resource/object_detection_model`. 

[Link to download object detection model](https://drive.google.com/file/d/1_eL2UrnNOHkNcyYLOGAb9FYyKRD2gGq6/view?usp=sharing)
(Side note: yolov3 works better)

## Step 3. Run `main.py`

`main.py` is the entry point for the program. It would take a while to load all database images and a tensorflow trained network. After finish loading, you can upload the query video directory to compare and search for match videos.  