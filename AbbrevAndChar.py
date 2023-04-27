import pandas as pd

df_profisee_char=pd.read_excel('C:\\Users\\NParker\\Documents\\SupportingAutoDocs\\Profisee_char_list.xlsx')
df_profisee_abbrev=pd.read_excel('C:\\Users\\NParker\\Documents\\SupportingAutoDocs\\Profisee_Abbrev_List.xlsx')
df_sap_abbrev=pd.read_excel("C:\\Users\\NParker\\Documents\\SupportingAutoDocs\\SAP_Abbrev_List.xlsx")
df_class_list=pd.read_excel("C:\\Users\\NParker\\Documents\\SupportingAutoDocs\\Seed_Class_List.xlsx")
df_id_list=pd.read_excel("C:\\Users\\NParker\\Documents\\SupportingAutoDocs\\ID_List.xlsx")
df_profisee_abbrev_feed=pd.read_excel("C:\\Users\\NParker\\Documents\\SupportingAutoDocs\\Profisee_Abbrev_NOTSEED.xlsx")
df_package=pd.read_excel("C:\\Users\\NParker\\Documents\\SupportingAutoDocs\\PackageList.xlsx")
df_manual_map=pd.read_excel("C:\\Users\\NParker\\Documents\\SupportingAutoDocs\\ManualMAPPING.xlsx")
df_MFG=pd.read_excel("C:\\Users\\NParker\\Documents\\SupportingAutoDocs\\MFG_List.xlsx")


def prof_char_dict_generator(char_df):
	char_dict={}
	for index, row in char_df.iterrows():
		char_dict[str(row["Abbreviation"])]=row["IngredientType"]
	return char_dict
prof_char_dict=prof_char_dict_generator(df_profisee_char)
prof_char_feed_dict=prof_char_dict_generator(df_profisee_abbrev_feed)
def prof_ab_dict_generator(char_df):
	char_dict={} 
	for index, row in char_df.iterrows():
		char_dict[row["Abbreviation"]]=row["Abbreviated Word"]
	return char_dict
prof_abbrev_dict=prof_ab_dict_generator(df_profisee_abbrev)
prof_abbrev_dict_feed=prof_ab_dict_generator(df_profisee_abbrev_feed)
def sap_ab_dict_generator(char_df):
	char_dict={}
	for index, row in char_df.iterrows():
		char_dict[row["Abbreviated Word"]]=row["Abbreviation"]
	return char_dict
sap_abbrev_dict=sap_ab_dict_generator(df_sap_abbrev)

def prof_class_list_generator(char_df):
    classList=[]
    for index,row in char_df.iterrows():
        classList.append({"ABBREVIATION":row["ABBREVIATION"], "NOUN":row["NOUN"], "NOUNMODIFIER":row["NOUNMODIFIER"], "CLASS":row["CLASS"], "DEFAULT":row["DEFAULT NOUN"],"FORMAT":row["FORMAT"]})
    return classList  
prof_class_list=prof_class_list_generator(df_class_list)    

def id_generator(char_df):
    id_dict={}
    for index,row in char_df.iterrows():
        id_dict[str(row["Product ID"])]=row["Class"]
    return id_dict
id_dict=id_generator(df_id_list)
def medication_list_generator(char_df):
    med_list=[]
    for index, row in char_df.iterrows():
        if row["IngredientType"]==11:
            med_list.append((row["Abbreviation"], row["DRUG P1"], row["DRUG P2"]))
    return med_list
med_list=medication_list_generator(df_profisee_abbrev_feed)

def findItem(nounMod):
    for item in prof_class_list:
        if item["ABBREVIATION"]==nounMod:
            return item["NOUN"], item["NOUNMODIFIER"], item["CLASS"], item["FORMAT"]
    return "notfound","notfound","notfound","notfound"
def findDefault(sap_class):
    for item in prof_class_list:
        if item["CLASS"]==sap_class:
            return item["NOUN"], item["NOUNMODIFIER"],item["FORMAT"]
    return "notfound","notfound","notfound"
def abbrev_check(val, abbrev_dict):
    val_new=val
    if val in abbrev_dict:
        val_new=abbrev_dict[val]
    return val_new
    
def package_dict_generator(char_df):
	char_dict={}
	for index, row in char_df.iterrows():
		char_dict[row["Code"]]=row["Packaging"]
	return char_dict
package_dict=package_dict_generator(df_package)

def brandList(char_df):
    brand_list=[]
    for index, row in char_df.iterrows():
        if row["IngredientType"]==17:
            brand_list.append(row["Abbreviation"])
    return brand_list
    
brand_list=brandList(df_profisee_abbrev_feed)

def manualMappingDict(char_df):
    char_dict={}
    for index, row in char_df.iterrows():
	    char_dict[str(row["SOURCE ID"])]=row["MANUALLY ASSIGNED CLASS"]
    return char_dict
mapDict=manualMappingDict(df_manual_map)


def mfgDict(char_df):
    char_dict={}
    char_dict2={}
    for index, row in char_df.iterrows():
        char_dict[row["Abbreviation"]]=row["Abbreviated Word"]
        char_dict2[row["Abbreviation"]]=row["SAP Short ABBREV"]
    return char_dict,char_dict2
MFG_Dict, MFG_Dict_Short=mfgDict(df_MFG) 