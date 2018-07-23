import logging
import os
import subprocess
from PyQt5.QtGui import QColor, QFont, QTextCharFormat

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



def char_format(color, style=[]):
    q_color = QColor()
    if type(color) == str:
        q_color.setNamedColor(color)
    elif type(color) == tuple:
        q_color.setRgb(*color)

    q_format = QTextCharFormat()
    q_format.setForeground(q_color)

    if 'bold' in style:
        q_format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        q_format.setFontItalic(True)

    return q_format
