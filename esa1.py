"""
Iterate recursively through directories and print the filename, relative path and the md5 sum.

Usage:
  eas1.py <path>
  eas1.py (-h | --help)
  eas1.py --version

Options:
  -h, --help    Show this screen.
  --version     Show version.
"""

__author__ = 'sattelmaier'

from hashlib import md5
from os import listdir, path
from docopt import docopt


def get_files_path_md5(abs_path, rel_path=''):
    get_path = lambda ref, x: ref + '/' + x
    get_abs_path = lambda x: get_path(abs_path, x)
    get_rel_path = lambda x: get_path(rel_path, x)
    md5_hash = md5()

    try:
        dir_list = listdir(abs_path)
    except OSError as err:
        print("OS error: {0}".format(err))
        return

    for element in dir_list:
        element_encoded = element.encode('utf-8')
        md5_hash.update(element_encoded)
        md5_hash_hex = md5_hash.hexdigest()
        print("Filename: {}, Path: {}, MD5: {})".format(element, get_rel_path(element), md5_hash_hex))

        if path.isdir(get_abs_path(element)):
            get_files_path_md5(get_abs_path(element), get_rel_path(element))


if __name__ == '__main__':
    arguments = docopt(__doc__, version='eas1 1.0')
    get_files_path_md5(arguments['<path>'])
