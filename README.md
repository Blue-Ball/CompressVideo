# CompressVideo

mp4 video (h.264) compress to it and create 4 versions of the video (1080p@1.7Mbps, 720p@1.1Mbps, 480p@0.5Mbps, 360p@0.25Mbps).

# Prepare
> pip install ffmpeg-python

## INPUT
* ### Prepare the video files into "input" directory.
```csharp
path/to/python/input/1.mp4
path/to/python/input/2.mp4
...
```

## OUTPUT
* ### The files will be stored in "out" directory.
```csharp
path/to/python/out/1.mp4/1080p.mp4
path/to/python/out/1.mp4/720p.mp4
...
```