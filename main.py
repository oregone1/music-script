#!/usr/bin/env python3

import json
import os

with open('config.json', 'r') as f:
    data = json.load(f)

run = True
music_dir = data['config'][0]['music_dir']
file_list = []
_input = {}
user_input = ''


def get_dir_contents(directory):
    file_list.clear()
    for file in os.listdir(directory):
        file_list.append(file)

    return(file_list)

def list_files(file_list):
    _input.clear()
    for i, file in enumerate(file_list):
        print(f'{i}, {file}')
        _input[i] = file
    return(_input)
    print('-----------------------------')

def ui(user_input):
    if len(user_input) > 0:
        if 'help' in user_input:
            pass

        else:
            try:
                new_music_dir = music_dir + _input[int(user_input)]
                #print(music_dir + new_music_dir)
                get_dir_contents(new_music_dir)
                list_files(file_list)
                #print(music_dir, new_music_dir)
            except Exception as e:
                if 'No such file or directory' in str(e):
                    cool_variable_name = new_music_dir.split('/')
                    #print(cool_variable_name[-1])
                    cool_variable_name.insert(4, _input[int(user_input)])
                    cool_variable_name.pop(5)
                    print(cool_variable_name)
                    new_music_dir = cool_variable_name
                    pass
    else:
        get_dir_contents(music_dir)
        list_files(file_list)

print("type help if you get stuck")

#get_dir_contents(music_dir)
#ui(file_list)
#print(_input)

#//: run part of the script

while run:
    ui(user_input)
    user_input = input('cool-prompt: ')
