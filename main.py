import streamlit as st

st.set_page_config(
    page_title="시험 계획표",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

SUBJECTS = ["국어", "수학", "영어", "과학", "사회"]


def init_state() -> None:
    """여러 페이지에서 공통으로 사용할 세션 데이터를 준비합니다."""
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
st.caption("각 기능은 pages 폴더 안의 별도 Python 파일로 분리되어 있습니다.")

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
st.subheader("페이지 구성")

left, right = st.columns(2)

with left:
    with st.container(border=True):
        st.markdown("### 🗓️ 날짜별 계획표")
        st.write("시험일까지 날짜별 학습 계획을 만듭니다.")
        st.write("교과서·자습서·문제집·프린트를 구분하여 배정합니다.")

    with st.container(border=True):
        st.markdown("### 📝 오답 기록")
        st.write("지금까지 틀린 문제와 해결 여부를 기록합니다.")

with right:
    with st.container(border=True):
        st.markdown("### 📊 모의고사 성적")
        st.write("시험별 과목 점수를 저장하고 확인합니다.")

    with st.container(border=True):
        st.markdown("### 🎯 현재 예상점수")
        st.write("최근 성적과 미해결 오답을 반영해 예상점수를 계산합니다.")

st.info(
    "왼쪽 사이드바에 표시되는 페이지 이름을 눌러 이동하세요. "
    "홈 화면에서는 페이지 파일 경로를 직접 호출하지 않으므로 "
    "StreamlitPageNotFoundError가 발생하지 않습니다."
)
