#from types import NoneType
from tracemalloc import start
from adapters import BullHornAdapter
from adapters import CaptiveAdapter
from repository import EntitiesRepository
import os
import time
import json
import datetime

from datetime import datetime, timedelta
from datetime import timezone

bullhorn_client_id = os.environ.get('BULLHORN_CLIENT_ID')
bullhorn_client_secret = os.environ.get('BULLHORN_CLIENT_SECRET')


bullhorn_client_id = "f8a61111-51a6-42c4-8e1f-08dd9dc2f463"
bullhorn_client_secret ="aQqr6rXTo61QWARgNjOSZWts"

def transform_direct_hires(data):
    result = []
    employment_type = data['employmentType']
    placement = data['id']
    company_name = data['jobOrder']['clientCorporation']['name']
    title = data['jobOrder']['title']
    days_guaranteed = data['daysGuaranteed']
    start_date = data['dateBegin']
    start_date = start_date / 1000
    start_date = time.strftime('%Y-%m-%d', time.localtime(start_date))
    flat_fee = data['flatFee']
    if data['customText14'] == "":
        placement_type = "NULL"
    else:
        placement_type =data['customText14']

    candidate_name = data['candidate']['firstName'] + \
        ' ' + data['candidate']['lastName']

    if "Approved" == data['status']:
        status = True
    else:
        status = False

    for item in range(len(data['commissions']['data'])):
        split = data['commissions']['data'][item]['commissionPercentage']
        role = data['commissions']['data'][item]['role']
        if role == "":
            role = "Empty"
        recipient_name = data['commissions']['data'][item]['user']['firstName'] + \
            " " + \
            data['commissions']['data'][item]['user']['lastName']
        ID =recipient_name+str(placement)+ " " + role + str(days_guaranteed)
        

        payload_direc_hires = {
            "ID": ID,
            "Recipient Name": recipient_name,
            "Placement Type": placement_type,
            "Split": split,
            "Role": role,
            "Employment Type": employment_type,
            "Company Name": company_name,
            "Candidate Name": candidate_name,
            "Candidate Title": title,
            "Week End Apply Date": start_date,
            "Guarantee Period": days_guaranteed,
            "Placement Start Date": start_date,
            "Placement Completed": status,
            "Direct Hire Fee": flat_fee,
            "Placement Completed Date": start_date,
        }

        result.append(payload_direc_hires)

    return result


