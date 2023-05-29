#import library 
import pandas as pd
from flask import Flask,render_template
import time
start_time = time.time()
app=Flask(__name__)
data=pd.read_excel( r'Testcase/autoTest1.xlsx') # read file by pandas : data is Dataframe
data.dropna(inplace=True)          # remove  any rows in Dataframe contains NaN values
# rename colums in DataFrame to new short name
data.rename( columns={'PRESENT STATE':'PS' }, inplace=True )
data.rename( columns={'NEXT STATE':'NS0' }, inplace=True )
data.rename( columns={'Unnamed: 2':'NS1'}, inplace=True )
data.rename( columns={'OUTPUT':'O0' }, inplace=True )
data.rename( columns={'Unnamed: 4':'O1'}, inplace=True)
# PART 1: Divide Group by common output
# Create List contain lists of state having common output
def devideGroupByOutput():
    groupList=[]
    for i in range(1,len(data["PS"]) + 1):
        List=[]
        for j in range(1,len(data["PS"]) + 1):
            if data['O0'][i]==data['O0'][j] and data['O1'][i]== data['O1'][j]:
                List.append(data["PS"][j])
        groupList.append(List)
    return groupList
# Minimize GroupList include lists include 1 time
def minimizeGroupList(groupList):
    for list in groupList:
        while groupList.count(list) >1:
            groupList.remove(list)
#Part 2:
# create Dictionary of each state when X=0
# create Dictionary of each state when X=1 
def createDictNextState(dict_NS0,dict_NS1):
    for i in range(1,len(data["PS"]) + 1):
        name=data["PS"][i]
        valueNS0=[]
        valueNS1=[]
        for lst in groupList:
            if data["NS0"][i] in lst:
                valueNS0=lst
            if data["NS1"][i] in lst:
                valueNS1=lst
        dict_NS0[name]=valueNS0
        dict_NS1[name]=valueNS1
def checkListNoDifferent(lists):
    for i in lists:
        for j in lists:
            if i !=j :
                return False
    return True
#PART 3: Check Condition and divide new list in groupList
def findListAppearMinTime(lists):
    min= lists.count(lists[0])
    for i in lists:
        if lists.count(i) <= min:
            min=lists.count(i)
    return min
def findListDifferent(parentlist):
    if len(parentlist)== 1 or checkListNoDifferent(parentlist) == True:
        return None
    for lst in parentlist:
        if parentlist.count(lst) == 1:
            return lst
        elif parentlist.count(lst) == findListAppearMinTime(parentlist):
            return lst
    return None
def findStringDifferent(parentlist,dictNS,list):
    li_string=[]
    if findListDifferent(parentlist) is None:
        return None
    else:
        for i in list:
            if dictNS[i] is findListDifferent(parentlist):
                li_string.append(i)
    return li_string
def findListNextStateInGroup(lst,dict_NS):
        List_NS0=[]
        for i in lst:
            List_NS0.append(dict_NS[i])
        return List_NS0
def updateDictNextState():
    for i in range(1,len(data["PS"]) + 1):
        for lst in groupList:
            if data["NS0"][i] in lst:
                dict_NS0[data["PS"][i]]=lst
            if data["NS1"][i] in lst:
                dict_NS1[data["PS"][i]]=lst
def findListRest(lst,List):
    li=[]
    for i in List:
        if len(lst)==1:
            if i != lst[0]:
                li.append(i)
        elif i not in lst and List != None:
            li.append(i)
    return li
def divideGroupbyNextState():
    for lst in groupList:
        #check states in lst whether their nextStates are common
        stateDifferentInput0=findStringDifferent(findListNextStateInGroup(lst,dict_NS0),dict_NS0,lst) 
        stateDifferentInput1=findStringDifferent(findListNextStateInGroup(lst,dict_NS1),dict_NS1,lst)
        # if Diffrent, add new list in groupList
        if stateDifferentInput0 != None or stateDifferentInput1 !=None:
            if stateDifferentInput0 != None:
                lstRest= findListRest(stateDifferentInput0,lst)
                groupList.remove(lst)
                groupList.append(stateDifferentInput0)
                groupList.append(lstRest)
            elif stateDifferentInput1 != None:
                lstRest=findListRest(stateDifferentInput1,lst)
                groupList.remove(lst)
                groupList.append(stateDifferentInput1)
                groupList.append(lstRest)
    # Updated in Dict_NS0,DictNS_1 when checking of states
    updateDictNextState()
# Part 3: Loop and perform recursion in groupList to create entire equivalent list
def minimizeState():
    for lst in groupList:
        stateDifferentInput0=findStringDifferent(findListNextStateInGroup(lst,dict_NS0),dict_NS0,lst)
        stateDifferentInput1=findStringDifferent(findListNextStateInGroup(lst,dict_NS1),dict_NS1,lst)
        if stateDifferentInput0 != None or stateDifferentInput1 != None:
            divideGroupbyNextState()
            minimizeState()
            
# Part 4: Minimize list in groupList by get 1 value in list 
def createDataMinimize():
    dict={}
    li=[]
    # create List of Present State Minimize:
    li_PSMinimize=[]
    for lst in groupList:
        li.append(lst[0])
    for i in dict_NS0:
        for j in li:
            if i == j:
                li_PSMinimize.append(i)
    li_Output0=[]
    for state in li_PSMinimize:
        for i in range(1,len(data["PS"]) + 1):
             if data["PS"][i] == state:
                li_Output0.append(data["O0"][i])
    li_Output1=[]
    for state in li_PSMinimize:
        for i in range(1,len(data["PS"]) + 1):
             if data["PS"][i] == state:
                li_Output1.append(data["O1"][i])
    li_NextState0=[]
    for state in li_PSMinimize:
        li_NextState0.append(dict_NS0[state][0])
    li_NextState1=[]
    for state in li_PSMinimize:
        li_NextState1.append(dict_NS1[state][0])
    dict["PS"]=li_PSMinimize
    dict["NS0"]=li_NextState0
    dict["NS1"]=li_NextState1
    dict["O0"]=li_Output0
    dict["O1"]=li_Output1
    return dict
#MAIN
groupList=[]
# Step 1:
groupList = devideGroupByOutput()
minimizeGroupList(groupList)
#Step 2:
dict_NS0={}
dict_NS1={}
createDictNextState(dict_NS0,dict_NS1)
# step 3:
minimizeState()
minimizeGroupList(groupList)
#step 4:
dataAfter=createDataMinimize()
# Put data has been solved to display in Web browser by Flask
len_DataAfter=len(groupList)
len_Data=len(data)
li_LenMiniMize=[i for i in range(0,len(dataAfter["PS"]))]
li_LenData=[i for i in range(1,len(data["PS"]) + 1)]
# Using library "time" to caculate total_time 
end_time = time.time()
total_time = end_time - start_time
print("Thời gian chạy: ", total_time, " giây")
# Using Flask to return template to file index.html
@app.route('/')
def index():
    return render_template("index.html",dataAfter=dataAfter,len_DataAfter=len_DataAfter,data=data,len_Data=len_Data,li_LenMiniMize=li_LenMiniMize,li_LenData=li_LenData )
if __name__ == '__main__':
    app.run(debug=True)       

