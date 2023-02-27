"""Helper functions for the tests"""

import os
from collections import namedtuple
from os import walk

from farialimer.parser.b3parser import B3Parser as Parser

SampleSuit = namedtuple("SampleSuit", "provider spec path")
SampleSpec = namedtuple("SampleSpec", "provider spec")


def _get_testfiles():
    """Collect the sample text files and return a dict with the specs as keys"""
    sample_list = []
    for dirpath, _, filenames in walk("tests/specs"):
        for filename in filenames:
            if filename.endswith("txt"):
                provider, spec = dirpath.split("/")[-2:]
                filepath = os.path.join(dirpath, filename)
                sample_list.append(SampleSuit(provider, spec, filepath))
    return sample_list


def _get_spec_list():
    """Collect the yaml specs and return a list of tuples (provider, spec)"""
    spec_list = []
    for dirpath, _, filenames in walk("farialimer/specs"):
        for filename in filenames:
            if filename.endswith("yaml"):
                provider = dirpath.split("/")[-1]
                spec = filename.split(".")[0]
                spec_list.append(SampleSpec(provider, spec))
    return spec_list


def _get_spec(provider, spec):
    """Given a provider and a spec, returns the respectiver parser object"""
    parser = Parser(provider)
    spec_parser = parser.get_spec_parser(spec)
    return spec_parser
