'''
This file contains format functions which separate material descriptions, label characteristics, and
create descriptions based off of material mapping and line of business. 
'''


import pandas as pd


from SAPCharacteristics import fertAddFact, Brand, PackageConfig, fertPercent, fertProduct, fertGuaranteedAnalysis, commDescript, fertAdd, Form
from SAPCharacteristics import shopORmerchDesc, feedGuaranteedAnalysis, feedMedication, feedMedicationLevel, feedPackage, feedPackageSize, feedTradeName, productName, brandOther
from SAPCharacteristics import SAE_Viscosity, ISO_Viscosity, tradeName, NLGI_Grade, PackageConfigFertBulk, packageCheck, eject, Create_Characteristic_Abbrev,Create_Characteristic
from AbbrevAndChar import abbrev_check, prof_char_dict, prof_abbrev_dict, id_dict, med_list, prof_char_feed_dict, prof_abbrev_dict_feed, package_dict,findDefault,findItem,mapDict,MFG_Dict
from Descriptions import create_descriptions
from HelperFunctions import fert_perc_helper, classCalc, formCalc, guaranteed_analysis_calc, element_seperator, analysis_calc_helper, mostNumeric, feed_analysis_calc, findMedication, mfgRemoval, obsoleteAttribute, numericFound, descriptionRetrieve, extractBrand, nlgiSplit
from HelperFunctions import otherChar, format1_cleanse, format2_cleanse, format3_cleanse, stateCalc

notValidList=["&", "/", ".", ",","#", "+"]

#Format function for seed materials
def format_seed(row, legacy_num):
    tag=False
    nounMod=row["Name"][:4].strip()
    noun,noun_Mod,sap_class,format_group=findItem(nounMod)
    if noun!="notfound":
        return eval(f"format{format_group}_cleanse(row, noun, noun_Mod, legacy_num, sap_class,tag)")
    elif row["ProductCategory"] in id_dict:
        sap_class2=id_dict[row["ProductCategory"]]
        noun2,noun_Mod2,format_group2=findDefault(sap_class2)
        if noun2!="notfound":
            tag=True
            return eval(f"format{format_group2}_cleanse(row, noun2, noun_Mod2, legacy_num, sap_class2,tag)")
    else:
        return eject(row, legacy_num,"ERROR:PRODUCT CATEGORY NOT MAPPED",row["ProductCategory"])
        
#Format function for chemical materials
def format_chem(row,legacy_num):
    attribute_Dict=[]
    attribute_List=[]
    otherList=[]
    
    row["ItemDescriptionPart1"]=mfgRemoval(row, str(row["ItemDescriptionPart3"]).strip().upper())
    
    try:
        sap_class=""
        if row["ProductCategory"] in id_dict:
            sap_class=id_dict[row["ProductCategory"]]
        else:
            return eject(row, legacy_num,"ERROR:PRODUCT CATEGORY NOT MAPPED",row["ProductCategory"])
           
        label_name=str(row["ItemDescriptionPart1"]).strip().upper()
        package_size=str(row["ItemDescriptionPart2"]).strip().upper()
        mfg=str(row["ItemDescriptionPart3"]).strip().upper()
       
        if label_name!="":
            label_name=str(label_name)
            attribute_Dict.append((1,"LABELED NAME",label_name))
            if len(label_name)>30:
                label_name=label_name[:30]  
            attribute_List.append({"Key":1,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"LABELED_NAME", "Characteristic Description":label_name})
        if package_size!="" and package_size!="NAN":
            package_size=str(abbrev_check(package_size, prof_abbrev_dict))
            pkg=packageCheck(row["PackageSize"])
            
            if pkg!="NA" and pkg not in package_size:
                package_size=package_size+" "+pkg
            consol_pkg=package_size.replace("LIQ BULK","").replace("BULK","").replace("EACH","").strip()
            if consol_pkg!="":
                attribute_Dict.append((2,"CHEM PACKAGE CONFIGURATION",consol_pkg))
            attribute_List.append({"Key":2,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"CHEM_PACKAGE_CONFIGURATION", "Characteristic Description":package_size})
        if mfg!="" and mfg!="NAN":
            mfg=str(abbrev_check(mfg, prof_abbrev_dict))
            brandID=str(row["Manufacturer"])+str(row["ItemDescriptionPart3"])
            if brandID in MFG_Dict:
                mfg=MFG_Dict[brandID]
                
            attribute_Dict.append((3,"MANUFACTURER",mfg))
            if len(mfg)>30:
                mfg=mfg[:30]  
            attribute_List.append({"Key":3,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"MANUFACTURER", "Characteristic Description":mfg})
        
        return descriptionRetrieve(attribute_Dict, attribute_List, row, sap_class), otherChar(legacy_num, row, otherList, sap_class)
        
    except IndexError:
        return eject(row, legacy_num,"ERROR:INDEX ERROR",row["Name"])

