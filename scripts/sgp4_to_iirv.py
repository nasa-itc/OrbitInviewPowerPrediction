#!/usr/bin/env python

import argparse
from argvalidator import ArgValidator
from datetime import datetime
import requests
from sgp4.api import Satrec

###############################################################################
# Script to use the sgp4 module to compute IIRVs for a satellite number
# (default is 43852, which is STF-1)
###############################################################################

class SatelliteTleException(BaseException):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class SatelliteTle:
    """Class to retrieve and use a two line element set for a given satellite """
    # Constructor
    def __init__(self, satellite_number, satellite_name = None, satellite_contact_name = None, tle_url = "http://www.celestrak.com/NORAD/elements/cubesat.txt", tle_file = None):
        """Constructor:  satellite number according to NORAD"""
        self.__satellite_number = satellite_number
        self.__tle_url = tle_url
        self.__tle_file = tle_file # Like "C:\Users\msuder\Desktop\STF1-TLE.txt"
        self.__satellite_name = satellite_name
        self.__satellite_contact_name = satellite_contact_name
        self.__line1 = None
        self.__line2 = None
        self.__get_tle()

    # Private method to fetch the TLE
    def __get_tle(self):
        """Method to retrieve the TLE for the initialized satellite number, usually from Celestrak (could be from a hardwired file).  No return value."""
        if (self.__tle_file is not None):
            lines = input(self.__tle_file)
        else:
            try:
                lines = requests.get(self.__tle_url).text.splitlines() 
            except:
                default_file = "C:/Users/msuder/Desktop/cubesat.txt"
                lines = input(default_file)

        last_name = ""
        for line in lines:
            if "1 %s" % self.__satellite_number in line:
                self.__line1 = line[0:69]
                if (self.__satellite_name is None):
                    self.__satellite_name = last_name
            if "2 %s" % self.__satellite_number in line:
                self.__line2 = line[0:69]
            if ("1 " != line[0:2]) and ("2 " != line[0:2]):
                last_name = line.rstrip()
            else:
                last_name = None
                
        if ((self.__line1 is None) or (self.__line2 is None)):
            if (self.__tle_file is not None):
                raise SatelliteTleException('Could not find TLE for satellite %s in file %s' % \
                    (self.__satellite_number, self.__tle_file))
            else:
                raise SatelliteTleException('Could not find TLE for satellite %s at URL %s' % \
                    (self.__satellite_number, self.__tle_url))
        else:
            self.__satellite = Satrec.twoline2rv(self.__line1, self.__line2)

def main():
    """Main function... makes 'forward declarations' of helper functions unnecessary"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--satnum", help="Specify satellite number (e.g. 25544=ISS, 43852=STF-1)", \
            type=int, metavar="[1-99999]", choices=range(1,99999), default=43852)
    parser.add_argument("-t", "--time", help="Specify date/time (UTC)", type=ArgValidator.validate_datetime, metavar="YYYY-MM-DDTHH:MM:SS", default=datetime.now())
    parser.add_argument("-r", "--endtime", help="Specify date time range with this end date/time (UTC)", \
            type=ArgValidator.validate_datetime, metavar="YYYY-MM-DDTHH:MM:SS", default=None)
    parser.add_argument("-d", "--timestep", help="Specify time step (delta) in seconds for tabular data", \
            type=int, metavar="[1-86400]", choices=range(1,86400), default=60)
    parser.add_argument("-f", "--file", help="TLE file to use (instead of looking up the TLE on CelesTrak)", type=ArgValidator.validate_file, default=None)
    parser.add_argument("-v", "--iirv", help="Print improved interrange vector (IIRV) format", action="store_true")
    args = parser.parse_args()

    if (args.file is not None):
        st = SatelliteTle(args.satnum, tle_file=args.file)
    else:
        saturl = "http://www.celestrak.com/cgi-bin/TLE.pl?CATNR=%s" % args.satnum
        st = SatelliteTle(args.satnum, tle_url=saturl)


# Python idiom to eliminate the need for forward declarations
if __name__=="__main__":
   main()
