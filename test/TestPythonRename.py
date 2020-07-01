#!/usr/bin/env python3

# Author: Ed Tucker, 2017
#
# Test suite for the PythonRename unit.

import unittest
import os
import shutil

import sys
sys.path.append('../')
import PythonRename as rename

# Global variables
path = os.getcwd()

test_directory = "TestFiles"

test_file_details =  [{'name': 'File-1.png', 'content': '1234'},
                    {'name': 'File_!$%^&.doc', 'content': '98765'},
                    {'name': '___ext.JPEG', 'content': 'asdfg'},
                    {'name': 'DSC_1000.PNG', 'content': 'qwerty brain'},
                    {'name': 'File_with_same_timestamp.gif', 'content': 'what is going on?'}]

test_folder_details = [{'name': 'Folder1', 'files': ['afile.png']},
                       {'name': 'Folder_2', 'files': ['ajpegfile.jpg', 'anotherfile.txt']}]

test_default_content = 'None'

test_tag = "1!%_abc"


# Utilities
def get_number_of_files_in_directory(directory):
    number_of_files = sum(os.path.isfile(os.path.join(directory, f)) for f in os.listdir(directory))
    print('Number of files = ', number_of_files)
    return number_of_files


def create_file(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)


def create_directory(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)


def remove_directory(directory):
    if directory is not None and os.path.exists(directory):
        shutil.rmtree(directory)



class TestPythonRename(unittest.TestCase):
    """ Test Class for PythonRename module."""

    def setUp(self):
        """test fixture"""
        print("SETUP")

        # Clean and then make directory for testing
        self.test_directory = os.path.join(path, test_directory)
        remove_directory(self.test_directory)
        create_directory(self.test_directory)
        self.number_of_files = 0
        self.number_of_folders = 0

        # Make files to move
        self.files = test_file_details
        self.file_contents = []
        for file in self.files:
            create_file(self.test_directory + "/" + file['name'], file['content'])
            self.file_contents.append(file['content'])
            self.number_of_files += 1

        # Create subfolders to test non-recursive renaming
        self.folders = test_folder_details
        for folder in self.folders:
            folder['full_path'] = self.test_directory + "/" + folder['name']
            create_directory(folder['full_path'])
            self.number_of_folders += 1
            for file in folder['files']:
                create_file(folder['full_path'] + "/" + file, test_default_content)

        self.tag = test_tag


    def test_count_files_and_folders(self):
        """count_files_and_folders() test case"""
        print("test count_files_and_folders()")
        self.assertEqual(rename.count_files_and_folders(self.test_directory),
            self.number_of_files+self.number_of_folders)


    def test_create_filename(self):
        """create_filename() test case"""
        print("test create_filename()")
        # Test without number input
        expected_filename = '20170716_160100_TEST.jpg'
        self.assertEqual(rename.create_filename('20170716_160100', 'jpg', 'TEST', None), expected_filename)

        # Test with number input
        expected_filename = '20170716_160100_10_TEST.jpg'
        self.assertEqual(rename.create_filename('20170716_160100', 'jpg', 'TEST', 10), expected_filename)

        # Test with None tag
        expected_filename = '20170716_160100_10.jpg'
        self.assertEqual(rename.create_filename('20170716_160100', 'jpg', None, 10), expected_filename)


    def test_create_unique_filename(self):
        """create_unique_filename() test case"""
        print("test create_unique_filename()")
        # Test creation of file that does not already exist
        expected_filename = '20170716_160100_TEST.jpg'
        self.assertEqual(rename.create_unique_filename(self.test_directory, '20170716_160100', 'jpg', 'TEST'), expected_filename)

        # Test creation of file that does already exist
        expected_filename = '20170716_160100_1_TEST.jpg'
        new_directory = 'NewTestFolder'
        create_directory(new_directory)
        create_file(new_directory + "/" + '20170716_160100_TEST.jpg', 'content')
        self.assertEqual(rename.create_unique_filename(new_directory, '20170716_160100', 'jpg', 'TEST'), expected_filename)
        remove_directory(new_directory)


    def test_rename_files_by_datetime(self):
        """rename_files_by_datetime() test case"""

        # Rename files created during setup and confirm output
        print("test rename_files_by_datetime()")

        # Rename files using PythonRename module
        rename.rename_files_by_datetime(self.test_directory, self.tag)

        # Confirm the correct number of files exists, i.e. we haven't lost any
        self.assertEqual(get_number_of_files_in_directory(self.test_directory), self.number_of_files)

        # Confirm sub directories have not been touched
        for folder in self.folders:
            self.assertTrue(os.path.exists(folder['full_path']))
            for file in folder['files']:
                expected_file = folder['full_path'] + "/" + file
                self.assertTrue(os.path.exists(expected_file))
                # Confirm contents are intact
                with open(expected_file) as f: self.assertEqual(f.read(), test_default_content)

        # Confirm file contents are complete
        for file in [os.path.join(self.test_directory, f) for f in os.listdir()]:
            if os.path.isfile(file):
                # Confirm contents are intact
                with open(file) as f: self.assertTrue(f.read() in self.file_contents)
                # Confirm tags have been used correctly
                if self.tag != None:
                    self.assertTrue(self.tag in file)

        print("test rename_files_by_datetime() complete")


    def tearDown(self):
        """test fixture"""
        # Remove generated folder and files
        print("TEARDOWN")
        remove_directory(self.test_directory)


if __name__ == '__main__':
    unittest.main()
