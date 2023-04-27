import pandas as pd
import time
import datetime
from AbbrevAndChar import prof_char_dict, prof_abbrev_dict, sap_abbrev_dict,findItem
from Formats import format1_cleanse, format2_cleanse, format3_cleanse, format_chem, format_Fert_Micro, format_Fert_Bulk, format_Shop_Merch,format_feed, formatOther, format_seed


#Starting timer to track how long this prpgram takes to run (in seconds)
start_time = time.time()

#Importing the file which contains uncleansed IMM profisee data
df_import=pd.read_excel('C:\\Users\\NParker\\Documents\\SampleFiles\\SampleFile_13.xlsx')

#List to hold cleansed output
char_output=[]
#List to hold Agris Master and B2B data
other_output=[]
#Two dictionaries which will keep track of different lines' of business total counts and cleansed counts
cleansedCountDict={"cleansedCounter":0, "seed_cleansed":0, "feed_cleansed":0, "fert_micro_cleansed":0,"fert_bulk_cleansed":0, "chem_cleansed":0,"other_cleansed":0}
countDict={"counter":0, "seed_count":0,"feed_count":0,"fert_micro_count":0,"fert_bulk_count":0,"chem_count":0,"other_count":0}

#Looping through each uncleansed material and attempting to cleanse it
for index, row in df_import.iterrows():
    countDict["counter"]+=1
    legacy_num=str(row["AGRISItemID"])
    noun=str(row["ItemIDPart1"])
    #print(legacy_num)
    try:
        #Line of business 203 will be cleansed as a seed material
        if noun=='203':
            countDict["seed_count"]+=1
            char_output_1,other_output_1=format_seed(row, legacy_num)
            if not char_output_1[0]["Characteristic Description"].startswith("ERROR"):
                cleansedCountDict["cleansedCounter"]+=1
                cleansedCountDict["seed_cleansed"]+=1
                other_output+=other_output_1
            char_output+=char_output_1
            
        #Line of business 202 cleansed as fertilizer micro      
        elif noun=='202':
            countDict["fert_micro_count"]+=1
            sap_class="M_FERT_MICRO_DRY"
            if row["ProductType"]=='052':
                sap_class='M_FERT_MICRO_LIQ'
            char_output_1,other_output_1=format_Fert_Micro(row, legacy_num,sap_class)
            if not char_output_1[0]["Characteristic Description"].startswith("ERROR"):
                cleansedCountDict["cleansedCounter"]+=1
                cleansedCountDict["fert_micro_cleansed"]+=1
                other_output+=other_output_1
            char_output+=char_output_1
        #Line of business 200 cleansed as fertilizer bulk 
        elif noun=='200':
            countDict["fert_bulk_count"]+=1
            char_output_1,other_output_1=format_Fert_Bulk(row, legacy_num)
            if not char_output_1[0]["Characteristic Description"].startswith("ERROR"):
                cleansedCountDict["cleansedCounter"]+=1
                cleansedCountDict["fert_bulk_cleansed"]+=1
                other_output+=other_output_1
            char_output+=char_output_1
        #Line of business 201 cleansed as a chemical
        elif noun=='201':
            countDict["chem_count"]+=1
            char_output_1,other_output_1=format_chem(row, legacy_num)
            if not char_output_1[0]["Characteristic Description"].startswith("ERROR"):
                cleansedCountDict["cleansedCounter"]+=1
                cleansedCountDict["chem_cleansed"]+=1
                other_output+=other_output_1
            char_output+=char_output_1
        #Line of business 143 cleansed as feed
        elif noun=='143':
            countDict["feed_count"]+=1
            char_output_1,other_output_1=format_feed(row, legacy_num)
            if not char_output_1[0]["Characteristic Description"].startswith("ERROR"):
                cleansedCountDict["cleansedCounter"]+=1
                cleansedCountDict["feed_cleansed"]+=1
                other_output+=other_output_1
            char_output+=char_output_1
        #All other lines of business will be cleansed as other
        else:
            countDict["other_count"]+=1
            char_output_1,other_output_1=formatOther(row,legacy_num, row["ItemIDPart1"])
            if not char_output_1[0]["Characteristic Description"].startswith("ERROR"):
                cleansedCountDict["cleansedCounter"]+=1
                cleansedCountDict["other_cleansed"]+=1
                other_output+=other_output_1
            char_output+=char_output_1
                        
    except IndexError:
        char_output+= [{"Legacy Number":legacy_num,"Legacy Description":row["Name"], "Characteristic":row["Name"], "Characteristic Description":"ERROR:INDEX ERROR","Short Description (SAP)": "DOES NOT FOLLOW FORMAT", "Long Description (SAP)":"DOES NOT FOLLOW FORMAT", "PO Description (SAP)":"DOES NOT FOLLOW FORMAT","SAP Class":"NO_CLASS"}]
      
try:       
    x = datetime.datetime.now()
    dateString=str(x.year)+str(x.month)+str(x.day)+"-"+str(x.second)
    updateFileName="Profisee_Desc_OutPut_"+dateString
    charFileName="Master&B2B_Char-"+dateString
    pd.DataFrame.from_dict(char_output).to_excel(f"C:\\Users\\NParker\\Documents\\OutputFiles\\{updateFileName}.xlsx")
    #pd.DataFrame.from_dict(other_output).to_excel(f"C:\\Users\\NParker\\Documents\\OutputFilesChar\\{charFileName}.xlsx")
    print("My program took", int(time.time() - start_time), "seconds to run")
    print("Out of ",countDict["counter"]," entries ",cleansedCountDict["cleansedCounter"]," were fully cleansed ",int((cleansedCountDict["cleansedCounter"]/countDict["counter"])*100),"%",sep="")
    print("SEED: ",int(((cleansedCountDict["seed_cleansed"])/countDict["seed_count"])*100),"% cleansed (",cleansedCountDict["seed_cleansed"],"/",countDict["seed_count"],")",sep="")
    print("FEED: ",int(((cleansedCountDict["feed_cleansed"])/countDict["feed_count"])*100),"% cleansed (",cleansedCountDict["feed_cleansed"],"/",countDict["feed_count"],")",sep="")
    print("FERT BULK: ",int(((cleansedCountDict["fert_bulk_cleansed"])/countDict["fert_bulk_count"])*100),"% cleansed (",cleansedCountDict["fert_bulk_cleansed"],"/",countDict["fert_bulk_count"],")",sep="")
    print("FERT MICRO: ",int(((cleansedCountDict["fert_micro_cleansed"])/countDict["fert_micro_count"])*100),"% cleansed (",cleansedCountDict["fert_micro_cleansed"],"/",countDict["fert_micro_count"],")",sep="")
    print("CHEMICAL: ",int(((cleansedCountDict["chem_cleansed"])/countDict["chem_count"])*100),"% cleansed (",cleansedCountDict["chem_cleansed"],"/",countDict["chem_count"],")",sep="")
    #print(f"SHOP & MERCH: {int(((shop_merch_cleansed)/shop_merch_count)*100)}% cleansed ({shop_merch_cleansed}/{shop_merch_count})")
    print("Other: ",int(((cleansedCountDict["other_cleansed"])/countDict["other_count"])*100),"% cleansed (",cleansedCountDict["other_cleansed"],"/",countDict["other_count"],")",sep="")
except ZeroDivisionError:
    print("Complete cleansed summary NA")