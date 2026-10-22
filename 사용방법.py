
import streamlit as st

st.set_page_config(
    page_title="양 조절 도우미 앱",
    page_icon="🥕",
    layout="centered",
)

st.markdown("""
<style>
.stApp {
    background: #fffdf5;
    color: #252525;
}
.block-container {
    max-width: 900px;
    padding-top: 1.5rem;
}
.main-frame {
    border: 4px solid #252525;
    border-radius: 5px;
    padding: 20px;
    background: #fffdf8;
    box-shadow: 3px 3px 0 #ded8c8;
}
.app-title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 800;
    margin: 8px 0;
}
.subtitle {
    text-align: center;
    color: #68645b;
    margin-bottom: 25px;
}
.menu-card {
    border: 3px solid #292929;
    border-radius: 7px;
    padding: 16px 10px;
    text-align: center;
    background: white;
    box-shadow: 3px 3px 0 #e7e1d4;
}
.menu-emoji {
    font-size: 3.4rem;
}
.menu-name {
    font-size: 1.2rem;
    font-weight: 800;
}
div.stButton > button {
    border: 2px solid #292929;
    border-radius: 7px;
    background: #eaf5e9;
    color: #222;
    font-weight: 700;
    width: 100%;
    min-height: 2.8rem;
}
div.stButton > button:hover {
    border-color: #168b76;
    color: #146b5c;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-frame">', unsafe_allow_html=True)
st.markdown(
    '<div class="app-title">✳ 양 조절 도우미 앱 ✳</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">먹을 만큼 준비하고, 음식물 낭비를 줄여요!</div>',
    unsafe_allow_html=True,
)

left, right = st.columns(2, gap="medium")

with left:
    st.markdown("""
    <div class="menu-card">
        <div class="menu-emoji">🧊</div>
        <div class="menu-name">유통기한</div>
    </div>
    """, unsafe_allow_html=True)
    expiry_clicked = st.button(
        "유통기한 도움 보기", key="expiry_button"
    )

with right:
    st.markdown("""
    <div class="menu-card">
        <div class="menu-emoji">🥘</div>
        <div class="menu-name">밀키트조리</div>
    </div>
    """, unsafe_allow_html=True)
    meal_clicked = st.button(
        "밀키트조리 도움 보기", key="meal_button"
    )

if "open_panel" not in st.session_state:
    st.session_state.open_panel = None

if expiry_clicked:
    st.session_state.open_panel = (
        None if st.session_state.open_panel == "expiry"
        else "expiry"
    )

if meal_clicked:
    st.session_state.open_panel = (
        None if st.session_state.open_panel == "meal"
        else "meal"
    )

if st.session_state.open_panel == "expiry":
    st.markdown("---")
    st.subheader("🧊 유통기한 도움")

    st.write(
        "식품을 안전하게 보관하고, 먼저 먹을 음식을 "
        "정리하는 방법을 확인할 수 있어요."
    )

    st.markdown("""
    - **날짜 확인:** 포장지의 소비기한과 보관 안내를 확인해요.
    - **먼저 먹을 음식:** 날짜가 가까운 식품을 앞쪽에 둬요.
    - **보관 상태 확인:** 포장과 보관 조건을 살펴봐요.
    - **낭비 줄이기:** 냉장고 속 식품부터 확인하고 구매해요.
    """)

    st.info(
        "날짜만으로 안전 여부를 판단할 수는 없어요. "
        "제품의 보관 방법을 지키고, 상태가 의심스러우면 "
        "먹지 마세요."
    )

elif st.session_state.open_panel == "meal":
    st.markdown("---")
    st.subheader("🥘 밀키트조리 도움")

    st.write(
        "먹을 사람 수에 맞게 재료를 조절하고, "
        "음식이 남지 않도록 준비해 봐요."
    )

    col1, col2 = st.columns(2)

    with col1:
        kit_servings = st.number_input(
            "밀키트 기준 인원",
            min_value=1,
            max_value=20,
            value=2,
            step=1,
        )

    with col2:
        eaters = st.number_input(
            "실제 식사 인원",
            min_value=1,
            max_value=20,
            value=2,
            step=1,
        )

    ratio = eaters / kit_servings

    st.markdown("**재료 양 조절 예시**")
    st.write(
        f"기준 {kit_servings}인분을 {eaters}명이 먹는다면, "
        f"필요한 양은 기준 재료의 약 **{ratio:.2f}배**예요."
    )

    st.caption(
        f"예: 재료가 200g이라면 약 {200 * ratio:.0f}g을 "
        "기준으로 조절할 수 있어요."
    )

    st.markdown("""
    - 조리 전에 기준 인원과 조리 순서를 확인해요.
    - 소스와 물은 제품 안내에 맞춰 넣어요.
    - 식재료를 위생적으로 다루고 충분히 가열해요.
    - 남은 음식은 안전한 보관 방법에 따라 냉장 또는 냉동해요.
    """)

    st.info(
        "계산 결과는 단순 비율이에요. 물과 양념은 조리법에 "
        "따라 달라질 수 있으니 제품 설명을 우선으로 따라 주세요."
    )

st.markdown(
    '<p style="text-align:center;color:#777168;">'
    '작은 양 조절부터 시작해 음식물 낭비를 줄여 봐요 🌱'
    '</p>',
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)
