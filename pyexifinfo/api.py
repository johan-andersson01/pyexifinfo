#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator as op
import subprocess
import json
import os
import sys
from warnings import warn


def _check_file_validity(filename):
    filename = os.path.abspath(filename)

    if not os.path.exists(filename):
        raise ValueError("The given filename {} does not exist".format(filename))
    if os.path.isdir(filename):
        raise ValueError("The given filename {} is a directory".format(filename))




def _get_cmd_output(filename, cmd_options):
    _check_file_validity(filename)
    filename = os.path.abspath(filename)
    return _command_line(['exiftool'] + cmd_options + [filename])


def _command_line(cmd):
    """Handle the command line call

    keyword arguments:
    cmd = a list

    Raises RuntimeError if the subprocess crashes.
    """
    try:
        s = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        s = s.stdout.read()

        return s.strip()

    except subprocess.CalledProcessError as e:
        raise RuntimeError("Subprocess {} exited with output: {}".format(' '.join(cmd), e))


def _information(filename):
    _check_file_validity(filename)
    filename = os.path.abspath(filename)
    result = get_json(filename)
    result = result[0]
    return result


def version():
    cmd_output = _command_line(["exiftool","-ver"])
    return cmd_output.decode('utf-8')


def get_json(filename):
    # get raw command output
    cmd_output = _get_cmd_output(filename, ['-G', '-j', '-sort'])

    #convert bytes to string
    cmd_output = cmd_output.decode('utf-8').rstrip('\r\n')

    # return json object
    return json.loads(cmd_output)


def get_csv(filename):
    # get raw command output
    csv_bytes = _get_cmd_output(filename, ['-G', '-csv', '-sort'])

    # return string
    return csv_bytes.decode('utf-8')


def get_xml(filename):
    xml_bytes = _get_cmd_output(filename, ['-G', '-X', '-sort'])

    #convert bytes to string
    xml_str = xml_bytes.decode('utf-8')
    
    #return string
    return xml_str


def get_tag(filename, tag_name):
    return _information(filename).get(tag_name, 0)


def get_filetype(filename):
    return get_tag(filename, 'File:FileType')


def get_mimetype(filename):
    return get_tag(filename, 'File:MIMEType')


def set_tag(filename, tag_name, value):
    _get_cmd_output(filename, ['-{}={}'.format(tag_name, value)])

