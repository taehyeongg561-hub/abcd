import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("🎮 Streamlit - 테트리스 (키보드 조작 + 자동 낙하)")

st.write("""
**조작 방법**
- ⬅ 왼쪽 화살표: 왼쪽 이동  
- ➡ 오른쪽 화살표: 오른쪽 이동  
- ⬆ 위쪽 화살표: 회전  
- ⬇ 아래 화살표: 빠른 낙하  
- Space: 하드 드롭  
""")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Tetris</title>

    <style>
        body {
            text-align: center;
            background: #111;
            color: white;
            font-family: Arial;
        }
        canvas {
            background: #222;
            margin-top: 20px;
        }
    </style>
</head>

<body>
<canvas id="tetris" width="300" height="600"></canvas>

<script>
const canvas = document.getElementById('tetris');
const context = canvas.getContext('2d');
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
                (arena[y + o.y] &&
                 arena[y + o.y][x + o.x]) !== 0) {
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
    } else if (type === 'I') {
        return [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ];
    } else if (type === 'S') {
        return [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0],
        ];
    } else if (type === 'Z') {
        return [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0],
        ];
    }
}

function drawMatrix(matrix, offset) {
    matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                context.fillStyle = colors[value];
                context.fillRect(x + offset.x,
                                 y + offset.y,
                                 1, 1);
            }
        });
    });
}

function draw() {
    context.fillStyle = "#222";
    context.fillRect(0, 0, canvas.width, canvas.height);
    drawMatrix(arena, {x: 0, y: 0});
    drawMatrix(player.matrix, player.pos);
}

function merge(arena, player) {
    player.matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                arena[y + player.pos.y][x + player.pos.x] = value;
            }
        });
    });
}

function playerDrop() {
    player.pos.y++;
    if (collide(arena, player)) {
        player.pos.y--;
        merge(arena, player);
        playerReset();
        arenaSweep();
    }
    dropCounter = 0;
}

function playerMove(dir) {
    player.pos.x += dir;
    if (collide(arena, player)) {
        player.pos.x -= dir;
    }
}

function playerReset() {
    const pieces = 'ILJOTSZ';
    player.matrix = createPiece(pieces[Math.floor(pieces.length * Math.random())]);
    player.pos.y = 0;
    player.pos.x = (10 / 2 | 0) - (player.matrix[0].length / 2 | 0);

    if (collide(arena, player)) {
        arena.forEach(row => row.fill(0));
    }
}

function rotate(matrix, dir) {
    for (let y = 0; y < matrix.length; ++y) {
        for (let x = 0; x < y; ++x) {
            [ matrix[x][y], matrix[y][x] ] = [ matrix[y][x], matrix[x][y] ];
        }
    }
    if (dir > 0) {
        matrix.forEach(row => row.reverse());
    } else {
        matrix.reverse();
    }
}

function playerRotate(dir) {
    const pos = player.pos.x;
    let offset = 1;
    rotate(player.matrix, dir);
    while (collide(arena, player)) {
        player.pos.x += offset;
        offset = -(offset + (offset > 0 ? 1 : -1));
        if (offset > player.matrix[0].length) {
            rotate(player.matrix, -dir);
            player.pos.x = pos;
            return;
        }
    }
}

let dropCounter = 0;
let dropInterval = 800;

let lastTime = 0;

function update(time = 0) {
    const deltaTime = time - lastTime;
    lastTime = time;

    dropCounter += deltaTime;

    if (dropCounter > dropInterval) {
        playerDrop();
    }

    draw();
    requestAnimationFrame(update);
}

document.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') playerMove(-1);
    else if (
