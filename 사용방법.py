
import streamlit as st
from google import genai

# ---------------------------
# 기본 설정
# ---------------------------
st.set_page_config(
    page_title="한상플랜 | 음식 양 계산 도우미",
    page_icon="🍱",
    layout="wide",
)

MODEL_NAME = "gemini-2.5-flash-lite"

FOODS = {
    "김치볶음밥": {
        "category": "밥 요리",
        "ingredients": "밥, 김치, 식용유, 대파. 취향에 따라 달걀, 햄 등을 추가해요.",
        "features": "김치의 새콤하고 매콤한 맛이 밥과 어우러지는 볶음 요리예요.",
        "cooking": "김치와 채소를 볶은 뒤 밥을 넣고 골고루 볶아요.",
        "amount": 300,
        "unit": "g",
    },
    "불고기": {
        "category": "고기 요리",
        "ingredients": "소고기, 간장, 마늘, 설탕 또는 배, 양파, 대파.",
        "features": "간장 양념을 사용해 달콤하고 짭짤하게 만드는 한국 요리예요.",
        "cooking": "고기를 양념에 재운 뒤 팬이나 불판에서 익혀요.",
        "amount": 200,
        "unit": "g",
    },
    "김치찌개": {
        "category": "국물 요리",
        "ingredients": "김치, 물 또는 육수, 두부, 대파. 돼지고기나 참치를 추가할 수 있어요.",
        "features": "김치의 깊은 맛과 매콤한 국물이 특징이에요.",
        "cooking": "김치와 재료를 넣고 충분히 끓여 맛을 우려내요.",
        "amount": 350,
        "unit": "ml",
    },
    "파스타": {
        "category": "면 요리",
        "ingredients": "파스타 면, 소금, 소스. 토마토, 크림, 마늘 등은 종류에 따라 달라져요.",
        "features": "소스와 면의 조합에 따라 맛과 식감이 달라지는 요리예요.",
        "cooking": "면을 삶은 뒤 준비한 소스와 섞어요.",
        "amount": 100,
        "unit": "g",
    },
    "샐러드": {
        "category": "채소 요리",
        "ingredients": "양상추, 토마토, 오이 등 채소와 드레싱. 원하는 재료를 추가할 수 있어요.",
        "features": "여러 채소의 식감과 드레싱의 맛이 어우러져요.",
        "cooking": "재료를 깨끗이 씻고 물기를 제거한 뒤 먹기 좋게 담아요.",
        "amount": 150,
        "unit": "g",
    },
    "떡볶이": {
        "category": "간식·분식",
        "ingredients": "떡, 고추장 또는 양념장, 물, 설탕, 대파. 어묵을 넣기도 해요.",
        "features": "쫄깃한 떡과 매콤달콤한 양념이 특징이에요.",
        "cooking": "양념을 푼 국물에 떡과 재료를 넣고 익혀요.",
        "amount": 250,
        "unit": "g",
    },
}

FOOD_ALIASES = {
    "볶음밥": "김치볶음밥",
    "김치 볶음밥": "김치볶음밥",
    "찌개": "김치찌개",
    "파스타면": "파스타",
}

PAGE_HELP = {
    "홈": "원하는 페이지를 선택하세요. 음식 이름을 먼저 알아본 뒤 양 계산을 하면 더 편리해요.",
    "양 계산": "음식과 인원수를 입력하고 1인당 양과 여유분을 설정한 뒤 계산 버튼을 누르세요. 결과는 대략적인 준비량이에요.",
    "음식 정보": "음식 이름을 입력하고 조회하세요. 기본 음식은 내장 자료로 확인할 수 있고, 다른 음식은 Gemini API 키가 있으면 AI가 설명해 줘요.",
    "음식 상담": "음식 이름, 재료, 조리 특징, 인원수별 준비량 등을 자연스럽게 질문하세요. 답변은 참고용이며 실제 재료와 조리법에 따라 달라질 수 있어요.",
}


def get_api_key():
    """Streamlit Secrets에서 API 키를 안전하게 읽어요."""
    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return ""


