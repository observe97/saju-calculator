from flask import Flask, render_template, request
from saju_calculator import calculate_saju, analyze_saju, generate_report

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        year = int(request.form['year'])
        month = int(request.form['month'])
        day = int(request.form['day'])
        hour = int(request.form['hour'])
        gender = request.form['gender']

        saju = calculate_saju(year, month, day, hour)
        analysis = analyze_saju(saju, year, month, day, gender)
        report = generate_report(saju, analysis, year, month, day, gender)

        return render_template('result.html', saju=saju, analysis=analysis, report=report)
    return render_template('index.html')


# Vercel requires the app to be named 'app'
app = app