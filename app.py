from flask import Flask, render_template, session, redirect, request, jsonify
from boggle import Boggle

app = Flask(__name__)
app.secret_key = "bigglebogglebibidibobidi"

boggle_game = Boggle()


@app.route("/")
def generate_board():
    """Generates the Boggle Board every refresh of the page and resets the game"""
    new_board = boggle_game.make_board()
    player_score = []
    session["board"] = new_board
    session["player_score"] = player_score
    return render_template("board.html")


@app.route("/checking", methods=["POST"])
def check_word():
    """Receives the word from the input on the front-end and checks if the word is a valid word or on the board and adds to to a list of words if valid"""
    other_word = request.get_json()
    json_info = other_word["json"]
    new_word = json_info["wordData"]
    if len(new_word) > 0:
        result = boggle_game.check_valid_word(session["board"], new_word)
        session["result"] = result
        score = session["player_score"]
        if result == "ok":
            if new_word not in score:
                score.append(new_word)
        session["player_score"] = score
        return result
    else:
        result = "please input a word"
        session["result"] = result
        return result


def get_results(result):
    """Makes the results dictionary"""
    res_dict = {"result": result}
    return res_dict


@app.route("/results/json")
def get_results_json():
    """Used for when the client requests the results of whether or not the word is valid"""
    dict = get_results(session["result"])
    return jsonify(dict)


@app.route("/score")
def get_score():
    """Used for when the client requests the list of words to calculate the score"""
    score_list = session["player_score"]
    return score_list


@app.route("/reset")
def reset_game():
    """resets the game when the button appears afterwards"""
    return redirect("/")


@app.route("/count")
def game_count():
    """counts the number of games that increases whenever the timer reaches zero"""
    session["count"] = session.get("count", 0) + 1
    count = str(session["count"])
    return count


@app.route("/high_score", methods=["POST"])
def get_high_score():
    """Determines whether the new score is a high score or not"""
    json = request.get_json()
    json_info = json["json"]
    json_score = json_info["total"]
    if json_score > session.get("player_high_score", 0):
        session["player_high_score"] = json_score
        return str(json_score)
    else:
        return str(json_score)
