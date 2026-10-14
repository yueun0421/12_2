
import streamlit as st
import math

st.set_page_config(
    page_title="한 끼 양 조절 도우미",
    page_icon="🍚",
    layout="wide",
)

# 음식별 1인 기준량(g)
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

# 식사 상황별 배율
MEAL_LEVELS = {
    "가볍게": 0.75,
    "보통": 1.0,
    "푸짐하게": 1.25,
}

st.title("🍚 한 끼 양 조절 도우미")
st.caption("인원수와 식사 상황에 맞춰 음식 준비량을 계산해 보세요.")

st.info(
    "기본 기준량을 활용한 간편 계산기입니다. "
    "음식의 종류, 조리 전후 상태, 개인의 식사량에 따라 "
    "실제 필요한 양은 달라질 수 있어요."
)

# 입력 영역
st.header("1. 식사 계획")

col1, col2 = st.columns(2)

with col1:
    people = st.number_input(
        "식사 인원",
        min_value=1,
        max_value=100,
        value=2,
        step=1,
    )

with col2:
    meal_level = st.selectbox(
        "식사 상황",
        list(MEAL_LEVELS.keys()),
        index=1,
    )

multiplier = MEAL_LEVELS[meal_level]

st.header("2. 준비할 음식")

food_names = list(FOODS.keys())

if "food_items" not in st.session_state:
    st.session_state.food_items = ["밥", "고기", "채소"]

with st.form("food_form"):
    selected_food = st.selectbox(
        "추가할 음식",
        food_names,
    )
    add_food = st.form_submit_button("음식 추가")

if add_food:
    if selected_food in st.session_state.food_items:
        st.warning("이미 추가된 음식입니다.")
    else:
        st.session_state.food_items.append(selected_food)
        st.rerun()

if not st.session_state.food_items:
    st.warning("음식을 하나 이상 추가해 주세요.")

# 음식별 계산
results = []

for index, food in enumerate(st.session_state.food_items):
    with st.container(border=True):
        col_name, col_amount, col_remove = st.columns([2, 2, 1])

        with col_name:
            st.subheader(food)

        with col_amount:
            base_amount = FOODS[food]
            recommended = base_amount * people * multiplier

            # 구매·준비하기 편하도록 10g 단위로 올림
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
            st.write("")
            if st.button(
                "삭제",
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
st.header("3. 준비량 한눈에 보기")

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

    # 복사하기 쉬운 텍스트
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
        height=220,
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
        - 밥: 1인 210g
        - 고기: 1인 180g
        - 생선: 1인 150g
        - 파스타·국수: 건면 기준 1인 100g
        - 채소: 1인 150g

        기준량은 계산 편의를 위한 예시입니다.
        밥·면처럼 조리 전후 무게가 달라지는 음식은
        표시된 기준량의 상태를 확인해 주세요.

        이 계산기는 음식별 준비량을 각각 계산하며,
        반찬 간의 대체 관계나 영양 균형을 자동 판단하지 않습니다.
        """
    )

st.caption("Made with Streamlit · 별도 API 키 없이 실행됩니다.")