def ask_gemini(prompt, history=None):
    """Gemini 요청. 실패하면 오류를 호출한 화면에서 처리해요."""
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY가 설정되지 않았어요. "
            "배포 설정의 Secrets에 API 키를 추가해 주세요."
        )

    client = genai.Client(api_key=api_key)

    try:
        parts = [
            "너는 한국어로 답하는 친절한 음식 및 식사 준비 도우미야. "
            "음식의 특징, 주요 재료, 조리 방식, 여러 명의 준비량을 설명해. "
            "준비량은 추정치라고 알리고, 사용자가 지정한 음식에 맞춰 답해. "
            "재료 알레르기는 반드시 확인하도록 안내해. "
            "모르는 사실은 확실하다고 단정하지 마.",
            "",
        ]

        if history:
            for item in history[-10:]:
                role = "사용자" if item["role"] == "user" else "도우미"
                parts.append(f"{role}: {item['content']}")

        parts.append(f"사용자의 현재 요청: {prompt}")

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents="\n".join(parts),
        )

        answer = getattr(response, "text", None)
        if not answer or not answer.strip():
            raise RuntimeError("AI가 빈 답변을 반환했어요. 다시 시도해 주세요.")

        return answer.strip()
    finally:
        client.close()


def show_help(page_name):
    key = f"help_{page_name}"
    if key not in st.session_state:
        st.session_state[key] = False

    label = "사용법 숨기기" if st.session_state[key] else "사용법 보기"
    if st.button(label, key=f"help_button_{page_name}"):
        st.session_state[key] = not st.session_state[key]

    if st.session_state[key]:
        st.info(PAGE_HELP[page_name])


def go_to(page_name):
    st.session_state["page"] = page_name


# ---------------------------
# 세션 상태 초기화
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "홈"

if "last_food" not in st.session_state:
    st.session_state.last_food = "김치볶음밥"

if "calc_result" not in st.session_state:
    st.session_state.calc_result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "food_info_result" not in st.session_state:
    st.session_state.food_info_result = None


# ---------------------------
# 사이드바 내비게이션
# ---------------------------
st.sidebar.title("🍱 한상플랜")
st.sidebar.caption("음식 정보부터 준비량까지 한곳에서")

pages = ["홈", "양 계산", "음식 정보", "음식 상담"]
if st.session_state.page not in pages:
    st.session_state.page = "홈"

st.sidebar.radio(
    "페이지 이동",
    pages,
    key="page",
)

st.sidebar.divider()
st.sidebar.write("**빠른 이동**")

for target in pages:
    if target != st.session_state.page:
        if st.sidebar.button(
            f"{target} 열기",
            key=f"quick_{target}",
            use_container_width=True,
        ):
            go_to(target)
            st.rerun()

st.sidebar.caption("AI 기능은 Gemini API 키가 필요해요.")


# ---------------------------
# 홈
# ---------------------------
if st.session_state.page == "홈":
    st.title("🍱 한상플랜")
    st.subheader("음식의 양, 이제 조금 더 쉽게 준비해요.")
    st.write(
        "무엇을 먹을지 정하고, 재료를 확인하고, "
        "먹는 사람 수에 맞는 준비량을 계산해 보세요."
    )

    show_help("홈")

    st.markdown("### 어디서 시작할까요?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🧮 양 계산")
        st.write("몇 명이 먹는지에 맞춰 필요한 양을 계산해요.")
        if st.button("양 계산 시작", use_container_width=True):
            go_to("양 계산")
            st.rerun()

    with col2:
        st.markdown("#### 🥘 음식 정보")
        st.write("음식의 특징과 주요 재료를 알아봐요.")
        if st.button("음식 찾아보기", use_container_width=True):
            go_to("음식 정보")
            st.rerun()

    with col3:
        st.markdown("#### 💬 음식 상담")
        st.write("궁금한 음식에 대해 AI에게 질문해요.")
        if st.button("상담 시작", use_container_width=True):
            go_to("음식 상담")
            st.rerun()

    st.divider()
    st.markdown("### 최근 선택한 음식")
    st.write(f"🍽️ {st.session_state.last_food}")

    if st.button("이 음식의 정보 보기"):
        go_to("음식 정보")
        st.rerun()