def transform_feed_contract(jsonContract_general_data, jsonContract_allEarnCodes, totalHours):
    result = []
    Candidate_ID = jsonContract_general_data['candidate']['id']
    Candidate_Name = jsonContract_general_data['candidate']['firstName'] + \
        " "+jsonContract_general_data['candidate']['lastName']
    if Candidate_ID == "":
        Candidate_ID = "Empty"
    Candidate_Title = jsonContract_general_data['jobOrder']['title']
    if Candidate_Title  == "":
        Candidate_Title = "Empty"
    Placement_ID = jsonContract_general_data['id']
    if Placement_ID == "":
        Placement_ID = "Empty"
    Company_ID = jsonContract_general_data['jobOrder']['clientCorporation']['id']
    if Company_ID == "":
        Company_ID = "Empty"
    Company_Name = jsonContract_general_data['jobOrder']['clientCorporation']['name']
    if Company_Name =="":
        Company_Name ="Empty"
    Employment_Type = jsonContract_general_data['employmentType']
    if Employment_Type =="":
        Employment_Type = "Empty"
    Burden_Rate = float(jsonContract_general_data['customText5'])/100
    if Burden_Rate =="":
        Burden_Rate = .999
    Period_End_Date = totalHours['periodEndDate']
    Placement_Start_Date = jsonContract_general_data['dateBegin']
    Placement_Start_Date = Placement_Start_Date / 1000
    Placement_Start_Date = time.strftime('%Y-%m-%d', time.localtime(Placement_Start_Date))
    date = Period_End_Date.translate({ord('-'): None})
    for commissionOwner in range(len(jsonContract_general_data['commissions']['data'])):
        Commission_Split_Pct = jsonContract_general_data[
            'commissions']['data'][commissionOwner]['commissionPercentage']
        if Commission_Split_Pct == "":
            Commission_Split_Pct = .999
        Role = jsonContract_general_data['commissions']['data'][commissionOwner]['role']
        if Role == "":
            Role = "Empty"
        Bullhorn_ID = jsonContract_general_data['commissions']['data'][commissionOwner]['user']['id']
        if Bullhorn_ID == "":
            Bullhorn_ID = "Empty"
        Recipient_Name = jsonContract_general_data['commissions']['data'][commissionOwner]['user']['firstName'] + \
            " " + \
            jsonContract_general_data['commissions']['data'][commissionOwner]['user']['lastName']
        if Recipient_Name =="":
            Recipient_Name = "Empty"
        for earnCodeCounter in range(len(jsonContract_allEarnCodes[0]['placementRateCardLineGroups']['data'])):
            for item in range(len(jsonContract_allEarnCodes[0]['placementRateCardLineGroups']['data'][earnCodeCounter]['placementRateCardLines']['data'])):
                Bill_Rate = jsonContract_allEarnCodes[0]['placementRateCardLineGroups'][
                    'data'][earnCodeCounter]['placementRateCardLines']['data'][item]['billRate']

                if Bill_Rate == " " or Bill_Rate is None or Bill_Rate == "None":
                    Burden_Rate = 0

                Pay_Rate = jsonContract_allEarnCodes[0]['placementRateCardLineGroups'][
                    'data'][earnCodeCounter]['placementRateCardLines']['data'][item]['payRate']
                if Pay_Rate == "":
                    Pay_Rate = 9999
                Earn_Code = jsonContract_allEarnCodes[0]['placementRateCardLineGroups'][
                    'data'][earnCodeCounter]['placementRateCardLines']['data'][item]['earnCode']['code']
                if Earn_Code =="":
                    Earn_Code = "Empty"
                Hours_Worked = 0
                for item in totalHours['data']:
                    earncode = item['earnCode']['code']
                    hour = item['quantity']
                    if hour is None:
                        hour=0
                    if(earncode == Earn_Code):
                            Hours_Worked = Hours_Worked + hour
                    ID = Recipient_Name + str(Candidate_ID)+str(Placement_ID) + str(Company_ID) + date+Earn_Code
                    if Hours_Worked > 0:
                        payloadContract = {
                            "ID": ID,
                            "Recipient Name": Recipient_Name,
                            "Bullhorn ID": Bullhorn_ID,
                            "Role": Role,
                            "Candidate ID": Candidate_ID,
                            "Candidate Name": Candidate_Name,
                            "Candidate Title": Candidate_Title,
                            "Placement ID": Placement_ID,
                            "Company ID": Company_ID,
                            "Company Name": Company_Name,
                            "Employment Type": Employment_Type,
                            "Period End Date": Period_End_Date,
                            "Earn Code": Earn_Code,
                            "Bill Rate": Bill_Rate,
                            "Pay Rate": Pay_Rate,
                            "Hours Worked": Hours_Worked, 
                            "Gross Margin": 99999,
                            "Commission Split Pct": Commission_Split_Pct,
                            "Spread Amount": 99999,
                            "Work Week Begin": Period_End_Date,
                            "Burden Rate": Burden_Rate,
                            "Placement Start Date": Placement_Start_Date 
                        }
                        result.append(payloadContract)
                
    
    
    
    return result


