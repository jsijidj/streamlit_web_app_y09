import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from math import pi, sin, cos, tanh, log, exp
from PIL import Image #画像や動画関係のライブラリ

#webサイトの設定
#タイトルやテキストの入力ができる
st.title('階段状水路解析アプリ')
st.caption('これはCv,Cm等を計算するテストアプリです')
st.subheader('解析について')
st.text('このサイトでは,あるデータの値を入力することで\n'
        '階段状水路の解析計算の一部ができるようになっています')