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


def _str_len_warning(string, len_limit, operation):
    if operation is op.lt and len(string) < len_limit:
        warn("Tag {} was padded, since it was below the minimum length threshold".format(string), RuntimeWarning)
    elif operation is op.gt and len(string) > len_limit:
        warn("Tag {} was truncated, since it exceeded the maximum length threshold".format(string), RuntimeWarning)


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
    """Returns the file exif"""
    _check_file_validity(filename)
    filename = os.path.abspath(filename)
    result = get_json(filename)
    result = result[0]
    return result

######################

"""
#API
===========================================================
===========================================================
===========================================================
===========================================================
"""


def ver():
    """ Version of Exiftool

    Retrieve the current version of exiftool installed on your computer

    Returns:
        [string] -- a string in a list. i.e: ['9.46']

    Raises:
        ValueError -- If you uninstalled or haven't installed yet Exiftool
        than this should raise an error
    """
    s = _command_line(["exiftool","-ver"])
    return s.split()


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


def get_city(filename, iptc=True):
    """Returns the IPTC City tag"""
    if iptc:
        tag_name = 'IPTC:City'
    else:
        tag_name = 'XMP:City'
    return _information(filename).get(tag_name, 0)


def get_country(filename, iptc=True):
    """Returns the IPTC Country tag"""
    if iptc:
        tag_name = 'IPTC:Country-PrimaryLocationName'
    else:
        tag_name = 'XMP:CountryName'
    return _information(filename).get(tag_name, 0)


def get_country_code(filename, iptc=True):
    if iptc:
        tag_name = 'IPTC:Country-PrimaryLocationCode'
    else:
        tag_name = 'XMP:CountryCode'
    return _information(filename).get(tag_name, 0)


def get_province_state(filename, iptc=True):
    if iptc:
        tag_name = 'IPTC:Province-State'
    else:
        tag_name = 'XMP:State'
    return _information(filename).get(tag_name, 0)


def get_filetype(filename):
    """Returns the file extension"""
    result =  _information(filename)
    return result.get('File:FileType', 0)


def get_mimetype(filename):
    """Returns the MIME type"""
    result =  _information(filename)
    return result.get('File:MIMEType', 0)


def set_city(filename, city, iptc=True):
    if iptc:
        tag_name = 'IPTC:City'
    else:
        tag_name = 'XMP:City'
    _get_cmd_output(filename, ['-{}={}'.format(tag_name, city)])


def set_country(filename, country, iptc=True):
    if iptc:
        tag_name = 'IPTC:Country-PrimaryLocationName'
        _str_len_warning(country, 64, op.gt)
    else:
        tag_name = 'XMP:CountryName'
    _get_cmd_output(filename, ['-{}={}'.format(tag_name, country)])


def set_country_code(filename, country_code, iptc=True):
    if iptc:
        tag_name = 'IPTC:Country-PrimaryLocationCode'
        _str_len_warning(country_code, 3, op.lt)
        _str_len_warning(country_code, 3, op.gt)
    else:
        tag_name = 'XMP:CountryCode'
    _get_cmd_output(filename, ['-{}={}'.format(tag_name, country_code)])


def set_province_state(filename, province_state, iptc=True):
    if iptc:
        tag_name = 'IPTC:Province-State'
        _str_len_warning(province_state, 32, op.gt)
    else:
        tag_name = 'XMP:State'
    _get_cmd_output(filename, ['-{}={}'.format(tag_name, province_state)])


