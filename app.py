from flask import Flask, request, url_for, session, redirect #python -m flask run
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
##OAUTH IS AUTHORIZATION NOT AUTHENTIFICATION
##AUTHORIZATION IS PROVING THAT SOMEONE ELSE TOLD ME I COULD ACCESS
app = Flask(__name__)

app.secret_key = "cookie"
app.config['SESSION_COOKIE_NAME'] = 'Andrews Cookie'
TOKEN_INFO = "token_info"

@app.route('/') #heading to direct to home page
def login():
    sp_oauth = create_spotify_oauth() #give us spotifyoauth object
    auth_url = sp_oauth.get_authorize_url() #redirect user to this url
    return redirect(auth_url)

@app.route('/redirect') #redirect url
def redirectPage():
    sp_oauth = create_spotify_oauth() #give us spotifyoauth object
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO]=token_info
    return redirect(url_for('getTracks', _external=True))

@app.route('/getTracks') #get songs
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not loggined in")
        return redirect("/")
        
    sp = spotipy.Spotify(auth = token_info['access_token'])
    all_songs=[]
    iteration = 0
    while True:
        items = sp.current_user_saved_tracks(limit=50, offset=iteration*50)['items']
        iteration +=1 
        all_songs += items
        if(len(items)<50):
            break
    return str(len(all_songs))
    #return "DUA LIPA SONGS PLEASE'redirectPage', _external=True"

 #dont post on github
def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id= "your client id on spotify developer",
        client_secret="your client secret on spotify developer",
        redirect_uri=url_for('redirectPage', _external=True),#url_for easier so dont have to hardcode localhost
        scope="user-library-read") #read library


