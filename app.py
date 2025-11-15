import pygame
import streamlit as st
import numpy as np
import time

# pygame 초기화
pygame.init()

# 게임 화면 크기
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 게임 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

# 블록 크기
BLOCK_SIZE = 30

# 테트리스 블록 모양
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]

# 게임 변수
game_over = False
board = np.zeros((20, 10), dtype=int)  # 20행 10열 보드
current_shape = None
current_pos = None

# 블록 색상
SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE]

def draw_board():
    """게임 보드 그리기"""
    for row in range(20):
        for col in range(10):
            color = WHITE if board[row, col] == 0 else SHAPE_COLORS[board[row, col] - 1]
            pygame.draw.rect(screen, color, (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, BLACK, (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_shape(shape, pos):
    """현재 모양 그리기"""
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                pygame.draw.rect(screen, GREEN, ((pos[1] + col) * BLOCK_SIZE, (pos[0] + row) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def check_collision(shape, pos):
    """충돌 확인"""
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                x = pos[1] + col
                y = pos[0] + row
                if x < 0 or x >= 10 or y >= 20 or (y >= 0 and board[y, x] != 0):
                    return True
    return False

def place_shape(shape, pos):
    """모양을 보드에 배치"""
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                board[pos[0] + row, pos[1] + col] = 1

def rotate_shape(shape):
    """모양 회전"""
    return [list(row) for row in zip(*shape[::-1])]

def clear_lines():
    """라인이 꽉 찼을 때 제거"""
    global board
    new_board = [row for row in board if any(val == 0 for val in row)]
    lines_cleared = 20 - len(new_board)
    new_board = np.vstack([np.zeros((lines_cleared, 10), dtype=int), new_board])
    board = new_board

def game_loop():
    """게임 루프"""
    global current_shape, current_pos, game_over
    current_shape = SHAPES[np.random.randint(0, len(SHAPES))]
    current_pos = [0, 4]  # 시작 위치
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

        # 아래로 떨어뜨리기
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

        # 게임 보드와 모양 그리기
        draw_board()
        draw_shape(current_shape, current_pos)

        # 게임 화면 업데이트
        pygame.display.flip()
        clock.tick(10)  # 게임 속도

# Streamlit UI 설정
st.title("Streamlit으로 만든 테트리스")
st.write("""
이 게임은 테트리스입니다. 
다음 키로 조작할 수 있습니다:
- **왼쪽 화살표**: 블록 왼쪽으로 이동
- **오른쪽 화살표**: 블록 오른쪽으로 이동
- **위쪽 화살표**: 블록 회전
- **아래쪽 화살표**: 블록 빠르게 내려가게 하기
""")

# 게임 시작 버튼
if st.button("게임 시작"):
    st.text("게임이 시작되었습니다!")
    game_loop()

pygame.quit()
