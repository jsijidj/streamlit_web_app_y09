import streamlit as st

st.title('コードについて')
st.caption('階段状水路のskimming flow解析コード')

st.text('コードは以下のように示す')
code = '''
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from math import pi, sin, cos, tanh, log, exp


#重力加速度の定義
g=9.8

#定数の設定
#入力したい値をinput関数で入力
# ＊input関数は文字列を返すため、float関数で数字列を返せるように
deg = input('degを入力してください')
S = input('Sを入力してください')
qw = input('qwを入力してください')
ur = input('urを入力してください')
dX = input('dXを入力してください')
Cmi = input('Cmiを入力してください')

#角度
deg = float(deg)
rad = deg / (180 * pi)

#流量
S = float(S)
qw = float(qw)
dc = (qw ** 2 / g) ** (1 / 3)

N = 14 ** (deg ** (-0.65)) * S * (100 / deg * S - 1) - (0.041 * deg) + 6.27

nu = 10 ** (-6)
Re = qw / nu  #レイノルズ数
ur = float(ur)

#計算
dX = float(dX)

#IP点
Cmi = float(Cmi) #Cmi = 0.2(断面平均空気混入率)
#Xi = input()
#Dwi = input()

#Xi = x / dc
Xi = 5 / ((sin(rad)) ** (0.485)) * ((S * cos(rad)) ** (-0.455))

#Dwi = dwi / dc
Dwi = 0.35 / ((sin(rad)) ** (0.3)) * ((S * cos(rad)) ** (0.1))

#疑似空気混入不等流
#疑似等流の抵抗係数fuの実験式
#fu = 8 * (dwu/dc) **3 * sin(deg)
fu = (-9.2 * deg * (10)**(-4) + 0.12) * tanh(4*S) 
+ 3.8 * (deg ** 2) * (10 **(-5)) -4.4 * deg * 10 **(-3) + 0.135

Dwu = (fu / (8 * sin(rad))) ** (1 / 3)

Cmu = (6.9 / deg - 0.12) * S + 0.656 * (1 - exp(-0.0356 * (deg - 10.9))) + 0.073

small_ko = ur * Dwi * dc * cos(deg * pi / 180) / qw
Ko = (1 / (1 - Cmu)) * (1 / (1 - Cmu) * log((1 - Cmi) / (Cmu - Cmi)) - 1 / (1 - Cmi))

#データを表形式で取得
data1 = pd.DataFrame({
    'deg':[deg],
    'rad':[rad],
    'S':[S],
    'qw':[qw],
    'dc':[dc],
    'N':[N],
    'nu':[nu],
    'Re':[Re],
    'ur':[ur],
    'dX':[dX],
    'Cmi':[Cmi],
    'Xi':[Xi],
    'Dwi':[Dwi],
    'fu':[fu],
    'Dwu':[Dwu],
    'Cmu':[Cmu],
    'small_ko':[small_ko],
    'Ko':[Ko]
})

# meltメソッドを使用して縦長に変換
#meltメソッド使用時にvar_name ='variable', value_name='value'のように引数を返すときは文字列で指定する
df_melt = pd.melt(data1, var_name ='variable', value_name='value')

print(df_melt)

# 結果を保存するためのデータフレーム
#pandasを使って繰り返し計算された結果を表形式で格納する
#Y = y/y0.9, C = C(空気混入率), U = u/u0.9
results = pd.DataFrame(columns=['Y', 'C', 'U'])

# 計算する前の定義
Cm = Cmi  #45行目(IP点)のCmi
Dw = Dwi  #53行目の dwi/dc
X = Xi  #50行目の  x/dc

#Y,U,C の取得
for i in range(int(50 / dX)):
    Y = 0
    m = 200
    dY = 1 / m

    D_dash = (0.848 * Cm - 0.00302) / (1 + 1.1375 * Cm - 2.2925 * Cm ** 2)
    k_dash = np.arctanh(0.1 ** 0.5) + 1 / (2 * D_dash)
    
    #ループ内でデータを格納するための空の配列を作成する
    #vba上のReDimをpythonのnumpyで変換
    DataY = np.zeros(m + 1)
    DataC = np.zeros(m + 1)
    DataU = np.zeros(m + 1)

    for j in range(m + 1):
        C = 1 - tanh(k_dash - Y / (2 * D_dash)) ** 2
        U = Y ** (1 / N(deg,S))

        DataC[j] = C
        DataU[j] = U
        DataY[j] = Y

        Y += dY

    # 結果をデータフレームに追加
    temp_df = pd.DataFrame({'Y': DataY, 'C': DataC, 'U': DataU})
    #修正前
    #results = pd.concat([results, temp_df], ignore_index=True)
    # 空のエントリやすべてがNAのエントリを除外
    #temp_df = temp_df.dropna(how='all', axis=1)

    # DataFrameを結合
    results = pd.concat([results, temp_df], ignore_index=True)
'''

st.code(code, language='python')