def format_Fert_Micro(row, legacy_num, sap_class):
    attribute_Dict=[]
    attribute_List=[]
    otherList=[]
    
    row["ItemDescriptionPart1"]=mfgRemoval(row, str(row["ItemDescriptionPart3"]).strip().upper())
    
    charg_group=str(row["ItemDescriptionPart1"])
    
    form=formCalc(row)
    
    try:
        if '%' in charg_group:
            if form!="":
                attribute_Dict, attribute_List=Form(attribute_Dict, attribute_List, row, legacy_num,form, sap_class,"MICRO NUTRIENT FORM","MICRO_FORM",5)
                charg_group=charg_group.replace(form,"")
            percent, product, add_fact= fert_perc_helper(charg_group)
            
            attribute_Dict, attribute_List=fertProduct(attribute_Dict, attribute_List, row, legacy_num, product, sap_class)
            attribute_Dict, attribute_List=fertPercent(attribute_Dict, attribute_List, row, legacy_num, percent, sap_class)
            
            attribute_Dict, attribute_List=fertAddFact(attribute_Dict, attribute_List, row, legacy_num, sap_class, add_fact)
            attribute_Dict, attribute_List=PackageConfig(attribute_Dict, attribute_List, row, legacy_num, sap_class)
            attribute_Dict, attribute_List=Brand(attribute_Dict, attribute_List, row, legacy_num, sap_class,7)   
            
        else:
            if form!="":
                attribute_Dict, attribute_List=Form(attribute_Dict, attribute_List, row, legacy_num, form,sap_class,"MICRO NUTRIENT FORM","MICRO_FORM",5)
                charg_group=charg_group.replace(form,"")
            product=charg_group.strip()
            attribute_Dict, attribute_List=fertProduct(attribute_Dict, attribute_List, row, legacy_num, product, sap_class)
            attribute_Dict, attribute_List=PackageConfig(attribute_Dict, attribute_List, row, legacy_num, sap_class)
            attribute_Dict, attribute_List=Brand(attribute_Dict, attribute_List, row, legacy_num, sap_class,7)   
        
        return descriptionRetrieve(attribute_Dict, attribute_List, row, sap_class), otherChar(legacy_num, row, otherList, sap_class)
        
    except IndexError:
        return eject(row, legacy_num,"ERROR:INDEX ERROR",row["Name"])
        

    
