import os


def debug_flag():
    return os.getenv('DEBUG') == 'True'
