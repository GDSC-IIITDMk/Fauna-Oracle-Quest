from flask import Flask, render_template,request
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

# Define global variables for the model and data
clf = None
X = None

# Load the dataset and train the classifier
def load_model():
    global clf, X
    df = pd.read_csv("zoo.csv")
    df = df.replace({"b'true'": 1, "b'false'": 0})
    X = df.drop('animal', axis=1)
    y = df['animal']
    clf = DecisionTreeClassifier()
    clf.fit(X, y)

# Route to render the form for playing the game
@app.route('/')
def index():
    global clf, X
    if clf is None:
        load_model()  # Load the model if it's not already loaded
    return render_template('f.html')

# Route to handle form submission and display results
@app.route('/play_game', methods=['POST'])
def play_game_route():
    global clf, X
    button_clicked= request.form['button']
    if button_clicked=='yes':
        answers=1
    else:
        answers=0
    answers = answers.to_dict()
    if clf is None:
        load_model()  # Load the model if it's not already loaded
    node_index = 0
    for feature_name, answer in answers.items():
        feature_index = X.columns.get_loc(feature_name)
        answer_code = 1 if answer == 'YES' else 0
        next_node_index = clf.tree_.children_left[node_index] if answer_code == 0 else clf.tree_.children_right[node_index]
        if next_node_index == -1:
            predicted_animal = clf.classes_[clf.tree_.value[node_index].argmax()]
            return render_template('f.html', predicted_animal=predicted_animal)
        node_index = next_node_index
    return "Error: Couldn't find the next node."

if __name__ == '__main__':
    app.run(debug=True)
