import streamlit as st

st.set_page_config(page_title="영양정보", page_icon="🥕")

st.title("🥕 밀키트 영양정보")
st.page_link("app.py", label="🏠 메인으로 돌아가기", icon="🏠")
st.divider()

nutrition_data = {
    "부대찌개 밀키트": {"칼로리": "650 kcal", "탄수화물": "55g", "단백질": "28g", "지방": "32g", "나트륨": "1800mg"},
    "우삼겹 떡볶이": {"칼로리": "780 kcal", "탄수화물": "95g", "단백질": "22g", "지방": "34g", "나트륨": "1500mg"}
}

selected = st.selectbox("영양성분을 조회할 밀키트를 선택하세요", list(nutrition_data.keys()))

if selected:
    data = nutrition_data[selected]
    st.subheader(f"📊 {selected} 영양 성분표 (1인분 기준)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔥 칼로리", data["칼로리"])
        st.metric("🍞 탄수화물", data["탄수화물"])
        st.metric("🥩 단백질", data["단백질"])
    with col2:
        st.metric("🥑 지방", data["지방"])
        st.metric("🧂 나트륨", data["나트륨"])
