#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator as op
import subprocess
import json
import os
import sys
from api import get_tag


xmp_tags = {
        'city': 'XMP:City',
        'state': 'XMP:State',
        'country': 'XMP:CountryName',
        'country_code': 'XMP:CountryCode'
        }

iptc_tags = {
        'city': 'IPTC:City',
        'state': 'IPTC:Province-State',
        'country': 'IPTC:Country-PrimaryLocationName',
        'country_code': 'IPTC:Country-PrimaryLocationCode',
        }



def _str_len_warning(string, len_limit, operation):
    if operation is op.lt and len(string) < len_limit:
        warn("Tag {} was padded, since it was below the minimum length threshold".format(string), RuntimeWarning)
    elif operation is op.gt and len(string) > len_limit:
        warn("Tag {} was truncated, since it exceeded the maximum length threshold".format(string), RuntimeWarning)


def get_city(filename):
    return get_tag(filename, iptc_tags['city'])


def get_city_xmp(filename):
    return get_tag(filename, xmp_tags['city'])


def get_country_xmp(filename):
    return get_tag(filename, xmp_tags['country'])


def get_country_iptc(filename):
    return get_tag(filename, iptc_tags['country'])


def get_country_code_iptc(filename):
    return get_tag(filename, iptc_tags['country_code'])


def get_country_code_xmp(filename):
    return _information(filename).get(xmp_tags['country_code'], 0)


def get_state_iptc(filename):
    return get_tag(filename, iptc_tags['state'])


def get_state_xmp(filename):
    return get_tag(filename, xmp_tags['state'])


def get_filetype(filename):
    return get_tag(filename, 'File:FileType')


def get_mimetype(filename):
    return get_tag(filename, 'File:MIMEType')


def set_city_iptc(filename, city):
    set_tag(filename, tag_name, iptc_tags['city'])


def set_country_iptc(filename, country):
    _str_len_warning(country, 64, op.gt)
    set_tag(filename, tag_name, iptc_tags['country'])


def set_country_code_iptc(filename, country_code):
    _str_len_warning(country_code, 3, op.lt)
    _str_len_warning(country_code, 3, op.gt)
    set_tag(filename, tag_name, iptc_tags['country_code'])


def set_province_state_iptc(filename, province_state):
    _str_len_warning(province_state, 32, op.gt)
    set_tag(filename, tag_name, iptc_tags['state'])


def set_city_xmp(filename, city):
    set_tag(filename, tag_name, xmp_tags['city'])


def set_country_xmp(filename, country):
    set_tag(filename, tag_name, xmp_tags['country'])


def set_country_code_xmp(filename, country_code):
    set_tag(filename, tag_name, xmp_tags['country_code'])


def set_province_state_xmp(filename, province_state):
    set_tag(filename, tag_name, xmp_tags['state'])

