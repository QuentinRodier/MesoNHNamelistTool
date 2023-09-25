#!/usr/bin/env python3

import os
from version import Version

class NAMELIST_TOOL(Version):

    def __init__(self, filename, output=None):
        """
        :param filename: Input file name containing FORTRAN code
        :param output: Output file name, None to replace input file
        """
        self._filename = filename
        self._originalName = filename
        assert os.path.exists(filename), 'Input filename must exist'
        self._output = output
        with open(self._filename, 'r') as f:
            self._namelist = f.read()
        self._outputnamelist = self._namelist
        
    def write(self):
        """
        Writes the output namelist file
        """
        with open(self._filename if self._output is None else self._output, 'w') as f:
            f.write(self._outputnamelist)
        if self._output is None and self._filename != self._originalName:
            #We must perform an in-place update of the file, but the output file
            #name has been updated. Then, we must remove the original file.
            os.unlink(self._originalName)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Namelist EXSEG.nam conversion from 5.6 to 5.7 ')

    #Inputs and outputs
    gInOut = parser.add_argument_group('Input and output')
    gInOut.add_argument('INPUT', help='EXSEG.nam input file')
    gInOut.add_argument('OUTPUT', default=None, help='EXSEG.nam output file', nargs='?')

    #Version conversion
    gVersion = parser.add_argument_group('Conversion and version control')
    gVersion.add_argument('--convert56to57', help='Convert namelist from version 5.6 to 5.7', default=False, action='store_true')

    args = parser.parse_args()

    namelist_tool = NAMELIST_TOOL(args.INPUT, args.OUTPUT)
    if args.convert56to57: namelist_tool.convert56to57()
    
    namelist_tool.write()