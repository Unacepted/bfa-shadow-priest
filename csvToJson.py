import csv
import json
import re
import time
import os

starttime = time.time()

#Define all file paths
#Trinkets
trinketsDA = os.path.os.path.abspath(os.path.join(os.getcwd(), 'trinkets/Results_DA.csv'))
trinketsLotV = os.path.os.path.abspath(os.path.join(os.getcwd(), 'trinkets/Results_LotV.csv'))
trinketsDAD = os.path.os.path.abspath(os.path.join(os.getcwd(), 'trinkets/Results_Dungeons_DA.csv'))
trinketsLotVD = os.path.os.path.abspath(os.path.join(os.getcwd(), 'trinkets/Results_Dungeons_LotV.csv'))

#Triats
traitsDA = os.path.os.path.abspath(os.path.join(os.getcwd(), 'azerite-traits/Results_DA.csv'))
traitsLotV = os.path.os.path.abspath(os.path.join(os.getcwd(), 'azerite-traits/Results_LotV.csv'))
traitsDAD = os.path.os.path.abspath(os.path.join(os.getcwd(), 'azerite-traits/Results_Dungeons_DA.csv'))
traitsLotVD = os.path.os.path.abspath(os.path.join(os.getcwd(), 'azerite-traits/Results_Dungeons_LotV.csv'))


#JSON Files
#Trinkets
trinketsDAJson = os.path.os.path.abspath(os.path.join(os.getcwd(), 'trinkets/Results_DA.json'))
trinketsLotVJson = os.path.os.path.abspath(os.path.join(os.getcwd(), 'trinkets/Results_LotV.json'))
trinketsDAJsonD = os.path.os.path.abspath(os.path.join(os.getcwd(), 'trinkets/Results_DA_D.json'))
trinketsLotVJsonD = os.path.os.path.abspath(os.path.join(os.getcwd(), 'trinkets/Results_LotV_D.json'))
#Traits
traitsDAJson = os.path.os.path.abspath(os.path.join(os.getcwd(), 'azerite-traits/Results_DA.json'))
traitsLotVJson = os.path.os.path.abspath(os.path.join(os.getcwd(), 'azerite-traits/Results_LotV.json'))
traitsDAJsonD = os.path.os.path.abspath(os.path.join(os.getcwd(), 'azerite-traits/Results_DA_D.json'))
traitsLotVJsonD = os.path.os.path.abspath(os.path.join(os.getcwd(), 'azerite-traits/Results_LotV_D.json'))

# SimC files
trinketsDungeonsDA = os.path.os.path.abspath(os.path.join(os.getcwd(), 'trinkets/trinkets_dungeons_DA.simc'))
trinketsOtherDA = os.path.os.path.abspath(os.path.join(os.getcwd(), 'trinkets/trinkets_other_DA.simc'))
trinketsRaidDA = os.path.os.path.abspath(os.path.join(os.getcwd(), 'trinkets/trinkets_raid_DA.simc'))

#CSV Field names
fieldnames = ('profile', 'actor', 'DPS', 'increase')

# Trait List (hack fix for the moment)
traitList = ['Apothecarys_Concoctions_',
'Archive_of_the_Titans_',
'Barrage_Of_Many_Bombs_',
'Battlefield_Focus_',
'Blightborne_Infusion_',
'Blood_Rite_',
'Bonded_Souls_',
'Champion_of_Azeroth_',
'Chorus_of_Insanity_',
'Collective_Will_',
'Combined_Might_',
'Dagger_in_the_Back_Behind_',
'Dagger_in_the_Back_Front_',
'Death_Throes_',
'Fight_or_Flight_',
'Filthy_Transfusion_',
'Glory_in_Battle_',
'Incite_the_Pack_',
'Laser_Matrix_',
'Meticulous_Scheming_',
'Relational_Normalization_Gizmo_',
'Retaliatory_Fury_',
'Rezans_Fury_',
'Ricocheting_Inflatable_Pyrosaw_',
'Ruinous_Bolt_',
'Searing_Dialogue_',
'Secrets_of_the_Deep_',
'Seductive_Power_',
'Shadow_of_Elune_',
'Spiteful_Apparitions_',
'Swirling_Sands_',
'Sylvanas_Resolve_',
'Synaptic_Spark_Capacitor_',
'Thought_Harvester_',
'Thunderous_Blast_',
'Tidal_Surge_',
'Tradewinds_',
'Treacherous_Covenant_',
'Unstable_Catalyst_',
'Whispers_of_the_Damned_',

#Secondary Traits
'Azerite_Globules_',
'Blood_Siphon_',
'Earthlink_',
'Elemental_Whirl_',
'Gutripper_',
'Heed_My_Call_',
'On_My_Way_',
'Overwhelming_Power_',
'Unstable_Flames_']



