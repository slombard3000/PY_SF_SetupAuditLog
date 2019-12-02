import simplejson as json
import csv
import time
import datetime
import requests
from defFile import ConfigSectionMap
#read config


params = {
    "grant_type": ConfigSectionMap("auth")['grant_type'],#grant type
    "client_id": ConfigSectionMap("auth")['client_id'], # Consumer Key
    "client_secret":  ConfigSectionMap("auth")['client_secret'], # Consumer Secret
    "username":  ConfigSectionMap("auth")['username'], # The email you use to login
    "password":  ConfigSectionMap("auth")['password'] # Concat your password and your security token
}

SF_url=ConfigSectionMap("auth")['server_url']
r = requests.post(SF_url+"/services/oauth2/token", params)
access_token = r.json().get("access_token")
instance_url = r.json().get("instance_url")

lastRunDate=''
#get last run date from file
try:
    file_lstRun = open("lastRunDate","r") 
    lastRunDate=file_lstRun.read(); 
    if lastRunDate=='':
        file_lstRun.write(time.strftime("%Y-%m-%dT%H:%M:%S")+'-06:00'+'\n')

except IOError:
    file_lstRun = open("lastRunDate","w")
    file_lstRun.write(time.strftime("%Y-%m-%dT%H:%M:%S")+'-06:00'+'\n')
    lastRunDate=time.strftime("%Y-%m-%dT%H:%M:%S")+'-06:00' #TODO default back 24 hours?
file_lstRun.close()

print("@@@@@@@@@@@@ Last Run Date:"+lastRunDate)

print("Access Token:", access_token)
print("Instance URL", instance_url)
print("Access Token:", r)

def sf_api_call(action, parameters = {}, method = 'get', data = {}):
    """
    Helper function to make calls to Salesforce REST API.
    Parameters: action (the URL), URL params, method (get, post or patch), data for POST/PATCH.
    """ 
    headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer %s' % access_token
    }
    if method == 'get':
        r = requests.request(method, instance_url+action, headers=headers, params=parameters, timeout=30)
    elif method in ['post', 'patch']:
        r = requests.request(method, instance_url+action, headers=headers, json=data, params=parameters, timeout=10)
    else:
        # other methods not implemented in this example
        raise ValueError('Method should be get or post or patch.')
    print('Debug: API %s call: %s' % (method, r.url) )
    if r.status_code < 300:
        if method=='patch':
            return None
        else:
            return r.json()
    else:
        raise Exception('API error when calling %s : %s' % (r.url, r.content))

query= 'SELECT CreatedBy.userName, CreatedBy.name, ID, Action, CreatedDate, DelegateUser, Display, Section from SetupAuditTrail where createdDate >= '+lastRunDate
#query='SELECT Action, DelegateUser,Display,Section from SetupAuditTrail where createdDate >= '+lastRunDate
print("++++++++ Query:"+query)

#print(json.dumps(sf_api_call('/services/data/v39.0/query/', {'q': query}), indent=2))

activities_json = sf_api_call('/services/data/v39.0/query/', { 'q': query})
activities= activities_json["records"]   

#create json
filename_json = "sf_audit_"+time.strftime("%d-%m-%Y-%H:%M:%S")+".json"
activity_data_json = open(filename_json, 'w')
json.dump(activities_json,activity_data_json)
activity_data_json.close()

filename = "sf_audit_"+time.strftime("%d-%m-%Y-%H:%M:%S")+".csv"
activity_data = open(filename, 'w')
csvwriter = csv.writer(activity_data)

count = 0


for act in activities:

      if count == 0: 
             header = act.keys()
             header.append("Name")
             header.append("User Name")
             csvwriter.writerow(header)
             count += 1
      
      values= act.values() 
      if act["CreatedBy"]!=None :
          uProps=act["CreatedBy"]["Name"]
          values.append(act["CreatedBy"]["Name"])
          values.append(act["CreatedBy"]["Username"])
      csvwriter.writerow(values)

activity_data.close()

#get last run date from file
try:
    file_lstRun = open("lastRunDate","w") 
    file_lstRun.write(time.strftime("%Y-%m-%dT%H:%M:%S")+'-06:00'+'\n')
except IOError:
    print("error writing file")
file_lstRun.close()

