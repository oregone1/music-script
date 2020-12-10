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

def play(music_dir):
    os.system(f'ffplay \'{music_dir}\' -autoexit -nodisp')

while run:
    try:
        os.system('clear')
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
            if 'play' in user_input:
                play(music_dir + '/' + _input[int(user_input.replace('play', ''))])
                run = False
        except:
            print('error')

print('exiting')