def format_Fert_Bulk(row, legacy_num):
    attribute_Dict=[]
    attribute_List=[]
    otherList=[]
    
    row["ItemDescriptionPart1"]=mfgRemoval(row, str(row["ItemDescriptionPart3"]).strip().upper())
    
    try:
        sap_class='M_FERT_BULK'
        if row["ProductCategory"] in id_dict:
            sap_class=id_dict[row["ProductCategory"]]
            #sap_class=classCalc(row,classItem[0],classItem[1])
        elif str(row["AGRISItemID"]) in mapDict:
            sap_class=mapDict[str(row["AGRISItemID"])]
        else:
            return eject(row, legacy_num,"ERROR:PRODUCT CATEGORY NOT MAPPED",row["ProductCategory"])
        
        form=formCalc(row)
        if form!="":
            attribute_Dict, attribute_List=Form(attribute_Dict, attribute_List, row, legacy_num, form, sap_class,"FORM","FERT_FORM",3)
            row['ItemDescriptionPart1']=row['ItemDescriptionPart1'].replace(form,"")
        if sap_class !="M_FERT_POTASH" and sap_class !="M_FERT_POTASSIUM":
            state=stateCalc(row)
            attribute_Dict, attribute_List=Create_Characteristic_Abbrev(attribute_Dict,attribute_List,row,legacy_num,state,sap_class,"FERTILIZER STATE","FERT_STATE",5)
        guar_analysis, fert_add_list, comm_desc=guaranteed_analysis_calc(row['ItemDescriptionPart1'])
        
        attribute_Dict, attribute_List=fertGuaranteedAnalysis(attribute_Dict, attribute_List, row, legacy_num,guar_analysis.strip(",+)("),sap_class)
        attribute_Dict, attribute_List=commDescript(attribute_Dict, attribute_List, row, legacy_num,comm_desc,sap_class)
        attribute_Dict, attribute_List=fertAdd(attribute_Dict, attribute_List, row, legacy_num,fert_add_list,sap_class)
        
        attribute_Dict, attribute_List=Brand(attribute_Dict, attribute_List, row, legacy_num, sap_class,7)
        attribute_Dict, attribute_List=PackageConfigFertBulk(attribute_Dict, attribute_List, row, legacy_num, sap_class)
        
        return descriptionRetrieve(attribute_Dict, attribute_List, row, sap_class), otherChar(legacy_num, row, otherList, sap_class)
        
    except IndexError:
        return eject(row, legacy_num,"ERROR:INDEX ERROR",row["Name"])  

    

