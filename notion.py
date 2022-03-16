import json
import requests
#from main import request_headers

url = 'https://api.notion.com/v1/databases/'
token = ''
database_id = ''

with open("database_id.txt", 'r') as file:
    database_id = file.read()
   
with open("integration_token.txt", 'r') as file:
    token = file.read()
    
    
'''
curl -X GET https://api.notion.com/v1/database/{database_id} \
  -H "Authorization: Bearer {INEGRATION_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-02-22" \
'''

# Set URL, request headers and response
url = url + database_id
request_headers = {
    "Authorization":token,
    "Content-Type":"application/json",
    "Notion-Version": "2022-02-22"
}
response = None


# Check for connectivity with notion API
def check_connectivity():

    # Send get request to API and capture response
    response = requests.get(url, headers = request_headers)

    # If response status code is 2000 i.e. the response is successfull
    # continue and leave the function
    if response.status_code == 200:
        return 0

    # In case if the response is incorrect
    else:
        # Check for internet connectivity
        try:
            # Trying to send a get request to google.com to check what happens
            resp = requests.get("https://www.google.com")

            # If we are able to connect to google.com, this means internet conenction is present
            # Which means, there must be something wrong with database ID or integration token
            if resp.status_code == 200:
                print("Something is wrong with you database Id or intergation token.")
                print("Please check it and try again.")
                exit(0)

            # If we are unable to connect to google.com, it means there is no internet connection
            # available
            else:
                print("Unable to connect to the internet.")
                print("Please check your internet connection and try again")
                exit(0)

        # Exception handling
        except:
            print("Some exception occured...please try again")
            exit(0)  



def retrieve_data():
    # We will use the response generated above to get the data
    response_data = requests.get(url, headers = request_headers)

    # Get json data from response
    data = response_data.json()

    # Return json data
    return data

def save_data_as_json(data, filename):
    # If user enters filename with json extension
    if filename.endswith('.json'):
        # Write data to json
        with open(filename, 'w+') as file:
            file.write(json.dumps(data))
    # In case .json is not included in filename, add it and then save the file
    else:
        # Write data to json 
        with open(filename + ".json", 'w+') as file:
            file.write(json.dumps(data))  
   
def create_page(description, date, status):
    create_url = "https://api.notion.com/v1/pages"
    data = {
    "parent": { "database_id": database_id },
    "properties": {
        "Description": {
            "title": [
                {
                    "text": {
                        "content": description
                    }
                }
            ]
        },
        "Date": {
            "date": {
                        "start": date,
                        "end": None
                    }
        },
        "Status": {
            "rich_text": [
                {
                    "text": {
                        "content": status
                    }
                }
            ]
        }
    }}

    data = json.dumps(data)
    res = requests.post(create_url, headers=request_headers, data=data)
    print(res.status_code)
    return res

if __name__ == "__main__":  
    isRead = False
    saveFilename = ''
    check_connectivity()