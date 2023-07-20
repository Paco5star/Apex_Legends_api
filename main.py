from flask import Flask, render_template , redirect
import requests
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
app = Flask(__name__)


API_KEY = "aaa0958e995c1287acf3513bcd4feb1a"
URL_STATS = "https://api.mozambiquehe.re/bridge"
URL_MATCH_HISTORY = "https://api.mozambiquehe.re/games"
app.config["SECRET_KEY"] = 'HELLOTEAM'

class PlayerForm(FlaskForm):
    playerName = StringField('Player Username', validators=[DataRequired()])
    submit = SubmitField("get stats")

parameters = {
    "auth": API_KEY,
    "player": "Paco5star",
    "platform": "PC"

}

def fetch_player_stats(player_name):
    parameters = {
    "auth": API_KEY,
    "player": player_name,
    "platform": "PC"

}

    data = requests.get(url=URL_STATS, params=parameters)
    apex_data = json.loads(data.text)
    player_uid = apex_data["global"]["uid"]
    player_level = apex_data["global"]["level"]
    player_ranked = apex_data["global"]["rank"]["rankName"]
    player_name = apex_data["global"]["name"]
    player_ranked_div = apex_data["global"]["rank"]["rankDiv"]
    player_ranked_img = apex_data["global"]["rank"]["rankImg"]
    games_played = apex_data["total"]["games_played"]["value"]
    player_kd = apex_data["total"]["kd"]["value"]
    player_kills = apex_data["total"]["kills"]["value"]
    return player_level, player_ranked, player_name, player_ranked_div, player_ranked_img, games_played, player_kd, player_kills


# data = requests.get(url=URL_STATS, params=parameters)
# apex_data = json.loads(data.text)
# player_uid = apex_data["global"]["uid"]
# player_level = apex_data["global"]["level"]
# player_ranked = apex_data["global"]["rank"]["rankName"]
# PLayer_name = apex_data["global"]["name"]
# player_ranked_div = apex_data["global"]["rank"]["rankDiv"]
# player_ranked_img = apex_data["global"]["rank"]["rankImg"]
# games_played = apex_data["total"]["games_played"]["value"]
# player_kd = apex_data["total"]["kd"]["value"]
# player_kills = apex_data["total"]["kills"]["value"]
# parameters_match = {
#     "auth": API_KEY,
#     "uid": player_uid
# }
# match_data = requests.get(url=URL_MATCH_HISTORY,params=parameters_match )
# apex_match_data = json.loads(match_data.text)
@app.route("/", methods=["GET","POST"])
def home():
    form = PlayerForm()
    player_level = None
    player_ranked = None
    player_name = None
    player_ranked_div = None
    player_ranked_img = None
    games_played = None
    player_kd = None
    player_kills = None
    if form.validate_on_submit():
        player_name = form.playerName.data
        player_level, player_ranked, player_name, player_ranked_div, player_ranked_img, games_played, player_kd, player_kills = fetch_player_stats(player_name)
        print(f"name: {player_name}, rank: {player_ranked}, kills: {player_kills}, KD: {player_kd}")
        return render_template("index.html",form=form, player_level=player_level,player_ranked=player_ranked, player_name=player_name, player_ranked_div=player_ranked_div, player_ranked_img=player_ranked_img, games_played=games_played, player_kd=player_kd, player_kills=player_kills )
        


    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run()