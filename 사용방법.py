
import streamlit as st

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="양 조절 도우미",
    page_icon="🥗",
    layout="wide"
)

# -----------------------------
# 디자인 설정
# -----------------------------
st.markdown("""
<style>

/* 전체 배경 */
.stApp {
    background-color: #A8F1F7;
}

/* 메인 화면 여백 - 제목 잘림 방지 */
.block-container {
    padding-top: 3.5rem !important;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* 제목 상자 */
.title-box {
    background-color: white;
    border: 4px solid black;
    border-radius: 2px;
    width: 100%;
    min-height: 100px;
    box-sizing: border-box;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 15px;
    margin-bottom: 25px;
}

/* 제목 글자 */
.title-text {
    color: black;
    font-size: 38px;
    font-weight: 900;
    line-height: 1.5;
    margin: 0;
    text-align: center;
}

/* 페이지 기능 안내 */
.page-info {
    color: black;
    font-size: 22px;
    margin-top: 15px;
    margin-bottom: 25px;
    padding-left: 10px;
}

/* 메뉴 버튼 */
div.stButton > button {
    background-color: white;
    color: black;
    border: 4px solid black;
    border-radius: 2px;

    /* 버튼 세로 크기 */
    min-height: 200px;
    height: 200px;

    width: 100%;
    font-size: 25px;
    font-weight: bold;
    white-space: normal;

    display: flex;
    align-items: center;
    justify-content: center;
}

/* 버튼 마우스 효과 */
div.stButton > button:hover {
    background-color: #E8FFFF;
    color: black;
    border: 4px solid black;
}

/* 버튼 클릭 효과 */
div.stButton > button:active {
    background-color: #D0F8FA;
    color: black;
}

/* 작은 화면 대응 */
@media (max-width: 600px) {
    .block-container {
        padding-top: 2rem !important;
    }

    .title-text {
        font-size: 30px;
    }

    div.stButton > button {
        min-height: 150px;
        height: 150px;
        font-size: 20px;
    }
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# 유통기한 팝업
# -----------------------------
@st.dialog("🥬 유통기한 페이지")
def expiry_dialog():
    st.write(
        "식재료나 음식의 유통기한을 쉽게 확인할 수 있다"
    )


# -----------------------------
# 조리법 팝업
# -----------------------------
@st.dialog("🍳 조리법 페이지")
def recipe_dialog():
    st.write(
        "가지고 있는 식재료의 적당량과 "
        "만들고자하는 음식의 조리법을 알려준다"
    )


# -----------------------------
# 메인 화면
# -----------------------------

# 제목
st.markdown("""
<div class="title-box">
    <p class="title-text">양조절 도우미</p>
</div>
""", unsafe_allow_html=True)


# 페이지 기능 안내
st.markdown("""
<div class="page-info">
    ❔ 페이지 기능
</div>
""", unsafe_allow_html=True)


# 버튼 배치
col1, col2 = st.columns(2, gap="large")

with col1:
    if st.button(
        "유통기한 페이지",
        key="expiry_button",
        use_container_width=True
    ):
        expiry_dialog()

with col2:
    if st.button(
        "조리법 페이지",
        key="recipe_button",
        use_container_width=True
    ):
        recipe_dialog()
