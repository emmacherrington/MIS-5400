from pymongo import MongoClient
from flask import Flask, g, render_template, abort, request, jsonify
from bson.json_util import dumps
from bson.objectid import ObjectId



# Setup Flask
app = Flask(__name__)
app.config.from_object(__name__)

# Main api page
@app.route('/api/')
def api_help():
    return render_template('games_api.html'), 200

# GET ALL /api/v1/games
@app.route('/api/v1/games', methods=['GET'])
def get_all_games():
    client = MongoClient("mongodb+srv://MIS5400Admin:5400MIS@mis5400-rgwuo.mongodb.net/test?retryWrites=true&w=majority")
    games_db = client.bgg

    game_collection = games_db.user_games.find()

    return dumps(game_collection), 200


# GET ONE /api/v1/game/gameid
@app.route('/api/v1/games/<string:id>', methods=['GET'])
def get_one_game(id):
    client = MongoClient(
        "mongodb+srv://MIS5400Admin:5400MIS@mis5400-rgwuo.mongodb.net/test?retryWrites=true&w=majority")
    games_db = client.bgg

    game = games_db.user_games.find_one({'id': int(id)})

    return dumps(game), 200

# Add one game /api/v1/games
@app.route("/api/v1/games", methods=['POST'])
def add_game():
    try:
        client = MongoClient("mongodb+srv://MIS5400Admin:5400MIS@mis5400-rgwuo.mongodb.net/test?retryWrites=true&w=majority")
        games_db = client.bgg
        game_collection = games_db.user_games

        max_record = (game_collection.find().sort("id", -1).limit(1))
        max_num = 0
        for entry in max_record:
            max_num = (entry["id"] + 1)
        new_game = request.get_json()
        new_game["id"] = max_num
        game_collection.insert_one(new_game)

        return "Game Inserted", 201
    except Exception as e:
        return "Problem Inserting Game", 500

#Delete an entry
@app.route('/api/v1/games/<string:id>', methods=['DELETE'])
def delete_one_game(id):
    try:
        client = MongoClient("mongodb+srv://MIS5400Admin:5400MIS@mis5400-rgwuo.mongodb.net/test?retryWrites=true&w=majority")
        games_db = client.bgg
        game = games_db.user_games.delete_one({"id":int(id)})
        return 'Game Deleted', 200
    except Exception as e:
        return "Problem Deleting Game", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0")