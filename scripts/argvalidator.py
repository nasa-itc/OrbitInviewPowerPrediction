#!/usr/bin/env python
from os import path
from datetime import datetime
import argparse

class ArgValidator:

    def __init__(self):
        pass
    
    @staticmethod
    def validate_datetime(s):
        try:
            return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S") 
        except ValueError:
            msg = "Not a valid date/time: '{0}'.".format(s)
            raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def validate_file(s):
        try:
            with open(s) as f:
                pass
            return s
        except:
            msg = "Not a valid file: '{0}'.".format(s)
            raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def validate_directory(s):
        if (path.exists(s)):
            return s
        else:
            msg = "Not a valid directory: '{0}'.".format(s)
            raise argparse.ArgumentTypeError(msg)
