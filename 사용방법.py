
import streamlit as st
from datetime import date, timedelta

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="양 조절 도우미",
    page_icon="🥗",
    layout="centered"
)

# -----------------------------
# 디자인
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #80F5F5;
}

.block-container {
    padding-top: 2rem;
    max-width: 900px;
}

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 900;
    color: #000000;
    margin-bottom: 40px;
}

.menu-button {
    width: 100%;
    height: 180px;
    background-color: #80F5F5;
    border: 4px solid black;
    border-radius: 12px;
    color: black;
    font-size: 30px;
    font-weight: bold;
    text-align: center;
}

div.stButton > button {
    background-color: #80F5F5;
    color: black;
    border: 3px solid black;
    border-radius: 12px;
    font-size: 25px;
    font-weight: bold;
    min-height: 140px;
    width: 100%;
    transition: 0.2s;
}

div.stButton > button:hover {
    background-color: #B0FFFF;
    color: black;
    border: 3px solid black;
    transform: scale(1.02);
}

h1, h2, h3, p, label {
    color: black !important;
}

.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stSelectbox div {
    background-color: white;
    color: black;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "foods" not in st.session_state:
    st.session_state.foods = []

if "page" not in st.session_state:
    st.session_state.page = "home"


# -----------------------------
# 팝업 창
# -----------------------------
@st.dialog("🥗 유통기한")
def expiry_dialog():
    st.write(
        "식재료나 음식의 유통기한을 쉽게 확인할 수 있다"
    )

    if st.button("유통기한 확인하기", use_container_width=True):
        st.session_state.page = "expiry"
        st.rerun()


@st.dialog("🍳 조리법")
def recipe_dialog():
    st.write(
        "가지고 있는 식재료의 적당량과 "
        "만들고자하는 음식의 조리법을 알려준다"
    )

    if st.button("조리법 확인하기", use_container_width=True):
        st.session_state.page = "recipe"
        st.rerun()


# -----------------------------
# 메인 화면
# -----------------------------
def home():
    st.markdown(
        '<div class="main-title">양 조절 도우미</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🥬\n\n유통기한",
            key="expiry_menu",
            use_container_width=True
        ):
            expiry_dialog()

    with col2:
        if st.button(
            "🍳\n\n조리법",
            key="recipe_menu",
            use_container_width=True
        ):
            recipe_dialog()

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center;'>"
        "냉장고 속 식재료를 알뜰하게 활용해 보세요!"
        "</p>",
        unsafe_allow_html=True
    )


# -----------------------------
# 유통기한 관리 페이지
# -----------------------------
def expiry_page():
    st.title("🥬 유통기한 확인")

    st.write(
        "냉장고에 있는 식재료를 등록하고 "
        "유통기한을 관리해 보세요."
    )

    st.markdown("---")

    st.subheader("식재료 등록")

    with st.form("food_form"):
        food_name = st.text_input("식재료 이름")

        storage = st.selectbox(
            "보관 장소",
            ["냉장실", "냉동실", "실온"]
        )

        expiry_date = st.date_input(
            "유통기한",
            value=date.today()
        )

        submitted = st.form_submit_button(
            "식재료 등록하기"
        )

        if submitted:
            if not food_name.strip():
                st.error("식재료 이름을 입력해 주세요.")
            elif expiry_date < date.today():
                st.warning(
                    "이미 지난 날짜입니다. "
                    "날짜를 다시 확인해 주세요."
                )
            else:
                st.session_state.foods.append({
                    "name": food_name.strip(),
                    "storage": storage,
                    "expiry": expiry_date
                })

                st.success(
                    f"{food_name} 등록이 완료되었습니다!"
                )

    st.markdown("---")
    st.subheader("등록된 식재료")

    foods = st.session_state.foods

    if not foods:
        st.info("아직 등록된 식재료가 없습니다.")
    else:
        today = date.today()

        for i, food in enumerate(foods):
            remaining = (food["expiry"] - today).days

            with st.container(border=True):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.write(f"### {food['name']}")
                    st.write(f"보관 장소: {food['storage']}")
                    st.write(
                        f"유통기한: "
                        f"{food['expiry'].strftime('%Y-%m-%d')}"
                    )

                    if remaining == 0:
                        st.warning("오늘까지!")
                    elif remaining <= 3:
                        st.warning(
                            f"유통기한 임박! "
                            f"{remaining}일 남음"
                        )
                    else:
                        st.success(
                            f"{remaining}일 남음"
                        )

                with col2:
                    if st.button(
                        "삭제",
                        key=f"delete_{i}"
                    ):
                        st.session_state.foods.pop(i)
                        st.rerun()

        st.markdown("---")
        st.subheader("보관 장소별 식재료 수")

        storage_count = {
            "냉장실": 0,
            "냉동실": 0,
            "실온": 0
        }

        for food in foods:
            storage_count[food["storage"]] += 1

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "냉장실",
            storage_count["냉장실"]
        )

        col2.metric(
            "냉동실",
            storage_count["냉동실"]
        )

        col3.metric(
            "실온",
            storage_count["실온"]
        )


