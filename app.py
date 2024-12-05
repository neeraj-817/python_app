from flask import Flask, request, render_template_string, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a more secure key

@app.route('/', methods=['GET', 'POST'])
def guess_number_game():
    # Initialize or retrieve the number to guess and attempts from the session
    if 'number_to_guess' not in session:
        session['number_to_guess'] = random.randint(1, 100)
        session['attempts'] = 0

    number_to_guess = session['number_to_guess']
    attempts = session['attempts']
    guessed_correctly = False
    feedback = ""

    if request.method == 'POST':
        try:
            user_guess = int(request.form['guess'])
            attempts += 1
            session['attempts'] = attempts  # Update the attempt count in the session

            if user_guess < number_to_guess:
                feedback = "Too low! Try again."
            elif user_guess > number_to_guess:
                feedback = "Too high! Try again."
            else:
                guessed_correctly = True
                feedback = f"Congratulations! You guessed the number in {attempts} attempts."
                # Reset game if guessed correctly
                session.pop('number_to_guess', None)
                session.pop('attempts', None)

        except ValueError:
            feedback = "Please enter a valid number!"

    return render_template_string(game_template, feedback=feedback, attempts=attempts, guessed_correctly=guessed_correctly)

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
