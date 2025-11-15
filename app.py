import streamlit as st

# Streamlit 페이지 설정
st.set_page_config(page_title="🎮 테트리스 게임", layout="wide")

# 게임 제목과 설명
st.title("🎮 테트리스 게임 (키보드 조작 가능)")
st.write("""
테트리스는 키보드로 조작할 수 있으며, 자동으로 블록이 떨어집니다.

**조작 방법**
- ⬅ : 왼쪽 이동  
- ➡ : 오른쪽 이동  
- ⬆ : 회전  
- ⬇ : 빠른 낙하  
- Space : 하드 드롭 (빠르게 끝까지 떨어짐)  
""")

# HTML, JS 코드를 포함한 게임
tetris_html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tetris Game</title>
    <style>
        body {
            background-color: #111;
            text-align: center;
            color: white;
            font-family: Arial, sans-serif;
        }
        canvas {
            background-color: #222;
            margin-top: 30px;
        }
    </style>
</head>
<body>
<canvas id="tetris" width="300" height="600"></canvas>

<script>
// Tetris 게임 로직
const canvas = document.getElementById("tetris");
const context = canvas.getContext("2d");
context.scale(30, 30);

function arenaSweep() {
    outer: for (let y = arena.length - 1; y > 0; --y) {
        for (let x = 0; x < arena[y].length; ++x) {
            if (arena[y][x] === 0) {
                continue outer;
            }
        }
        const row = arena.splice(y, 1)[0].fill(0);
        arena.unshift(row);
        ++y;
    }
}

function collide(arena, player) {
    const m = player.matrix;
    const o = player.pos;
    for (let y = 0; y < m.length; ++y) {
        for (let x = 0; x < m[y].length; ++x) {
            if (m[y][x] !== 0 &&
                (arena[y + o.y] && arena[y + o.y][x + o.x]) !== 0) {
                return true;
            }
        }
    }
    return false;
}

function createMatrix(w, h) {
    const matrix = [];
    while (h--) matrix.push(new Array(w).fill(0));
    return matrix;
}

function createPiece(type) {
    if (type === 'T') {
        return [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0],
        ];
    } else if (type === 'O') {
        return [
            [1, 1],
            [1, 1],
        ];
    } else if (type === 'L') {
        return [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0],
        ];
    } else if (type === 'J') {
        return [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0],
        ];
    } else if (typ
