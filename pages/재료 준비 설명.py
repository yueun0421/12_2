import streamlit as st
import math

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="재료 준비 - POZZO Style",
    page_icon="🍚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. POZZO 웹사이트 커스텀 CSS
st.markdown(
    """
    <style>
    /* 전체 배경 - 밝은 파스텔 크림/아이보리 */
    .stApp {
        background-color: #F8F5EE !important;
        font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
    }

    /* 좌측 사이드바 - 분홍색 세로 메뉴바 */
    [data-testid="stSidebar"] {
        background-color: #FA8C9D !important;
        border-right: 3px solid #E87587;
        padding-top: 1rem;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] .stNumberInput input, 
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border-radius: 10px;
    }

    /* 메인 타이틀 어닝(Awning) 차양 지붕 및 비주얼 상자 */
    .awning-roof {
        height: 18px;
        background: repeating-linear-gradient(
            -45deg,
            #E95A6C,
            #E95A6C 20px,
            #FFFFFF 20px,
            #FFFFFF 40px
        );
        border-radius: 12px 12px 0 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
    }
    .header-banner {
        background-color: #FFFFFF;
        padding: 25px 20px;
        border-radius: 0 0 16px 16px;
        text-align: center;
        border: 2px solid #F3C2C9;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .header-banner h1 {
        color: #E95A6C;
        font-weight: 800;
        margin-bottom: 8px;
        font-size: 2.1rem;
    }
    .header-banner p {
        color: #777777;
        margin: 0;
        font-size: 0.95rem;
    }

    /* 파스텔 디자인 카드 스타일 */
    .pozzo-card {
        background-color: #FFFDF7;
        border-radius: 16px;
        padding: 20px;
        border: 2px solid #F0E6D2;
        box-shadow: 0 4px 10px rgba(0,0,0,0.02);
        margin-bottom: 15px;
    }
    .card-yellow { background-color: #FFF9E6; border-color: #F5E2B3; }
    .card-green  { background-color: #F0F9F5; border-color: #CCEAD8; }
    .card-blue   { background-color: #F0F7FF; border-color: #CCE0FF; }
    .card-pink   { background-color: #FFF0F2; border-color: #FCD0D7; }

    /* 입체감 있는 뽀쪼 스타일 버튼 */
    .stButton>button {
        background-color: #7AC0B6 !important; /* 민트 그린 */
        color: #FFFFFF !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 8px 18px !important;
        box-shadow: 0 4px 0 #5B9B92 !important;
        transition: all 0.1s ease;
    }
    .stButton>button:hover {
        transform: translateY(2px);
        box-shadow: 0 2px 0 #5B9B92 !important;
    }

    /* 폼 제출 버튼 (분홍색 입체 버튼) */
    .stFormSubmitButton>button {
        background-color: #FA8C9D !important;
        box-shadow: 0 4px 0 #D66D7E !important;
        width: 100%;
    }
    .stFormSubmitButton>button:hover {
        box-shadow: 0 2px 0 #D66D7E !important;
    }

    /* 강조 메트릭 텍스트 */
    [data-testid="stMetricValue"] {
        color: #E95A6C !important;
        font-weight: 800 !important;
    }

    /* 입력창 및 구분선 */
    .stTextArea textarea {
        background-color: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #E5D8C5;
    }
    hr {
        border-top: 2px dashed #E5D8C5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 기본 데이터: 1인 기준 중량(g) 및 100g당 평균 칼로리(kcal)
FOODS = {
    "밥": {"amount": 210, "kcal_per_100g": 130},
    "고기": {"amount": 180, "kcal_per_100g": 250},
    "생선": {"amount": 150, "kcal_per_100g": 140},
    "파스타(건면)": {"amount": 100, "kcal_per_100g": 360},
    "국수(건면)": {"amount": 100, "kcal_per_100g": 350},
    "감자": {"amount": 200, "kcal_per_100g": 76},
    "채소": {"amount": 150, "kcal_per_100g": 25},
    "과일": {"amount": 150, "kcal_per_100g": 50},
    "두부": {"amount": 150, "kcal_per_100g": 84},
    "떡볶이 떡": {"amount": 200, "kcal_per_100g": 220},
}

MEAL_LEVELS = {
    "가볍게": 0.75,
    "보통": 1.0,
    "푸짐하게": 1.25,
}

# 좌측 사이드바
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🏠 POZZO Menu</h2>", unsafe_allow_html=True)
    st.divider()
    
    st.subheader("⚙️ 조건 설정")
    people = st.number_input(
        "식사 인원 (명)",
        min_value=1,
        max_value=100,
        value=2,
        step=1,
    )
    meal_level = st.selectbox(
        "식사 분량",
        list(MEAL_LEVELS.keys()),
        index=1,
    )
    
    st.divider()
    st.caption("💖 Sweet & Cute Prep Helper")

multiplier = MEAL_LEVELS[meal_level]

# 메인 헤더
st.markdown('<div class="awning-roof"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="header-banner">
        <h1>🍨 재료 준비 & 칼로리 계산기</h1>
        <p>인원수와 식사 양에 맞춰 식재료 준비량과 예상 칼로리를 손쉽게 계산해 보세요!</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 1. 추가할 재료 선택 카드
with st.container():
    st.markdown('<div class="pozzo-card card-yellow">', unsafe_allow_html=True)
    st.subheader("🥗 1. 준비할 재료 선택")
    
    food_names = list(FOODS.keys())
    if "food_items" not in st.session_state:
        st.session_state.food_items = ["밥", "고기", "채소"]

    with st.form("food_form"):
        col_select, col_btn = st.columns([3, 1])
        with col_select:
            selected_food = st.selectbox(
                "추가할 재료 선택",
                food_names,
                label_visibility="collapsed"
            )
        with col_btn:
            add_food = st.form_submit_button("＋ 재료 추가")

    if add_food:
        if selected_food in st.session_state.food_items:
            st.warning("이미 목록에 추가된 재료입니다.")
        else:
            st.session_state.food_items.append(selected_food)
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.food_items:
    st.warning("재료를 하나 이상 추가해 주세요.")

# 개별 재료 카드 및 칼로리 계산
st.subheader("📋 선택한 재료별 권장량 및 예상 칼로리")

results = []
card_colors = ["card-pink", "card-green", "card-blue", "card-yellow"]

for index, food in enumerate(st.session_state.food_items):
    color_class = card_colors[index % len(card_colors)]
    
    with st.container():
        st.markdown(f'<div class="pozzo-card {color_class}">', unsafe_allow_html=True)
        col_name, col_amount, col_kcal, col_remove = st.columns([1.8, 1.5, 1.5, 0.8])

        base_amount = FOODS[food]["amount"]
        kcal_per_100g = FOODS[food]["kcal_per_100g"]
        
        # 권장량(10g 단위 올림) 및 예상 칼로리 계산
        recommended = base_amount * people * multiplier
        rounded_amount = math.ceil(recommended / 10) * 10
        total_kcal = math.round((rounded_amount / 100) * kcal_per_100g) if hasattr(math, 'round') else round((rounded_amount / 100) * kcal_per_100g)

        with col_name:
            st.markdown(f"<h3 style='margin:0; color:#444;'>🥑 {food}</h3>", unsafe_allow_html=True)
            st.caption(f"1인 {base_amount}g 기준 (100g당 약 {kcal_per_100g}kcal)")

        with col_amount:
            st.metric(
                "추천 준비량",
                f"{rounded_amount:,} g",
            )

        with col_kcal:
            st.metric(
                "예상 칼로리",
                f"{total_kcal:,} kcal",
            )

        with col_remove:
            st.write("")
            if st.button("삭제 🗑️", key=f"remove_{index}_{food}"):
                st.session_state.food_items.pop(index)
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        results.append({
            "재료": food,
            "1인 기준량(g)": base_amount,
            "권장량(g)": rounded_amount,
            "권장량(kg)": round(rounded_amount / 1000, 2),
            "예상 칼로리(kcal)": total_kcal,
        })

st.divider()

# 요약 카드 및 결과
st.subheader("📝 2. 재료 준비 및 칼로리 요약")

if results:
    total_g = sum(item["권장량(g)"] for item in results)
    total_calories = sum(item["예상 칼로리(kcal)"] for item in results)
    per_person_kcal = round(total_calories / people)

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown('<div class="pozzo-card card-blue">', unsafe_allow_html=True)
        st.metric("준비할 재료 종류", f"{len(results)}가지")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_m2:
        st.markdown('<div class="pozzo-card card-yellow">', unsafe_allow_html=True)
        st.metric("전체 중량 합계", f"{total_g:,} g")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_m3:
        st.markdown('<div class="pozzo-card card-pink">', unsafe_allow_html=True)
        st.metric("총 칼로리 (1인당)", f"{total_calories:,} kcal ({per_person_kcal:,} kcal/인)")
        st.markdown('</div>', unsafe_allow_html=True)

    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True,
    )

    # 메모용 요약 텍스트
    summary_lines = [
        "🥦 재료 준비 & 칼로리 요약 목록",
        f"식사 인원: {people}명",
        f"식사 분량: {meal_level}",
        "",
    ]
    for item in results:
        summary_lines.append(
            f"- {item['재료']}: {item['권장량(g)']:,}g ({item['권장량(kg)']:.2f}kg) | 약 {item['예상 칼로리(kcal)']:,}kcal"
        )
    summary_lines.append("")
    summary_lines.append(f"전체 중량 합계: {total_g:,}g")
    summary_lines.append(f"전체 칼로리 합계: {total_calories:,}kcal (1인당 약 {per_person_kcal:,}kcal)")

    summary = "\n".join(summary_lines)

    st.text_area(
        "재료 준비 메모 (복사해서 사용하세요)",
        value=summary,
        height=200,
    )

    st.download_button(
        "📄 재료 목록 다운로드 (.txt)",
        data=summary,
        file_name="ingredient_prep_kcal_list.txt",
        mime="text/plain",
        use_container_width=True,
    )

with st.expander("ℹ️ 1인 기본 기준량 및 칼로리 정보 안내"):
    st.markdown(
        """
        - **밥**: 1인 210g (약 273kcal)
        - **고기**: 1인 180g (약 450kcal)
        - **생선**: 1인 150g (약 210kcal)
        - **파스타·국수**: 건면 기준 1인 100g (약 350~360kcal)
        - **채소**: 1인 150g (약 38kcal)
        - **과일**: 1인 150g (약 75kcal)

        *표시된 칼로리는 대표 식재료 기준의 평균값으로 조리 방식 및 부위에 따라 달라질 수 있습니다.*
        """
    )

st.caption("Made with Streamlit · POZZO Gelateria Style Design")
