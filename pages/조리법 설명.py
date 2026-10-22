Python
import streamlit as st
import math

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="한 끼 양 조절 도우미",
    page_icon="🍚",
    layout="wide",
)

# 2. POZZO 파스텔 커스텀 CSS 주입
st.markdown(
    """
    <style>
    /* 전체 배경색 - 파스텔 톤 크림/아이보리 */
    .stApp {
        background-color: #FAF6EE;
        font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
    }
    
    /* 사이드바 스타일링 - 이미지 좌측 분홍색 바 느낌 */
    [data-testid="stSidebar"] {
        background-color: #F8A3B2 !important;
        border-right: 2px solid #E88B9E;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] .stNumberInput input, 
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border-radius: 12px;
    }

    /* 메인 타이틀 & 어닝(Awning) 차양 스타일 */
    .main-header {
        background: repeating-linear-gradient(
            -45deg,
            #E75A6E,
            #E75A6E 20px,
            #FFFFFF 20px,
            #FFFFFF 40px
        );
        padding: 15px;
        border-radius: 16px 16px 0 0;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .main-title-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 0 0 16px 16px;
        text-align: center;
        margin-bottom: 25px;
        border: 2px solid #F3C5CE;
    }
    
    /* POZZO 파스텔 컬러 카드 컨테이너 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFF9E6 !important; /* 소프트 옐로우 파스텔 */
        border: 2px dashed #EED596 !important;
        border-radius: 16px !important;
        padding: 15px !important;
        box-shadow: 2px 4px 8px rgba(0,0,0,0.03);
    }

    /* 버튼 스타일 - 둥글고 장난감 같은 입체감 */
    .stButton>button {
        background-color: #83C5BE !important; /* 파스텔 민트 */
        color: white !important;
        font-weight: bold !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 8px 20px !important;
        box-shadow: 0 4px 0 #609A94 !important;
        transition: all 0.1s ease;
    }
    .stButton>button:hover {
        transform: translateY(2px);
        box-shadow: 0 2px 0 #609A94 !important;
    }

    /* Form submit 버튼 - 분홍색 스타일 */
    .stFormSubmitButton>button {
        background-color: #F497A9 !important;
        box-shadow: 0 4px 0 #D47587 !important;
    }
    .stFormSubmitButton>button:hover {
        box-shadow: 0 2px 0 #D47587 !important;
    }

    /* Metric 및 강조 텍스트 */
    [data-testid="stMetricValue"] {
        color: #E75A6E !important;
        font-weight: 800;
    }
    
    /* Dataframe 및 텍스트 상자 */
    .stTextArea textarea {
        background-color: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #E2D3C1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 데이터 정의
FOODS = {
    "밥": 210,
    "고기": 180,
    "생선": 150,
    "파스타(건면)": 100,
    "국수(건면)": 100,
    "감자": 200,
    "채소": 150,
    "과일": 150,
    "두부": 150,
    "떡볶이 떡": 200,
}

MEAL_LEVELS = {
    "가볍게": 0.75,
    "보통": 1.0,
    "푸짐하게": 1.25,
}

# 사이드바 설정 (이미지 좌측 메뉴 스타일 적용)
with st.sidebar:
    st.title("⚙️ 식사 계획")
    people = st.number_input(
        "식사 인원",
        min_value=1,
        max_value=100,
        value=2,
        step=1,
    )
    meal_level = st.selectbox(
        "식사 상황",
        list(MEAL_LEVELS.keys()),
        index=1,
    )
    st.divider()
    st.caption("🎈 POZZO Pastel Theme")

multiplier = MEAL_LEVELS[meal_level]

# 헤더 영역 (어닝 차양 디자인)
st.markdown('<div class="main-header"></div>', unsafe_allow_html=True)
with st.container():
    st.markdown(
        """
        <div class="main-title-box">
            <h1 style="color: #E75A6E; margin-bottom: 5px;">🍚 한 끼 양 조절 도우미</h1>
            <p style="color: #666; margin: 0;">인원수와 식사 상황에 맞춰 음식 준비량을 계산해 보세요.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.info(
    "기본 기준량을 활용한 간편 계산기입니다. "
    "음식의 종류, 조리 전후 상태, 개인의 식사량에 따라 "
    "실제 필요한 양은 달라질 수 있어요."
)

st.header("🍱 1. 준비할 음식 추가")

food_names = list(FOODS.keys())

if "food_items" not in st.session_state:
    st.session_state.food_items = ["밥", "고기", "채소"]

with st.form("food_form"):
    selected_food = st.selectbox(
        "추가할 음식 선택",
        food_names,
    )
    add_food = st.form_submit_button("＋ 음식 목록에 추가")

if add_food:
    if selected_food in st.session_state.food_items:
        st.warning("이미 추가된 음식입니다.")
    else:
        st.session_state.food_items.append(selected_food)
        st.rerun()

if not st.session_state.food_items:
    st.warning("음식을 하나 이상 추가해 주세요.")

st.subheader("📋 선택된 음식 계산 목록")

# 음식별 계산
results = []

for index, food in enumerate(st.session_state.food_items):
    with st.container(border=True):
        col_name, col_amount, col_remove = st.columns([2, 2, 1])

        with col_name:
            st.subheader(f"🍲 {food}")

        with col_amount:
            base_amount = FOODS[food]
            recommended = base_amount * people * multiplier

            # 10g 단위 올림
            rounded_amount = math.ceil(recommended / 10) * 10

            st.metric(
                "권장 준비량",
                f"{rounded_amount:,} g",
            )
            st.caption(
                f"1인 기준 {base_amount}g × "
                f"{people}명 × {multiplier}"
            )

        with col_remove:
            st.write("")
            if st.button(
                "삭제 🗑️",
                key=f"remove_{index}_{food}",
            ):
                st.session_state.food_items.pop(index)
                st.rerun()

        results.append({
            "음식": food,
            "1인 기준량(g)": base_amount,
            "인원수": int(people),
            "식사 배율": multiplier,
            "권장량(g)": rounded_amount,
            "권장량(kg)": round(rounded_amount / 1000, 2),
        })

st.divider()
st.header("📊 2. 준비량 한눈에 보기")

if results:
    total = sum(item["권장량(g)"] for item in results)

    metric1, metric2 = st.columns(2)
    metric1.metric("준비할 음식 종류", f"{len(results)}가지")
    metric2.metric("전체 준비량 합계", f"{total:,} g")

    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True,
    )

    # 복사용 텍스트 생성
    summary_lines = [
        "한 끼 양 조절 도우미 - 준비 목록",
        f"인원: {people}명",
        f"식사 상황: {meal_level}",
        "",
    ]

    for item in results:
        summary_lines.append(
            f"- {item['음식']}: {item['권장량(g)']:,}g "
            f"({item['권장량(kg)']:.2f}kg)"
        )

    summary_lines.append("")
    summary_lines.append(f"전체 합계: {total:,}g")

    summary = "\n".join(summary_lines)

    st.text_area(
        "준비 목록 (선택해서 복사하세요)",
        value=summary,
        height=200,
    )

    st.download_button(
        "📄 준비 목록 다운로드",
        data=summary,
        file_name="meal_plan.txt",
        mime="text/plain",
        use_container_width=True,
    )

else:
    st.info("음식을 추가하면 준비량이 여기에 표시됩니다.")

with st.expander("ℹ️ 기준량 안내"):
    st.markdown(
        """
        - **밥**: 1인 210g
        - **고기**: 1인 180g
        - **생선**: 1인 150g
        - **파스타·국수**: 건면 기준 1인 100g
        - **채소**: 1인 150g

        *기준량은 계산 편의를 위한 예시입니다.*
        """
    )

st.caption("Made with Streamlit · POZZO Style Customized Design")
