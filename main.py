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


#π,重力加速度の定義
pi = 3.14159265359
g=9.8
origin = 5 #??

#定数の設定
#角度
deg = input()
rad = deg / 180 * pi

S = input()
qw = input()
dc = (qw ^ 2 / g) ^ (1 / 3)

N = 14 * (deg ^ (-0.65)) * S * (100 / deg * S - 1) - (0.041 * deg) + 6.27

nu = 10 ^ (-6)
Re = qw / nu
ur = input()

#計算
dX = input()

#IP点
Cmi = input() #Cmi = 0.2
#Xi = input()
#Dwi = input()
Xi = 5 / ((sin(rad)) ^ (0.485)) * (S * cos(rad)) ^ (-0.455)
Dwi = 0.35 / ((sin(rad)) ^ (0.3)) * (S * cos(rad)) ^ (0.1)

#疑似空気混入不等流
fu = (-9.2 * deg * (10)^(-4) + 0.12) * tanh(4*S) 
+ 3.8 * (deg ^2) * (10 ^(-5)) -4.4 * deg * 10 ^(-3) + 0.135

Dwu = (fu / (8 * sin(rad))) ^ (1 / 3)

Cmu = (6.9 / deg - 0.12) * S + 0.656 * (1 - exp(-0.0356 * (deg - 10.9))) + 0.073

small_ko = ur * Dwi * dc * cos(deg * pi / 180) / qw
Ko = (1 / (1 - Cmu)) * (1 / (1 - Cmu) * log((1 - Cmi) / (Cmu - Cmi)) - 1 / (1 - Cmi))

# 結果を保存するためのデータフレーム
results = pd.DataFrame(columns=['Y', 'C', 'U'])

# 計算
Cm = Cmi
Dw = Dwi
X = Xi

for i in range(int(50 / dX)):
    Y = 0
    m = 200
    dY = 1 / m

    D_dash = (0.848 * Cm - 0.00302) / (1 + 1.1375 * Cm - 2.2925 * Cm ** 2)
    k_dash = np.arctanh(0.1 ** 0.5) + 1 / (2 * D_dash)

    DataY = np.zeros(m + 1)
    DataC = np.zeros(m + 1)
    DataU = np.zeros(m + 1)

    for j in range(m + 1):
        C = 1 - tanh(k_dash - Y / (2 * D_dash)) ** 2
        U = Y ** (1 / N)

        DataC[j] = C
        DataU[j] = U
        DataY[j] = Y

        Y += dY

    # 結果をデータフレームに追加
    temp_df = pd.DataFrame({'Y': DataY, 'C': DataC, 'U': DataU})
    results = pd.concat([results, temp_df], ignore_index=True)

def calculate_cp_cv(DataC, DataU, DataY, dY, m):
    sumA = sumB = sumD = sumF = 0

    for j in range(m):
        d_sumA = dY / 2 * (DataC[j + 1] + DataC[j])
        d_sumB = dY / 2 * ((1 - DataC[j + 1]) * DataU[j + 1] + (1 - DataC[j]) * DataU[j])
        d_sumD = dY / 2 * ((1 - DataC[j + 1]) * DataU[j + 1] ** 3 + (1 - DataC[j]) * DataU[j] ** 3)
                
        sumA += d_sumA
        sumB += d_sumB
        sumD += d_sumD
             
        sumE = 0

        for k in range(j, m):
            if k < m - 1:
                d_sumE = dY / 2 * ((1 - DataC[k + 2]) + (1 - DataC[k + 1]))
            else:
                d_sumE = 0
            
            sumE += d_sumE
                                        
        d_sumF = dY / 2 * (((1 - DataC[j + 1]) * DataY[j + 1] + sumE) * DataU[j + 1] +
                           ((1 - DataC[j + 1]) * DataY[j + 1] + sumE) * DataU[j + 1])
        
        sumF += d_sumF

    Cp = sumF / ((1 - sumA) * sumB)
    Cv = (1 - sumA) ** 2 * sumD / (sumB ** 3)

    return Cp, Cv

def calculate_clear_water_depth(Dw, Dwu, Cp, Cv, rad, dX):
    DDwDX = np.sin(rad) * (Dw ** 3 - Dwu ** 3) / (Cp * Dw ** 3 * np.cos(rad) - Cv)
    
    k1 = dX * DDwDX
    k2 = dX * DDwDX + k1 / 2
    k3 = dX * DDwDX + k2 / 2
    k4 = dX * DDwDX + k3

    Dw = Dw + k1
    # Dw = Dw + (k1 + 2 * k2 + 2 * k3 + k4) / 6

    return Dw, DDwDX

def depth_averaged_air_concentration(Cmi, Cmu, small_ko, X, Xi, Dwi, Ko):
    Cm = Cmi
    t = 0.001

    Left = 1 / ((1 - Cmu) ** 2) * np.log((1 - Cm) / (Cmu - Cm)) - 1 / ((1 - Cmu) * (1 - Cm))
    Right = small_ko * ((X - Xi) / Dwi) + Ko
    Error = Right - Left

    count = 1

    while abs(Error) >= 1e-10:
        if Error > 0:
            Cm += t
        else:
            Cm -= t
            t *= 0.1
            
        if Cm > Cmu:
            Cm -= t
            t *= 0.1
        elif Cm < Cmi:
            Cm += 10 * t

        Left = 1 / ((1 - Cmu) ** 2) * np.log((1 - Cm) / (Cmu - Cm)) - 1 / ((1 - Cmu) * (1 - Cm))
        Error = Right - Left

        count += 1

    return Cm, count