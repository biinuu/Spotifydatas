import base64
import requests
from dotenv import load_dotenv
import os
import json


# LOAD ENV VARIABLES

load_dotenv(".env")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# CREATE SPOTIFY TOKEN

def access_token():
    try:
        credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(
            credentials.encode("utf-8")
        ).decode("utf-8")

        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={
                "Authorization": f"Basic {encoded_credentials}",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data={"grant_type": "client_credentials"}
        )

        if response.status_code != 200:
            print("Token error:", response.text)
            return None

        return response.json()["access_token"]

    except Exception as e:
        print("Error in token generation:", e)
        return None


# FETCH NEW RELEASES

def get_new_release():
    try:
        token = access_token()
        if not token:
            return

        headers = {"Authorization": f"Bearer {token}"}
        params = {"limit": 50}

        response = requests.get(
            "https://api.spotify.com/v1/browse/new-releases",
            headers=headers,
            params=params
        )

        if response.status_code != 200:
            print("Failed to fetch data:", response.text)
            return

        data = response.json()
        albums = data["albums"]["items"]

        output = []

        for album in albums:
            info = {
                "album_name": album["name"],
                "artist_name": album["artists"][0]["name"],
                "release_date": album["release_date"],
                "album_type": album["album_type"],
                "total_tracks": album["total_tracks"],
                "spotify_url": album["external_urls"]["spotify"],
                "album_image": album["images"][0]["url"] if album["images"] else None
            }
            output.append(info)


        # SAVE TO JSON FILE

        with open("spotify_new_releases.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)

        print(" Data saved to spotify_new_releases.json")

    except Exception as e:
        print("Error in latest release data fetching:", e)



# RUN PROGRAM

if __name__ == "__main__":
    get_new_release()
