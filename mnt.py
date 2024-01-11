#!/usr/bin/env python3

import os
import f90nml
from version import Version
from prettify import Prettify

class NAMELIST_TOOL(Version, Prettify):

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
        self._namDict = f90nml.read(self._filename)
        
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
    
    def openwithnml(self):
        """
        Open the namelist file by using f90nml
        """            
        self._namelist = f90nml.read(self._filename)
        self._namelist.uppercase = True
        self._outputnamelist = self._namelist
        
    def writewithnml(self):
        """
        Writes the output namelist file by using f90nml
        """
        with open(self._filename if self._output is None else self._output, 'w') as fnml:
            self._outputnamelist.write(fnml)
        if self._output is None and self._filename != self._originalName:
            os.unlink(self._originalName)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Namelist conversion from 5.6 to 5.7. Use only ONE TIME by namelist file. You may save your namelist before applying.')

    #Inputs and outputs
    gInOut = parser.add_argument_group('Input(s) namelists ton convert')
    gInOut.add_argument('INPUT', help='EXSEG.nam input file(s), multiple files allowed. Outputfile name = Input file name', nargs='+')

    #Version conversion
    gVersion = parser.add_argument_group('Conversion and version control')
    gVersion.add_argument('--convert56to57', help='Convert namelist from version 5.6 to 5.7', default=False, action='store_true')

    #Prettify
    gAspect = parser.add_argument_group('Aspect and prettifying control')
    gAspect.add_argument('--applyf90nml', help='Only read and write by f90nml makes it prettier and ordered (not testes yet)', default=False, action='store_true')

    args = parser.parse_args()
    for inputfile in args.INPUT:
            namelist_tool = NAMELIST_TOOL(inputfile)            
            if args.convert56to57: 
                namelist_tool.convert56to57(namelist_tool._namDict)
                namelist_tool.write()    
            if args.applyf90nml:
                namelist_tool.openwithnml()
                namelist_tool.applyf90nml()
                namelist_tool.writewithnml()