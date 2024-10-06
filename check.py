from iteration_utilities import duplicates

def checkFormat(nam):
        """
       Control the format of the namelist:
       - missing / at the end of a sub-group
       - (OK) duplicates of &NAM_XXX
       - duplicates of keys
       - missing & in front of a sub-group
       - extra . after a real number (e.g. '2.0.')',
       - real number sent to an integer variable (starting by N or I) 
        """
        # Look for all sub-groups
        subGroups = []
        inSub = False
        for el in nam:
            if el == '&':
                sub=''
                inSub=True
            elif el ==' ' or el == '\n':
                if inSub:
                     subGroups.append(sub)
                inSub=False
            elif inSub:
                 sub+=el
            else:
                 exit
        print(subGroups)
        # Check duplicates of sub-groups:
        if len(list(duplicates(subGroups))) != 0:
            print('!!!!! ERROR: DUPLICATES OF SUB-GROUPS !!!!!')
            print(list(duplicates(subGroups)))
        else:
            print(' Sub-groups OK (no duplicates)')
              

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
