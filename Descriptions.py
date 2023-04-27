import pandas as pd
from AbbrevAndChar import abbrev_check, prof_abbrev_dict, sap_abbrev_dict, MFG_Dict_Short
def create_descriptions(tupleList, row, sap_class):
    PO_Desc=[]
    Long_Desc=[]
    
    res_list=[i for n, i in enumerate(tupleList) if i not in tupleList[n+1:]]
    sortedList=sorted(res_list)
    for item in sortedList:
        if item[1]=="NOUN":
            varList=item[2].split()
            PO_Desc.append(varList[0]+" ")
            Long_Desc.append(varList[0]+" ")
            if len(varList)>1:
                PO_Desc.append("".join(varList[1:len(varList)])+" ")
                Long_Desc.append("".join(varList[1:len(varList)])+" ")
        else:
            PO_Desc.append(str(item[1])+" "+str(item[2])+" ")
            Long_Desc.append(str(item[2])+" ")
    short_desc,long_special=create_short_desc(sortedList,row,sap_class)
    
    long="".join(Long_Desc)
    po="".join(PO_Desc)
    return short_desc, long[:len(long)-1], po[:len(po)-1], long_special

	
def consolidate_Desc(attribute_Dict,row,sap_class):
    attribute_dict_short=[]
    attribute_dict_long_special=[]
    exceptListAttribute=["BRAND","MANUFACTURER"]
    exceptList=["M_GREASE", "M_ANTIFREEZE", "M_FUEL_ADDITIVES", "M_SPECIALITY_LUBES"]
    exceptListForShort=["M_GREASE", "M_ANTIFREEZE", "M_FUEL_ADDITIVES", "M_SPECIALITY_LUBES","M_LUBRICANTS"]
    for key in attribute_Dict:
        #Variable made for special long description
        
        if (key[1]=="BRAND" and  sap_class not in exceptListForShort) or key[1]=="MANUFACTURER":
            brand_mfg_add=key[2]
            if str(row["Manufacturer"])+str(row["ItemDescriptionPart3"]) in MFG_Dict_Short:
                brand_mfg_add=MFG_Dict_Short[str(row["Manufacturer"])+str(row["ItemDescriptionPart3"])]
            attribute_dict_long_special.append((key[0],key[1],brand_mfg_add))   
        '''
        Commented out for short desc adjust
            if sap_class not in exceptList and(key[1]=="BRAND" or key[1]=="MANUFACTURER"):
                key=(key[0],key[1],str(row["Manufacturer"])+str(row["ItemDescriptionPart3"]))
        '''
        
        if key[2] in sap_abbrev_dict and (key[1] not in exceptListAttribute or (sap_class in exceptListForShort and key[1]=="BRAND")):#Added for short desc adjust
            attribute_dict_short.append((key[0],key[1],sap_abbrev_dict[key[2]]))
            attribute_dict_long_special.append((key[0],key[1],sap_abbrev_dict[key[2]]))
            continue
        strSplit=key[2].split()
        strJoin=[]
        for str1 in strSplit:
            if str1 in sap_abbrev_dict:
                strJoin.append(sap_abbrev_dict[str1])
            else:
                strJoin.append(str1)
        if (key[1] not in exceptListAttribute) or (sap_class in exceptListForShort and key[1]=="BRAND"):#Added for short desc adjust
            attribute_dict_short.append((key[0],key[1]," ".join(strJoin)))
            attribute_dict_long_special.append((key[0],key[1]," ".join(strJoin)))
		
    return attribute_dict_short,attribute_dict_long_special
	
def short_desc_helper(desc_dict):
	short_desc=[]
	for item in desc_dict:
		
		short_desc.append(str(item[2])+" ")
		
	short="".join(short_desc)
	return short[:len(short)-1]
	
def create_short_desc(attribute_Dict,row,sap_class):
    short_desc_dict,attribute_dict_long_special=consolidate_Desc(attribute_Dict,row,sap_class)
	
    short_desc=short_desc_helper(short_desc_dict)
    #added for special long
    long_desc_special=short_desc_helper(attribute_dict_long_special)
    '''
    comment added for short desc adjust
    if len(short_desc)>40:
        short_desc=short_desc[:40]
    '''
 
    return short_desc,long_desc_special
    

