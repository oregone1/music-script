#!/usr/bin/env python3

import json
import os

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
    os.system(f'mpv --no-video --speed={int(data["config"]["back-speed"])} \'{music_dir}\'')

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
            if user_input == 'exit':
                run = False
            elif 'play' in user_input:
                play(music_dir + '/' + _input[int(user_input.replace('play', ''))])
            elif 'list' in user_input:
                index = user_input.replace('list', '').split(',')
                print(index)
                for num in index:
                    play(music_dir + '/' + _input[int(num)])

            elif 'config' in user_input:
                if len(user_input) == 6:
                    for option in data['config']:
                        print(' ',option)
                elif 'edit' in user_input:
                    property = user_input.replace(f'config edit ', '')
                    property = property.split(' ')
                    print(data)
                    #if not str(property[0]) == 'config' and str(property[1]) == 'edit':
                    print('test')
                    data["config"][property[0]] = str(property[1])
                    #data["config"]["playback-speed"] = "2"
                    with open(real_dir, 'w') as w:
                        json.dump(data, w, indent=2)
            else:
                print('error') # detailed error handling
                break

        except Exception as e:
            print('error', e)
            
print('exiting')
