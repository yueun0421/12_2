
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

/* 전체 배경 */
.stApp {
    background-color: #80F5F5;
}

/* 화면 너비 */
.block-container {
    padding-top: 2rem;
    max-width: 900px;
}

/* 제목 */
.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 900;
    color: black;
    margin-bottom: 50px;
}

/* 메뉴 버튼 */
div.stButton > button {
    background-color: #80F5F5;
    color: black;
    border: 3px solid black;
    border-radius: 12px;
    font-size: 28px;
    font-weight: bold;
    min-height: 180px;
    width: 100%;
    white-space: pre-wrap;
    transition: 0.2s;
}

/* 버튼에 마우스를 올렸을 때 */
div.stButton > button:hover {
    background-color: #B0FFFF;
    color: black;
    border: 3px solid black;
    transform: scale(1.02);
}

/* 글자 색상 */
h1, h2, h3, p {
    color: black !important;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# 유통기한 설명 팝업
# -----------------------------
@st.dialog("🥬 유통기한")
def expiry_dialog():

    st.write(
        "식재료나 음식의 유통기한을 쉽게 확인할 수 있다"
    )


# -----------------------------
# 조리법 설명 팝업
# -----------------------------
@st.dialog("🍳 조리법")
def recipe_dialog():

    st.write(
        "가지고 있는 식재료의 적당량과 "
        "만들고자하는 음식의 조리법을 알려준다"
    )


# -----------------------------
# 메인 화면
# -----------------------------
st.markdown(
    '<div class="main-title">양 조절 도우미</div>',
    unsafe_allow_html=True
)

# 메뉴 버튼 2개
col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🥬\n유통기한",
        key="expiry_menu",
        use_container_width=True
    ):
        expiry_dialog()

with col2:

    if st.button(
        "🔎\n조리법",
        key="recipe_menu",
        use_container_width=True
    ):
        recipe_dialog()


# -----------------------------
# 하단 안내 문구
# -----------------------------
st.markdown("---")

st.markdown(
    """
    <p style="
        text-align: center;
        font-size: 18px;
        color: black;
    ">
        냉장고 속 식재료를 알뜰하게 활용해 보세요!
    </p>
    """,
    unsafe_allow_html=True
)
