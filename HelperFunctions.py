from AbbrevAndChar import package_dict, med_list, brand_list, prof_abbrev_dict, prof_char_dict, abbrev_check,prof_char_feed_dict, prof_abbrev_dict_feed
from SAPCharacteristics import seedVariety_1,seedTrait,seedClass,seedSize,seedTrait,seedTreatment,additionalFeat,Brand,seedPackageSize,eject
from Descriptions import create_descriptions
notValidList=["&", "/", ".", ",","#", "+"]

def fert_perc_helper(rowDesc):
    
    pointer=rowDesc.rfind('%')
    temp_point=pointer
    percentList=[]    
    while rowDesc[pointer]!=" " and rowDesc[pointer]!="-" and pointer>-1:
        percentList.append(rowDesc[pointer])
        pointer-=1
    percent="".join(percentList[::-1])
    product=rowDesc[0:pointer].strip()
    add_fact=rowDesc[temp_point+1:len(rowDesc)].strip()
    return percent,product,add_fact
    
    
    
def classCalc(row, sap_class1, sap_class2):
    sap_class=sap_class1
    if 'BULK' in row["ItemDescriptionPart2"].upper():
        sap_class=sap_class2
    return sap_class

def formCalc(row):
    form=""
    char_group=str(row["ItemDescriptionPart1"])
    group_list=char_group.split()
    for i in range(0,len(group_list)):
        if group_list[i] in prof_char_feed_dict and prof_char_feed_dict[group_list[i]]==15:
            form+=str(abbrev_check(group_list[i],prof_abbrev_dict_feed))
    return form
def guaranteed_analysis_calc(rowDesc):
    chargroup=rowDesc.split()
    tempChar=rowDesc.split()
    fert_add_list=[]
    g_analysis='NA'
    
    check=False
    for i in range(len(chargroup)):
       
        if chargroup[i].count('-')>1:
            var=chargroup[i]
            tempChar.remove(var)
            
            g_analysis, fert_addition=analysis_calc_helper(chargroup[i])
            [fert_add_list.append(x) for x in fert_addition]
            check=True
        elif chargroup[i].startswith('W/'):
            fert_add_list.append(" ".join(chargroup[i:len(chargroup)]).replace("W/",""))
         
            for x in range(i, len(chargroup)):
                tempChar.remove(chargroup[x])
            break 
        elif(check and element_seperator(str(chargroup[i]))!="NA"):
            fert_add_list.append(element_seperator(str(chargroup[i])))
            tempChar.remove(chargroup[i])
    comm_desc=" ".join(tempChar)
    return g_analysis,fert_add_list,comm_desc
    
def element_seperator(item):
    elementSet={'S','ZN','MN','MG','CU','CA','B','FE','NA','CL','CO','MO'}
    element=[]
    percent=[]
    
    for ch in item:
        if ch.isalpha():
            element.append(ch)
        elif ch.isnumeric() or ch=='.':
            percent.append(ch)
    if "".join(element) in elementSet:
        return "".join(percent)+"".join(element)
    return "NA"
def analysis_calc_helper(a1):
    
    dash_counter=0
    pointer=0
    g_analysis=[]
    fert_add_list=[]
    fert_add=""
    for i in range(0,len(a1)):
        pointer=i
        if a1[i]=='-':
            dash_counter+=1
            if dash_counter>2 : break
        g_analysis.append(a1[i])
        
    if dash_counter>2:
        fert_add=a1[pointer+1:len(a1)]
        fert_add_list=fert_add.split('-')
    return "".join(g_analysis), fert_add_list
    
    
def mostNumeric(str1):
    num_count=0
    for char in str1:
        if char.isnumeric():
            num_count+=1
        elif char.isalpha():
            return False
    if num_count/len(str1) >= .5:
        return True
    return False
    
def feed_analysis_calc(item):
    if item.count('-')>1 and mostNumeric(item):
        return True
    return False
    
def findMedication(abbrev):
    for item in med_list:
        if abbrev==item[0]:
            return item
    return "NA"
    
def mfgRemoval(row,mfg):
    return row["ItemDescriptionPart1"].replace(mfg,"")

def obsoleteAttribute(attributeDict, medicateList, additiveList, char):
    
    for item in attributeDict:
        if item[2].startswith(char):
            return True
    for item in medicateList:
        if item.startswith(char):
            return True
    for item in additiveList:        
        if item.startswith(char):
            return True
    return False
            
def numericFound(str1):
    for char in str1:
        if char.isnumeric():
            return True       
    return False
    
