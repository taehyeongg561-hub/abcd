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

# 외부 테트리스 게임 URL을 iframe으로 불러오기
tetris_url = "https://tetris.jutge.org/tetris_en.html"

# iframe으로 테트리스를 표시
st.components.v1.iframe(src=tetris_url, height=600)