def format_feed(row, legacy_num):
    attribute_Dict=[]
    attribute_List=[]
    otherList=[]
    
    row["ItemDescriptionPart1"]=mfgRemoval(row, str(row["ItemDescriptionPart3"]).strip().upper())
    
    id1=(str(row["ProductCategory"])+str(row["ProductType"])).strip().upper()
    id2=str(row["ProductType"]).strip().upper()
    id3=str(row["ProductCategory"]).strip().upper()
    sap_class="M_FEED"
    if " BLOCK " in row["ItemDescriptionPart1"]:
        sap_class="M_FEED_BLOCK"
    elif " TUB " in row["ItemDescriptionPart1"]:
        sap_class="M_FEED_PROTEIN_TUB"
    elif id1 in id_dict:
        sap_class=id_dict[id1]
    elif id2 in id_dict:
        sap_class=id_dict[id2]
        id1=id2
    elif id3 in id_dict:
        sap_class=id_dict[id3]
        id1=id3
    
    else:
        return eject(row, legacy_num,"ERROR:PRODUCT CATEGORY AND PRODUCT TYPE NOT MAPPED",str(row["ProductCategory"]+" "+row["ProductType"]))
        
    feed_desc=[]
    medicateList=[]
    additiveList=[]
    char_group=str(row["ItemDescriptionPart1"])
    group_list=char_group.split()
    marker=len(group_list)
    
    packageFound=False
    mfgFound=False
    
   
    if sap_class=="M_FEED_MEDICATION":
        exceptionDict={'DC.125%':12,'DC.5%':12, 'DC568':12,'AS700':11}
        levelList=[]
        for i in range(0,len(group_list)):
            if numericFound(group_list[i]) and group_list[i] not in exceptionDict:
                levelList.append(group_list[i])
            elif group_list[i] in prof_char_feed_dict:
                if prof_char_feed_dict[group_list[i]]==11 or group_list[i]=='BIOMOS':
                    feed_desc.append(group_list[i])
                elif prof_char_feed_dict[group_list[i]]==12:
                    additiveList.append(group_list[i])
                elif prof_char_feed_dict[group_list[i]]==15:
                    attribute_Dict,attribute_List=Form(attribute_Dict,attribute_List,row,legacy_num,group_list[i],sap_class,"FEED FORM","FEED_FORM",8)
                elif prof_char_feed_dict[group_list[i]]==16:
                    packageFound=True
                    attribute_Dict,attribute_List=feedPackage(attribute_Dict, attribute_List,row,legacy_num,group_list[i],sap_class,id1)
                elif prof_char_feed_dict[group_list[i]]==17:
                    mfgFound=True
                    attribute_Dict, attribute_List=brandOther(attribute_Dict,attribute_List,row,legacy_num,group_list[i],sap_class,2)
                elif prof_char_feed_dict[group_list[i]]==18:
                    feed_desc.append(str(group_list[i]))
            elif group_list[i].startswith("WITH"):
                additiveList.append(group_list[i].replace("WITH",""))
            else:
                feed_desc.append(group_list[i])
        if levelList:
            medicateList.append(" ".join(levelList))
        elif 'AS700' in char_group:
            medicateList.append('700G')
    else:
        for i in range(0,len(group_list)):
                
            if group_list[i] in prof_char_feed_dict:
                    
                if prof_char_feed_dict[group_list[i]]==11:
                    marker=i
                    medicateList.append(group_list[i])
                elif prof_char_feed_dict[group_list[i]]==12:
                    marker=i
                    if sap_class=="M_FEED_INGREDIENT":
                        feed_desc.append(group_list[i])
                    else:
                        additiveList.append(group_list[i])
                elif prof_char_feed_dict[group_list[i]]==15:
                    attribute_Dict,attribute_List=Form(attribute_Dict,attribute_List,row,legacy_num,group_list[i],sap_class,"FEED FORM","FEED_FORM",8)
                elif prof_char_feed_dict[group_list[i]]==16:
                    packageFound=True
                    attribute_Dict,attribute_List=feedPackage(attribute_Dict, attribute_List,row,legacy_num,group_list[i],sap_class,id1)
                elif prof_char_feed_dict[group_list[i]]==17:
                    mfgFound=True
                    attribute_Dict, attribute_List=brandOther(attribute_Dict,attribute_List,row,legacy_num,group_list[i],sap_class,2)
                elif prof_char_feed_dict[group_list[i]]==18:
                    feed_desc.append(str(group_list[i]))
            elif feed_analysis_calc(group_list[i]):
                attribute_Dict,attribute_List=feedGuaranteedAnalysis(attribute_Dict,attribute_List,row,legacy_num,group_list[i].strip(",)(+"),sap_class)
            elif group_list[i].startswith("WITH"):
                marker=i
                additiveList.append(group_list[i].replace("WITH",""))    
            elif i < marker:
                feed_desc.append(str(group_list[i]))
            elif '%' in group_list[i]:
                feed_desc.append(str(group_list[i]))
            elif i==len(group_list)-1 and obsoleteAttribute(attribute_Dict, medicateList, additiveList, group_list[i]):
                pass
            
            else:
                return eject(row, legacy_num,"ERROR:CHAR NOT IDENTIFIED",group_list[i]) 

    if not packageFound:
        package=packageCheck(row["PackageSize"])
        if package!="NA":
            attribute_Dict,attribute_List=feedPackage(attribute_Dict,attribute_List,row,legacy_num,package,sap_class,id1)
        else:
            return eject(row, legacy_num,"ERROR:PACKAGE NOT IDENTIFIED",row["PackageSize"]) 
    if feed_desc:
        tradeName=" ".join(feed_desc)
        attribute_Dict,attribute_List=feedTradeName(attribute_Dict,attribute_List,row,legacy_num,tradeName,sap_class)
    if medicateList:
        medicateList=list(set(medicateList))
        attribute_Dict,attribute_List=feedMedicationLevel(attribute_Dict,attribute_List,row,legacy_num,medicateList,sap_class)
    if additiveList:
        additiveList=list(set(additiveList))
        attribute_Dict,attribute_List=feedMedication(attribute_Dict, attribute_List,row, legacy_num,additiveList,sap_class)
    if not mfgFound:
        attribute_Dict, attribute_List=Brand(attribute_Dict,attribute_List,row,legacy_num,sap_class,2)
    attribute_Dict, attribute_List=feedPackageSize(attribute_Dict,attribute_List,row,legacy_num,row["ItemDescriptionPart2"],sap_class,id1)
    return descriptionRetrieve(attribute_Dict, attribute_List, row, sap_class), otherChar(legacy_num, row, otherList, sap_class)
    