def descriptionRetrieve(attribute_Dict, attribute_List, row, sap_class):
    short_desc, Long_Desc, PO_Desc, long_special=create_descriptions(attribute_Dict,row,sap_class)
    for r in attribute_List:
        r["Short Description (SAP)"]=short_desc
        r["Long Description Special"]=long_special
        r["Long Description (SAP)"]=Long_Desc
        r["PO Description (SAP)"]=PO_Desc
        r["SAP Class"]=sap_class
        
    res_list=[i for n, i in enumerate(attribute_List) if i not in attribute_List[n+1:]]
    attribute_List_Sorted=sorted(res_list, key=lambda i:i["Key"])
    return attribute_List_Sorted
    
def extractBrand(desc):
    brand=""
    
    for item in brand_list:
        if item in desc:
            
            desc=desc.replace(item,"")
            brand=item
            return desc,brand

    return desc,brand

def nlgiSplit(str1):
    final=[]
    check=False
    for char in str1:
        if char.isnumeric() and not check:
            final.append(f" {char}")
        else:
            final.append(char)
    return "".join(final)
 
def otherMaster(legacy_num, row, otherList, sap_class):
    MasterDict={"ProductCategory":"AGRIS_PRODUCT_CATEGORY", "ProductType":"AGRIS_PRODUCT_TYPE", "Product":"AGRIS_EHS_PRODUCT", "Manufacturer":"AGRIS_MANUFACTURER", "IsActive":"AGRIS_ACTIVE", "LineOfBusiness":"AGRIS_LINE_OF_BUSINESS", "ReportingUOM":"AGRIS_REPORTING_UOM"}
    for item in MasterDict:
        if str(row[item]).upper().strip()!="NAN" and str(row[item]).upper().strip()!="" and str(row[item]).upper().strip()!="UNK":
            otherList.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":row[item], "Characteristic Description":MasterDict[item], "SAP Class":sap_class})
    return otherList

def otherB2B(legacy_num, row, otherList, sap_class):
    B2BDict={"B2BUOMCode":"B2B_UOM_CODE", "B2BOrderInMultiplesOf":"B2B_ORDER_UNITS", "B2BTradingPartnerCropTypeID":"B2B_CROP_TYPE", "Manufacturer":"B2B_TRADING_PARTNER", "SeedYear":"B2B_SEED_YEAR", "ItemDescriptionPart3":"B2B_BRAND"}
    B2B_BrandDict={"ASGROW":"ASG", "DEKALB":"DKC", "DELTAPIN":"DLP"}
    B2B_MfgList=["ZZZ", "BYR"]
    if str(row["LineOfBusiness"])=='203' and str(row["ItemDescriptionPart3"]).upper().strip() in B2B_BrandDict and str(row["Manufacturer"]) in B2B_MfgList:
        for item in B2BDict:
            otherList.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"B2B_RELEVANT_INDICATOR", "Characteristic Description":"X", "SAP Class":sap_class})
            if str(row[item]).upper().strip()!="NAN" and str(row[item]).upper().strip()!="":
                otherList.append({"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":row[item], "Characteristic Description":B2BDict[item], "SAP Class":sap_class})
    return otherList

def otherChar(legacy_num, row, otherList, sap_class):
    otherList+=otherB2B(legacy_num, row, otherList, sap_class)
    otherList+=otherMaster(legacy_num, row, otherList, sap_class)
    return otherList
def stateCalc(row):
    if 'LIQ' in str(row["ItemDescriptionPart2"]) or str(row["ItemDescriptionPart2"]).strip().endswith('G'):
        return 'LIQUID'
    return 'DRY'
