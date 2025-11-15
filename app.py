import streamlit as st

# 제목
st.title("Hello Streamlit!")

# 텍스트 출력
st.write("이것은 Streamlit의 아주 기본적인 예제입니다 😊")

# 입력창
name = st.text_input("이름을 입력하세요:")

# 슬라이더
age = st.slider("나이를 선택하세요:", 1, 100, 20)

# 버튼
if st.button("확인"):
    st.success(f"안녕하세요, {name}님! 나이는 {age}세군요!")
