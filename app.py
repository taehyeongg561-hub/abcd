import pygame
import numpy as np
import streamlit as st
from io import BytesIO

# 게임 화면 크기
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# 테트리스 블록 모양 정의 (I, O, T, S, Z, L, J)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]

# 게임 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE]

# 테트리스 보드 크기 (20 x 10)
board = np.zeros((20, 10), dtype=int)
current_shape = None
current_pos = None
game_over = False

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Streamlit Tetris")

def draw_board():
    """테트리스 보드 그리기"""
    for row in range(20):
        for col in range(10):
            color = WHITE if board[row, col] == 0 else SHAPE_COLORS[board[row, col] - 1]
            pygame.draw.rect(screen, color, (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, BLACK, (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_shape(shape, pos):
    """현재 떨어지는 블록 그리기"""
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                pygame.draw.rect(screen, GREEN, ((pos[1] + col) * BLOCK_SIZE, (pos[0] + row) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def check_collision(shape, pos):
    """블록이 충돌하는지 확인"""
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                x = pos[1] + col
                y = pos[0] + row
                if x < 0 or x >= 10 or y >= 20 or (y >= 0 and board[y, x] != 0):
                    return True
    return False

def place_shape(shape, pos):
    """블록을 보드에 배치"""
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                board[pos[0] + row, pos[1] + col] = 1

def rotate_shape(shape):
    """블록 회전"""
    return [list(row) for row in zip(*shape[::-1])]

def clear_lines():
    """완전한 라인 제거"""
    global board
    new_board = [row for row in board if any(val == 0 for val in row)]
    lines_cleared = 20 - len(new_board)
    new_board = np.vstack([np.zeros((lines_cleared, 10), dtype=int), new_board])
    board = new_board

def capture_screen():
    """pygame 화면을 캡처하여 이미지로 변환"""
    image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    image.blit(screen, (0, 0))
    img_bytes = BytesIO()
    pygame.image.save(image, img_bytes)
    img_bytes.seek(0)
    return img_bytes

def game_loop():
    """게임 루프"""
    global current_shape, current_pos, game_over
    current_shape = SHAPES[np.random.randint(0, len(SHAPES))]
    current_pos = [0, 4]  # 블록 시작 위치
    clock = pygame.time.Clock()

    while not game_over:
        screen.fill(BLACK)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_pos = [current_pos[0], current_pos[1] - 1]
                    if not check_collision(current_shape, new_pos):
                        current_pos = new_pos
                elif event.key == pygame.K_RIGHT:
                    new_pos = [current_pos[0], current_pos[1] + 1]
                    if not check_collision(current_shape, new_pos):
                        current_pos = new_pos
                elif event.key == pygame.K_DOWN:
                    new_pos = [current_pos[0] + 1, current_pos[1]]
                    if not check_collision(current_shape, new_pos):
                        current_pos = new_pos
                elif event.key == pygame.K_UP:
                    new_shape = rotate_shape(current_shape)
                    if not check_collision(new_shape, current_pos):
                        current_shape = new_shape

        # 블록이 바닥에 닿았으면
        new_pos = [current_pos[0] + 1, current_pos[1]]
        if check_collision(current_shape, new_pos):
            place_shape(current_shape, current_pos)
            clear_lines()
            if current_pos[0] <= 0:
                game_over = True
            current_shape = SHAPES[np.random.randint(0, len(SHAPES))]
            current_pos = [0, 4]
        else:
            current_pos = new_pos

        # 게임 보드와 블록 그리기
        draw_board()
        draw_shape(current_shape, current_pos)

        # 화면 캡처
        img_bytes = capture_screen()

        # Streamlit에서 이미지 표시
        st.image(img_bytes, use_column_width=True)

        # 게임 속도 조절
        clock.tick(10)

# Streamlit UI 설정
st.title("Streamlit으로 만든 테트리스")
st.write("""
이 게임은 테트리스입니다. 
다음 키로 조작할 수 있습니다:
- **왼쪽 화살표**: 블록 왼쪽으로 이동
- **오른쪽 화살표**: 블록 오른쪽으로 이동
- **위쪽 화살표**: 블록 회전
- **아래쪽 화살표**: 블록 빠르게 내려가기
""")

# 게임 시작 버튼
if st.button("게임 시작"):
    st.text("게임이 시작되었습니다!")
    game_loop()
