import requests

url = "https://www.thebluealliance.com/api/v3/event/2024ausc/teams?X-TBA-Auth-Key=8xnOPBtV3yQxLNOgLWciKJI946VjkoqrKH2HkGnZerFwqhVZhcCkXrYtlXIKbYKd"

payload={}
headers = {
  'Authorization': '8xnOPBtV3yQxLNOgLWciKJI946VjkoqrKH2HkGnZerFwqhVZhcCkXrYtlXIKbYKd',
  'If-Modified-Since': ''
}

response = requests.request("GET", url)

print(response.text)