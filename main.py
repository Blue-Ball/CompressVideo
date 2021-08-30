import os
import ffmpeg
from os import listdir
from os.path import isfile, join
import mimetypes


def compress_video(video_full_path, output_file_name, videoResolution):
    print('process:' + output_file_name)
    i = ffmpeg.input(video_full_path)
    ffmpeg.output(i, output_file_name,
                  **{'loglevel':'panic', 'c:v': 'libx264', 'b:v': videoResolution['rate'], 'vf': 'scale='+videoResolution['width']+':'+videoResolution['height']}
                  ).overwrite_output().run()


videoResolusions = {'1080p': {'width': '1920', 'height': '1080', 'rate':'1.7M'},
                    '720p': {'width': '1280', 'height': '720', 'rate':'1.1M'},
                    '480p': {'width': '858', 'height': '480', 'rate':'0.5M'},
                    '360p': {'width': '480', 'height': '360', 'rate':'0.25M'}}

mypath = os.path.abspath(__file__)
rootdir = os.path.dirname(mypath)
inputdir = join(rootdir, 'input')

print('-----Start-----')

onlyfiles = [f for f in listdir(inputdir) if isfile(join(inputdir, f))]
for file in onlyfiles:
    if mimetypes.guess_type(file)[0].startswith('video'):
        outdir = join(rootdir, 'out\\' + file)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        
        inputFile = join(inputdir, file)
        print('\ninputFile:' + inputFile)
        for rs in videoResolusions:
            outFile = join(outdir, rs+".mp4")
            compress_video(inputFile, outFile, videoResolusions[rs])
            print('Done:' + outFile)

print('-----End-----')