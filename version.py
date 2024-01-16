from util import getKeysValue, cleanCommas
import re

def convert56to57(nam, namDict):
    """
    Convert namelist (especially EXSEG*.nam) in version 5.6 to version 5.7
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
    nam = nam.replace('CSUBG_AUCV_RI','CSUBG_RIAUCV') # protect CSUBG_AUCV_RI
    nam = nam.replace('CSUBG_AUCV','CSUBG_AUCV_RC')
    nam = nam.replace('CSUBG_RIAUCV','CSUBG_AUCV_RI') # remove protection CSUBG_AUCV_RI

    # &NAM_TURB_CLOUD removed, keys moved to NAM_TURBn
    if nam.find('NMODEL_CLOUD') != -1:
        print('WARNING, NMODEL_CLOUD must be converted ----BY HAND--- with LCLOUDMODIF=T in &NAM_TURBn to each respective EXSEGn.nam ')
    
    # The following protection is if one applies this function multiple times on the same namelist. Should be handle differently
    nam = nam.replace('CSUBG_AUCV_RC_RC','CSUBG_AUCV_RC')

    # NMAXITER in &NAM_PARAM_ICEn (Warning, in LIMA NMAXITER exists and keeps its name unchanged)   
    if 'nam_param_ice' in namDict.keys() and 'nam_param_lima' in namDict.keys():
        if 'nmaxiter' in namDict['nam_param_lima'].keys() and 'nmaxiter' in namDict['nam_param_ice'].keys() :
            # In that case, replace in NAM_PARAM_ICEn but not in NAM_PARAM_LIMA
            indICE = nam.find('&NAM_PARAM_ICE')
            indLIMA = nam.find('&NAM_PARAM_LIMA')
            if indICE < indLIMA:
                nam = nam.replace('NMAXITER','NMAXITER_MICRO', 1) # Replace only at first occurence ==> in NAM_PARAM_ICE
            else:
                nam = nam.replace('NMAXITER','MICRO_LIMA', 1) # temporary replace NMAXITER by NMAXITER_MICRO_LIMA
                nam = nam.replace('NMAXITER','NMAXITER_MICRO', 1) # replace in PARAM_ICE
                nam = nam.replace('MICRO_LIMA','NMAXITER', 1) # replace back correctly by NMAXITER in PARAM_LIMA
        elif 'nmaxiter' in namDict['nam_param_lima'].keys() : # if present only in LIMA, do nothing
            pass
        else: # if present only in PARAM_ICE
            nam = nam.replace('NMAXITER','NMAXITER_MICRO') 
    elif 'nam_param_lima' in namDict.keys(): # NAM_PARAM_ICE not present, do nothing as NAM_PARAM_LIMA NMAXITER is not changed
        pass
    else: # replace in NAM_PARAM_ICEn NMAXITER if present.
        nam = nam.replace('NMAXITER','NMAXITER_MICRO') 

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
    def convert56to57(self, namDict):
        self._outputnamelist = convert56to57(self._outputnamelist, self._namDict)
