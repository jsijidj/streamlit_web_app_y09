import streamlit as st

st.title('コードについて')
st.caption('階段状水路流れの様子を示す動画表示用コード')

st.text('コードは以下のように示す')
code = '''
import streamlit as st
from PIL import Image #画像や動画関係のライブラリ

st.title('階段状水路流れの様子')
st.caption('これは階段状水路流れの様子が見られるサイトです')
st.text('階段状水路流れ')
#画像,動画の添付とサイズ指定
#image = Image.open('画像ファイル.png')
#st.image(image, width=200)
st.text('動画1')
st.text('階段状水路正面の様子')
video_file1 = open('kaidannsyoumen.mp4', 'rb')
video_bytes1 = video_file1.read()
st.video(video_bytes1)

st.text('動画2')
st.text('横方向からの様子')
video_file2 = open('kaidannyoko.mp4', 'rb')
video_bytes2 = video_file2.read()
st.video(video_bytes2)
'''

st.code(code, language='python')