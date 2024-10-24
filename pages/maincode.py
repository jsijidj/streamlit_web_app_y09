import streamlit as st

st.title('コードについて')
st.caption('階段状水路流れの様子を示すメインページ用コード')

st.text('streamlitを用いた当ウェブサイトのソースコード')
#入力したコードの表示
code = '''
import streamlit as st

st.title('階段状水路解析アプリ')
st.caption('これはCv,Cm等を計算するテストアプリです')
st.subheader('解析について')
st.text('このサイトでは,あるデータの値を入力することで\n'
        '階段状水路の解析計算の一部ができるようになっています')

'''
st.code(code, language='python')