# ---------------------------
# 양 계산
# ---------------------------
elif st.session_state.page == "양 계산":
    st.title("🧮 음식 양 계산")
    st.write("인원수에 맞는 음식 준비량을 계산해 보세요.")
    show_help("양 계산")

    food_options = list(FOODS.keys()) + ["직접 입력"]
    default_food = st.session_state.last_food
    default_index = (
        food_options.index(default_food)
        if default_food in food_options else 0
    )

    with st.form("amount_form"):
        selected_food = st.selectbox(
            "음식 선택",
            food_options,
            index=default_index,
        )

        custom_food = ""
        if selected_food == "직접 입력":
            custom_food = st.text_input(
                "음식 이름",
                placeholder="예: 잡채",
            )

        people = st.number_input(
            "먹는 사람 수",
            min_value=1,
            max_value=500,
            value=4,
            step=1,
        )

        if selected_food == "직접 입력":
            unit = st.selectbox("단위", ["g", "kg", "ml", "L", "개"])
            default_per_person = 200.0
        else:
            food_data = FOODS[selected_food]
            unit = food_data["unit"]
            default_per_person = float(food_data["amount"])
            st.caption(
                f"기본 예시: 1인당 {default_per_person:g} {unit}"
            )

        per_person = st.number_input(
            f"1인당 준비할 양 ({unit})",
            min_value=0.1,
            max_value=100000.0,
            value=default_per_person,
            step=10.0 if unit in ["g", "ml"] else 1.0,
        )

        extra_percent = st.slider(
            "여유분",
            min_value=0,
            max_value=50,
            value=10,
            step=5,
        )

        submitted = st.form_submit_button(
            "필요한 양 계산하기",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        food_name = (
            custom_food.strip()
            if selected_food == "직접 입력"
            else selected_food
        )

        if not food_name:
            st.error("음식 이름을 입력해 주세요.")
        else:
            base = float(people) * float(per_person)
            extra = base * extra_percent / 100
            total = base + extra

            st.session_state.last_food = food_name
            st.session_state.calc_result = {
                "food": food_name,
                "people": int(people),
                "per_person": float(per_person),
                "unit": unit,
                "base": base,
                "extra": extra,
                "total": total,
                "extra_percent": extra_percent,
            }

    result = st.session_state.calc_result
    if result:
        st.divider()
        st.subheader(f"📋 {result['food']} 준비 결과")

        def fmt(value):
            return f"{value:,.1f} {result['unit']}"

        c1, c2, c3 = st.columns(3)
        c1.metric("인원수", f"{result['people']}명")
        c2.metric("기본 필요량", fmt(result["base"]))
        c3.metric("여유분 포함", fmt(result["total"]))

        st.write(f"- 1인당 준비량: {fmt(result['per_person'])}")
        st.write(f"- 추가 여유분: {fmt(result['extra'])}")
        st.success(f"총 약 {fmt(result['total'])}을 준비하면 돼요.")

        st.caption(
            "음식의 무게와 부피는 서로 다르며, "
            "조리 전후에도 양이 달라질 수 있어요."
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button("음식 특징과 재료 보기", use_container_width=True):
                go_to("음식 정보")
                st.rerun()
        with c2:
            if st.button("이 음식 상담하기", use_container_width=True):
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": (
                        f"{result['food']}를 {result['people']}명이 먹을 거야. "
                        f"계산한 총 준비량은 약 {result['total']:.1f} "
                        f"{result['unit']}야. 재료와 준비할 점을 알려 줘."
                    ),
                })
                go_to("음식 상담")
                st.rerun()


