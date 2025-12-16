import base64

import requests
from dotenv import load_dotenv
import os

load_dotenv('.env')

CLIENT_ID=os.getenv('CLIENT_ID')
CLIENT_SECRET=os.getenv('CLIENT_SECRET')

#creating token for spotify
def access_token():
    try:
        # combine client id and client secret
        credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        response=requests.post(
            'https://accounts.spotify.com/api/token',
            headers={"Authorization": f'Basic {encoded_credentials}'},
            data={'grant_type': 'client_credentials'}
        )

        return response.json()['access_token']


    except Exception as e:
        print('Error in generating')
# print(access_token())
#Latest release in spotify
def get_new_releases():
    token=access_token()
    header={'Authorization':f'Bearer {token}'}
    Param={'limit':50}
    response=requests.get('https://api.spotify.com/v1/browse/new-releases',headers=header,params=Param)

    # print(response)
    if response.status_code==200:
        # print(response.json())
        data=response.json()
      
        albums=data['albums']['items']
        for album in albums:
            a={
                'album_name':i['name'],
                'Release_date':i['release_date']
            }

            print(a)
get_new_releases()


#watched till 20:00





