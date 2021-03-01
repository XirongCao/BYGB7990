client_id = '9ed36a6b1f414d35af796a15cb941bde'
client_secret = '4aeb9295aa804f758999c3041682d19f'

import base64
import datetime 
from urllib.parse import urlencode 

import requests
import csv

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
    
    def get_client_credentials(self):    # return a base64 encoded string
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }
    
    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        } 

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            # return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token() 
        return token

    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def get_resource(self, lookup_id, resource_type, version, extra=None):
        if extra == None:
            endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        else:
            endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}/{extra}"
        # print(endpoint)
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    

    def get_related_artists(self, _id):
        return self.get_resource(_id, "artists", "v1", "related-artists")
    
    def get_artists_albums(self, _id):
        return self.get_resource(_id, "artists", "v1", "albums")

    def get_track(self, _id):
        return self.get_resource(_id, "albums", "v1", "tracks")

    def get_track_attribute(self, _id):
        return self.get_resource(_id, "audio-features", "v1")

    def search(self, query, search_type):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({"q": query, "type": search_type.lower()})
        lookup_url = f"{endpoint}?{data}"
        r = requests.get(lookup_url, headers = headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()








def artists_search():
    spotify = SpotifyAPI(client_id, client_secret)
    name = input("who?\n").lower()
    new_search = spotify.search(name, "artist")
    for i in new_search["artists"]["items"]:
        if i["name"].lower() == name:
            return {"a_name": name, "a_id":i["id"]}
        else:
            print("there's not such an artist")




spotify =SpotifyAPI(client_id, client_secret)
x = spotify.get_related_artists("7nzSoJISlVJsn7O0yTeMOB")
for i in x["artists"]:
    print(i["genres"])
    print(i["name"])
    print(i["id"])
    print()
    print()




'''
# search specific artist
x = spotify.search("coldplay", "artist")
print(x)


# get track attribute 
z = spotify.get_track_attribute("4wCmu0vbPiwpd2vbLl95qy")
print(z)
for i in z:
    print(f"{i}: {z[i]}")

# search all related artists on spotify
x = spotify.get_related_artists("4gzpq5DPGxSnKTe4SA8HAU")
for i in x["artists"]:
    print(i["genres"])
    print(i["name"])
    print(i["id"])
    print()
    print()

# get track from album
y = spotify.get_track("7qz838dTkWnA9kZECzipD3")
print(type(y))
for i in y["items"]:
    print(i["name"])
    print(i["id"])
    print(i["type"])
    print(i["track_number"])
    print()
    print()


# get all albums of artist on spotify 
spotify =SpotifyAPI(client_id, client_secret)
x = spotify.get_artists_albums("4gzpq5DPGxSnKTe4SA8HAU")
print(type(x["items"]))
for i in range(len(x["items"])):
    if x["items"][i]["name"] != x["items"][i-1]["name"]:
        print(x["items"][i]["name"])
        print(x["items"][i]["id"])
        print()
        print()
'''

# print(spotify.get_related_artists("3tJoFztHeIJkJWMrx0td2f"))
# print(spotify.get_resource("3tJoFztHeIJkJWMrx0td2f", "artists", "v1", "related-artists"))
