from flask import Flask, render_template, request, redirect, url_for
from saju_calculator import calculate_saju, analyze_saju, generate_report
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            birthdate = request.form.get('birthdate')
            birthtime = request.form.get('birthtime')
            gender = request.form.get('gender')

            # 데이터가 제대로 받아졌는지 확인 (디버깅용)
            print(f"Birthdate: {birthdate}, Birthtime: {birthtime}, Gender: {gender}")

            # 필수 필드 검증
            if not all([birthdate, birthtime, gender]):
                raise ValueError("필수 필드가 누락되었습니다.")

            # 날짜와 시간을 분리
            year, month, day = map(int, birthdate.split('-'))
            hour = int(birthtime.split(':')[0])

            # 사주 계산 및 보고서 생성
            saju = calculate_saju(year, month, day, hour)
            analysis = analyze_saju(saju, year, month, day, gender)
            report = generate_report(saju, analysis, year, month, day, gender)

            return render_template('result.html', saju=saju, analysis=analysis, report=report)
        except Exception as e:
            return f"Error: {e}", 400  # 오류 발생 시 400 오류 반환

    return render_template('index.html')


# Vercel requires the app to be named 'app'
app = app
