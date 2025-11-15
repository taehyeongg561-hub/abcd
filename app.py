import streamlit as st
import numpy as np
import random

st.set_page_config(layout="centered")

# ---------------------
# 초기 상태 설정
# ---------------------
if "board" not in st.session_state:
    st.session_state.board = np.zeros((20, 10), dtype=int)
if "shape" not in st.session_state:
    st.session_state.shape = None
if "pos" not in st.session_state:
    st.session_state.pos = [0, 3]  # (row, col)

# 두 가지 간단한 블록(I, O)
SHAPES = {
    "I": np.array([[1, 1, 1, 1]]),
    "O": np.array([[1, 1],
                   [1, 1]])
}

def spawn_new_block():
    shape_name = random.choice(["I", "O"])
    st.session_state.shape = SHAPES[shape_name]
    st.session_state.pos = [0, 3]

def can_move(shape, pos):
    rows, cols = shape.shape
    r, c = pos

    # 보드 밖으로 나가면 안 됨
    if r < 0 or r + rows > 20 or c < 0 or c + cols > 10:
        return False

    # 충돌 검사
    for i in range(rows):
        for j in range(cols):
            if shape[i, j] == 1 and st.session_state.board[r + i, c + j] == 1:
                return False
    return True

def fix_block():
    shape = st.session_state.shape
    r, c = st.session_state.pos
    rows, cols = shape.shape

    for i in range(rows):
        for j in range(cols):
            if shape[i, j] == 1:
                st.session_state.board[r + i, c + j] = 1

def move_block(dr, dc):
    shape = st.session_state.shape
    r, c = st.session_state.pos
    new_pos = [r + dr, c + dc]

    if can_move(shape, new_pos):
        st.session_state.pos = new_pos
        return True
    return False

def rotate_block():
    new_shape = np.rot90(st.session_state.shape)
    if can_move(new_shape, st.session_state.pos):
        st.session_state.shape = new_shape

def step():
    if not move_block(1, 0):  # 아래로 이동
        fix_block()
        spawn_new_block()

# ---------------------
# UI 구성
# ---------------------
st.title("🎮 Streamlit 초간단 테트리스")
st.write("버튼으로 조작하세요!")

# 첫 블록 생성
if st.session_state.shape is None:
    spawn_new_block()

col1, col2, col3, col4 = st.columns(4)
if col1.button("⬅ 왼쪽"):
    move_block(0, -1)
if col2.button("➡ 오른쪽"):
    move_block(0, 1)
if col3.button("🔄 회전"):
    rotate_block()
if col4.button("⬇ 아래"):
    step()

# 자동 낙하 버튼
if st.button("한 단계 진행"):
    step()

# ---------------------
# 보드 + 현재 블록 시각화
# ---------------------
temp_board = st.session_state.board.copy()

shape = st.session_state.shape
r, c = st.session_state.pos
rows, cols = shape.shape

for i in range(rows):
    for j in range(cols):
        if shape[i, j] == 1:
            temp_board[r + i, c + j] = 2  # falling block 표시

# 화면 표시 (emoji로 표시)
display = ""
for row in temp_board:
    for cell in row:
        if cell == 0:
            display += "⬛"
        elif cell == 1:
            display += "🟩"
        else:
            display += "🟦"
    display += "\n"

st.markdown(f"<pre style='font-size:20px'>{display}</pre>", unsafe_allow_html=True)
