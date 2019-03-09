#!/usr/bin/env python3

# Author: Ed Tucker, 2017
#
# PythonRename is a module that renames all files in a directory (non-recursive) 
# according to the file creation date-time, with a possible appended tag.
# This module was written to deal with the intensely annoying Android habit of 
# naming photos DSC_XXXX_Y.png, thus upsetting the ordering of your photos when
# moving between device and SD Card storage.  

from os import path, listdir, rename 
from time import strftime, gmtime

import sys
import argparse


def count_files_and_folders(directory):
    """Count the number of files and folders in a given directory.

    Args:
        directory: The directory to inspect.
    """
    number_of_files = len(listdir(directory))
    print ("Number of Files and Folders in {} = {}".format(directory, number_of_files))
    return number_of_files


def listdir_fullpath(directory):
    """List the full path for each file in a directory.

    Args:
        directory: The directory to inspect.
    """
    return [path.join(directory, f) for f in listdir(directory)]


def create_filename(time, tag, ext, number = None):
    """Create a file name based upon an input time, a given tag and extension.

    Args:
        time: A time string
        tag: A tag string
        ext: The extension to be used for the constructed filename
        number: A number (possibly None) to differentiate identical filenames
    
    Returns:
        The constructed filename.
    """
    if number == None:
        new_filename = time + "_" + tag + "." + ext
    else:
        new_filename = time + "_" + str(number) + "_" + tag + "." + ext
    return new_filename

    
def create_unique_filename(directory, time, tag, ext):
    """Create a unique filename from a time string, file tag, and extension
    If the created filename already exists, this function will create a 
    new filename with FILENAME_X where X is an integer.
    
    Args:
        time: A time string
        tag: A tag string
        ext: The extension to be used for the constructed filename
    
    Returns:
        The constructed unique filename.
    """
    potential_filename = create_filename(time, tag, ext, None)

    number = 1
    while path.isfile(path.join(directory, potential_filename)):
        potential_filename = create_filename(time, tag, ext, number)
        number += 1

    return potential_filename

    
def rename_files_by_datetime(directory, tag = None):
    """Method that recursively renames all files in a directory, using a 
    filename format based upon their modified time.
    
    Args:
        directory: either the full path or a directory in the same folder as the execution path.
        tag: Used to add a tag to the renamed files.
    """
    starting_number_of_files = count_files_and_folders(directory)

    for filename in listdir_fullpath(directory):
        if path.isfile(filename):
            filepath = path.join(directory, filename)

            # Get file creation time
            t = strftime('%Y%m%d_%H%M%S', gmtime(path.getmtime(filepath)))
            ext = filename.split(".")[-1]

            new_filename = create_unique_filename(directory, t, tag, ext)
            new_file_path = path.join(directory, new_filename)
            print("Rename ", filepath, " as ", new_file_path)

            rename(filepath, new_file_path)

    end_number_of_files = count_files_and_folders(directory)
    print("Lost files = ", starting_number_of_files - end_number_of_files)
    print("Completed renaming files")
    
    
if __name__ == '__main__':
    # Usage:  PythonRename.py  DIRECTORY  -t TAG
    # Command line arguments
    
    parser = argparse.ArgumentParser(description="Rename all files"
     "in a directory by their created date."
     "  PythonRename is a module that renames all files in a directory (non-recursive)"
     " according to the file creation date-time, with a possible appended tag. "
     "This module was written to deal with the intensely annoying Android habit of "
     "naming photos DSC_XXXX_Y.png, thus upsetting the ordering of your photos when "
     "moving between device and SD Card storage."
    )
    parser.add_argument('directory', type=str,
                        help='The directory of the files to rename.')
    parser.add_argument('-t', '--tag', type=str, default=None, 
                        help='String tag to append to all the renamed filenames.')

    args = parser.parse_args()
    if args.directory !=  None:
        short_directory = args.directory
        directory = path.abspath(short_directory)
        print ("Renaming files in directory: ", directory)

        tag = None if args.tag == None else args.tag

        rename_files_by_datetime(directory, tag)
    else:
        print("No input directory provided.")