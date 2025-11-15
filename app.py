import streamlit as st

st.set_page_config(page_title="Tetris", layout="wide")
st.title("🎮 Streamlit Tetris (Score & Level)")

st.write("""
**조작법**
- ⬅ : 왼쪽 이동  
- ➡ : 오른쪽 이동  
- ⬆ : 회전  
- ⬇ : 빠른 낙하  
- Space : 하드 드롭  
""")

tetris_html = r'''
<div style="display:flex; flex-direction:column; align-items:center;">
    <h3>Score: <span id="score">0</span> | Level: <span id="level">1</span></h3>
    <canvas id="tetris" width="240" height="400" style="border:1px solid #333;"></canvas>
</div>

<script>
const canvas = document.getElementById("tetris");
const context = canvas.getContext("2d");
context.scale(20,20);

let score = 0;
let level = 1;
let dropInterval = 1000;
let dropCounter = 0;
let lastTime = 0;

const scoreElem = document.getElementById("score");
const levelElem = document.getElementById("level");

function arenaSweep() {
    let rowCount = 0;
    outer: for (let y = arena.length - 1; y >= 0; --y) {
        for (let x = 0; x < arena[y].length; ++x) {
            if (arena[y][x] === 0) continue outer;
        }
        arena.splice(y, 1);
        arena.unshift(Array(12).fill(0));
        rowCount++;
        y++;
    }
    if(rowCount > 0){
        score += rowCount * 10;
        scoreElem.innerText = score;
        if(score >= level*50){
            level++;
            levelElem.innerText = level;
            dropInterval *= 0.9; 
        }
    }
}

function collide(arena, player) {
    const [m, o] = [player.matrix, player.pos];
    for (let y = 0; y < m.length; ++y)
        for (let x = 0; x < m[y].length; ++x)
            if (m[y][x] && (arena[y + o.y] && arena[y + o.y][x + o.x]) !== 0)
                return true;
    return false;
}

function createMatrix(w,h){
    const matrix=[];
    while(h--) matrix.push(new Array(w).fill(0));
    return matrix;
}

function createPiece(type){
    if(type==="T") return [[0,1,0],[1,1,1],[0,0,0]];
    if(type==="O") return [[1,1],[1,1]];
    if(type==="L") return [[0,0,1],[1,1,1],[0,0,0]]