# -----------------------------
# 조리법 페이지
# -----------------------------
def recipe_page():
    st.title("🍳 조리법 & 양 조절")

    st.write(
        "만들고 싶은 음식과 식사 인원을 입력하면 "
        "재료의 적당량을 계산해 줍니다."
    )

    st.markdown("---")

    dish = st.text_input(
        "만들고 싶은 음식",
        placeholder="예: 김치볶음밥"
    )

    ingredients = st.text_input(
        "가지고 있는 식재료",
        placeholder="예: 밥, 김치, 계란, 햄"
    )

    people = st.number_input(
        "식사 인원",
        min_value=1,
        max_value=20,
        value=2,
        step=1
    )

    base_people = st.number_input(
        "기준 레시피 인원",
        min_value=1,
        max_value=20,
        value=2,
        step=1
    )

    st.markdown("---")

    st.subheader("재료량 계산")

    st.write(
        "기준 레시피의 재료량을 입력하면 "
        "식사 인원에 맞게 자동으로 계산됩니다."
    )

    ingredient_name = st.text_input(
        "재료 이름",
        placeholder="예: 밥"
    )

    amount = st.number_input(
        "기준 재료량",
        min_value=0.0,
        value=2.0,
        step=0.5
    )

    unit = st.selectbox(
        "단위",
        ["공기", "g", "ml", "개", "큰술", "작은술"]
    )

    if st.button(
        "재료량 계산하기",
        use_container_width=True
    ):
        if not ingredient_name.strip():
            st.error("재료 이름을 입력해 주세요.")
        else:
            result = amount * people / base_people

            st.success(
                f"{people}인분 {ingredient_name}: "
                f"{result:g}{unit}"
            )

    st.markdown("---")

    st.subheader("간단한 조리법")

    if dish.strip():
        st.write(f"### {dish}")

        if ingredients.strip():
            st.write(
                f"사용할 재료: {ingredients}"
            )

        st.write("1. 필요한 식재료를 준비합니다.")
        st.write("2. 재료를 먹기 좋은 크기로 손질합니다.")
        st.write(
            "3. 음식에 맞는 조리 방법으로 익히거나 볶습니다."
        )
        st.write("4. 간을 맞추고 완성합니다.")

        st.caption(
            "※ 위 조리법은 기본 안내입니다. "
            "정확한 조리 시간과 방법은 음식에 따라 달라집니다."
        )
    else:
        st.info(
            "만들고 싶은 음식의 이름을 입력하면 "
            "기본 조리 안내를 확인할 수 있습니다."
        )


# -----------------------------
# 페이지 이동
# -----------------------------
if st.session_state.page == "home":
    home()

elif st.session_state.page == "expiry":
    expiry_page()

elif st.session_state.page == "recipe":
    recipe_page()

# -----------------------------
# 하단 홈 버튼
# -----------------------------
if st.session_state.page != "home":
    st.markdown("---")

    if st.button("🏠 메인 화면으로 돌아가기"):
        st.session_state.page = "home"
        st.rerun()
