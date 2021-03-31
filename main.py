#!/usr/bin/env python3

from youtube_search import YoutubeSearch
from time import sleep
from typing import Union
import json
import os

# for error handling in handle_ui()
class ConnectionError(Exception):
    pass

# not at all necessary i just felt like it
def IO () -> None: # haskell keyword go brrrr
    return None

run: bool = True
CONFIG_LOCATION: str = os.getcwd() + '/config.json'

with open(CONFIG_LOCATION, 'r') as f:
    json_data: dict = json.load(f)
    current_dir: str = json_data["config"]["music-dir"]

print("loaded config at: " + CONFIG_LOCATION)

# order files for get_input()
def get_dir_contents(directory: str) -> dict:
    files: list = [file for file in os.listdir(directory)]
    return dict(enumerate(files))

def get_input(file_addrs: dict) -> str: # parameter should be called different thing but i am lazy
    print("-"*15)
    [print(f"{file[0]}: {file[1]}") for file in file_addrs.items()]
    print("-"*15)
    return input("-> ")

def handle_ui(i: str, select_from: dict) -> Union[str, bool, IO ()]: # TODO: when python3.10 is out adapt to new switch statement
    try: # if select_from can be indexed by i
        os.system("clear")
        return select_from[int(i)]
    except: # this is probably bad, yes
        try: # particularly this part
            command: list = i.split(' ')
            if command[0] == "play":
                play(command[1].split(','), select_from)
            elif command[0] == "download":
                download(command[1:])
            elif command[0] == "file":                                # set type shouldnt be here but it is
                os.mkdir(command[1] if command[-1] == command[1] else str(command[1] + '-' + '-'.join(command[2:])))
            elif command[0] == "del":
                os.system(f"rm -rf \'" + select_from[int(command[1])] + "\'") # not using os.remove as it cant delete directories
            elif command[0] == "edit":
                edit_json(' '.join(command[1:]))
            elif command[0] == "exit":
                return False
            elif command[0] == '':
                return 'back'
            else:
                print("unknown command")

        except ValueError:
            os.system("clear")
            print('something is wrong, maybe you input a non integer?')
            sleep(1)
        except ConnectionError:
            os.system("clear")
            print("something is wrong, maybe internet?")
            sleep(1)

def play(files: list, file_dict: dict) -> IO ():
    for file in files:
        os.system("clear")
        os.system(f'mpv --no-video --speed={float(json_data["config"]["back-speed"])} \'{file_dict[int(file)]}\'')

def download(search: str) -> IO ():
    search_dict: dict = {"results":[{"title": "clear me"}]}

    try:
        results: dict = YoutubeSearch(' '.join(search), max_results=10).to_dict()
        search_dict.clear()
        print(search_dict)
        for i in range(len(results)):
            search_dict[i]: str = results[i]["title"].replace('\n', '')
    except:
        raise ConnectionError

    select: int = int(get_input(search_dict))

    print('downloading ' + results[select]["title"])
    os.system("youtube-dl -f 251 https://www.youtube.com" + results[select]["url_suffix"])

def edit_json(user_input: str='') -> IO ():
    print(json_data)
    json_data['config'][user_input.split(':')[0]] = user_input.split(':')[1]
    with open(CONFIG_LOCATION, 'w') as f:
        json.dump(json_data, f, indent=2)
    os.system("clear")
    print(json_data)

while run:
    try:
        os.chdir(current_dir)
        file_addrs: dict = get_dir_contents(current_dir)
        ui: str = get_input(file_addrs) # ui as in user input not user interface
        handle_result: Union[str, bool, None] = handle_ui(ui, file_addrs)
        if handle_result == 'back':
            current_dir = '/'.join(current_dir.split('/')[:-1])
        elif type(handle_result) == str:
            current_dir = current_dir + '/' + handle_result
        elif type(handle_result) == bool:
            run = handle_result

    except NotADirectoryError: # take care of dumb user that tries to cd into file
        play(ui, file_addrs)
        current_dir: str = '/'.join(current_dir.split('/')[:-1])

    except Exception as e:
        print("uh oh something bad happened: " + str(e))
