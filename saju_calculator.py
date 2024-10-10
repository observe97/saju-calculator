import datetime
from typing import Dict, List, Tuple

# 천간, 지지, 오행, 음양, 60갑자 데이터
TIANGAN: List[str] = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
DIZHI: List[str] = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
WUXING: Dict[str, str] = {
    '갑': '목', '을': '목', '병': '화', '정': '화', '무': '토', '기': '토',
    '경': '금', '신': '금', '임': '수', '계': '수',
    '자': '수', '축': '토', '인': '목', '묘': '목', '진': '토', '사': '화',
    '오': '화', '미': '토', '신': '금', '유': '금', '술': '토', '해': '수'
}
YINYANG: Dict[str, str] = {
    '갑': '양', '을': '음', '병': '양', '정': '음', '무': '양', '기': '음',
    '경': '양', '신': '음', '임': '양', '계': '음',
    '자': '양', '축': '음', '인': '양', '묘': '음', '진': '양', '사': '음',
    '오': '양', '미': '음', '신': '양', '유': '음', '술': '양', '해': '음'
}
WUXING_RELATIONS: Dict[str, Dict[str, str]] = {
    '목': {'생': '화', '극': '토', '피극': '금'},
    '화': {'생': '토', '극': '금', '피극': '수'},
    '토': {'생': '금', '극': '수', '피극': '목'},
    '금': {'생': '수', '극': '목', '피극': '화'},
    '수': {'생': '목', '극': '화', '피극': '토'}
}

# 십신 관계 정의
SHISHEN: Dict[str, Dict[str, str]] = {
    '목': {'목': '비겁', '화': '식신', '토': '재성', '금': '관곡', '수': '인수'},
    '화': {'목': '인수', '화': '비겁', '토': '식신', '금': '재성', '수': '관곡'},
    '토': {'목': '관곡', '화': '인수', '토': '비겁', '금': '식신', '수': '재성'},
    '금': {'목': '재성', '화': '관곡', '토': '인수', '금': '비겁', '수': '식신'},
    '수': {'목': '식신', '화': '재성', '토': '관곡', '금': '인수', '수': '비겁'}
}

# 60갑자 주기
SIXTY_JIAZI: List[str] = [f"{t}{d}" for t in TIANGAN for d in DIZHI]


