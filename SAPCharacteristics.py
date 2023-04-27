'''
This file contains the separate formatting functions for each material's SAP Characteristic.
Each function takes in an already determined characteristic, and formats it into a list which
will be exported into an excel document. Any abbreviations are put back into their regular form.
Characteristic descriptions are limited to 30 Characters.

Each function takes constant time.
'''

from AbbrevAndChar import abbrev_check, prof_abbrev_dict, prof_abbrev_dict_feed, package_dict, MFG_Dict

notValidList=["&", "/", ".", ",","#", "+"]

def seedVariety_1(attribute_Dict,attribute_List, group_list_i,row,legacy_num):


    seed_variety=str(group_list_i).strip().upper()
    attribute_Dict.append((3,"SEED VARIETY",seed_variety))
 
    if len(seed_variety)>30:
        seed_variety=seed_variety[:30] 
    attribute_List.append({"Key":3,"Legacy Number":legacy_num, "Legacy Description":row["Name"],"Characteristic":"SEED_VARIETY", "Characteristic Description":seed_variety})
    return attribute_Dict, attribute_List
    
def seedSize(attribute_Dict, attribute_List, group_list_i, marker, size_count,row,legacy_num,i):
    
    seed_size=str(group_list_i).strip().upper()
    attribute_Dict.append((5,f"SEED SIZE",seed_size))
    
    if len(seed_size)>30:
        seed_size=seed_size[:30]
    attribute_List.append({"Key":5,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":f"SEED_SIZE_{size_count}", "Characteristic Description":seed_size})
    marker=i
    size_count+=1
    return attribute_Dict, attribute_List, size_count, marker

def seedTrait(attribute_Dict, attribute_List, group_list_i, marker, trait_count,row,legacy_num,i):
    
    seed_trait=str(group_list_i).strip().upper()
    attribute_Dict.append((4,f"SEED TRAIT",seed_trait))
    
    if len(seed_trait)>30:
        seed_trait=seed_trait[:30]   
    attribute_List.append({"Key":4,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":f"SEED_TRAIT_{trait_count}", "Characteristic Description":seed_trait}) 
    marker=i
    trait_count+=1
    return attribute_Dict, attribute_List, trait_count, marker

def seedTreatment(attribute_Dict, attribute_List, group_list_i, marker, treat_count,row,legacy_num,i):
    
    seed_treatment=str(group_list_i).strip().upper()
    attribute_Dict.append((6,f"SEED TREATMENT", seed_treatment))
    
    if len(seed_treatment)>30:
        seed_treatment=seed_treatment[:30] 
    attribute_List.append({"Key":6,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":f"SEED_TREATMENT_{treat_count}", "Characteristic Description":seed_treatment})
    marker=i
    treat_count+=1
    return attribute_Dict, attribute_List,treat_count, marker
    
def seedClass(attribute_Dict, attribute_List, group_list_i, marker, class_count,row,legacy_num,i):
    
    seed_class=str(group_list_i).strip().upper()
    attribute_Dict.append((4,f"SEED CLASS",seed_class))
    
    
    if len(seed_class)>30:
        seed_class=seed_class[:30]
    attribute_List.append({"Key":4,"Legacy Number":legacy_num, "Legacy Description":row["Name"],"Characteristic":f"SEED_CLASS_{class_count}", "Characteristic Description":seed_class})
    class_count+=1
    return attribute_Dict, attribute_List, class_count, marker
    
def additionalFeat(attribute_Dict, attribute_List, group_list_i, marker,row,legacy_num,i):
    
    add_feat=str(group_list_i).strip().upper()
    attribute_Dict.append((7,"ADDITIONAL FEATURES",add_feat))
    
    if len(add_feat)>30:
        add_feat=add_feat[:30] 
    attribute_List.append({"Key":7,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"ADDITIONAL_FACTORS", "Characteristic Description":add_feat})
    marker=i
    return attribute_Dict, attribute_List, marker
    

     
def seedPackageSize(attribute_Dict,attribute_List,row,legacy_num):
    seed_package_configuration=str(row["ItemDescriptionPart2"]).strip().upper()
    
    if seed_package_configuration!="NAN":
        pkg=packageCheck(row["PackageSize"])
        if pkg!="NA" and pkg not in seed_package_configuration:
            seed_package_configuration=seed_package_configuration+" "+pkg
        consol_pkg=seed_package_configuration.replace("BULK","").replace("EACH","").strip()
        if consol_pkg!="":
            attribute_Dict.append((8,"SEED PACKAGE CONFIGURATION", consol_pkg))
        attribute_List.append({"Key":8,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"SEED_PACKAGE_CONFIGURATION", "Characteristic Description":seed_package_configuration})
    return attribute_Dict, attribute_List

def fertProduct(attribute_Dict, attribute_List, row, legacy_num, product, sap_class):
    if product!="":
        attribute_Dict.append((1,"PRODUCT",product.strip().upper()))
        if len(product)>30:
            product=product[:30]
        attribute_List.append({"Key":3,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"PRODUCT", "Characteristic Description":product.strip().upper(), "SAP Class":sap_class})
    return attribute_Dict, attribute_List

def fertPercent(attribute_Dict, attribute_List, row, legacy_num, percent, sap_class):
    attribute_Dict.append((2,"PERCENTAGE CONCENTRATION",percent.strip().upper()))
    attribute_List.append({"Key":2,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"PERCENTAGE_CONCENTRATION", "Characteristic Description":percent, "SAP Class":sap_class})
    return attribute_Dict, attribute_List
    


def fertAddFact(attribute_Dict, attribute_List, row, legacy_num, sap_class, add_fact):
    if add_fact!="":
        add_fact=add_fact.strip().upper()
        attribute_Dict.append((3,"ADDITIONAL FACTORS",add_fact))
        if len(add_fact)>30:
            add_fact=add_fact[:30]
        attribute_List.append({"Key":3,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"ADDITIONAL_FACTORS", "Characteristic Description":add_fact, "SAP Class":sap_class})
    return attribute_Dict, attribute_List
def PackageConfig(attribute_Dict, attribute_List, row, legacy_num, sap_class):
    pkg_config=str(row["ItemDescriptionPart2"]).strip().upper()
    if pkg_config!="NAN":
        pkg=packageCheck(row["PackageSize"])
        if pkg!="NA" and pkg not in pkg_config:
            pkg_config=pkg_config+" "+pkg
        consol_pkg=pkg_config.replace("LIQ BULK","").replace("BULK","").replace("EACH","").strip()
        if consol_pkg!="":
            attribute_Dict.append((4,"PACKAGE CONFIGURATION",consol_pkg))
        attribute_List.append({"Key":4,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"PACKAGE_CONFIGURATION", "Characteristic Description":pkg_config, "SAP Class":sap_class})
    return attribute_Dict, attribute_List
def PackageConfigFertBulk(attribute_Dict, attribute_List, row, legacy_num, sap_class):
    pkg_config=str(row["ItemDescriptionPart2"]).strip().upper()
    if pkg_config!="NAN":
        pkg=packageCheck(row["PackageSize"])
        if pkg!="NA" and pkg not in pkg_config:
            pkg_config=pkg_config+" "+pkg
        consol_pkg=pkg_config.replace("LIQ BULK","").replace("BULK","").replace("EACH","").strip()
        if consol_pkg!="":
            attribute_Dict.append((4,"PACKAGE CONFIGURATION",consol_pkg))
        attribute_List.append({"Key":4,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"FERT_PACKAGE_CONFIGURATION", "Characteristic Description":pkg_config, "SAP Class":sap_class})
    return attribute_Dict, attribute_List


    
def fertGuaranteedAnalysis(attribute_Dict, attribute_List, row, legacy_num,guar_analysis ,sap_class):
    if guar_analysis!='NA':
        attribute_Dict.append((1,"GUARENTEED ANALYSIS",guar_analysis.strip()))
        attribute_List.append({"Key":1,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"FERT_GUARENTEED_ANALYSIS", "Characteristic Description":guar_analysis.strip(), "SAP Class":sap_class})
    return attribute_Dict, attribute_List

def commDescript(attribute_Dict, attribute_List, row, legacy_num,comm_desc,sap_class):
    comm_desc=comm_desc.strip().upper()
    if comm_desc!="" and comm_desc not in notValidList:
        attribute_Dict.append((2,"FERTILIZER COMMON DESCRIPTION",comm_desc))
        if len(comm_desc)>30:
            comm_desc=comm_desc[:30]  
        attribute_List.append({"Key":2,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"FERT_COMMON_DESCRIPTION", "Characteristic Description":comm_desc, "SAP Class":sap_class})
    return attribute_Dict, attribute_List
    
def fertAdd(attribute_Dict, attribute_List, row, legacy_num,fert_add_list,sap_class):
    counter=1
    uniqueDict={}
    if fert_add_list:
        for i in fert_add_list:
            if i not in uniqueDict:
                uniqueDict[i]=counter
                attribute_Dict.append((3,f'FERTILIZER ADDITIVE',i.strip().upper()))
                attribute_List.append({"Key":3,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":f'FERT_ADDITIVE_{counter}', "Characteristic Description":str(i).strip().upper(), "SAP Class":sap_class})
                counter+=1
    return attribute_Dict, attribute_List

def feedMedication(attribute_Dict, attribute_List,row, legacy_num,med,sap_class):
    uniqueDict={}
    for i in range(0,len(med)):
        medVar=abbrev_check(med[i].strip().upper(), prof_abbrev_dict_feed)
        if medVar not in uniqueDict:
            uniqueDict[medVar]=i
            attribute_Dict.append((4,f"NON MED ADDITIVE",medVar))
            if len(medVar)>30:
                medVar=medVar[:30]
            attribute_List.append({"Key":4,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":f"NON_MED_ADDITIVE_{i+1}", "Characteristic Description":medVar, "SAP Class":sap_class})
    return attribute_Dict, attribute_List

def feedMedicationLevel(attribute_Dict,attribute_List,row,legacy_num,level,sap_class):
    uniqueDict={}
    uniqueMed={}
    for i in range(0,len(level)):
        levelVar=abbrev_check(level[i].strip().upper(), prof_abbrev_dict_feed)
        
        if levelVar not in uniqueDict:
            uniqueDict[levelVar]=i
            attribute_Dict.append((5,f"MEDICATION DRUG LEVEL",levelVar))
            attribute_List.append({"Key":5,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":f"MEDICATION_DRUG_LEVEL_{i+1}", "Characteristic Description":levelVar, "SAP Class":sap_class})
    return attribute_Dict, attribute_List
    

    
def feedGuaranteedAnalysis(attribute_Dict,attribute_List,row,legacy_num,analysis,sap_class):
    analysis=analysis.strip().upper()
    attribute_Dict.append((3,"GUARENTEED ANALYSIS",analysis))
    attribute_List.append({"Key":3,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"FEED_GUARENTEED_ANALYSIS", "Characteristic Description":analysis, "SAP Class":sap_class})
    return attribute_Dict, attribute_List
    
def feedPackage(attribute_Dict,attribute_List,row,legacy_num,package,sap_class,id1):
    packagingList=["M_FEED_INGREDIENT"]
    char_desc="PACKAGE"
    package=abbrev_check(package.strip().upper(),prof_abbrev_dict_feed)
    if sap_class in packagingList:
        char_desc="PACKAGING"
    consol_pkg=package.replace("LIQ BULK","").replace("BULK","").replace("EACH","").strip()
    if consol_pkg!="":    
        attribute_Dict.append((11,char_desc,consol_pkg))
    attribute_List.append({"Key":11,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":char_desc, "Characteristic Description":package, "SAP Class":sap_class})
    return attribute_Dict, attribute_List
    
def feedPackageSize(attribute_Dict,attribute_List,row,legacy_num,package,sap_class,id1):
    configList=["M_FEED_BIRD_BRAND"]
    packagingList=["M_FEED_INGREDIENT"]
    char_desc="PACKED WEIGHT"
    char="PACKED_WEIGHT"
    package=abbrev_check(str(package).strip().upper(),prof_abbrev_dict_feed)
    if sap_class in configList:
        char_desc="PACKAGE CONFIGURATION"
        char="PACKAGE_CONFIGURATION"
    elif sap_class in packagingList:
        char_desc="PACKAGE SIZE"
        char="PACKAGE_SIZE"
    consol_pkg=package.replace("LIQ BULK","").replace("BULK","").replace("EACH","").strip()
    if consol_pkg!="":
        attribute_Dict.append((10,char_desc,consol_pkg))
        
    attribute_List.append({"Key":10,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":char, "Characteristic Description":package, "SAP Class":sap_class})
    return attribute_Dict, attribute_List
    

    
def feedTradeName(attribute_Dict,attribute_List,row,legacy_num,desc,sap_class):
    desc=desc.strip().upper()
    attribute_Dict.append((3,"TRADE NAME",desc))
    if len(desc)>30:
        desc=desc[:30]  
    attribute_List.append({"Key":3,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"TRADE_NAME", "Characteristic Description":desc, "SAP Class":sap_class})
    return attribute_Dict, attribute_List
   
def shopORmerchDesc(attribute_Dict,attribute_List,row,legacy_num,desc,sap_class):
    char_desc=""
    char=""
    
    if sap_class=="M_FARM_SUPPLY":
        char_desc="FARM SUPPLY DESCRIPTION"
        char="FARM_SUPPLY_DESCRIPTION"
    elif sap_class=="M_GENERAL_MERCH":
        char_desc="MERCHANDISE DESCRIPTION"
        char="MERCHANDISE_DESCRIPTION"
    elif sap_class=="M_SHOP_SPLY_SALES":
        char_desc="MERCHANDISE DESCRIPTION"
        char="SHOP_SUPPLY_DESCRIPTION"
    elif sap_class=="M_MERCH_HARDWARE":
        char_desc="HARDWARE DESCRIPTION"
        char="HARDWARE_DESCRIPTION"
    elif sap_class=="M_MERCH_TANKS":
        char_desc="TANK DESCRIPTION"
        char="TANK_DESCRIPTION"
    elif sap_class=="M_MERCH_PRESC_AG":
        char_desc="PRECISION AG MERCH DESC"
        char="PRECISION_AG_MERCH_DESC"
    elif sap_class=="M_AUTO_ACCESSORIES":
        char_desc="MERCHANDISE DESCRIPTION"
        char="MERCHANDISE_DESCRIPTION"
    elif sap_class=="M_LUBE_FUEL_EQUIP":
        char_desc="EQUIPMENT DESCRIPTION"
        char="EQUIPMENT_DESCRIPTION"
    desc=desc.strip().upper().replace("\"","IN").replace("'","FT")
  
    attribute_Dict.append((1,char_desc,desc))
    if len(desc)>30:
        desc=desc[:30] 
    attribute_List.append({"Key":1,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":char, "Characteristic Description":desc, "SAP Class":sap_class})
    return attribute_Dict, attribute_List
    
    
def productName(attribute_Dict,attribute_List,row,legacy_num,name,sap_class):
 
    name=name.strip("- ")
    if name!="":
        attribute_Dict.append((2,"PRODUCT NAME",name))
        if len(name)>30:
            name=name[:30]
        attribute_List.append({"Key":2,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"PRODUCT_NAME", "Characteristic Description":name, "SAP Class":sap_class})
    return attribute_Dict, attribute_List
    

    
    
def SAE_Viscosity(attribute_Dict,attribute_List,row,legacy_num,viscosity,sap_class):
    viscosity=str(abbrev_check(viscosity.strip().upper(),prof_abbrev_dict_feed))
    attribute_Dict.append((2,"SAE VISCOSITY",viscosity))
    attribute_List.append({"Key":2,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"SAE_VISCOSITY", "Characteristic Description":viscosity, "SAP Class":sap_class})
    return attribute_Dict, attribute_List
    
def ISO_Viscosity(attribute_Dict,attribute_List,row,legacy_num,viscosity,sap_class):
    viscosity=str(abbrev_check(viscosity.strip().upper(),prof_abbrev_dict_feed))
    attribute_Dict.append((2,"ISO VISCOSITY",viscosity))
    attribute_List.append({"Key":2,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"ISO_VISCOSITY", "Characteristic Description":viscosity, "SAP Class":sap_class})
    return attribute_Dict, attribute_List
def NLGI_Grade(attribute_Dict,attribute_List,row,legacy_num,grade,sap_class):
    grade=str(abbrev_check(grade.strip().upper(),prof_abbrev_dict_feed))
    attribute_Dict.append((3,"NLGI GRADE",grade))
    attribute_List.append({"Key":3,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"NLGI_GRADE", "Characteristic Description":grade, "SAP Class":sap_class})
    return attribute_Dict, attribute_List
    

    
def tradeName(attribute_Dict,attribute_List,row,legacy_num,trade_name,sap_class):
    attribute_Dict.append((1,"TRADE NAME",trade_name))
    if len(trade_name)>30:
        trade_name=trade_name[:30]  
    attribute_List.append({"Key":1,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"TRADE_NAME_BRAND", "Characteristic Description":trade_name, "SAP Class":sap_class})
    return attribute_Dict, attribute_List
    
def packageCheck(UOM):
    if UOM in package_dict:
        return package_dict[UOM]
    return "NA"
'''
eject function handles materials that cannot be cleansed. 
It takes in the reason, and reason description for why the material was not cleansed.
Runtime of O(1)
'''
def eject(row, legacy_num,reason,reason_desc):
    attribute_List_eject=[{"Legacy Number":legacy_num, "Legacy Description":row["Name"],"Characteristic":reason_desc, "Characteristic Description":reason,"Short Description (SAP)":"DOES NOT FOLLOW FORMAT", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT","SAP Class":"NO_CLASS"}]
    return attribute_List_eject,[]
    
'''
Brand function creates a Brand or Manufacturer characteristic based on ItemDescription3.
The key parameter varies between classes, and determines the ranking of the brand/mfg characteristic.
Runtime of O(1)
'''
    
def Brand(attribute_Dict, attribute_List, row, legacy_num, sap_class, key):

    classList=["M_AUTO_ACCESSORIES","M_LUBE_FUEL_EQUIP","M_FEED_INGREDIENT", "M_LUBRICANTS"]
    char="BRAND"
    
    if sap_class in classList:
        char="MANUFACTURER"
    
    brand=str(row["ItemDescriptionPart3"]).strip().upper()
    brandID=str(row["Manufacturer"])+str(row["ItemDescriptionPart3"])
    
    if brandID in MFG_Dict:
        brand=str(MFG_Dict[brandID])
        
    if brand!="NAN"and brand!="UNK" and brand!="UNKNOWN":
        attribute_Dict.append((key,char,brand))
        if len(brand)>30:
            brand=brand[:30]
        attribute_List.append({"Key":key,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":char, "Characteristic Description":brand, "SAP Class":sap_class})
        
    return attribute_Dict, attribute_List
    


'''
brandOther function creates a Brand or Manufacturer characteristic based on brand parameter.
The key parameter varies between classes, and determines the ranking of the brand/mfg characteristic.
O(1) Runtime
'''
    
def brandOther(attribute_Dict,attribute_List,row,legacy_num,brand,sap_class,key):
    brand=brand.strip().upper()
    
    classList=["M_AUTO_ACCESSORIES","M_LUBE_FUEL_EQUIP","M_FEED_INGREDIENT", "M_LUBRICANTS"]
    char="BRAND"
    
    if sap_class in classList:
        char="MANUFACTURER"
        
    if brand!="NAN"and brand!="UNK" and brand!="UNKNOWN":
        brand=abbrev_check(str(brand).strip().upper(),prof_abbrev_dict_feed)
        attribute_Dict.append((key,char,brand))
        attribute_List.append({"Key":key,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":char, "Characteristic Description":brand, "SAP Class":sap_class})
    return attribute_Dict, attribute_List

'''
Form function creates a form characteristic based on parameters
O(1) Runtime
'''
    
def Form(attribute_Dict,attribute_List,row,legacy_num,form,sap_class,desc,char,key):
    form=abbrev_check(form.strip().upper(),prof_abbrev_dict_feed)
    attribute_Dict.append((key,desc,form))
    attribute_List.append({"Key":key,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":char, "Characteristic Description":form, "SAP Class":sap_class})
    return attribute_Dict, attribute_List
    

def Create_Characteristic_Abbrev(attribute_Dict,attribute_List,row,legacy_num,char_value,sap_class,char_desc,char,key):
    char_value=abbrev_check(char_value.strip().upper(),prof_abbrev_dict_feed)
    attribute_Dict.append((key,char_desc,char_value))
    attribute_List.append({"Key":key,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":char, "Characteristic Description":char_value, "SAP Class":sap_class})
    return attribute_Dict, attribute_List

def Create_Characteristic(attribute_Dict,attribute_List,row,legacy_num,char_value,sap_class,char_desc,char,key):
    attribute_Dict.append((key,char_desc,char_value))
    attribute_List.append({"Key":key,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":char, "Characteristic Description":char_value, "SAP Class":sap_class})
    return attribute_Dict, attribute_List