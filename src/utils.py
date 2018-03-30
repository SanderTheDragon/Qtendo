import logging
import os
import subprocess

def setup_logging():
    formatter = '[%(asctime)s %(filename)s %(levelname)s] %(message)s'
    log_level = logging.DEBUG

    #Log to file
    logging.basicConfig(filename='qtendo.log', filemode='w', format=formatter, level=log_level)

    #Also log to terminal
    terminal_logging = logging.StreamHandler()
    terminal_logging.setLevel(log_level)
    terminal_logging.setFormatter(logging.Formatter(formatter))
    logging.getLogger().addHandler(terminal_logging)

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

def execute(path, args):
    arguments = []
    if type(args) == str:
        arguments = args.split(' ')
    elif type(args) == list:
        arguments = args

    return subprocess.run([ path ] + arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8').strip()
