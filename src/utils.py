import logging
import os
import subprocess

def find_executable(name):
    paths = [
        #Standard paths
        '/bin',
        '/usr/bin',
        '/usr/local/bin',

        #Other possible paths
        '/usr/games',
        '/usr/local/games'
    ]

    for path in paths:
        filepath = path + '/' + name
        if os.path.isfile(filepath):
            return filepath


def find_files(root, filters):
    if type(filters) == str:
        filters = [ filters ]

    file_list = []
    for root_, directories, files in os.walk(root):
        for file in files:
            if '.' + file.split('.')[-1] in filters:
                file_list.append(os.path.join(root_, file))

    return file_list



def execute(path, args):
    arguments = []
    if type(args) == str:
        arguments = args.split(' ')
    elif type(args) == list:
        arguments = args

    return subprocess.run([ path ] + arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8').strip()



def get_short_platform_name(name):
    if ' ' in name:
        short_name = ''

        for word in name.split(' '):
            if word.isdigit():
                short_name += word
            else:
                short_name += word[0].lower()

        return short_name
    else:
        return name.lower()
