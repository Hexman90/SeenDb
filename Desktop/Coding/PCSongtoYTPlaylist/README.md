# PCSongtoYTPlaylist


## Description:
This program allows you to create a new playlist on your YouTube account and add songs to it from a local directory on your computer.

## Usage
To add videos to a new playlist, run the script and follow the prompts to enter the directory path of your music and the name of the new playlist you want to create. If the playlist is created successfully, the script will continue to search for and add the songs to the playlist.

If you have an existing playlist that you want to add the songs to, you can use the playlist_id variable in the script. Uncomment the playlist_id line and replace 'your_playlist_id' with the ID of your existing playlist and comment out the other variable.

Note: To get the ID of an existing playlist, you can go to the playlist page on YouTube and copy the string of characters after "list=" in the URL.

## Prerequisites
### Youtube Api Key Configuration

1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. If you're not already signed in, create an account and log in.
3. Create a new project by clicking on the "Select a Project" dropdown at the top of the page and clicking "New Project". Give it a name and click "Create".
4. Access the [APIs & Services Dashboard](https://console.cloud.google.com/apis/dashboard) and click "Enable APIs and Services". Search for "YouTube Data API v3" and enable it.
5. Head to the [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent)  select "External", then click "Create". Provide your app's name, email address for "User support email", and email address for "Developer contact information". Finally, click "SAVE AND CONTINUE".
6. On the "Scopes" page select "ADD OR REMOVE SCOPES". Look for "YoutubeData API V3" and check the box next to ".../auth/youtube.force-ssl" scope. Click "UPDATE" and "SAVE AND CONTINUE".
7. On the "Test users" page, select "ADD USERS" and enter your email address. Then, click "ADD" and "SAVE AND CONTINUE".
8. Go to the [Credentials](https://console.cloud.google.com/apis/credentials) page and click "Create Credentials". Choose "OAuth client ID".
9. Pick "Web application" as the application type. Give it a name and add the authorized redirect URIs to your OAuth consent screen. For instance, enter "https://localhost:8080/" as the redirect URI. If you have a domain name, you can replace "localhost" with it. Click "Create".
10. Click "DOWNLOAD JSON" and save it in the root directory. Rename the file to "YOUR_CLIENT_SECRET_FILE.json".