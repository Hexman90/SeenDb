import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from sys import exit



def main():

    credentials = creds()
    youtube = build('youtube', 'v3', credentials=credentials)
    songs = get_songs_name()
    
    # Uncomment the playlist_id variable below and comment the other one if 
    # #you have already created a playlist and want to add the videos there
    
    # playlist_id = 'your_playlist_id'
    
    playlist_id = create_playlist(youtube)
    search_and_add_to_playlist(youtube, songs, playlist_id)

            
# Get credentials to connect to the API 
def creds():
    # Path to secret file
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
    # Check if secret file exists
    if os.path.exists(client_secrets_file):
        # Disable OAuthlib's HTTPS verification when running locally.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        # Get credentials and create an API client
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes=["https://www.googleapis.com/auth/youtube.force-ssl"])
        flow.run_local_server()
        credentials = flow.credentials
    else:
        print("'YOUR_CLIENT_SECRET_FILE.json' file does not exist. Please create the secret file!")
        print("Or if it is created place it in the root directory")
        exit(1)
    return credentials


def get_songs_name():
    # Create an empty list to store the names of songs in the music directory
    songs = []
    # Prompt the user to enter the music directory path
    while True:
        try:
            prompt_path = input('Music directory path: ')
            # Get a list of files in the directory
            folder_path = os.listdir(prompt_path)
            break
        except OSError:
            print("The filename/directory name is incorrect.")
    
    # Create a list of valid audio file extensions
    audio_extensions = [".mp3", ".wav", ".aac", ".m4a", ".flac", ".wma"]
    
    # Loop through the files in the directory and append the names of any audio files to the songs list
    for filename in folder_path:
        song, extension = os.path.splitext(filename)
        if extension in audio_extensions:
            songs += [song]
    
    return songs


def create_playlist(youtube):
    # Prompt the user to enter the name of the playlist to be created
    playlist_name = input('Playlist name: ')
    
    # Create the new playlist
    request = youtube.playlists().insert(
        part='snippet',
        body={
            'snippet': {
                'title': playlist_name,
                'description': 'A new playlist created using the YouTube API'
            }
        }
    )
    response = request.execute()
    # Extract the playlist ID from the response
    playlist_id = response['id']
    return playlist_id


def search_and_add_to_playlist(youtube,songs,playlist_id):
    # Loop trough the list of songs and search on youtube for the song
    for song in songs:
        try:
            request1 = youtube.search().list(
                part='snippet',
                q= song, 
                maxResults=1,
                type='video', 
            )
            response = request1.execute()
            song_id = ""
            try:
                # Get the ID of the first video in the response
                song_id = response['items'][0]['id']['videoId']
                # Print the title of the video found
                print(response['items'][0]['snippet']['title'])
            except IndexError:
                print(f'\u001b[44m{song}\u001b[0m\u001b[40;1m has not been found!\u001b[0m')

            if song_id: 
                # Add the song to the playlist
                request2 = youtube.playlistItems().insert(
                    part='snippet',
                    body={
                        'snippet': {
                            'playlistId': playlist_id,
                            'resourceId': {
                                'kind': 'youtube#video',
                                'videoId': song_id
                            }
                        }
                    }
                )
                request2.execute()
                if song == songs[-1]:
                    # If the last song has been added, print a message
                    print(f'\u001b[44mAll songs added to the playlist.\u001b[0m')
            else:
                pass
        except HttpError as e:
            if "quotaexceeded" in str(e).lower():
                print("\n\u001b[44mAPI usage limit exceeded. Wait for some time before trying again.\u001b[0m\n")
            exit(1)

    return song_id



if __name__ == '__main__':
    main()