def format_Shop_Merch(row, legacy_num):
    sap_class="M_MERCH&SHOP"
    attribute_Dict=[]
    attribute_List=[]
    otherList=[]
    
    row["ItemDescriptionPart1"]=mfgRemoval(row, str(row["ItemDescriptionPart3"]).strip().upper())
    id1=str(row["ProductCategory"])
    if id1 in id_dict:
        sap_class=id_dict[id1]
    else:
        return eject(row, legacy_num,"ERROR:PRODUCT CATEGORY NOT MAPPED",row["ProductCategory"])
    desc=str(row["ItemDescriptionPart1"])
    attribute_Dict,attribute_List=shopORmerchDesc(attribute_Dict,attribute_List,row,legacy_num,desc,sap_class)
    attribute_Dict,attribute_List=PackageConfig(attribute_Dict, attribute_List, row, legacy_num, sap_class)
    attribute_Dict,attribute_List=Brand(attribute_Dict, attribute_List, row, legacy_num, sap_class,7)
    
    return descriptionRetrieve(attribute_Dict, attribute_List, row, sap_class), otherChar(legacy_num, row, otherList, sap_class)
    
    
def formatOther(row, legacy_num, businessID):
    sap_class="NO_CLASS"
    
    baseList=["M_GENERAL_MERCH","M_FARM_SUPPLY","M_MERCH_HARDWARE","M_MERCH_PRESC_AG","M_MERCH_TANKS","M_SHOP_SPLY_SALES"]
    baseList2=["M_ANTIFREEZE", "M_FUEL_ADDITIVES", "M_SPECIALITY_LUBES"]
    baseList3=["M_AUTO_ACCESSORIES","M_LUBE_FUEL_EQUIP"]
    
    attribute_Dict=[]
    attribute_List=[]
    otherList=[]
    
    row["ItemDescriptionPart1"]=mfgRemoval(row, str(row["ItemDescriptionPart3"]).strip().upper())
    id1=str(row["ProductCategory"])+str(businessID)
    if id1 in id_dict:
        sap_class=id_dict[id1]
    elif str(row["ProductCategory"]) in id_dict:
        sap_class=id_dict[str(row["ProductCategory"])]
    else:
        return eject(row, legacy_num,"ERROR:PRODUCT CATEGORY NOT MAPPED",row["ProductCategory"])
    
    if sap_class in baseList:
        desc=str(row["ItemDescriptionPart1"])
        attribute_Dict,attribute_List=shopORmerchDesc(attribute_Dict,attribute_List,row,legacy_num,desc,sap_class)
        attribute_Dict,attribute_List=PackageConfig(attribute_Dict, attribute_List, row, legacy_num, sap_class)
        attribute_Dict,attribute_List=Brand(attribute_Dict, attribute_List, row, legacy_num, sap_class,7)
    elif sap_class in baseList2:
        desc=str(row["ItemDescriptionPart1"])
        name,brand=extractBrand(desc)
       
        attribute_Dict,attribute_List=productName(attribute_Dict,attribute_List,row,legacy_num,name,sap_class)
        attribute_Dict,attribute_List=PackageConfig(attribute_Dict, attribute_List, row, legacy_num, sap_class)
        
        if brand!="":
            attribute_Dict,attribute_List=brandOther(attribute_Dict,attribute_List,row,legacy_num,brand,sap_class,1)
            
    elif sap_class in baseList3:
        desc=str(row["ItemDescriptionPart1"])
        attribute_Dict,attribute_List=shopORmerchDesc(attribute_Dict,attribute_List,row,legacy_num,desc,sap_class)
        attribute_Dict,attribute_List=PackageConfig(attribute_Dict, attribute_List, row, legacy_num, sap_class)
        attribute_Dict,attribute_List=Brand(attribute_Dict, attribute_List, row, legacy_num, sap_class,2)
    
    elif sap_class=="M_LUBRICANTS":
    
        char_group=str(row["ItemDescriptionPart1"])
        group_list=char_group.split()
        tradename=[]
        for item in group_list:
            
            if item in prof_char_feed_dict:
                
                if prof_char_feed_dict[item]==30:
                    attribute_Dict,attribute_List=SAE_Viscosity(attribute_Dict,attribute_List,row,legacy_num,item,sap_class)
                    
                elif prof_char_feed_dict[item]==31:
                    attribute_Dict,attribute_List=ISO_Viscosity(attribute_Dict,attribute_List,row,legacy_num,item,sap_class)
                
                elif prof_char_feed_dict[item]==33 and ("EP" in char_group):
                    attribute_Dict,attribute_List=ISO_Viscosity(attribute_Dict,attribute_List,row,legacy_num,item,sap_class)
                elif prof_char_feed_dict[item]==34 and ("SAE" in char_group):
                    attribute_Dict,attribute_List=SAE_Viscosity(attribute_Dict,attribute_List,row,legacy_num,item,sap_class)
                else:
                    tradename.append(item)
            else:
                tradename.append(item)
        trade_name=" ".join(tradename).replace("SAE","")
        attribute_Dict,attribute_List=PackageConfig(attribute_Dict, attribute_List, row, legacy_num, sap_class)
        attribute_Dict,attribute_List=Brand(attribute_Dict,attribute_List,row,legacy_num,sap_class,5)
        attribute_Dict,attribute_List=tradeName(attribute_Dict,attribute_List,row,legacy_num,trade_name,sap_class)
        
    elif sap_class=="M_GREASE":
        desc=str(row["ItemDescriptionPart1"])
        name,brand=extractBrand(desc)
        
        if brand!="":
            attribute_Dict,attribute_List=brandOther(attribute_Dict,attribute_List,row,legacy_num,brand,sap_class,1)
            
        group_list=name.split()
        product_name=[]
        
        for item in group_list:
            if item in prof_char_feed_dict:
                
                if prof_char_feed_dict[item]==36:
                    attribute_Dict,attribute_List=NLGI_Grade(attribute_Dict,attribute_List,row,legacy_num,item,sap_class)
                    
                elif prof_char_feed_dict[item]==37:
                    attribute_Dict,attribute_List=NLGI_Grade(attribute_Dict,attribute_List,row,legacy_num,item,sap_class)
                    product_name.append(nlgiSplit(item))
                    
                elif prof_char_feed_dict[item]==32 and ("EP" in name):
                    attribute_Dict,attribute_List=NLGI_Grade(attribute_Dict,attribute_List,row,legacy_num,item,sap_class)
                    
                else:
                    product_name.append(item)
            else:
                product_name.append(item)
        product_name=" ".join(product_name).replace("EP","")
        attribute_Dict,attribute_List=PackageConfig(attribute_Dict, attribute_List, row, legacy_num, sap_class)
        if product_name!="":
            attribute_Dict,attribute_List=productName(attribute_Dict,attribute_List,row,legacy_num,product_name,sap_class)
    else:
        return eject(row, legacy_num,"ERROR:LOGIC NOT SET UP",row["Name"])
    
    return descriptionRetrieve(attribute_Dict, attribute_List, row, sap_class), otherChar(legacy_num, row, otherList, sap_class)


