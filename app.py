import streamlit as st

st.set_page_config(page_title="Tetris", layout="wide")
st.title("🎮 Streamlit Tetris")

st.write("""
**조작법**
- ⬅ : 왼쪽 이동  
- ➡ : 오른쪽 이동  
- ⬆ : 회전  
- ⬇ : 빠른 낙하  
- Space : 하드 드롭  
""")

tetris_html = r'''
<canvas id='tetris' width='240' height='400'></canvas>
<script>
const canvas = document.getElementById('tetris');
const context = canvas.getContext('2d');
context.scale(20,20);

// arena sweep
function arenaSweep() {
    outer: for (let y = arena.length - 1; y >= 0; --y) {
        for (let x = 0; x < arena[y].length; ++x) {
            if (arena[y][x] === 0) continue outer;
        }
        arena.splice(y, 1);
        arena.unshift(Array(12).fill(0));
    }
}

// collision
function collide(arena, player) {
    const [m, o] = [player.matrix, player.pos];
    for (let y = 0; y < m.length; ++y)
        for (let x = 0; x < m[y].length; ++x)
            if (m[y][x] && (arena[y + o.y] && arena[y + o.y][x + o.x]) !== 0)
                return true;
    return false;
}

// create matrix
function createMatrix(w,h){
    const matrix=[];
    while(h--) matrix.push(new Array(w).fill(0));
    return matrix;
}

// create pieces
function createPiece(type){
    if(type==='T') return [[0,1,0],[1,1,1],[0,0,0]];
    if(type==='O') return [[1,1],[1,1]];
    if(type==='L') return [[0,0,1],[1,1,1],[0,0,0]];
    if(type==='J') return [[1,0,0],[1,1,1],[0,0,0]];
    if(type==='I') return [[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]];
    if(type==='S') return [[0,1,1],[1,1,0],[0,0,0]];
    if(type==='Z') return [[1,1,0],[0,1,1],[0,0,0]];
}

// draw functions
function drawMatrix(matrix, offset){
    matrix.forEach((row,y)=>row.forEach((value,x)=>{
        if(value!==0){
            context.fillStyle=colors[value];
            context.fillRect(x+o
