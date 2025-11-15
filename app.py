import streamlit as st
import streamlit.components.v1 as components

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

# HTML + JS를 Python 문자열에 안전하게 넣기 위해 """ 대신 ''' 사용
tetris_html = '''
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

const colors=[null,"#FF0","#0FF","#F0F","#0F0","#F00","#00F","#FFA500"];

function createMatrix(w,h){
    const matrix=[];
    while(h--) matrix.push(new Array(w).fill(0));
    return matrix;
}

function createPiece(type){
    if(type==="T") return [[0,1,0],[1,1,1],[0,0,0]];
    if(type==="O") return [[1,1],[1,1]];
    if(type==="L") return [[0,0,1],[1,1,1],[0,0,0]];
    if(type==="J") return [[1,0,0],[1,1,1],[0,0,0]];
    if(type==="I") return [[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]];
    if(type==="S") return [[0,]()]()
