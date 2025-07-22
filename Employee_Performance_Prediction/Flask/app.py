from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load your ML model (make sure model.pkl is in the same folder)
model = pickle.load(open('model.pkl', 'rb'))

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/predict")
def predict():
    return render_template('predict.html')

@app.route("/submit")
def submit():
    return render_template('submit.html')

@app.route("/pred", methods=['POST'])
def prediction():
    # Extract form data
    quarter = request.form['quarter']
    department = request.form['department']
    day = request.form['day']
    team = request.form['team']
    targeted_productivity = request.form['targeted_productivity']
    smv = request.form['smv']
    over_time = request.form['over_time']
    incentive = request.form['incentive']
    idle_time = request.form['idle_time']
    idle_men = request.form['idle_men']
    no_of_style_change = request.form['no_of_style_change']
    no_of_workers = request.form['no_of_workers']
    month = request.form['month']

    # Prepare input for prediction - convert all to correct types
    total = [[
        int(quarter), int(department), int(day), int(team),
        float(targeted_productivity), float(smv), int(over_time),
        int(incentive), float(idle_time), int(idle_men),
        int(no_of_style_change), float(no_of_workers), int(month)
    ]]

    prediction = model.predict(total)[0]  # Assuming model.predict returns list/array

    # Decide prediction message
    if prediction <= 0.3:
        text = 'Averagely Productive.'
    elif 0.3 < prediction <= 0.8:
        text = 'Medium Productive.'
    else:
        text = 'Highly Productive.'

    # Render submit.html with prediction text
    return render_template('submit.html', prediction_text=text)

if __name__ == "__main__":
    app.run(debug=True)
