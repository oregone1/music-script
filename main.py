#!/usr/bin/env python3

import json
import os

with open('config.json', 'r') as f:
    data = json.load(f)

update = True
run = True
music_dir = data['config']['music-dir']
file_list = []
_input = {}
user_input = ''
extension_list = data['config']['recognized-files']

os.chdir(music_dir)

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

while run:
    try:
        if update:
            music_dir2 = music_dir
            get_dir_contents(music_dir)
            list_files(file_list)
            user_input = input(data['config']['prompt-name'])
            if len(user_input) > 0:
                music_dir += '/' + _input[int(user_input)]
                for extension in extension_list:
                    if extension in music_dir:
                        update = False

            else:
                split_dir = music_dir.split('/')
                del split_dir[-1]
                #debug    print(split_dir)
                music_dir = '/'.join(split_dir)
                #debug    print(music_dir)
        else:
            try:
                os.system(f'ffplay \'{music_dir}\' -autoexit -nodisp')
                music_dir = music_dir2
                update = True
            except:
                print('error: file could not be played')
                music_dir = music_dir2
                update = True

    except:
        try:
            if user_input == 'exit':
                run = False
                print('test')
        except:
            print('error')

print('exiting')
