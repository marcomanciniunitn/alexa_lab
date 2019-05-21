import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_game():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)

@ask.intent("NoIntent")
def byebye():
    bye_message = render_template("bye")

    return statement(bye_message)

@ask.intent("ChangeGame")
def change_game():
    change_message = render_template("change")

    numbers = [randint(0, 9) for _ in range(4)]

    session.attributes['numbers'] = numbers[::-1]  # reverse

    return statement(change_message)

@ask.intent("AMAZON.FallbackIntent")
def fallback_intent():
    fall_back_message = "Can you repeat please?"

    return question(fall_back_message)


@ask.intent("YesIntent")
def next_round():
    numbers = [randint(0, 9) for _ in range(3)]

    round_msg = render_template('round', numbers=numbers)

    session.attributes['numbers'] = numbers[::-1]  # reverse

    return question(round_msg)


@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int, "fourth": int})
def answer(first, second, third, fourth):

    winning_numbers = session.attributes['numbers']

    if len(winning_numbers) == 3:
        if [first, second, third] == winning_numbers:

            msg = render_template('win')

        else:

            msg = render_template('lose')
    elif len(winning_numbers) == 4:
        if [first, second, third, fourth] == winning_numbers:

            msg = render_template('win')

        else:

            msg = render_template('lose')

    return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)