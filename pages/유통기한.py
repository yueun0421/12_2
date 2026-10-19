import streamlit as st
import pandas as pd
import csv
import io
import uuid
from datetime import date, timedelta

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="냉장고 구출 작전",
    page_icon="🥦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    div[data-testid="stMetric"] {
        background: #F7F9FC;
        border: 1px solid #E5EAF1;
        padding: 16px;
        border-radius: 12px;
    }
    .food-tip {
        background: #F0F7F2;
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 5px solid #299764;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 세션 데이터 초기화
# -----------------------------
if "foods" not in st.session_state:
    st.session_state.foods = []

if "notice" not in st.session_state:
    st.session_state.notice = None


def safe_foods():
    """세션에 저장된 음식 목록을 안전하게 반환합니다."""
    foods = st.session_state.get("foods", [])
    if not isinstance(foods, list):
        st.session_state.foods = []
        return []
    return foods


def days_left(expiry):
    """유통기한까지 남은 날짜를 계산합니다."""
    return (expiry - date.today()).days


def food_status(expiry):
    remaining = days_left(expiry)
    if remaining < 0:
        return "🔴 기한 지남", remaining
    if remaining == 0:
        return "🟠 오늘까지", remaining
    if remaining <= 3:
        return "🟡 임박", remaining
    return "🟢 여유", remaining


def find_food(food_id):
    for food in safe_foods():
        if food.get("id") == food_id:
            return food
    return None


def export_csv():
    """현재 재고를 CSV 파일로 변환합니다."""
    output = io.StringIO()
    columns = [
        "음식명", "수량", "단위", "보관 장소",
        "구매일", "유통기한", "메모"
    ]
    writer = csv.DictWriter(output, fieldnames=columns)
    writer.writeheader()

    for food in safe_foods():
        writer.writerow({
            "음식명": food.get("name", ""),
            "수량": food.get("quantity", 0),
            "단위": food.get("unit", ""),
            "보관 장소": food.get("location", ""),
            "구매일": food.get("purchase_date", ""),
            "유통기한": food.get("expiry_date", ""),
            "메모": food.get("memo", ""),
        })

    return output.getvalue().encode("utf-8-sig")


# -----------------------------
# 공통 제목 및 메뉴
# -----------------------------
st.title("🥦 냉장고 구출 작전")
st.caption("음식이 많아도 괜찮아요. 먼저 먹을 음식부터 차근차근 관리해요.")

with st.sidebar:
    st.header("🍽️ 메뉴")
    page = st.radio(
        "이동할 화면",
        ["🏠 오늘의 대시보드", "➕ 음식 등록", "📦 재고 관리"],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### 💡 관리 팁")
    st.write("1. 새로 산 음식을 등록하세요.")
    st.write("2. 임박한 음식부터 확인하세요.")
    st.write("3. 다 먹은 음식은 목록에서 정리하세요.")
    st.caption("※ 현재 데이터는 브라우저 세션 동안 유지됩니다.")

foods = safe_foods()
today = date.today()

# -----------------------------
# 대시보드
# -----------------------------
if page == "🏠 오늘의 대시보드":
    st.subheader("오늘의 음식 현황")
    st.markdown(
        '<div class="food-tip">'
        '🥕 <b>작은 실천:</b> 오늘은 유통기한이 가까운 음식 하나부터 '
        '먼저 먹어 보세요!'
        '</div>',
        unsafe_allow_html=True,
    )

    expired = [
        f for f in foods
        if days_left(f["expiry_date"]) < 0
    ]
    urgent = [
        f for f in foods
        if 0 <= days_left(f["expiry_date"]) <= 3
    ]

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 등록된 음식", f"{len(foods)}개")
    col2.metric("⏰ 3일 이내 만료", f"{len(urgent)}개")
    col3.metric("🔴 기한 경과", f"{len(expired)}개")

    st.divider()
    st.subheader("🚨 먼저 확인할 음식")

    priority_foods = sorted(
        foods,
        key=lambda f: (f["expiry_date"], f["name"].lower()),
    )

    priority_foods = [
        f for f in priority_foods
        if days_left(f["expiry_date"]) <= 3
    ]

    if priority_foods:
        for food in priority_foods:
            status, remaining = food_status(food["expiry_date"])
            with st.container(border=True):
                left, middle, right = st.columns([2, 2, 1])
                left.markdown(f"**{food['name']}**")
                left.caption(
                    f"{food['quantity']} {food['unit']} · "
                    f"{food['location']}"
                )

                if remaining < 0:
                    middle.error(f"{abs(remaining)}일 지남")
                elif remaining == 0:
                    middle.warning("오늘까지")
                else:
                    middle.warning(f"{remaining}일 남음")

                right.caption(str(food["expiry_date"]))
    else:
        st.success("좋아요! 3일 이내에 만료되는 음식이 없습니다.")

    st.divider()
    st.subheader("📊 보관 장소별 음식 수")

    if foods:
        location_counts = {}
        for food in foods:
            location = food.get("location", "기타")
            location_counts[location] = (
                location_counts.get(location, 0) + 1
            )

        chart_data = pd.DataFrame({
            "보관 장소": list(location_counts.keys()),
            "음식 수": list(location_counts.values()),
        }).set_index("보관 장소")

        st.bar_chart(chart_data, color="#299764")
    else:
        st.info("아직 등록된 음식이 없습니다. '음식 등록'에서 시작해 보세요.")

# -----------------------------
# 음식 등록
# -----------------------------
elif page == "➕ 음식 등록":
    st.subheader("새로운 음식 등록")
    st.write("음식의 양이 많아도 하나씩 기록하면 관리하기 쉬워집니다.")

    with st.form("add_food_form", clear_on_submit=True):
        name = st.text_input(
            "음식 이름 *",
            placeholder="예: 사과, 우유, 닭가슴살",
        )

        col1, col2 = st.columns(2)
        with col1:
            quantity = st.number_input(
                "수량 *",
                min_value=1,
                max_value=100000,
                value=1,
                step=1,
            )
        with col2:
            unit = st.selectbox(
                "단위",
                ["개", "팩", "봉지", "통", "병", "g", "kg", "ml", "L", "인분"],
            )

        location = st.selectbox(
            "보관 장소",
            ["냉장실", "냉동실", "실온", "기타"],
        )

        col3, col4 = st.columns(2)
        with col3:
            purchase_date = st.date_input(
                "구매일",
                value=today,
                max_value=today,
            )
        with col4:
            expiry_date = st.date_input(
                "유통기한 *",
                value=today + timedelta(days=7),
            )

        memo = st.text_area(
            "메모 (선택)",
            placeholder="예: 대용량 구매, 개봉함, 가족과 나눠 먹기",
            max_chars=500,
        )

        submitted = st.form_submit_button(
            "➕ 음식 등록하기",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        clean_name = name.strip()

        if not clean_name:
            st.error("음식 이름을 입력해 주세요.")
        elif expiry_date < purchase_date:
            st.error("유통기한은 구매일보다 빠를 수 없습니다. 날짜를 확인해 주세요.")
        else:
            try:
                new_food = {
                    "id": str(uuid.uuid4()),
                    "name": clean_name,
                    "quantity": int(quantity),
                    "unit": unit,
                    "location": location,
                    "purchase_date": purchase_date,
                    "expiry_date": expiry_date,
                    "memo": memo.strip(),
                }
                st.session_state.foods.append(new_food)
                st.success(f"'{clean_name}' 등록이 완료되었습니다!")
                st.rerun()
            except (ValueError, TypeError, AttributeError):
                st.error("등록 중 문제가 발생했습니다. 입력 내용을 확인해 주세요.")

    st.divider()
    st.caption("팁: 냉동 보관 식품은 포장지에 표시된 보관 방법과 기한을 확인하세요.")

# -----------------------------
# 재고 관리
# -----------------------------
elif page == "📦 재고 관리":
    st.subheader("우리 집 음식 목록")
    st.write("검색하고, 수정하고, 다 먹은 음식은 정리할 수 있어요.")

    foods = safe_foods()

    if not foods:
        st.info("등록된 음식이 없습니다. 먼저 음식을 등록해 주세요.")
    else:
        search = st.text_input(
            "🔎 음식 검색",
            placeholder="음식 이름 또는 메모 검색",
        )

        col1, col2 = st.columns(2)
        with col1:
            location_filter = st.selectbox(
                "보관 장소",
                ["전체"] + sorted(
                    {f.get("location", "기타") for f in foods}
                ),
            )
        with col2:
            status_filter = st.selectbox(
                "유통기한 상태",
                ["전체", "기한 지남", "오늘까지", "3일 이내", "여유"],
            )

        filtered = []
        for food in foods:
            if search.strip():
                keyword = search.strip().lower()
                searchable = (
                    food.get("name", "") + " " + food.get("memo", "")
                ).lower()
                if keyword not in searchable:
                    continue

            if location_filter != "전체" and food.get("location") != location_filter:
                continue

            remaining = days_left(food["expiry_date"])

            if status_filter == "기한 지남" and remaining >= 0:
                continue
            if status_filter == "오늘까지" and remaining != 0:
                continue
            if status_filter == "3일 이내" and not (1 <= remaining <= 3):
                continue
            if status_filter == "여유" and remaining <= 3:
                continue

            filtered.append(food)

        filtered.sort(key=lambda f: (f["expiry_date"], f["name"].lower()))

        st.caption(f"검색 결과: {len(filtered)}개")

        if filtered:
            table_rows = []
            for food in filtered:
                status, remaining = food_status(food["expiry_date"])
                if remaining < 0:
                    remaining_text = f"{abs(remaining)}일 지남"
                elif remaining == 0:
                    remaining_text = "오늘까지"
                else:
                    remaining_text = f"{remaining}일 남음"

                table_rows.append({
                    "음식": food["name"],
                    "수량": f"{food['quantity']} {food['unit']}",
                    "보관 장소": food["location"],
                    "유통기한": food["expiry_date"].isoformat(),
                    "상태": status,
                    "남은 기간": remaining_text,
                })

            st.dataframe(
                pd.DataFrame(table_rows),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.warning("조건에 맞는 음식이 없습니다.")

        st.divider()
        st.subheader("🛠️ 음식 관리")

        # 검색 결과에 한정하지 않고 전체 재고에서 선택합니다.
        options = {
            f"{f['name']} · {f['expiry_date']} · {f['location']} · {f['id'][:8]}": f["id"]
            for f in foods
        }

        selected_label = st.selectbox(
            "관리할 음식 선택",
            list(options.keys()),
        )
        selected_id = options.get(selected_label)
        selected_food = find_food(selected_id) if selected_id else None

        if selected_food is not None:
            st.markdown(f"**선택한 음식: {selected_food['name']}**")

            action = st.radio(
                "작업 선택",
                ["수정", "먹음 처리", "삭제"],
                horizontal=True,
                key="food_action",
            )

            if action == "수정":
                with st.form("edit_food_form"):
                    edit_name = st.text_input(
                        "음식 이름",
                        value=selected_food["name"],
                    )

                    c1, c2 = st.columns(2)
                    with c1:
                        edit_quantity = st.number_input(
                            "수량",
                            min_value=1,
                            max_value=100000,
                            value=int(selected_food["quantity"]),
                            step=1,
                        )
                    with c2:
                        units = ["개", "팩", "봉지", "통", "병", "g", "kg", "ml", "L", "인분"]
                        current_unit = selected_food.get("unit", "개")
                        unit_index = units.index(current_unit) if current_unit in units else 0
                        edit_unit = st.selectbox(
                            "단위",
                            units,
                            index=unit_index,
                        )

                    locations = ["냉장실", "냉동실", "실온", "기타"]
                    current_location = selected_food.get("location", "기타")
                    location_index = locations.index(current_location) if current_location in locations else 3
                    edit_location = st.selectbox(
                        "보관 장소",
                        locations,
                        index=location_index,
                    )

                    edit_purchase = st.date_input(
                        "구매일",
                        value=selected_food["purchase_date"],
                        max_value=today,
                    )
                    edit_expiry = st.date_input(
                        "유통기한",
                        value=selected_food["expiry_date"],
                    )
                    edit_memo = st.text_area(
                        "메모",
                        value=selected_food.get("memo", ""),
                        max_chars=500,
                    )

                    save_edit = st.form_submit_button(
                        "변경 사항 저장",
                        type="primary",
                        use_container_width=True,
                    )

                if save_edit:
                    if not edit_name.strip():
                        st.error("음식 이름을 입력해 주세요.")
                    elif edit_expiry < edit_purchase:
                        st.error("유통기한은 구매일보다 빠를 수 없습니다.")
                    else:
                        try:
                            selected_food.update({
                                "name": edit_name.strip(),
                                "quantity": int(edit_quantity),
                                "unit": edit_unit,
                                "location": edit_location,
                                "purchase_date": edit_purchase,
                                "expiry_date": edit_expiry,
                                "memo": edit_memo.strip(),
                            })
                            st.success("음식 정보가 수정되었습니다.")
                            st.rerun()
                        except (ValueError, TypeError, AttributeError):
                            st.error("수정 중 문제가 발생했습니다. 다시 시도해 주세요.")

            elif action == "먹음 처리":
                st.info("먹음 처리는 해당 음식을 재고에서 제거합니다.")
                if st.button(
                    "✅ 다 먹었어요",
                    type="primary",
                    use_container_width=True,
                ):
                    try:
                        st.session_state.foods = [
                            f for f in safe_foods()
                            if f.get("id") != selected_id
                        ]
                        st.success("재고에서 제거했습니다. 잘하셨어요!")
                        st.rerun()
                    except (ValueError, TypeError, AttributeError):
                        st.error("처리에 실패했습니다. 다시 시도해 주세요.")

            elif action == "삭제":
                st.warning("삭제한 음식은 현재 세션의 목록에서 제거됩니다.")
                confirm_delete = st.checkbox(
                    "삭제할 음식이 맞는지 확인했습니다.",
                    key="confirm_delete",
                )
                if st.button(
                    "🗑️ 음식 삭제",
                    disabled=not confirm_delete,
                    use_container_width=True,
                ):
                    try:
                        st.session_state.foods = [
                            f for f in safe_foods()
                            if f.get("id") != selected_id
                        ]
                        st.success("음식을 삭제했습니다.")
                        st.rerun()
                    except (ValueError, TypeError, AttributeError):
                        st.error("삭제에 실패했습니다. 다시 시도해 주세요.")

        st.divider()
        st.subheader("💾 재고 백업")

        st.download_button(
            "⬇️ 전체 재고 CSV 다운로드",
            data=export_csv(),
            file_name=f"food_inventory_{today.isoformat()}.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.caption(
            "CSV 파일은 엑셀 등에서 열 수 있습니다. "
            "현재 앱은 CSV를 자동으로 다시 불러오지는 않습니다."
        )

# -----------------------------
# 하단 안내
# -----------------------------
st.divider()
st.caption(
    "🥦 냉장고 구출 작전 · 유통기한 관리를 위한 개인용 도구 "
    "| 음식의 실제 상태와 보관 방법도 함께 확인하세요."
)