def calculate_saju(year: int, month: int, day: int, hour: int) -> Dict[str, Tuple[str, str]]:
    """년, 월, 일, 시 사주 계산"""
    base_date = datetime.date(1984, 2, 4)  # 기준일
    birth_date = datetime.date(year, month, day)
    days_diff = (birth_date - base_date).days

    year_tiangang = TIANGAN[days_diff % 10]
    year_dizhi = DIZHI[days_diff % 12]

    month_tiangang = TIANGAN[(year * 2 + month + 1) % 10]
    month_dizhi = DIZHI[(month + 1) % 12]

    day_tiangang = TIANGAN[(days_diff + 9) % 10]
    day_dizhi = DIZHI[(days_diff + 3) % 12]

    hour_tiangang = TIANGAN[(days_diff * 2 + hour // 2) % 10]
    hour_dizhi = DIZHI[(hour // 2) % 12]

    return {
        'year': (year_tiangang, year_dizhi),
        'month': (month_tiangang, month_dizhi),
        'day': (day_tiangang, day_dizhi),
        'hour': (hour_tiangang, hour_dizhi)
    }


def analyze_wuxing(saju: Dict[str, Tuple[str, str]]) -> Dict[str, int]:
    """오행 분석"""
    wuxing_count = {'목': 0, '화': 0, '토': 0, '금': 0, '수': 0}
    for tiangan, dizhi in saju.values():
        wuxing_count[WUXING[tiangan]] += 1
        wuxing_count[WUXING[dizhi]] += 1
    return wuxing_count


def analyze_yinyang(saju: Dict[str, Tuple[str, str]]) -> Dict[str, int]:
    """음양 분석"""
    yinyang_count = {'음': 0, '양': 0}
    for tiangan, dizhi in saju.values():
        yinyang_count[YINYANG[tiangan]] += 1
        yinyang_count[YINYANG[dizhi]] += 1
    return yinyang_count


def analyze_wuxing_relations(wuxing_count: Dict[str, int]) -> str:
    """오행 관계 분석"""
    analysis = ""
    for wuxing, count in wuxing_count.items():
        if count > 0:
            analysis += f"{wuxing}({count}개): "
            relations = WUXING_RELATIONS[wuxing]
            analysis += f"생성: {relations['생']}, 통제: {relations['극']}, 제약: {relations['피극']}\n"
    return analysis


def analyze_day_master(saju: Dict[str, Tuple[str, str]]) -> str:
    """일간 분석"""
    day_master = WUXING[saju['day'][0]]
    return f"일주(日柱)의 천간 오행인 {day_master}이 일간(日干)이며, 사주의 중심이 됩니다."


def calculate_shishen(day_master: str, saju: Dict[str, Tuple[str, str]]) -> Dict[str, List[str]]:
    """십신 계산"""
    shishen_result = {}
    day_master_wuxing = WUXING[day_master]
    for pillar, (tiangan, dizhi) in saju.items():
        if pillar != 'day':  # 일주는 제외
            tiangan_shishen = SHISHEN[day_master_wuxing][WUXING[tiangan]]
            dizhi_shishen = SHISHEN[day_master_wuxing][WUXING[dizhi]]
            shishen_result[pillar] = [tiangan_shishen, dizhi_shishen]
    return shishen_result


def calculate_daeun(year: int, month: int, day: int, gender: str) -> List[str]:
    """대운 계산"""
    birth_date = datetime.date(year, month, day)
    next_jieqi = birth_date + datetime.timedelta(days=30)  # 간단히 다음 절기를 30일 후로 가정
    start_age = 1 if gender == 'male' else 2  # 남성은 순행, 여성은 역행

    daeun = []
    current_year_index = SIXTY_JIAZI.index(f"{TIANGAN[year % 10]}{DIZHI[year % 12]}")
    for i in range(8):  # 8개의 대운
        index = (current_year_index + (i * (1 if gender == 'male' else -1))) % 60
        daeun.append(f"{start_age + i * 10}세: {SIXTY_JIAZI[index]}")

    return daeun


def calculate_saeun(year: int) -> List[str]:
    """세운 계산"""
    saeun = []
    current_year_index = SIXTY_JIAZI.index(f"{TIANGAN[year % 10]}{DIZHI[year % 12]}")
    for i in range(10):
        index = (current_year_index + i) % 60
        saeun.append(f"{year + i}년: {SIXTY_JIAZI[index]}")

    return saeun


def analyze_saju(saju: Dict[str, Tuple[str, str]], birth_year: int, birth_month: int, birth_day: int,
                 gender: str) -> str:
    """사주 분석"""
    wuxing_count = analyze_wuxing(saju)
    yinyang_count = analyze_yinyang(saju)
    wuxing_relations = analyze_wuxing_relations(wuxing_count)
    day_master_analysis = analyze_day_master(saju)

    day_master = saju['day'][0]
    shishen_analysis = calculate_shishen(day_master, saju)
    daeun = calculate_daeun(birth_year, birth_month, birth_day, gender)
    saeun = calculate_saeun(birth_year)

    analysis = "사주 분석 결과:\n\n"
    analysis += f"1. 오행 분석:\n{', '.join([f'{k}: {v}' for k, v in wuxing_count.items()])}\n\n"
    analysis += f"2. 음양 분석:\n음 {yinyang_count['음']}, 양 {yinyang_count['양']}\n\n"
    analysis += f"3. 오행 관계 분석:\n{wuxing_relations}\n"
    analysis += f"4. 일간 분석:\n{day_master_analysis}\n\n"
    analysis += "5. 십신 분석:\n"
    for pillar, shishen in shishen_analysis.items():
        analysis += f"   {pillar}: {shishen[0]}(천간), {shishen[1]}(지지)\n"
    analysis += "\n6. 대운:\n"
    for daeun_item in daeun[:5]:  # 처음 5개 대운만 표시
        analysis += f"   {daeun_item}\n"
    analysis += "\n7. 세운 (향후 10년):\n"
    for saeun_item in saeun[:5]:  # 처음 5년만 표시
        analysis += f"   {saeun_item}\n"

    # 종합 분석
    dominant_element = max(wuxing_count, key=wuxing_count.get)
    weak_element = min(wuxing_count, key=wuxing_count.get)

    analysis += "\n8. 종합 분석:\n"
    analysis += f"- 가장 강한 기운: {dominant_element}\n"
    analysis += f"- 가장 약한 기운: {weak_element}\n"
    analysis += f"- 음양 균형: {'음' if yinyang_count['음'] > yinyang_count['양'] else '양'}의 기운이 강합니다.\n"

    # 운세 해석
    day_master_wuxing = WUXING[day_master]
    current_year = datetime.datetime.now().year
    current_year_wuxing = WUXING[TIANGAN[current_year % 10]]

    analysis += "\n9. 운세 해석:\n"
    if WUXING_RELATIONS[day_master_wuxing]['생'] == current_year_wuxing:
        analysis += "올해는 일간을 생해주는 해로, 전반적으로 긍정적인 기운이 흐릅니다.\n"
    elif WUXING_RELATIONS[day_master_wuxing]['극'] == current_year_wuxing:
        analysis += "올해는 일간을 극하는 해로, 도전과 변화의 시기가 될 수 있습니다.\n"
    else:
        analysis += "올해는 일간과 중성적인 관계의 해로, 안정적이나 큰 변화는 없을 수 있습니다.\n"

    return analysis


def generate_report(saju: Dict[str, Tuple[str, str]], analysis: str, birth_year: int, birth_month: int, birth_day: int,
                    gender: str) -> str:
    """사주 팔자 종합 보고서"""
    report = "사주 팔자 종합 보고서\n\n"
    report += "1. 사주 구성\n"
    for key, value in saju.items():
        report += f"   {key}: {value[0]}{value[1]}\n"
    report += "\n2. 상세 분석\n"
    report += analysis
    report += "\n3. 조언\n"
    report += "이 분석은 사주의 기본 원리와 복잡한 요소들을 고려한 것이지만, 개인의 구체적인 상황과 경험에 따라 해석이 달라질 수 있습니다. "
    report += "더 정확하고 개인화된 해석을 위해서는 전문가와의 상담을 추천드립니다."
    return report


# 사용 예시
def main():
    year, month, day, hour = 1990, 5, 15, 14
    gender = 'male'

    saju = calculate_saju(year, month, day, hour)
    analysis = analyze_saju(saju, year, month, day, gender)
    report = generate_report(saju, analysis, year, month, day, gender)

    print(report)


if __name__ == "__main__":
    main()
