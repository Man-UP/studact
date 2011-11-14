#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
import argparse
import sys

import wikipedia as pywikibot

HEADER='''
{{MenuBox
| title = Welcome to the Student-Led Activities Wiki
| content =
If you run into any problems and need help, or have any questions, please contact apesupport@cs.man.ac.uk.}}

These pages will describe the various student-led activities in the School of Computer Science at The University of Manchester.

The main editor is Puter Sutton, but the pages for each of the various activities described here are managed by the relevant people.
'''

indent = 0
def print(obj, *args, **kwargs):
    __builtins__.print('%s%s' % ('    ' * indent, obj), *args, **kwargs)

def resolve_path(relative_path):
    return os.path.abspath(
            os.path.join(os.path.dirname(__file__), relative_path))

def try_read_file(path):
    global indent
    print('Reading %s' % path)
    try:
        with open(path) as infile:
            return infile.read()
    except IOError as e:
        indent += 1
        print('Failed to read %s (%s)' % (path, e))
        indent -= 1
        return ''

def build_body(info_paths):
    global indent
    print('Building body from %d file(s)' % len(info_paths))
    indent += 1
    parts = []
    for info_path in info_paths:
        parts.append(try_read_file(info_path))
    indent -= 1
    return '\n'.join(parts)

def build_page(body):
    print('Building page from body length of %d' % len(body))
    return '\n'.join((HEADER, body))

def update_page(page, text):
    print('Updating %s' % page)
    site = pywikibot.getSite()
    page = pywikibot.Page(site, page)
    page.put(text, comment='Auto update.')

def build_argument_parser():
    argument_parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    argument_parser.add_argument('-p', '--page', default='Main_Page')
    argument_parser.add_argument('info_path', nargs='+')
    return argument_parser

def main(argv=None):
    global indent
    if argv is None:
        argv = sys.argv
    argument_parser = build_argument_parser()
    arguments = argument_parser.parse_args(args=argv[1:])
    print('Running studact.py')
    indent += 1
    body = build_body(arguments.info_path)
    page = build_page(body)
    update_page(arguments.page, page)
    indent -= 1
    print('Done, goodbye :).')
    return 0

if __name__ == '__main__':
    exit(main())

