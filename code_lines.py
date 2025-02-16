#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 03:04:22 2023

@author: dev
"""

import os

def count_lines_in_file(file_path):
    with open(file_path) as f:
        return len(f.readlines())

def count_lines_in_directory(directory):
    total_lines = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                lines = count_lines_in_file(file_path)
                print('file:', file_path, 'num_lines:', lines)
                total_lines += lines

    return total_lines

source_folder = os.getcwd()
total_lines_of_code = count_lines_in_directory(source_folder)
print()
print('Total lines of code:', total_lines_of_code)