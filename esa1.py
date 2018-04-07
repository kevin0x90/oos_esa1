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

import sys
from hashlib import md5
from os import listdir, path
from collections import namedtuple

def get_file_hash(filePath):
    """
    Get the md5 hash for the contents of a given file.

    Parameters
    ----------
    filePath : str

    Returns
    -------
    str
        The calculated md5 hashcode in hexadecimal format.
    """
    md5_hash = md5()

    try:
        with open(filePath, 'rb') as fileHandle:
            while True:
                chunk = fileHandle.read(2048)

                if not chunk:
                    break

                md5_hash.update(chunk)
    except PermissionError as accessErr:
        print("No permission to read file: {}. {}".format(filePath, accessErr), file=sys.stderr)
        
    return md5_hash.hexdigest()

FileInfo = namedtuple('FileInfo', ['file_name', 'relative_path', 'hash_code'])

def iterate_directory(directoryPath):
    """
    Iterate the contents of a directory recursively and collect file information.

    Parameters
    ----------
    directoryPath : str

    Yields
    ------
    FileInfo
        A 3 tuple with file name, relative path and the calculated hash code.

    Raises
    ------
    OSError
        If a problem occurs during directory access that is not permission related.
    """

    directoryItems = []

    try:
        directoryItems = listdir(directoryPath)
    except PermissionError as accessErr:
        print("No permission to open directory: {}. {}".format(directoryPath, accessErr), file=sys.stderr)
    except OSError as err:
        print("OS error: {}".format(err), file=sys.stderr)
        raise

    for item in directoryItems:
        fullItemPath = path.join(directoryPath, item)

        if path.isfile(fullItemPath):

            hashCode = get_file_hash(fullItemPath)
            fileInfo = FileInfo(item, path.relpath(directoryPath), hashCode)
            yield fileInfo

        elif path.isdir(fullItemPath):

            for fileInfo in iterate_directory(fullItemPath):
                yield fileInfo

if __name__ == '__main__':

    directoryPath = sys.argv[1]

    for fileInfo in iterate_directory(directoryPath):
        print("Filename: {}, Path: {}, Hash: {}".format(fileInfo.file_name, fileInfo.relative_path, fileInfo.hash_code))