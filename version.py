from util import getKeysValue, cleanCommas
import re
#f90nml
def convert56to57(nam):
    """
    Convert EXSEG*.nam in version 5.6 to version 5.7
    """
    
    # New namelist NAM_NEBn
    nam_nebn_keys = ['XTMINMIX', 'XTMAXMIX', 'LHGT_QS', 'CFRAC_ICE_ADJUST', 'CFRAC_ICE_SHALLOW_MF',
                'VSIGQSAT', 'CCONDENS', 'CLAMBDA3', 'LSTATNW', 'LSIGMAS', 'LSUBG_COND']
    nam_nebn = ''
    if nam.find('&NAM_NEBn ') == -1:
        for el in nam_nebn_keys:
            keyValueString, keyValue = getKeysValue(nam, el)
            nam = nam.replace(keyValueString,'')
            if keyValue:
                nam_nebn = nam_nebn + keyValueString + ', '
        if nam_nebn:
            nam_nebn = nam_nebn + ' /'
            nam = nam + '&NAM_NEBn ' + nam_nebn + '\n'

    # &NAM_PARAM_ICE moved to &NAM_PARAM_ICEn
    if '&NAM_PARAM_ICEn' not in nam:
        nam = nam.replace('&NAM_PARAM_ICE','&NAM_PARAM_ICEn')
    
    # &NAM_TURBn
    # Key change names
    nam = nam.replace('XKEMIN','XTKEMIN')
    nam = nam.replace('XCEDIS','XCED')
    nam = nam.replace('CSUBG_AUCV','CSUBG_AUCV_RC')
    
    # &NAM_TURB_CLOUD removed, keys moved to NAM_TURBn
    if nam.find('NMODEL_CLOUD') != -1:
        print('WARNING, NMODEL_CLOUD must be converted ----BY HAND--- with LCLOUDMODIF=T in &NAM_TURBn to each respective EXSEGn.nam ')
    
    # The following protection is if one applies this function multiple times on the same namelist. Should be handle differently
    nam = nam.replace('CSUBG_AUCV_RC_RC','CSUBG_AUCV_RC')

    # &NAM_PARAM_ICEn (and LIMA)
    # Key change names
    nam = nam.replace('NMAXITER_MICRO','NMAXITER')
    
    # Keys moved to NAM_PARAM_ICEn
    nam_to_icen_keys = ['CSUBG_AUCV_RC', 'CSUBG_AUCV_RI', 'CSUBG_MF_PDF']
    for el in nam_to_icen_keys:
        keyValueString, keyValue = getKeysValue(nam, el)
        nam = nam.replace(keyValueString,'')   
        if keyValue:
            # Check if the namelist already exist
            if nam.find('&NAM_PARAM_ICEn') == -1:
                nam = nam + '&NAM_PARAM_ICEn ' + keyValueString + '/'
            else:
                nam = nam.replace('&NAM_PARAM_ICEn', '&NAM_PARAM_ICEn ' + keyValueString + ', ')
    
    # Keys moved to NAM_TURBn
    nam_to_turbn_keys = ['CTURBLEN_CLOUD', 'XCOEF_AMPL_SAT', 'XCEI_MIN', 'XCEI_MAX']
    for el in nam_to_turbn_keys:
        keyValueString, keyValue = getKeysValue(nam, el)
        nam = nam.replace(keyValueString,'')   
        if keyValue:
            # Check if the namelist already exist
            if nam.find('&NAM_TURBn') == -1:
                nam = nam + '&NAM_TURBn ' + keyValueString + '/'
            else:
                nam = nam.replace('&NAM_TURBn', '&NAM_TURBn ' + keyValueString + ', ')
                
    # &NAM_PARAM_LIMA
    keyValueString, keyValue = getKeysValue(nam, 'LBOUND')
    nam = nam.replace(keyValueString,'')

    # &NAM_TURB keys is moved to &NAM_TURBn
    if nam.find('&NAM_TURB ') != -1:
       nam_to_turbn_keys = ['XPHI_LIM', 'XSBL_O_BL', 'XFTOP_O_FSURF']
       for el in nam_to_turbn_keys:
        keyValueString, keyValue = getKeysValue(nam, el)
        nam = nam.replace(keyValueString,'')   
        if keyValue:
            # Check if the namelist already exist
            if nam.find('&NAM_TURBn') == -1:
                nam = nam + '&NAM_TURBn ' + keyValueString + '/'
            else:
                nam = nam.replace('&NAM_TURBn', '&NAM_TURBn ' + keyValueString + ', ') 
        nam = re.sub('&NAM_TURB\s*/', '', nam)

    # &NAM_PARAM_MF_SHALLn
    if nam.find('XLAMBDA_MF') != -1:
        keyValueString, keyValue = getKeysValue(nam, 'XLAMBDA_MF')
        print('WARNING, XLAMBDA_MF must be converted ----BY HAND--- with LTHETAS_MF=T to correspond to XLAMBDA_MF=5.87; LTHETAS_MF=F for XLAMBDA_MF=0')
        nam = nam.replace(keyValueString,'')
    
    # &NAM_DIAG
    keyValueString, keyValue = getKeysValue(nam, 'CRAD_SAT')
    nam = nam.replace(keyValueString,'')

    # some SURFEX changes(not all)
    keyValueString, keyValue = getKeysValue(nam, 'LSNOWDRIFT')
    nam = nam.replace(keyValueString,'')

    keyValueString, keyValue = getKeysValue(nam, 'NTIME_COUPLING')
    nam = nam.replace(keyValueString,'')
    
    keyValueString, keyValue = getKeysValue(nam, 'XDT_RES')
    nam = nam.replace(keyValueString,'')

    keyValueString, keyValue = getKeysValue(nam, 'XDT_OFF')
    nam = nam.replace(keyValueString,'')
    
    nam = nam.replace('XTDEEP_TEB','XTI_ROAD')

    if nam.find('&NAM_TEB ') != -1:
        print('WARNING, NAM_TEB not converted automatically !! must be converted ----BY HAND---, see https://www.umr-cnrm.fr/surfex/spip.php?article451')
    if nam.find('&NAM_DATA_TEB_GARDEN ') != -1:
        print('WARNING, NAM_DATA_TEB_GARDEN not converted automatically !! must be converted ----BY HAND---, see https://www.umr-cnrm.fr/surfex/spip.php?article451')
    if nam.find('&NAM_DATA_TEB ') != -1:
        print('WARNING, NAM_DATA_TEB not converted automatically !! must be converted ----BY HAND---, see https://www.umr-cnrm.fr/surfex/spip.php?article451')
    if nam.find('&NAM_DATA_BEM ') != -1:
        print('WARNING, NAM_DATA_BEM not converted automatically !! must be converted ----BY HAND---, see https://www.umr-cnrm.fr/surfex/spip.php?article451')

    nam = cleanCommas(nam)
    
    # Add line return at end-of-file
    nam = nam + '\n'
    return nam

class Version():
    def convert56to57(self):
        self._outputnamelist = convert56to57(self._outputnamelist)
