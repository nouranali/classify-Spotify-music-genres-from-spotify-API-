from __future__ import print_function    # (at top of module)
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
# query

def create_query():
    client_credentials_manager = SpotifyClientCredentials(client_id='4fc98dac7caa40a4ba3b5e3cd1d343f5',
                                                      client_secret='5980228801d8475d8ff252a478c851bf')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp
# retrieve songs ids from playlists
def get_ids(sp,id):
    songs_ids=[]
    res=sp.playlist(id)
    tracks=res['tracks']
    show_tracks(tracks,songs_ids)
    while tracks['next']:
        tracks=sp.next(tracks)
        show_tracks(tracks, songs_ids)
    return songs_ids  
  
def show_tracks(res,uri):
    for i,item in enumerate(res['items']):
        track=item['track']
        uri.append(track['id']) 
        
#extract audio features from song and create dataframe,csv file     
def get_features_df(sp,song_ids):
    features=[]
    idx=0
    while idx < len(song_ids):
        features+=sp.audio_features(song_ids[idx:idx+50])
        idx+=50
    features_ls=[]
    for f in features:
        features_ls.append([f['id'],f['energy'], f['liveness'],
                              f['tempo'], f['speechiness'],
                              f['acousticness'], f['instrumentalness'],
                              f['time_signature'], f['danceability'],
                              f['key'], f['duration_ms'],
                              f['loudness'], f['valence'],
                              f['mode']])
    df = pd.DataFrame(features_ls, columns=['id','energy', 'liveness',
                                              'tempo', 'speechiness',
                                              'acousticness', 'instrumentalness',
                                              'time_signature', 'danceability',
                                              'key', 'duration_ms', 'loudness',
                                              'valence', 'mode'])
    return df
    
        
if __name__ == '__main__':
    # playlists urls
    ids=['3ZgmfR6lsnCwdffZUan8EA',
          '1VirHbmy0KMtN8vbaOvIL6',
          '76h0bH2KJhiBuLZqfvPp3K',
          '5tA2x3J6yAaJpa7mHGvhmB',
          ] 
    genres=['pop','rock','r&b','country']
    sp=create_query()
    i=0
    for genre in genres:
        song_ids=get_ids(sp,ids[i])
        df=get_features_df(sp, song_ids)
        df.to_csv('{}_spotify.csv'.format(genre),index=False)
        i+=1

    
  
    