import streamlit as st

st.set_page_config(layout="wide")

st.title("🎮 Streamlit 테트리스 (키보드 조작 가능)")

st.write("""
이 테트리스는 키보드로 조작할 수 있고 자동으로 블록이 떨어집니다.

**조작 방법**  
- ⬅ : 왼쪽 이동  
- ➡ : 오른쪽 이동  
- ⬆ : 회전  
- ⬇ : 빠른 낙하  
- Space : 하드 드롭  
""")

# 신뢰성 있는 무료 테트리스 HTML (오픈소스)
tetris_url = "https://tetris.jutge.org/tetris_en.html"

st.components.v1.iframe(src=tetris_url, height=650)
