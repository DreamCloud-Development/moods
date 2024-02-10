from flask import Flask, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

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

if __name__ == '__main__':
    app.run(debug=True)