# ---------------------------
# 음식 정보
# ---------------------------
elif st.session_state.page == "음식 정보":
    st.title("🥘 음식 정보 탐색")
    st.write("어떤 음식이 궁금한가요? 음식 이름을 입력해 주세요.")
    show_help("음식 정보")

    with st.form("food_info_form"):
        food_query = st.text_input(
            "먹고 싶은 음식",
            value=st.session_state.last_food,
            placeholder="예: 잡채, 김치찌개, 파스타",
        )
        info_submit = st.form_submit_button(
            "음식 정보 알아보기",
            type="primary",
            use_container_width=True,
        )

    if info_submit:
        name = food_query.strip()
        if not name:
            st.warning("음식 이름을 먼저 입력해 주세요.")
        else:
            st.session_state.last_food = name
            normalized = FOOD_ALIASES.get(name, name)
            local_data = FOODS.get(normalized)

            if local_data:
                st.session_state.food_info_result = {
                    "name": normalized,
                    "source": "내장 음식 자료",
                    "text": (
                        f"### 음식 분류\n{local_data['category']}\n\n"
                        f"### 음식의 특징\n{local_data['features']}\n\n"
                        f"### 주요 재료\n{local_data['ingredients']}\n\n"
                        f"### 조리 방식\n{local_data['cooking']}\n\n"
                        f"### 준비량 참고\n"
                        f"1인당 약 {local_data['amount']} "
                        f"{local_data['unit']}를 예시로 사용할 수 있어요. "
                        "식사 구성과 식욕에 따라 조절하세요."
                    ),
                }
            else:
                try:
                    with st.spinner("음식 정보를 정리하고 있어요..."):
                        answer = ask_gemini(
                            f"음식 이름: {name}\n"
                            "이 음식의 특징, 주요 재료, 조리 방식, "
                            "여러 명을 위해 준비할 때 고려할 점을 "
                            "한국어로 소제목을 사용해 설명해 줘. "
                            "1인당 준비량은 대략적인 범위로 설명하고 "
                            "확실하지 않은 정보는 단정하지 마."
                        )
                    st.session_state.food_info_result = {
                        "name": name,
                        "source": "Gemini AI",
                        "text": answer,
                    }
                except ValueError as exc:
                    st.session_state.food_info_result = {
                        "name": name,
                        "source": "AI 연결 필요",
                        "text": (
                            "이 음식은 기본 자료에 없어요. "
                            "다른 음식은 Gemini API 키를 설정하면 "
                            "AI로 정보를 알아볼 수 있어요.\n\n"
                            f"설정 안내: {exc}"
                        ),
                    }
                except Exception:
                    st.session_state.food_info_result = {
                        "name": name,
                        "source": "요청 실패",
                        "text": (
                            "음식 정보를 불러오지 못했어요. "
                            "인터넷 연결과 API 키, 모델 사용 가능 여부를 "
                            "확인한 뒤 다시 시도해 주세요."
                        ),
                    }

    info = st.session_state.food_info_result
    if info:
        st.divider()
        st.subheader(f"🍽️ {info['name']}")
        st.caption(f"정보 출처: {info['source']}")
        st.markdown(info["text"])

        c1, c2 = st.columns(2)
        with c1:
            if st.button("이 음식의 양 계산하기", use_container_width=True):
                st.session_state.last_food = info["name"]
                go_to("양 계산")
                st.rerun()
        with c2:
            if st.button("음식에 대해 질문하기", use_container_width=True):
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": (
                        f"{info['name']}의 특징과 재료에 대해 더 알려 줘."
                    ),
                })
                go_to("음식 상담")
                st.rerun()


# ---------------------------
# AI 음식 상담
# ---------------------------
elif st.session_state.page == "음식 상담":
    st.title("💬 음식 상담실")
    st.write(
        "음식의 재료, 특징, 조리법, 여러 명을 위한 준비량을 질문해 보세요."
    )
    show_help("음식 상담")

    if not get_api_key():
        st.warning(
            "AI 대화에는 GEMINI_API_KEY가 필요해요. "
            "기본 음식 정보와 양 계산은 계속 사용할 수 있어요."
        )

    with st.expander("질문 예시 보기"):
        st.markdown(
            "- 김치볶음밥의 주요 재료는 뭐야?\n"
            "- 친구 8명이 떡볶이를 먹으려면 얼마나 준비해야 해?\n"
            "- 파스타 종류에 따라 재료가 어떻게 달라져?\n"
            "- 음식을 준비할 때 미리 확인할 점은 뭐야?"
        )

    if st.button("대화 기록 지우기"):
        st.session_state.chat_history = []
        st.rerun()

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input(
        "궁금한 음식이나 필요한 양을 입력하세요..."
    )

    if prompt:
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt,
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                with st.spinner("답변을 준비하고 있어요..."):
                    answer = ask_gemini(
                        prompt,
                        history=st.session_state.chat_history[:-1],
                    )
                st.markdown(answer)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer,
                })
            except ValueError as exc:
                st.error(str(exc))
            except Exception:
                st.error(
                    "AI 응답을 가져오지 못했어요. "
                    "API 키, 인터넷 연결, 사용량 제한 및 모델 설정을 "
                    "확인한 뒤 다시 질문해 주세요."
                )

st.divider()
st.caption(
    "한상플랜은 음식 준비를 돕는 참고용 앱이에요. "
    "음식 알레르기와 실제 조리 환경을 반드시 확인하세요."
)
