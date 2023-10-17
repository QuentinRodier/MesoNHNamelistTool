def applyf90nml(nam):
    """
    Apply f90nml to open and write namelist
    """
    print(nam)
    return nam

class Prettify():
    def applyf90nml(self):
        self._outputnamelist = applyf90nml(self._outputnamelist)