def format1_cleanse(row, noun, nounMod,legacy_num, sap_class,tag):

    attribute_Dict=[]
    attribute_List=[]
    otherList=[]
    
    row["ItemDescriptionPart1"]=mfgRemoval(row, str(row["ItemDescriptionPart3"]).strip().upper())
    
    if nounMod!="nomod":
        attribute_Dict.append((2,"NOUN",noun+" "+nounMod))
        attribute_List.append({"Key":2,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"NOUN_MODIFIER", "Characteristic Description":nounMod})
        attribute_List.append({"Key":1,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"NOUN", "Characteristic Description":noun})
    else:
        attribute_Dict.append((1,"NOUN", noun))
        attribute_List.append({"Key":1,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"NOUN", "Characteristic Description":noun})
    
    trait_count=1
    size_count=1
    treat_count=1
    
    try:
        char_group=str(row["ItemDescriptionPart1"][4:])
        if tag:
            char_group=str(row["ItemDescriptionPart1"]).strip()
            
        group_list=char_group.split()
        marker=len(group_list)
        seed_variety=""
        for i in range(0,len(group_list)):
            if group_list[i] in prof_char_dict:
                if prof_char_dict[group_list[i]]==6:
                    attribute_Dict,attribute_List,trait_count, marker=seedTrait(attribute_Dict, attribute_List, group_list[i], marker, trait_count,row,legacy_num,i)
                   
                elif prof_char_dict[group_list[i]]==7:
                    attribute_Dict,attribute_List,size_count, marker=seedSize(attribute_Dict, attribute_List, group_list[i], marker, size_count,row,legacy_num,i)
                    
                elif prof_char_dict[group_list[i]]==8:
                    attribute_Dict,attribute_List,treat_count, marker=seedTreatment(attribute_Dict, attribute_List, group_list[i], marker, treat_count,row,legacy_num,i)
                    
                elif prof_char_dict[group_list[i]]==12 and (sap_class=="M_SEED_CORN" or sap_class=="M_SEED_SOYBEANS"):
                    attribute_Dict, attribute_List, marker=additionalFeat(attribute_Dict, attribute_List, group_list[i], marker,row,legacy_num,i)
                    
                elif prof_char_dict[group_list[i]]==16:
                    seed_variety+=" "+str(abbrev_check(group_list[i], prof_abbrev_dict))
                    
            elif i==0:
                seed_variety+=" "+str(abbrev_check(group_list[i], prof_abbrev_dict))
               
            else:
                return eject(row, legacy_num,"ERROR:CHAR NOT IDENTIFIED",group_list[i]) 
				
        if seed_variety!="":
            attribute_Dict,attribute_List=seedVariety_1(attribute_Dict,attribute_List, seed_variety,row,legacy_num)
            	
        attribute_Dict, attribute_List=seedPackageSize(attribute_Dict,attribute_List,row,legacy_num) 
        attribute_Dict,attribute_List=attribute_Dict,attribute_List=Brand(attribute_Dict, attribute_List,row,legacy_num, sap_class,9)
            
		#Getting Descriptions
        return descriptionRetrieve(attribute_Dict, attribute_List, row, sap_class), otherChar(legacy_num, row, otherList, sap_class)
		
    except IndexError:
    	return eject(row, legacy_num,"ERROR:INDEX ERROR",row["Name"])

def format2_cleanse(row, noun, nounMod,legacy_num, sap_class,tag):
    attribute_Dict=[]
    attribute_List=[]
    otherList=[]
    
    row["ItemDescriptionPart1"]=mfgRemoval(row, str(row["ItemDescriptionPart3"]).strip().upper())
    
    if nounMod!="nomod":
        attribute_Dict.append((2,"NOUN",noun+" "+nounMod))
        attribute_List.append({"Key":2,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"NOUN_MODIFIER", "Characteristic Description":nounMod})
        attribute_List.append({"Key":1,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"NOUN", "Characteristic Description":noun})
    else:
        attribute_Dict.append((1,"NOUN", noun))
        attribute_List.append({"Key":1,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"NOUN", "Characteristic Description":noun})
		
    trait_count=1
    size_count=1
    treat_count=1
    
    seed_variety=""
    try:
        char_group=str(row["ItemDescriptionPart1"][4:])
        if tag:
            char_group=str(row["ItemDescriptionPart1"]).strip()
        group_list=char_group.split()
        marker=len(group_list)
        for i in range(0,len(group_list)):
            
            if group_list[i] in prof_char_dict:
                
                if prof_char_dict[group_list[i]]==6:
                    attribute_Dict,attribute_List,trait_count, marker=seedTrait(attribute_Dict, attribute_List, group_list[i], marker, trait_count,row,legacy_num,i)
                   
                elif prof_char_dict[group_list[i]]==7:
                    attribute_Dict,attribute_List,size_count, marker=seedSize(attribute_Dict, attribute_List, group_list[i], marker, size_count,row,legacy_num,i)
                    
                elif prof_char_dict[group_list[i]]==8:
                    attribute_Dict,attribute_List,treat_count, marker=seedTreatment(attribute_Dict, attribute_List, group_list[i], marker, treat_count,row,legacy_num,i)
                    
                elif prof_char_dict[group_list[i]]==16:
                    seed_variety+=" "+str(abbrev_check(group_list[i], prof_abbrev_dict))
                    
                
            elif i==0:
                seed_variety+=str(group_list[i])
                
            elif i < marker:
                add=" "+str(group_list[i])
                seed_variety+=add
                
            elif group_list[i] in notValidList:
                return eject(row, legacy_num,"ERROR:CHAR NOT IDENTIFIED",group_list[i]) 
                
            else:
                return eject(row, legacy_num,"ERROR:CHAR NOT IDENTIFIED",group_list[i]) 
        if seed_variety.startswith("&"):
           return eject(row, legacy_num,"ERROR:CHAR NOT IDENTIFIED",seed_variety) 
            
        if seed_variety!="":
            seed_variety=str(seed_variety).strip().upper()
            attribute_Dict.append((3,"SEED VARIETY",seed_variety))
          
            if len(seed_variety)>30:
                seed_variety=seed_variety[:30]
            attribute_List.append({"Key":3,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"SEED_VARIETY", "Characteristic Description":seed_variety})		
		
        attribute_Dict, attribute_List=seedPackageSize(attribute_Dict,attribute_List,row,legacy_num) 
        attribute_Dict,attribute_List=Brand(attribute_Dict, attribute_List,row,legacy_num, sap_class,9)
            
		#Getting Descriptions
        return descriptionRetrieve(attribute_Dict, attribute_List, row, sap_class), otherChar(legacy_num, row, otherList, sap_class)
		
    except IndexError:
        return eject(row, legacy_num,"ERROR:INDEX ERROR",row["Name"])
		
