from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def guess_number_game():
    number_to_guess = random.randint(1, 100)
    attempts = 0
    guessed_correctly = False

    if request.method == 'POST':
        user_guess = int(request.form['guess'])
        attempts = int(request.form['attempts'])
        attempts += 1

        if user_guess < number_to_guess:
            feedback = "Too low! Try again."
        elif user_guess > number_to_guess:
            feedback = "Too high! Try again."
        else:
            guessed_correctly = True
            feedback = f"Congratulations! You guessed the number in {attempts} attempts."

        return render_template_string(game_template, feedback=feedback, attempts=attempts, guessed_correctly=guessed_correctly)
    else:
        return render_template_string(game_template, feedback="Enter a guess!", attempts=0, guessed_correctly=False)

game_template = """
<!DOCTYPE html>
<html>
<head><title>Number Guessing Game</title></head>
<body>
    <h2>Guess the number between 1 and 100!</h2>
    <form method="POST">
        <input type="number" name="guess" required>
        <input type="hidden" name="attempts" value="{{ attempts }}">
        <button type="submit">Guess</button>
    </form>
    <p>{{ feedback }}</p>
    {% if guessed_correctly %}
        <p><a href="/">Play Again</a></p>
    {% endif %}
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
