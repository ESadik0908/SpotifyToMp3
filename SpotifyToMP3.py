import spotipy
import spotipy.oauth2 as oauth2
import yt_dlp
from youtube_search import YoutubeSearch

CLIENT_ID = 'Your_ID'
CLIENT_SECRET = "Your_SECRET"

def download_playlist(link):
    results = spotify.user_playlist(None, link, fields='tracks,next,name')
    playlist_name = results['name']
    tracks = results['tracks']
    
    for track in tracks['items']:
        if 'track' in track:
            track = track['track']
            
        else:
            track = track
        download_track(track, playlist_name)
        
def download_album(link):
    results = spotify.album(link)
    playlist_name = results['name']
    tracks = results['tracks']

    for track in tracks['items']:
        if 'track' in track:
            track = track['track']
            
        else:
            track = track
    download_track(track, playlist_name)


def download_track(track, playlist_name):
    track_name = track['name']
    track_artist = track['artists'][0]['name']
    full_name = track_name + ' - ' + track_artist
    full_name = full_name.replace('/', '')
    full_name = full_name.replace('\\', '')
    search_promopt = full_name + " audio"
    print(search_promopt)
    results_list = YoutubeSearch(search_promopt, max_results=1).to_dict()
    best_url = "https://www.youtube.com{}".format(results_list[0]['url_suffix'])
    print("Initiating download for {}.".format(search_promopt))
    download_location = 'C:/Users/Ethan/Desktop/Playlists' + '/' + playlist_name + '/' + full_name
    ydl_opts = {
        'outtmpl': download_location,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([best_url])


if __name__ == "__main__":
    auth_manager = oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    link = input("Paste link: ")
    if 'playlist' in link:
        download_playlist(link)
    
    if 'track' in link:
        track = spotify.track(link)
        track_name = track['name'] + ' Song Only'
        download_track(track, track_name)
    
    if 'album' in link:
        download_album(link)