def format3_cleanse(row, noun, nounMod,legacy_num,sap_class,tag):
    attribute_Dict=[]
    attribute_List=[]
    otherList=[]
    
    row["ItemDescriptionPart1"]=mfgRemoval(row, str(row["ItemDescriptionPart3"]).strip().upper())
    
    if nounMod!="nomod":
        attribute_Dict.append((2,"NOUN",noun+" "+nounMod))
        attribute_List.append({"Key":2,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"NOUN_MODIFIER", "Characteristic Description":nounMod})
        attribute_List.append({"Key":1,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"NOUN", "Characteristic Description":noun})
    else:
        attribute_Dict.append((1,"NOUN", noun))
        attribute_List.append({"Key":1,"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":"NOUN", "Characteristic Description":noun})
    
    trait_count=1
    size_count=1
    treat_count=1
    class_count=1
    
    try:
        char_group=str(row["ItemDescriptionPart1"][4:])
        if tag:
            char_group=str(row["ItemDescriptionPart1"]).strip()
        group_list=char_group.split()
        marker=len(group_list)
        seed_variety=""
        for i in range(0,len(group_list)):
            if group_list[i] in prof_char_dict:
                if prof_char_dict[group_list[i]]==6:
                    attribute_Dict, attribute_List, class_count, marker=seedClass(attribute_Dict, attribute_List, group_list[i], marker, class_count,row,legacy_num,i)
                    
                elif prof_char_dict[group_list[i]]==7:
                    attribute_Dict,attribute_List,size_count, marker=seedSize(attribute_Dict, attribute_List, group_list[i], marker, size_count,row,legacy_num,i)
                    
                elif prof_char_dict[group_list[i]]==8:
                    attribute_Dict,attribute_List,treat_count, marker=seedTreatment(attribute_Dict, attribute_List, group_list[i], marker, treat_count,row,legacy_num,i)
                    
                elif prof_char_dict[group_list[i]]==16:
                    seed_variety+=" "+str(abbrev_check(group_list[i], prof_abbrev_dict))                
                elif prof_char_dict[group_list[i]]==12 and sap_class=="M_SEED_WHEAT":
                    attribute_Dict, attribute_List, marker=additionalFeat(attribute_Dict, attribute_List, group_list[i], marker,row,legacy_num,i)
                   
            elif i==0:
                seed_variety+=" "+str(abbrev_check(group_list[i], prof_abbrev_dict))
            else:
                attribute_List_eject=[{"Legacy Number":legacy_num, "Legacy Description":row["Name"],"Characteristic":group_list[i], "Characteristic Description":"ERROR:CHAR NOT IDENTIFIED","Short Description (SAP)":"DOES NOT FOLLOW FORMAT", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT","SAP Class":sap_class}]
                return attribute_List_eject,[]
        if seed_variety!="":
            attribute_Dict,attribute_List=seedVariety_1(attribute_Dict,attribute_List, seed_variety,row,legacy_num)
            
        attribute_Dict, attribute_List=seedPackageSize(attribute_Dict,attribute_List,row,legacy_num) 
        attribute_Dict,attribute_List=attribute_Dict,attribute_List=Brand(attribute_Dict, attribute_List,row,legacy_num, sap_class,9)
            
		#Getting Descriptions		
        return descriptionRetrieve(attribute_Dict, attribute_List, row, sap_class), otherChar(legacy_num, row, otherList, sap_class)
		
    except IndexError:
        return eject(row, legacy_num,"ERROR:INDEX ERROR",row["Name"])