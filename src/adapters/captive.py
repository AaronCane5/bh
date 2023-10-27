from datetime import timedelta
import string
import requests
import time

class CaptiveAdapter:
    def __init__(self, token: string) -> None:
        self.token = token
        super().__init__()

    def edit_ciq(self, payload):
        url = "https://api.captivateiq.com/ciq/v1/data-worksheets/9f2695ab-81a3-4fc1-9a97-a4e75d1e6b1f/records/"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Token ".format(self.token)
        }
        response = requests.post(url, headers=headers, json=payload)
        print(response.text)

    def create_ciq(self, payload):
        url = "https://api.captivateiq.com/ciq/v1/data-worksheets/9f2695ab-81a3-4fc1-9a97-a4e75d1e6b1f/records/"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Token ".format(self.token)
        }
        response = requests.post(url, headers=headers, json=payload)
        print(response.text)

    

    def createCIQ(self, url, element):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Token ".format(self.token),
            "Authorization": "Token a38b58a6659006a0d66f52ef144b9b9139b299a9491d6d7f41"
        }
        response = requests.post(url, headers=headers, json=element)
        #print("createCIQ",response.text)
        print(element)
        
        print("response line 43 ", response)
        responseDict = response.json() 
        #print(response.status_code,response.text) 
        if response.status_code == 201:
            line = responseDict['id'] + " " + responseDict['data']['ID']
            print("Create: id", line)
        elif response.status_code == 400:
            id = element['ID']
            url = "{}{}/".format(url,id)
            response = requests.request("PUT", url, json=element, headers=headers)
            #print("response.status_code == 400:",response.text)
            responseDict = response.json()
            line = responseDict['id'] + " " + responseDict['data']['ID']
            print("Update: id", line)
        elif response.status_code ==529:
            timeDetails = timeDetails.upper() 
            characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ  , . "
            for x in range(len(characters)):
                timeDetails = timeDetails.replace(characters[x],"")
            timeDetails = int(timeDetails)
            print("PAUSE FOR:",timeDetails )
            time.sleep(timeDetails)
        else:
            print(response.status_code, response.text)
        """
        if response.status_code == 201:
            print("Create: id", responseDict['id'], responseDict['data']['ID'])
        elif responseDict['errors']:
            try:
                id = element['ID']
                url = "{}{}/".format(url,
                                 id)
                response = requests.request(
                "PUT", url, json=element, headers=headers)
                responseDict = response.json()
                print("Update: id", responseDict['id'], responseDict['data']['ID'])
            except:
                print(responseDict)
        """
        
        return
