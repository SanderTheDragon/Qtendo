import importlib

from .. import utils

class Rom:
    def __init__(self, path, platform_hints):
        self.path = path

        possible_platforms = []
        for platform in platform_hints.keys():
            if '.' + self.path.split('.')[-1] in platform_hints[platform]:
                possible_platforms.append(platform)

        self.module = None
        if len(possible_platforms) == 1:
            temp_module = importlib.import_module('.' + utils.get_short_platform_name(possible_platforms[0]), 'src.roms')

            if temp_module.verify(self.path):
                self.module = temp_module
        else:
            for possible_platform in possible_platforms:
                temp_module = importlib.import_module('.' + utils.get_short_platform_name(possible_platform), 'src.roms')

                if temp_module.verify(self.path):
                    self.module = temp_module
                    break

        self.is_rom = not self.module is None
