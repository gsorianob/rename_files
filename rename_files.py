#!/usr/bin/python
#encoding:utf-8
import itertools
import os
import sys

AVOID_NAMES = ('CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9')

AVOID_CHARACTERS = ('<', '>', ':', '"', '/', '\\', '|', '?', '*', ' ')


def remove_non_ascii(s):
    return "".join(x if ord(x) < 128 else '_' for x in s)

def any_in_list(a, b):
    # I use generator and any built-in because in that way i'll stop iteration
    # when any element of a is found in b
    return any(x for x in a if x in b)

def replace_invalid_characters(name):
    for letter in itertools.chain(AVOID_CHARACTERS, [' ']):
        name = name.replace(letter, '_')
    return remove_non_ascii(name)

def split_name_and_extension(filename):
    if '.' in filename:
        filename_splitted = filename.split('.')
        name = '.'.join(filename_splitted[:-1])
        extension = filename_splitted[-1]
    else:
        name = filename
        extension = ''
    return name, extension

def get_unique_name(dirpath, filename):
    fullpath = os.path.join(dirpath, filename)
    if not os.path.exists(fullpath):
        return fullpath

    name, extension = split_name_and_extension(filename)
    fullpath = os.path.join(dirpath, name)
    counter = 0
    while os.path.exists('%s%03d.%s' % (fullpath, counter, extension)):
        counter += 1
    return '%s%03d.%s' % (fullpath, counter, extension)

def rename(dirpath, name):
    fullname = os.path.join(dirpath, name)
    new_name = replace_invalid_characters(name)
    if new_name != name:
        new_name = get_unique_name(dirpath, new_name)
        print 'next:', fullname, '--->', new_name
        os.rename(fullname, new_name)

def check_and_rename(dirpath, filename):
    # http://msdn.microsoft.com/en-us/library/aa365247(VS.85).aspx#naming_conventions
    # http://msdn.microsoft.com/en-us/library/aa365247(VS.85).aspx#maxpath
    filename_splitted = filename.split('.')
    name, extension = '.'.join(filename_splitted[:-1]), filename_splitted[-1]
    if any_in_list((filename, name), AVOID_NAMES):
        print 'WARNING: Invalid filename: %s' % os.path.join(dirpath, filename)
    else:
        rename(dirpath, filename)


parameters = sys.argv[1:]
if not parameters:
    print 'To run this script you need to give him a list of directories'

for rootpath in parameters:
    for directory, dirnames, filenames in os.walk(rootpath, topdown=False):
        for name in itertools.chain(filenames, dirnames):
            check_and_rename(directory, name)