def handler(event, context):
    print("Starting")
    bullhorn_adapter = BullHornAdapter(
        bullhorn_client_id, bullhorn_client_secret)
    captivate_adapter = CaptiveAdapter("")
    code = bullhorn_adapter.get_code("")
    access_token = bullhorn_adapter.get_access_token(code)
    session_token = bullhorn_adapter.get_session_token(access_token)



    now = datetime.now() -timedelta(days=1)
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    timestamp = day_start.replace(tzinfo=timezone.utc).timestamp()
    timestamp = int(timestamp)*1000
    contracts = bullhorn_adapter.get_contracts(timestamp)
    contracts_mod =bullhorn_adapter.get_contracts_modified(timestamp)
    contracts = contracts_mod +contracts
    #print(contracts)
    for contract in contracts:
        placementID = contract['placement']['id']
        contractType = contract['placement']['employmentType']
        print("placementID",placementID)

    repository = EntitiesRepository()


if __name__ =="__main__":  
    e = datetime.now()
    print("Starting", e.strftime("%Y-%m-%d %H:%M:%S"))
    bullhorn_adapter = BullHornAdapter(
        bullhorn_client_id, bullhorn_client_secret)
    captivate_adapter = CaptiveAdapter("")
    code = bullhorn_adapter.get_code("")
    access_token = bullhorn_adapter.get_access_token(code)
    session_token = bullhorn_adapter.get_session_token(access_token)

    start_Period = datetime.now()- timedelta(13)
    for day in range(7):
        contract_counter=0
        period_Date= start_Period+ timedelta(days=day)
        period_Search = period_Date.strftime("%Y-%m-%d")
        print(period_Search)
        contracts_billable = bullhorn_adapter.get_contracts_billable(period_Search)
        #print(contracts_billable)
        contracts_payable = bullhorn_adapter.get_contracts_payable(period_Search)
        #print(contracts_payable)
        for contract in contracts_payable:
            if contract not in contracts_billable:
                contracts_billable.append(contract) 
               
        #9
        #10
        #11
        #12
        #13
        #14
        #15


        print(contracts_billable)
        print(len(contracts_billable))
        for contract in contracts_billable:
            contract_counter =contract_counter+1
            #print(contract_counter, contract['placement']['id'],contract['placement']['employmentType'])
            if contract_counter == 10:
                #print("se reinicia contador: ",contract_counter)
                code = bullhorn_adapter.get_code("")
                access_token = bullhorn_adapter.get_access_token(code)
                session_token = bullhorn_adapter.get_session_token(access_token)
                contract_counter=0

            placementID = contract['placement']['id']
            contractType = contract['placement']['employmentType']
            print(placementID)
            if contractType == "Contract" or contractType =="Right To Hire" or contractType == "Right-to-Hire":
                url = "https://api.captivateiq.com/ciq/v1/data-worksheets/dc66c975-cb71-482c-b533-fa6991c83a3d/records/"
                jsonContract_general_data = bullhorn_adapter.general_data(placementID)
                jsonContract_allEarnCodes = bullhorn_adapter.earn_codes(placementID)
                id_payable_list = bullhorn_adapter.id_payable_charge(placementID,period_Search)
                id_billable = bullhorn_adapter.id_billable_charge(placementID,period_Search)
                #print(id_payable_list)    

                if(len(id_payable_list)!=0):
                    for id_payable in id_payable_list:
                        #print(id_payable)
                        jsonContract_earnCodeHours = bullhorn_adapter.get_hours_data(id_payable)
                        #print("jsonContract_earnCodeHours",jsonContract_earnCodeHours)
                        jsonContract_exportedHours = bullhorn_adapter.get_exported_transactions(id_payable)
                        #print("jsonContract_exportedHours",jsonContract_exportedHours)
                        totalHours = dict(periodEndDate=jsonContract_exportedHours['periodEndDate'],data=jsonContract_earnCodeHours['payableTransactions']['data'] +jsonContract_exportedHours['exportedTransactions']['data'])
                        #print("totalHours",totalHours)
                        elements = transform_feed_contract(jsonContract_general_data, jsonContract_allEarnCodes, totalHours)
                        #cambiar identacion
                        for element_counter  in range(len(elements)):
                            next = element_counter  +1
                            try: 
                                if elements[element_counter]['Earn Code'] =="Car Rental Reimbursement" or \
                                    elements[element_counter]['Earn Code'] =="Lodging Reimbursement" or \
                                        elements[element_counter]['Earn Code'] =="Meals Reimbursement" or \
                                            elements[element_counter]['Earn Code'] =="On Call Bonus" or \
                                                elements[element_counter]['Earn Code'] =="Bonus" or \
                                                    elements[element_counter]['Earn Code'] =="Holiday Bonus" or \
                                                        elements[element_counter]['Earn Code'] =="Hotel/Flight Billable Ex" or \
                                                            elements[element_counter]['Earn Code'] =="Mileage Reimbursement" or \
                                                                elements[element_counter]['Earn Code'] =="Parking Reimbursement" or \
                                                                    elements[element_counter]['Earn Code'] =="Per Diem" or \
                                                                        elements[element_counter]['Earn Code'] =="Reimbursements":
                                    print("do not write in CaptivateIQ: ", elements[element_counter]['ID'])
                                else: 
                                    try: 
                                        if (elements[element_counter]['ID']!=elements[element_counter  +1]['ID']):
                                            captivate_adapter.createCIQ(url,elements[element_counter])
                                            #print("write in CaptivateIQ: ", elements[element_counter]['ID'],elements[element_counter]['Hours Worked'])
                                    except:     
                                        captivate_adapter.createCIQ(url,elements[element_counter])
                                        #print("first except write in CaptivateIQ: ", elements[element_counter]['ID'],elements[element_counter]['Hours Worked'])
                            except: 
                                if (elements[element_counter]['ID']!=elements[element_counter  +1]['ID']):
                                        print("write in CaptivateIQ in second except: ", elements[element_counter]['ID'],elements[element_counter]['Hours Worked'])
                                        captivate_adapter.createCIQ(url,elements[element_counter])
                elif(id_billable!=0):
                    jsonContract_earnCodeHours = bullhorn_adapter.get_hours_data_billable(id_payable)
                    jsonContract_exportedHours = bullhorn_adapter.get_exported_transactions_billable(id_payable)
                    totalHours = dict(periodEndDate=jsonContract_exportedHours['periodEndDate'],data=jsonContract_earnCodeHours['payableTransactions']['data'] +jsonContract_exportedHours['exportedTransactions']['data'])
                    elements = transform_feed_contract(jsonContract_general_data, jsonContract_allEarnCodes, totalHours)
                    
                    for element_counter  in range(len(elements)):
                        next = element_counter  +1
                        try:
                            if(elements[element_counter]['ID']!=elements[next]['ID']):
                                captivate_adapter.createCIQ(url, elements[element_counter])
                        except:
                            captivate_adapter.createCIQ(url, elements[element_counter])
            
            elif(contractType=="Direct Hire"):
                url = "https://api.captivateiq.com/ciq/v1/data-worksheets/9f2695ab-81a3-4fc1-9a97-a4e75d1e6b1f/records/"
                jsonDirectHire = bullhorn_adapter.search_direct_hires(placementID)
                elements = transform_direct_hires(jsonDirectHire)
                for element_counter  in range(len(elements)):
                    #line = elements[element_counter]['ID']+", "+elements[element_counter]['Recipient Name']+", "+elements[element_counter]['Placement Type']+", "+str(elements[element_counter]['Split'])+", "+elements[element_counter]['Role']+", "+elements[element_counter]['Employment Type']+", "+elements[element_counter]['Company Name']+", "+elements[element_counter]['Candidate Name']+", "+elements[element_counter]['Candidate Title']+", "+str(elements[element_counter]['Week End Apply Date'])+", "+str(elements[element_counter]['Guarantee Period'])+", "+str(elements[element_counter]['Placement Start Date'])+", "+str(elements[element_counter]['Placement Completed'])+", "+str(elements[element_counter]['Direct Hire Fee'])+", "+elements[element_counter]['Placement Completed Date']
                    #print(line)
                    captivate_adapter.createCIQ(url, elements[element_counter])
        repository = EntitiesRepository()
    e = datetime.now()
    print("END", e.strftime("%Y-%m-%d %H:%M:%S"))
    