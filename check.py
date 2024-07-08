def checkFormat(nam):
        """
       Control the format of the namelist:
       - missing / at the end of a sub-group
       - duplicates of &NAM_XXX
       - duplicates of keys
       - missing & in front of a sub-group
       - extra . after a real number (e.g. '2.0.')',
       - real number sent to an integer variable (starting by N or I) 
        """
        

def checkValues(nam):
        """
       Control the values selected in the namelist:
       - check all types of values with the first letter of the variable
       - check the existence of the keys by reading the FORTRAN code program by program
       - check the possible values for strings by reading the FORTRAN code
       - check missing sub-groups and missing keys (optional prints)
       - 
        """  


class Check():
    def checkFormat(self):
        self._outputnamelist = checkFormat(self._outputnamelist)
    def checkValues(self):
        self._outputnamelist = checkValues(self._outputnamelist)
