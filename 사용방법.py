import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="밀키트 사용방법",
    page_icon="⭐",
    layout="centered"
)

# 손그림 상단 타이틀 반영
st.markdown("<h1 style='text-align: center;'>⭐ 밀키트 사용방법 ⭐</h1>", unsafe_allow_html=True)
st.write("")
st.write("")

# 3개의 메뉴 카드 (손그림의 3개 아이콘 및 하단 레이블 반영)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<h1 style='text-align: center;'>📄</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>▲ 유통기한</h3>", unsafe_allow_html=True)
    st.caption("남은 유통기한 및 D-Day를 확인하세요.")
    st.page_link("pages/유통기한.py", label="유통기한 확인하기", icon="📅", use_container_width=True)

with col2:
    st.markdown("<h1 style='text-align: center;'>🍳</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>▲ 밀키트 조리</h3>", unsafe_allow_html=True)
    st.caption("단계별 조리법과 타이머를 확인하세요.")
    st.page_link("pages/조리법 설명.py", label="조리법 설명보기", icon="👨‍🍳", use_container_width=True)

with col3:
    st.markdown("<h1 style='text-align: center;'>🥕</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>▲ 영양정보</h3>", unsafe_allow_html=True)
    st.caption("밀키트 주요 영양성분을 확인하세요.")
    st.page_link("pages/영양정보.py", label="영양정보 확인하기", icon="🥗", use_container_width=True)

st.divider()
st.caption("💡 아래 또는 메뉴를 통해 원하시는 페이지로 이동할 수 있습니다.")
