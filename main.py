import random
import pandas
import logging
logging.basicConfig(level=logging.INFO)

from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from db.connection import Session, init_db
from repo.dictionary_crud import DictionaryRepository
from models import word_practice_history
from repo.word_practice_history_crud import WordPracticeHistoryRepository

game_modes = ["random", "least-practiced", "mixed"]

FLASH_CARD_GAME_DIFFICULTY_SETTINGS = {
    "easy": {"x": 4, "y": 3},
    "medium": {"x": 5, "y": 4},
    "hard": {"x": 6, "y": 5}
}

VOCABULARY_TEST_DIFFICULTY_SETTINGS = {
    "easy": 10,
    "medium": 20,
    "hard": 30,
}

#FLASH_CARD_GAME_SETTINGS = {
#    "easy": {"word_count": 6, "x": 4, "y": 3},
#    "medium": {"word_count": 10, "x": 5, "y": 4},
#    "hard": {"word_count": 15, "x": 6, "y": 5}
#}

# Load environment variables
load_dotenv()

app = Flask(__name__)

#Call the function that creates all the DB tables with SQLAlchemy ORM
init_db()

def get_word_list_for_game(game_mode, word_count):

    dict_repo = DictionaryRepository(Session())

    word_list = []

    if game_mode == "least-practiced":

        #We pick the least practiced words from the database in specified amount
        word_list = dict_repo.get_least_practiced_words(word_count)

    elif game_mode == "random":

        word_list = random.sample( dict_repo.get_all_words(), word_count )

    elif game_mode == "mixed":

        amount_of_least_practiced_words = random.randint(1, word_count - 1)

        least_practiced_words = dict_repo.get_least_practiced_words(amount_of_least_practiced_words)

        excluded_word_id_list = [dictionary_item.id for dictionary_item in least_practiced_words]

        random_words = random.sample(dict_repo.get_all_words_except(excluded_word_id_list), word_count - amount_of_least_practiced_words)

        word_list = least_practiced_words + random_words

    return word_list

#   Define a simple route
@app.route("/")
def home():
    return render_template("menu.html")


@app.route("/vocabulary-test-options", methods=["GET", "POST"])
def vocabulary_test_options():
    if request.method == "POST":
        mode = request.form.get("mode")
        difficulty = request.form.get("difficulty")
        word_count = VOCABULARY_TEST_DIFFICULTY_SETTINGS[difficulty]
        return redirect(url_for("vocabulary_test", game_mode=mode, word_count=word_count))
    return render_template(
        "vocabulary_test_options.html",
        game_modes=game_modes,
        difficulties=VOCABULARY_TEST_DIFFICULTY_SETTINGS.keys(),
    )


@app.route("/flash-card-options", methods=["GET", "POST"])
def flash_card_options():
    if request.method == "POST":
        mode = request.form.get("mode")
        difficulty = request.form.get("difficulty")
        return redirect(
            url_for("flash_card_game", game_mode=mode, game_difficulty=difficulty)
        )
    return render_template(
        "flash_card_options.html",
        game_modes=game_modes,
        difficulties=FLASH_CARD_GAME_DIFFICULTY_SETTINGS.keys(),
    )

@app.route("/show-dictionary")
def show_dictionary():
    dict_repo = DictionaryRepository(Session())
    word_list = dict_repo.get_all_words()

    words = ""

    for word in word_list:
        words += ( str(word) + "\n" )

    return words

@app.route("/vocabulary-test/<string:game_mode>/<int:word_count>")
def vocabulary_test(game_mode, word_count):

    words_in_game = get_word_list_for_game(game_mode, word_count)

    random.shuffle(words_in_game)

    return render_template("vocabulary_test.html", word_list = words_in_game)

@app.route("/flash-card-game/<string:game_mode>/<string:game_difficulty>")
def flash_card_game(game_mode, game_difficulty):

    x_dimension =  FLASH_CARD_GAME_DIFFICULTY_SETTINGS[game_difficulty]["x"]
    y_dimension = FLASH_CARD_GAME_DIFFICULTY_SETTINGS[game_difficulty]["y"]

    word_count = x_dimension * y_dimension // 2

    words_in_game = get_word_list_for_game(game_mode, word_count)

    cards = []

    for word in words_in_game:

        id_list = [word.id]

        for word_match in words_in_game:

            if word.id != word_match.id:

                if word.english == word_match.english:
                    id_list.append(word_match.id)
                if word.italian == word_match.italian:
                    id_list.append(word_match.id)

        id_list.sort()

        #prep cards with english words
        card_english = {'id': id_list, 'content': word.english, 'language': 'english'}

        #prep cards with italian words
        card_italian = {'id': id_list, 'content': word.italian, 'language': 'italian'}

        #add both types of cards to the card list
        cards.append(card_english)
        cards.append(card_italian)

    #randomize the order of words in the card list
    random.shuffle(cards)

    return render_template("flash_card_game.html", cards = cards, x_dimension = x_dimension, y_dimension = y_dimension)

@app.route("/import-words")
def import_words():

    #Import the words from the CSV file to a Pandas DataFrame
    imported_words_df = pandas.read_csv("dictionary.csv")

    #Create a list of dictionaries
    word_list = imported_words_df.to_dict(orient="records")

    dict_repo = DictionaryRepository(Session())
    dict_repo.add_word_list(word_list)

    return "Dictionary updated!"

@app.route("/update-practice-history", methods=["POST"])
def update_practice_history():

    data = request.get_json()
    word_id_list =  data.get("word_id_list", [])

    #Remove duplicate word ids
    word_id_list = list(dict.fromkeys(word_id_list))

    #Cast str ids to int ids
    word_id_list = [ int(word_id) for word_id in word_id_list ]

    word_practice_history_repo = WordPracticeHistoryRepository(Session())
    word_practice_history_repo.insert_update_practice_records(word_id_list)

    return word_id_list

if __name__ == '__main__':
    app.run(host="0.0.0.0")