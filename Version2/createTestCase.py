import xlsxwriter,random

workbook = xlsxwriter.Workbook("F:/Python/Project/Tuan_code/autoTestCase/autoTest25.xlsx")
#workbook = xlsxwriter.Workbook("F:/Python/TestCase/Testcase_13.xlsx")
worksheet = workbook._add_sheet("Sheet1")

worksheet.write("A1","PRESENT STATE")
worksheet.write("B1","NEXT STATE")
worksheet.write("D1","OUTPUT")
worksheet.write("B2","X=0")
worksheet.write("C2","X=1")
worksheet.write("D2","X=0")
worksheet.write("E2","X=1")


#stateNum = random.randint(300,500)
stateNum = 10000
form = "S{}"

#Write present state
for i in range(0,stateNum):
    state = form.format(i)
    worksheet.write(i+2,0,state)

    # temp1 = random.randint(0,stateNum-1)
    # temp2 = random.randint(0,stateNum-1)

    # Random trạng thái kế tiếp
    temp1 = random.randint(0,stateNum/100)
    temp2 = random.randint(0,stateNum/100)

    nextState0 = form.format(temp1) 
    nextState1 = form.format(temp2) 

    worksheet.write(i+2,1,nextState0)
    worksheet.write(i+2,2,nextState1)

    output0 = random.randint(0,1)
    output1 = random.randint(0,1)
    #output0 = 1
    #output1 = 0

    worksheet.write(i+2,3,output0)
    worksheet.write(i+2,4,output1)

workbook.close()
























