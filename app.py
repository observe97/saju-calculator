from flask import Flask, render_template, request
from saju_calculator import calculate_saju, analyze_saju, generate_report

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            year = request.form.get('year')
            month = request.form.get('month')
            day = request.form.get('day')
            hour = request.form.get('hour')
            gender = request.form.get('gender')

            # 데이터가 제대로 받아졌는지 출력 (디버깅용)
            print(f"Year: {year}, Month: {month}, Day: {day}, Hour: {hour}, Gender: {gender}")

            # 데이터가 비어있는지 확인
            if not all([year, month, day, hour, gender]):
                raise ValueError("필수 필드가 누락되었습니다.")

            # 사주 계산 및 분석
            year = int(year)
            month = int(month)
            day = int(day)
            hour = int(hour)

            saju = calculate_saju(year, month, day, hour)
            analysis = analyze_saju(saju, year, month, day, gender)
            report = generate_report(saju, analysis, year, month, day, gender)

            return render_template('result.html', saju=saju, analysis=analysis, report=report)
        except Exception as e:
            return f"Error: {e}", 400  # 오류 발생 시 400 오류 반환

    return render_template('index.html')


# Vercel requires the app to be named 'app'
app = app