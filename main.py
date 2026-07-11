import streamlit as st

st.set_page_config(
    page_title="시험 계획표",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

SUBJECTS = ["국어", "수학", "영어", "과학", "사회"]


def init_state() -> None:
    defaults = {
        "mock_scores": [],
        "wrong_questions": [],
        "study_plan": [],
        "study_materials": {},
    }

    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default.copy()

    if not isinstance(st.session_state.mock_scores, list):
        st.session_state.mock_scores = []
    if not isinstance(st.session_state.wrong_questions, list):
        st.session_state.wrong_questions = []
    if not isinstance(st.session_state.study_plan, list):
        st.session_state.study_plan = []
    if not isinstance(st.session_state.study_materials, dict):
        st.session_state.study_materials = {}


def unresolved_count(subject: str) -> int:
    return sum(
        1
        for item in st.session_state.wrong_questions
        if item.get("과목") == subject and not bool(item.get("해결", False))
    )


def expected_score(subject: str) -> float:
    records = sorted(
        st.session_state.mock_scores,
        key=lambda item: str(item.get("날짜", "")),
    )

    scores = [
        float(item[subject])
        for item in records
        if isinstance(item.get(subject), (int, float))
    ]

    recent = scores[-3:]
    average = sum(recent) / len(recent) if recent else 70.0
    trend = recent[-1] - recent[-2] if len(recent) >= 2 else 0.0
    penalty = min(12.0, unresolved_count(subject) * 0.8)

    return max(0.0, min(100.0, average + trend * 0.35 - penalty))


init_state()

st.title("📚 나만의 시험 계획표")
st.caption(
    "왼쪽 사이드바에서 날짜별 계획표, 모의고사 성적, "
    "오답 기록, 현재 예상점수 페이지를 각각 열 수 있습니다."
)

unsolved_total = sum(
    1
    for item in st.session_state.wrong_questions
    if not bool(item.get("해결", False))
)
predictions = [expected_score(subject) for subject in SUBJECTS]

col1, col2, col3, col4 = st.columns(4)
col1.metric("모의고사 기록", f"{len(st.session_state.mock_scores)}회")
col2.metric("전체 오답", f"{len(st.session_state.wrong_questions)}문제")
col3.metric("미해결 오답", f"{unsolved_total}문제")
col4.metric("평균 예상점수", f"{sum(predictions) / len(predictions):.1f}점")

st.divider()
st.subheader("페이지 바로가기")

col1, col2 = st.columns(2)

with col1:
    st.page_link(
        "pages/1_날짜별_계획표.py",
        label="날짜별 계획표",
        icon="🗓️",
        use_container_width=True,
    )
    st.page_link(
        "pages/3_오답_기록.py",
        label="오답 기록",
        icon="📝",
        use_container_width=True,
    )

with col2:
    st.page_link(
        "pages/2_모의고사_성적.py",
        label="모의고사 성적",
        icon="📊",
        use_container_width=True,
    )
    st.page_link(
        "pages/4_현재_예상점수.py",
        label="현재 예상점수",
        icon="🎯",
        use_container_width=True,
    )

st.info("각 페이지의 코드는 pages 폴더 안의 서로 다른 Python 파일에 들어 있습니다.")
