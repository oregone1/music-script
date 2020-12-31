#!/usr/bin/env python3

from youtube_search import YoutubeSearch
import json
import os
import youtube_dl

with open('config.json', 'r') as f:
    data = json.load(f)

run = True
music_dir = data['config']['music-dir']
file_list = []
_input = {}
user_input = ''
extension_list = data['config']['recognized-files']
real_dir = os.path.realpath('config.json')

def get_dir_contents(directory):
    file_list.clear()
    for file in os.listdir(directory):
        file_list.append(file)

def list_files(file_list):
    _input.clear()
    for i, file in enumerate(file_list):
        print(f'{i}, {file}')
        _input[i] = file
    print('-----------------------------')
    return(_input)

def play(music_dir):
    os.system(f'mpv --no-video --speed={float(data["config"]["back-speed"])} \'{music_dir}\'')

def download_file(title):

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'webm',
            'preferredquality': '192',
            }]
        }

    is_video = 'n'
    i = -1
    results = YoutubeSearch(title, max_results=10).to_dict()
    while is_video.lower() == 'n':
        i += 1
        print(f'found {results[i]["title"]}')
        is_video = input('is the title correct? (y/n) ')

    download = 'https://www.youtube.com' + str(results[i]['url_suffix'])
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([download])

while run:
    try:
        os.chdir(music_dir)
        print('-----------------------------')
        get_dir_contents(music_dir)
        list_files(file_list)
        user_input = input(data['config']['prompt-name'])
        os.system('clear')
        music_dir2 = music_dir
        if len(user_input) > 0:
            music_dir += '/' + _input[int(user_input)]

        else:
            split_dir = music_dir.split('/')
            del split_dir[-1]
            #debug    print(split_dir)
            music_dir = '/'.join(split_dir)
            #debug    print(music_dir)

    except:
        try:
            command = user_input.split(' ')

            if command[0] == 'exit':
                run = False

            elif command[0] == 'play':
                play(music_dir + '/' + _input[int(user_input.replace('play', ''))])

            elif command[0] == 'list':
                index = user_input.replace('list', '').split(',')
                print(index)
                for num in index:
                    play(music_dir + '/' + _input[int(num)])

            elif command[0] == 'config':
                if len(user_input) == 6:
                    for option in data['config']:
                        print(' ',option)
                elif command[1] == 'edit':
                    property = user_input.replace(f'config edit ', '')
                    property = property.split(' ')
                    print(data)
                    #if not str(property[0]) == 'config' and str(property[1]) == 'edit':
                    print('test')
                    data["config"][property[0]] = str(property[1])
                    #data["config"]["playback-speed"] = "2"
                    with open(real_dir, 'w') as w:
                        json.dump(data, w, indent=2)

            elif command[0] == 'download':
                download_file(user_input.replace('download', ''))

            elif command[0] == 'file':
                os.mkdir(command[1])

            else:
                print('error') # detailed error handling
                break

        except Exception as e:
            print('error', e)

print('exiting')
