import datetime
from typing import Dict, List, Tuple

TIANGAN: List[str] = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
DIZHI: List[str] = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']

WUXING: Dict[str, str] = {
    '갑': '목', '을': '목', 
    '병': '화', '정': '화', 
    '무': '토', '기': '토', 
    '경': '금', '신': '금', 
    '임': '수', '계': '수',
    '자': '수', '축': '토', '인': '목', '묘': '목',
    '진': '토', '사': '화', '오': '화', '미': '토',
    '신': '금', '유': '금', '술': '토', '해': '수'
}

def calculate_saju(year: int, month: int, day: int, hour: int) -> Dict[str, Tuple[str, str]]:
    base_date = datetime.date(1984, 2, 4)
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

def analyze_saju(saju: Dict[str, Tuple[str, str]]) -> str:
    elements = [WUXING[gan] for gan, _ in saju.values()]
    element_counts = {element: elements.count(element) for element in set(elements)}
    
    strongest = max(element_counts, key=element_counts.get)
    weakest = min(element_counts, key=element_counts.get)
    
    analysis = f"가장 강한 기운: {strongest}, 가장 약한 기운: {weakest}\n"
    
    if strongest == '목':
        analysis += "창의적이고 진취적인 성향이 강합니다. 새로운 아이디어를 내고 실행에 옮기는 능력이 뛰어납니다."
    elif strongest == '화':
        analysis += "열정적이고 카리스마 있는 성격입니다. 리더십이 있고 사람들을 이끄는 능력이 뛰어납니다."
    elif strongest == '토':
        analysis += "안정적이고 신중한 성격입니다. 책임감이 강하고 믿음직한 사람으로 인정받을 수 있습니다."
    elif strongest == '금':
        analysis += "정의롭고 결단력 있는 성격입니다. 분석력이 뛰어나고 공정함을 중요시합니다."
    elif strongest == '수':
        analysis += "지혜롭고 유연한 성격입니다. 적응력이 뛰어나고 깊이 있는 사고를 하는 경향이 있습니다."
    
    return analysis
