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
        first4=''
        inSub = False
        for i,el in enumerate(nam):

            # Check '&' in front of groups
            first4+=el
            # first4 keeps only the first 4 characters to look for 'NAM_'
            if len(first4)>5:
                 first4=first4[1:]
            if first4[1:].upper() == 'NAM_' and first4[0] != '&':
                completeName = ''
                j=1
                while nam[i+j] != ' ':
                    completeName+=nam[j]
                    j+=1
                print('!!!!! ERROR: MISSING & IN FRONT OF ' + completeName + ' !!!!!')
            
            # Look for all sub-groups
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

        # Check duplicates of sub-groups from Pypi iteration_utilities.duplicates
        if len(list(duplicates(subGroups))) != 0:
            print('!!!!! ERROR: DUPLICATES OF GROUPS !!!!!')
            print(list(duplicates(subGroups)))
        else:
            print(' Groups OK (no duplicates)')
              

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
