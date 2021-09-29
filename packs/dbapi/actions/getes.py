import sys
import requests                                                             
                                                                       
from st2common.runners.base_action import Action                       
                                                                       
class Dbgetes(Action):                                                
    def run(self):
        url = "http://dummy.restapiexample.com/api/v1/employees"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)                                         
        if response.status_code == 200:
            print(response.json())
            return(True, 200)
        return(False, "Failed!")