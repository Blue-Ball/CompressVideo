import os
#from tkinter import colorchooser
from PySimpleGUI.PySimpleGUI import Input
import ffmpeg
from os import listdir
from os.path import isfile, join
import mimetypes
import PySimpleGUI as sg
import logging
import threading

g_bStart = False
g_bInProcess = False

def compress_video(video_full_path, output_file_name, videoResolution):
    inputVideo = ffmpeg.input(video_full_path)
    
    ffmpeg.output(inputVideo, output_file_name,
                  **{'loglevel': 'panic', 'c:v': 'libx264', 'b:v': videoResolution['rate'], 'vf': 'scale='+videoResolution['width']+':'+videoResolution['height']}
                  ).overwrite_output().run()

def Execute_Process(rate, infolder, outfolder, overlayFile):
    global g_bInProcess

    g_bInProcess = True
    videoResolusions = {'360p': {'width': '480', 'height': '360', 'rate': rate['360p']},
                        '480p': {'width': '858', 'height': '480', 'rate': rate['480p']},
                        '720p': {'width': '1280', 'height': '720', 'rate': rate['720p']},
                        '1080p': {'width': '1920', 'height': '1080', 'rate': rate['1080p']}}

    inputdir = infolder

    print('-----Start-----')

    onlyfiles = [f for f in listdir(inputdir) if isfile(join(inputdir, f))]
    for file in onlyfiles:
        if g_bStart == False:
            break
        if mimetypes.guess_type(file)[0].startswith('video'):
            outdir = join(outfolder, file)
            if not os.path.exists(outdir):
                os.makedirs(outdir)

            inputFile = join(inputdir, file)
            print('\ninputFile:' + inputFile)

            audio_stream = ffmpeg.input(inputFile).audio
            video_stream = ffmpeg.overlay(ffmpeg.input(inputFile, **{'acodec':'mp3'}), ffmpeg.input(overlayFile), **{'x':'(main_w-overlay_w)/2', 'y':'(main_h-overlay_h)/2'})
            # video_stream = ffmpeg.overlay(ffmpeg.input(inputFile, **{'acodec':'mp3'}), ffmpeg.input(overlayFile), **{'x':'0', 'y':'0'})
            ffmpeg.output(audio_stream, video_stream, 'temp.mp4').overwrite_output().run()
            
            if g_bStart == False:
                break
            for rs in videoResolusions:
                if g_bStart == False:
                    break
                outFile = join(outdir, rs+".mp4")
                compress_video('temp.mp4', outFile, videoResolusions[rs])
                print('Done:' + outFile)
            os.remove("temp.mp4")

    g_bInProcess = False
    print('-----End-----')

sg.theme('DarkAmber')   # Add a touch of color

resolution_column = [   [sg.Text('Resolution', justification='center')],
                        [sg.Text('360p', justification='center')],
                        [sg.Text('480p', justification='center')],
                        [sg.Text('720p', justification='center')],
                        [sg.Text('1080p', justification='center')]   ]
bitrate_column = [  [sg.Text('Bit Rate', justification='center')],
                    [sg.InputText(default_text='0.25M', size=(10, None), key='360p', justification='center')],
                    [sg.InputText(default_text='0.5M', size=(10, None), key='480p', justification='center')],
                    [sg.InputText(default_text='1.1M', size=(10, None), key='720p', justification='center')],
                    [sg.InputText(default_text='1.7M', size=(10, None), key='1080p', justification='center')],   ]

action_buttons = [[sg.Button('Start')], [sg.Button('Stop')]]

merge_colmun = [[       sg.Frame(title="", layout=resolution_column, border_width=0,
                           element_justification='center',
                           vertical_alignment="center"), 
                        sg.Frame(title="", layout=bitrate_column, border_width=0,
                           element_justification='center',
                           vertical_alignment="center"), 
                        sg.Button('Start', size=(10, 5)), sg.Button('Stop', size=(10, 5))]]

layout = [  [sg.Text('Input Folder Location:', size=(20, None)), sg.Input(), sg.FolderBrowse('Open Folder', size=(10, None), key='k_inputFolder')],
            [sg.Text('Output Folder Location:', size=(20, None)), sg.Input(), sg.FolderBrowse('Open Folder', size=(10, None), key='k_outputFolder')],
            [sg.Text('Watermark Logo:', size=(20, None)), sg.Input(), sg.FileBrowse('Open File', size=(10, None), key='k_waterMarkFile')],
            [sg.Column(merge_colmun, vertical_alignment='center', justification='center',  k='-C-')],
            [sg.Output(size=(80,10), key='log')] ]

log_file = 'run_log.txt'

# Logging setup to send one format of logs to a log file and one to stdout:
logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s, %(asctime)s, [%(levelname)s], %(message)s',
    filename=log_file,
    filemode='w')

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter('%(name)s, [%(levelname)s], %(message)s'))
logging.getLogger('').addHandler(ch)

# Create the Window
window = sg.Window('Compress Video', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break

    if event == 'Start':
        if g_bStart == False and g_bInProcess == False:
            g_bStart = True
            rate = {'360p':values['360p'], 
                    '480p':values['480p'],
                    '720p':values['720p'],
                    '1080p':values['1080p']}
            threading.Thread(target=Execute_Process, args=(rate, values['k_inputFolder'], values['k_outputFolder'], values['k_waterMarkFile']), daemon=True).start()
        else:
            print('Already started')

    if event == 'Stop':
        g_bStart = False
    print(f"Event: {event} , {values}")
    print(f"You entered: {event} , {values['k_inputFolder']}")