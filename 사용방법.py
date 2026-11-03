
import streamlit as st

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="양 조절 도우미",
    page_icon="🥗",
    layout="centered"
)

# -----------------------------
# 디자인 설정
# -----------------------------
st.markdown("""
<style>

/* 배경 */
.stApp {
    background-color: #9BF3FA;
}

/* 페이지 여백 */
.block-container {
    padding-top: 1rem;
    max-width: 800px;
}

/* 제목 상자 */
.title-box {
    background-color: white;
    border: 4px solid black;
    border-radius: 2px;
    padding: 12px;
    text-align: center;
    margin-bottom: 18px;
}

/* 제목 글자 */
.title-text {
    color: black;
    font-size: 36px;
    font-weight: 900;
    margin: 0;
}

/* 페이지 기능 안내 */
.page-info {
    color: black;
    font-size: 20px;
    margin: 10px 0 15px 10px;
}

/* 메뉴 버튼 */
div.stButton > button {
    background-color: white;
    color: black;
    border: 4px solid black;
    border-radius: 2px;
    height: 75px;
    width: 100%;
    font-size: 22px;
    font-weight: bold;
}

/* 버튼에 마우스를 올렸을 때 */
div.stButton > button:hover {
    background-color: #E8FFFF;
    color: black;
    border: 4px solid black;
}

/* 버튼 클릭 시 */
div.stButton > button:active {
    background-color: #D0F8FA;
    color: black;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# 유통기한 설명 팝업
# -----------------------------
@st.dialog("🥬 유통기한 페이지")
def expiry_dialog():
    st.write(
        "식재료나 음식의 유통기한을 쉽게 확인할 수 있다"
    )


# -----------------------------
# 조리법 설명 팝업
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


# 페이지 기능
st.markdown("""
<div class="page-info">
    ❔ 페이지 기능
</div>
""", unsafe_allow_html=True)


# 메뉴 버튼
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
