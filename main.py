from flask import Flask, render_template, request, redirect, url_for, session
import requests
import json
import random

HOST = random.choice((requests.get('https://api.audius.co')).json()['data'])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

# Audius authentication configuration
API_KEY = '1265a8aa372fb0d436c528e5aad0e369fc72d7f5'
SECRET_KEY = '039babed4cc0332a3b58376025342469c3cfb16155b1770de7336f51dd60267b'
REDIRECT_URI = 'http://localhost:5000/callback'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    url = f'https://audius-discovery-7.cultur3stake.com/v1/tracks/search?query={query}'
    response = requests.get(url)
    data = response.json()
    return render_template('results.html', tracks=data['data'], query=query)

@app.route('/play/<track_id>')  
def play(track_id):
    url = f'https://audius-discovery-6.cultur3stake.com/v1/tracks/{track_id}/stream'
    return render_template('player.html', track_url=url)

@app.route('/login')
def login():
    auth_url = f'https://audius.co/oauth/auth?scope=write&api_key={API_KEY}&redirect_uri={REDIRECT_URI}&state=123456&response_mode=query'
    return redirect(auth_url)

@app.route('/callback')
def callback():
    access_token = request.args.get('token')
    session['access_token'] = access_token
    # Store the access_token securely for future use
    # You can redirect the user to a different page or perform any other action here
    
    # Get user info using the API and request
    user_info_url = f'{HOST}/v1/users/verify_token?token={access_token}'
    response = requests.get(user_info_url)
    if response.status_code == 200:
        session['name'] = response.json()['data']['name']
        session['handle'] = response.json()['data']['handle']
        session['email'] = response.json()['data']['email']
        session['userId'] = response.json()['data']['userId']
        session['pp'] = response.json()['data']['profilePicture']['1000x1000']
        return str(response.json())
    else:
        return 'Error: invalid token. Did you reload an old, old, ooooold page ?'

if __name__ == '__main__':
    app.run(debug=True)