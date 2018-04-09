VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_BUILD = 1
VERSION_TYPE  = 0
VERSION_NTYPE = 1

def get_version_string(full=True):
    version = str(VERSION_MAJOR) + '.' + str(VERSION_MINOR) + '.' + str(VERSION_BUILD)

    if full and VERSION_TYPE >= 0 and VERSION_TYPE < 3:
        version += '-' + [ 'a', 'b', 'rc' ][VERSION_TYPE] + str(VERSION_NTYPE)

    return version
