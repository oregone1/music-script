#!/usr/bin/env python3

import json
import os

with open('config.json', 'r') as f:
    data = json.load(f)

run = True
music_dir = data['config']['music_dir']
file_list = []
_input = {}
user_input = ''
extension_list = ['.mp3', '.webm']

os.chdir('/')

def get_dir_contents(directory):
    file_list.clear()
    for file in os.listdir(directory):
        file_list.append(file)

    #return(file_list)

def list_files(file_list):
    _input.clear()
    for i, file in enumerate(file_list):
        print(f'{i}, {file}')
        _input[i] = file
    return(_input)
    print('-----------------------------')

#

print("type help if you get stuck")

#get_dir_contents(music_dir)
#ui(file_list)
#print(_input)

#//: run part of the script

while run:
    get_dir_contents(music_dir)
    list_files(file_list)
    #change_dir(user_input)
    user_input = input(data['config']['prompt-name'])
    if len(user_input) > 0:
        music_dir += '/' + _input[int(user_input)]
        for extension in extension_list:
            if extension in music_dir:
                os.system(f'cvlc {music_dir}')
                music_dir = music_dir - _input[int(user_input)]
    else:
        print('error')