def parseCSV(file, json_file):
    csv_rows = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        field = reader.fieldnames
        for row in reader:
            csv_rows.extend([{field[i]:row[field[i]] for i in range(len(field))}])
        csvToJson(csv_rows, json_file)

def csvToJson(data, json_file):
    with open(json_file, "w") as f:
        f.write(json.dumps(data, sort_keys=False, indent=2, separators=(',', ': ')))


parseCSV(trinketsDA,trinketsDAJson)
parseCSV(trinketsLotV,trinketsLotVJson)
parseCSV(trinketsDAD,trinketsDAJsonD)
parseCSV(trinketsLotVD,trinketsLotVJsonD)
parseCSV(traitsDA,traitsDAJson)
parseCSV(traitsLotV,traitsLotVJson)
parseCSV(traitsDAD,traitsDAJsonD)
parseCSV(traitsLotVD,traitsLotVJsonD)


def getItemId(itemname):
    itemname = itemname.lower().rstrip()
    with open(trinketsDungeonsDA, 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                if re.search(r'(trinket1=)\D*',line).group(0).replace('trinket1=','').replace(',id=','').lower() == itemname:
                    itemID = re.search(r'(id=)\d*',line.strip('\n')).group(0).strip('id=')
                    return itemID
            except:
                continue
    with open(trinketsOtherDA, 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                if re.search(r'(trinket1=)\D*',line).group(0).replace('trinket1=','').replace(',id=','').lower() == itemname:
                    itemID = re.search(r'(id=)\d*',line).group(0).strip('id=')
                    return itemID
            except:
                continue
    with open(trinketsRaidDA, 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                if re.search(r'(trinket1=)\D*',line).group(0).replace('trinket1=','').replace(',id=','').lower() == itemname:
                    itemID = re.search(r'(id=)\d*',line).group(0).strip('id=')
                    return itemID
            except:
                continue


def make_unique(original_list):
    unique_list = []
    [unique_list.append(obj) for obj in original_list if obj not in unique_list]
    return unique_list

def getNames(jsonFile):
	with open(jsonFile,'r') as f:
		nameList = list()
		data = json.load(f)
		for x in data:
			m = re.search(r"\D*",x['actor']).group(0).replace('_',' ').rstrip()
			nameList.append(m)
		uniqueList = make_unique(nameList)
	return uniqueList

def getIlvl(jsonFile):
    with open(jsonFile,'r') as f:
        nameList = list()
        data = json.load(f)
        for x in data:
            m = re.search(r"\d*",x['actor'].lstrip().split('_')[-1]).group(0)
            nameList.append(m)
        uniqueList = make_unique(nameList)
    return uniqueList

def addNamesToJson(jsonFile):
	names = getNames(jsonFile)
	with open(jsonFile, 'r+') as f:
		data = json.load(f)
		data.append(names)
		f.write(json.dumps(names, sort_keys=False, indent =2))

def ilvlPerItem(itemName):
    with open(trinketsDAJson) as f:
        ilvlList = list()
        data = json.load(f)
        for x in data:
            itemName = itemName.replace('_',' ').rstrip()
            n = re.search(r"\D*",x['actor']).group(0).replace('_',' ').rstrip()
            m = re.search(r'\d*',x['actor'].lstrip().split('_')[-1]).group(0)
            if itemName == n:
                ilvlList.append(m)
        uniqueList = make_unique(ilvlList)
    return uniqueList


trinketnames = getNames(trinketsDAJson)
trinketilvl = getIlvl(trinketsDAJson)

def buildTrinketJsonChart(injsonFile, outjsonFile, simType):
    '''
    injsonFile - The original CSV data converted to a raw unformatted JSON
    outjsonFile - The newly formatted JSON
    simType - Composite, Single Target, Dungeons
    '''
    #trinketnames = getNames(injsonFile) #Get all the trinket names from the inputted JSON file
    namelist = list()
    j = open(outjsonFile,'w') #Start writing our JSON file
    j.write('{\n') #JSON formatting
    with open(injsonFile,'r') as f: #Start reading the inputted JSON file.
        data = json.load(f)
        for x in data: #Easier to parse the originally converted JSON to organize the data
            m = re.search(r"\D*",x['actor'].rstrip()).group(0)
            namelist.append(m)
        uniqueList = make_unique(namelist)
        j.write('\t"data": {\n')
        ucntMax = len(uniqueList)
        ucnt = 0
        for u in uniqueList:
            ucnt+=1
            trinketilvl = ilvlPerItem(u)
            j.write('\t\t"' + u.replace('_',' ').rstrip() +'": {\n')
            maxCnt = len(trinketilvl)
            cnt = 0
            for y in trinketilvl:
                cnt+=1
                for x in data:
                    if x['profile'] == simType and x['actor'] == str(u+y):
                        if x['actor'] == 'Base':
                            j.write('\t\t\t"300": '+x['DPS']+'\n')
                        else:
                            if cnt < maxCnt:
                                j.write('\t\t\t"'+y+'": '+x['DPS']+',\n')
                            else:
                                j.write('\t\t\t"'+y+'": '+x['DPS']+'\n')
            if ucnt < ucntMax:
                j.write('\t\t},\n')
            else:
                j.write('\t\t}\n')
        j.write('\t},\n')
        j.write('\t"Data_type": "trinkets",\n\t"item_ids" : {\n')
        maxCnt = len(uniqueList)
        cnt = 0
        for u in uniqueList:
            cnt+=1
            u = u.replace(' ','_')
            if not u == 'Base':
                u = u[:-1]
            itemID = getItemId(u)
            if not str(itemID) == 'None':
                if cnt < maxCnt-1:
                    j.write('\t\t"'+u+'": '+str(itemID)+',\n')
                else:
                    j.write('\t\t"'+u+'": '+str(itemID)+'\n')
            else:
                if not u == 'Base':
                    print('Error: ' + u + ' Trinket was not included in the item ID list.')

        j.write('\t},\n')
        j.write('\t"simulated_steps": [\n')
        ilvls = getIlvl(injsonFile)
        ilvls = ilvls[:-1]
        cnt = 0
        maxCnt = len(ilvls)
        for i in ilvls:
            cnt+=1
            if cnt < maxCnt:
                j.write('\t\t'+str(i)+',\n')
            else:
                j.write('\t\t'+str(i)+'\n')
        j.write('\t],\n')
        DPSSort = list()
        for u in uniqueList:
            maxIlvl = ilvlPerItem(u)[0]
            for x in data:
                if x['profile'] == simType and x['actor'] == str(u+maxIlvl):
                    DPSSort.append(x['DPS'])
        sortedTrinkets = [x for _,x in sorted(zip(DPSSort, uniqueList),reverse=True)]
        sortedTrinkets = sortedTrinkets[:-1] #Remove Base since it will always be the last option.
        ucnt = 0
        ucntMax = len(sortedTrinkets)
        j.write('\t"sorted_data_keys": [\n')
        for s in sortedTrinkets:
            ucnt+=1
            if not s == 'Base':
                if ucnt < ucntMax:
                    j.write('\t\t"'+s.replace('_',' ').strip()+'",\n')
                else:
                    j.write('\t\t"'+s.replace('_',' ').strip()+'"\n')
        j.write('\t]')
        #j.write('\n\t},')
        j.write('\n}')
    j.close()

def buildTraitJsonChart(injsonFile, outjsonFile, simType):
    '''
    injsonFile - The original CSV data converted to a raw unformatted JSON
    outjsonFile - The newly formatted JSON
    simType - Composite, Single Target, Dungeons
    '''

    namelist = list()
    j = open(outjsonFile,'w') #Start writing our JSON file
    j.write('{\n') #JSON formatting
    with open(injsonFile,'r') as f: #Start reading the inputted JSON file.
        data = json.load(f)
        for x in data: #Easier to parse the originally converted JSON to organize the data
            m = re.search(r"\D*",x['actor'].rstrip()).group(0)
            namelist.append(m)
        uniqueList = make_unique(namelist)
        if "Base" in uniqueList: uniqueList.remove("Base")
        j.write('\t"data": {\n')
        ucntMax = len(uniqueList)
        #print(ucntMax)
        ucnt = 0
        for u in uniqueList:
            ucnt+=1
            traitSteps = ['1','2','3'] #Should always be 1-3 unless they add some random 4th azerite gear slot
            if not u.replace('_',' ').rstrip() == 'Int' or u == 'Base': #Pull the int sims out
                j.write('\t\t"' + u.replace('_',' ').rstrip() +'": {\n')
            maxCnt = 3
            cnt = 0
            for y in traitSteps:
                cnt+=1
                for x in data:
                    if x['profile'] == simType:
                        if x['actor'] == str(u+y):
                            if x['actor']== ("Champion_of_Azeroth_" + y):
                                j.write('\t\t\t"1_stack": '+x['DPS']+',\n')
                                j.write('\t\t\t"2_stack": 0,\n')
                                j.write('\t\t\t"3_stack": 0\n') #Have to add empty stacks here because highcharts is dumb.
                            elif 'combo' in x['actor']:
                                j.write('\t\t\t"1_stack": 0,\n')
                                j.write('\t\t\t"2_stack": ' + x['DPS']+',\n')
                                j.write('\t\t\t"3_stack": 0' + '\n')
                            else:
                                if cnt < maxCnt:
                                    j.write('\t\t\t"'+y+'_stack": '+x['DPS']+',\n')
                                else:
                                    j.write('\t\t\t"'+y+'_stack": '+x['DPS']+'\n')
            if ucnt < ucntMax:
                if not u.replace('_',' ').rstrip() == 'Int': #Have to check for int sims again
                    j.write('\t\t},\n')
            else:
                j.write('\t\t},')
                for x in data:
                    if x['profile'] == simType and x['actor'] == 'Base':
                        j.write('\n\t\t"Base": {\n')
                        j.write('\t\t\t"1_stack": '+x['DPS']+',\n')
                        j.write('\t\t\t"2_stack": 0,\n')
                        j.write('\t\t\t"3_stack": 0\n') #Have to add empty stacks here because highcharts is dumb.
                j.write('\t\t}\n')
        j.write('\t},\n')
        j.write('\t"Data_type": "traits",\n\t"spell_ids" : {\n')
        #Manually write in spell id's for traits
        j.write('\t\t"Ancients Bulwark ":'+'"287631"'+',\n')
        j.write('\t\t"Apothecarys Concoctions ":'+'"287604"'+',\n')
        j.write('\t\t"Archive of the Titans ":'+'"280708"'+',\n')
        j.write('\t\t"Azerite Empowered ":'+'"263978"'+',\n')
        j.write('\t\t"Azerite Globules ":'+'"279955"'+',\n')
        j.write('\t\t"Barrage Of Many Bombs ":'+'"280163"'+',\n')
        j.write('\t\t"Battlefield Focus ":'+'"280582"'+',\n')
        j.write('\t\t"Blightborne Infusion ":'+'"273823"'+',\n')
        j.write('\t\t"Blood Rite ":'+'"280409"'+',\n')
        j.write('\t\t"Blood Siphon ":'+'"264108"'+',\n')
        j.write('\t\t"Bonded Souls ":'+'"288841"'+',\n')   
        j.write('\t\t"Champion of Azeroth ":'+'"270583"'+',\n')
        j.write('\t\t"Chorus of Insanity ":'+'"278661"'+',\n')
        j.write('\t\t"Collective Will ":'+'"280837"'+',\n')
        j.write('\t\t"Combined Might ":'+'"280848"'+',\n')
        j.write('\t\t"Dagger in the Back Behind ":'+'"280285"'+',\n')
        j.write('\t\t"Dagger in the Back Front ":'+'"280285"'+',\n')
        j.write('\t\t"Death Throes ":'+'"278659"'+',\n')
        j.write('\t\t"Earthlink ":'+'"279927"'+',\n')
        j.write('\t\t"Elemental Whirl ":'+'"270667"'+',\n')
        j.write('\t\t"Endless Hunger ":'+'"287662"'+',\n')
        j.write('\t\t"Fight or Flight ":'+'"287818"'+',\n')
        j.write('\t\t"Filthy Transfusion ":'+'"273836"'+',\n')
        j.write('\t\t"Glory in Battle ":'+'"280852"'+',\n')
        j.write('\t\t"Gutripper ":'+'"266937"'+',\n')
        j.write('\t\t"Heed My Call ":'+'"271681"'+',\n')
        j.write('\t\t"Incite the Pack ":'+'"280410"'+',\n')
        j.write('\t\t"Laser Matrix ":'+'"280702"'+',\n')
        j.write('\t\t"Lifespeed":'+'"267665"'+',\n')
        j.write('\t\t"Meticulous Scheming ":'+'"273684"'+',\n')
        j.write('\t\t"On My Way ":'+'"267879"'+',\n')
        j.write('\t\t"Overwhelming Power ":'+'"266180"'+',\n')
        j.write('\t\t"Relational Normalization Gizmo ":'+'"280178"'+',\n')
        j.write('\t\t"Retaliatory Fury ":'+'"280785"'+',\n')
        j.write('\t\t"Rezans Fury ":'+'"281834"'+',\n')
        j.write('\t\t"Ricocheting Inflatable Pyrosaw ":'+'"280168"'+',\n')
        j.write('\t\t"Ruinous Bolt ":'+'"280206"'+',\n')
        j.write('\t\t"Searing Dialogue ":'+'"272788"'+',\n')
        j.write('\t\t"Secrets of the Deep ":'+'"273829"'+',\n')
        j.write('\t\t"Shadow of Elune ": ' + '"287471" ' + ',\n')
        j.write('\t\t"Spiteful Apparitions ":'+'"277682"'+',\n')
        j.write('\t\t"Swirling Sands ":'+'"280433"'+',\n')
        j.write('\t\t"Sylvanas Resolve ":'+'"280810"'+',\n')
        j.write('\t\t"Synaptic Spark Capacitor ":'+'"280174"'+',\n')
        j.write('\t\t"Thought Harvester ":'+'"273320"'+',\n')
        j.write('\t\t"Thunderous Blast ":'+'"280384"'+',\n')
        j.write('\t\t"Tidal Surge ":'+'"280404"'+',\n')
        j.write('\t\t"Tradewinds ":'+'"281843"'+',\n')
        j.write('\t\t"Treacherous Covenant ":'+'"288989"'+',\n')
        j.write('\t\t"Unstable Catalyst ":'+'"281516"'+',\n')
        j.write('\t\t"Unstable Flames ":'+'"279902"'+',\n')
        j.write('\t\t"Whispers of the Damned ":'+'"275726"'+'\n')
        j.write('\t},\n')
        #end manual
        j.write('\t"simulated_steps": [\n')
        #write the 3 levels of traits
        j.write('\t\t"1_stack",\n')
        j.write('\t\t"2_stack",\n')
        j.write('\t\t"3_stack"\n')
        j.write('\t],\n')
        DPSSort = list()
        for u in traitList:
            for x in data:
                if x['profile'] == simType and x['actor'] == str(u+'1'):
                    DPSSort.append(x['DPS'])
        #if "Int_" in uniqueList: uniqueList.remove("Int_")
        sortedTraits = [x for _,x in sorted(zip(DPSSort, traitList),reverse=True)]
        ucnt = 0
        j.write('\t"sorted_data_keys": [\n')
        if "Int_" in sortedTraits: sortedTraits.remove("Int_")
        ucntMax = len(sortedTraits)
        for s in sortedTraits:
            ucnt+=1
            if not s == 'Base':
                if ucnt < ucntMax:
                    j.write('\t\t"'+s.replace('_',' ')+'",\n')
                else:
                    j.write('\t\t"'+s.replace('_',' ')+'"\n')
        j.write('\t]')
        #j.write('\n\t},')
        j.write('\n}')
    j.close()


def buildTraitJsonComboChart(injsonFile, outjsonFile, simType):
    namelist = list()
    j = open(outjsonFile,'w') #Start writing our JSON file
    j.write('{\n') #JSON formatting
    with open(injsonFile,'r') as f: #Start reading the inputted JSON file.
        data = json.load(f)
        for x in data: #Easier to parse the originally converted JSON to organize the data
            m = re.search(r"\D*",x['actor'].rstrip()).group(0)
            if "combo" in m:
                namelist.append(m)
        uniqueList = make_unique(namelist)
        if "Base" in uniqueList: uniqueList.remove("Base")
        j.write('\t"data": {\n')
        ucntMax = len(uniqueList)
        #print(ucntMax)
        ucnt = 0
        for u in uniqueList:
            ucnt+=1
            traitSteps = ['2']
            if not u.replace('_',' ').rstrip() == 'Int' or u == 'Base': #Pull the int sims out
                j.write('\t\t"' + u.replace('_',' ').rstrip() +'": {\n')
            maxCnt = 3
            cnt = 0
            for y in traitSteps:
                cnt+=1
                for x in data:
                    if x['profile'] == simType:
                        if x['actor'] == str(u+y):
                            if cnt < maxCnt:
                                j.write('\t\t\t"'+'1_stack": '+x['DPS']+',\n')
                            else:
                                j.write('\t\t\t"'+'1_stack": '+x['DPS']+'\n')
            if ucnt < ucntMax:
                if not u.replace('_',' ').rstrip() == 'Int': #Have to check for int sims again
                    j.write('\t\t},\n')
            else:
                j.write('\t\t},')
                for x in data:
                    if x['profile'] == simType and x['actor'] == 'Base':
                        j.write('\n\t\t"Base": {\n')
                        j.write('\t\t\t"1_stack": '+x['DPS']+',\n')
                j.write('\t\t}\n')
        j.write('\t},\n')
        DPSSort = list()
        for u in uniqueList:
            for x in data:
                if x['profile'] == simType and x['actor'] == str(u+'2'):
                    DPSSort.append(x['DPS'])
        #if "Int_" in uniqueList: uniqueList.remove("Int_")
        sortedTraits = [x for _,x in sorted(zip(DPSSort, uniqueList),reverse=True)]   
        j.write('\t"sorted_data_keys": [\n')
        ucntMax = len(sortedTraits)
        ucnt = 0
        for s in sortedTraits:
            ucnt+=1
            if not s == 'Base':
                s = s.replace('_',' ')
                s = s.replace(" combo", ' ')
                s = s.rstrip()
                if ucnt < ucntMax:
                    j.write('\t\t"'+s+'",\n')
                else:
                    j.write('\t\t"'+s+'"\n')
        j.write('\t]')
        #j.write('\n\t},')
        j.write('\n}')
    j.close()

os.chdir("json_Charts/")




buildTrinketJsonChart(trinketsDAJson, "trinkets_DA_C.json", 'composite')
buildTrinketJsonChart(trinketsDAJson, "trinkets_DA_ST.json", 'single_target')
buildTrinketJsonChart(trinketsDAJsonD, "trinkets_DA_D.json", 'dungeons')
buildTrinketJsonChart(trinketsLotVJson, "trinkets_LotV_C.json", 'composite')
buildTrinketJsonChart(trinketsLotVJson, "trinkets_LotV_ST.json", 'single_target')
buildTrinketJsonChart(trinketsLotVJsonD, "trinkets_LotV_D.json", 'dungeons')
buildTraitJsonChart(traitsDAJson, "traits_DA_C.json", 'composite')
buildTraitJsonChart(traitsDAJson, "traits_DA_ST.json", 'single_target')
buildTraitJsonChart(traitsDAJsonD, "traits_DA_D.json", 'dungeons')
buildTraitJsonChart(traitsLotVJson, "traits_LotV_C.json", 'composite')
buildTraitJsonChart(traitsLotVJson, "traits_LotV_ST.json", 'single_target')
buildTraitJsonChart(traitsLotVJsonD, "traits_LotV_D.json", 'dungeons')

buildTraitJsonComboChart(traitsDAJson, "traits_DA_C_Combo.json", 'composite')
buildTraitJsonComboChart(traitsDAJson, "traits_DA_ST_Combo.json", 'single_target')
buildTraitJsonComboChart(traitsDAJsonD, "traits_DA_D_Combo.json", 'dungeons')
buildTraitJsonComboChart(traitsLotVJson, "traits_LotV_C_Combo.json", 'composite')
buildTraitJsonComboChart(traitsLotVJson, "traits_LotV_ST_Combo.json", 'single_target')
buildTraitJsonComboChart(traitsLotVJsonD, "traits_LotV_D_Combo.json", 'dungeons')

#exit()

os.remove(trinketsDAJson)
os.remove(trinketsLotVJson)
os.remove(traitsDAJson)
os.remove(traitsLotVJson)
os.remove(trinketsDAJsonD)
os.remove(trinketsLotVJsonD)
os.remove(traitsDAJsonD)
os.remove(traitsLotVJsonD)



endtime = time.time()
totaltime = endtime-starttime
print("Sucessfully converted charts to JSON format in %d seconds" % (totaltime))
