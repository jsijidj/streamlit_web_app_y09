import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from math import pi, sin, cos, tanh, log, exp
from PIL import Image #画像や動画関係のライブラリ
import time
import io

# 現在のUNIX時間を取得
current_time = time.time()
print("UNIX時間:", current_time)

# 現在の時間を人間が読みやすい形式で表示
readable_time = time.ctime(current_time)
print("現在の時間:", readable_time)
st.text(readable_time)

#webサイトの設定
#タイトルやテキストの入力ができる
st.title('階段状水路解析アプリ')
st.caption('これは水面計計算までの解析とそのグラフ等を計算するテストアプリです')
st.subheader('解析について')
st.text('このサイトでは,あるデータの値を入力することで\n'
        '階段状水路の解析計算の一部ができるようになっています\n'
        '*繰り返し計算は50/dXとし、200個のデータが出力されます。\n'
        '目標の断面はIP点を0とし、流下方向にどれだけ離れたかを基に決定する。*')


st.subheader('解析計算')

#重力加速度の定義
g=9.8

#定数の設定
#入力したい値をinput関数で入力
# ＊input関数は文字列を返すため、float関数で数字列を返せるように
with st.form(key='data_form'):
    st.text('deg=')
    deg = st.text_input('deg', '')
    st.text('S/dc=')
    S = st.text_input('S/dc', '')
    st.text('qwの値')
    qw = st.text_input('qw=', '')
    st.text('urの値')
    ur = st.text_input('ur=', '')
    st.text('dXの値')
    dX = st.text_input('dX=', '')
    st.text('Cmiの値')
    Cmi = st.text_input('Cmi=', '')
    st.text('水温Tの値')
    T = st.text_input('T=', '')
    st.text('yの値')
    suuti_y = st.text_input('y=', '')
    st.text('C(長針)の値')
    suuti_c_tip1 = st.text_input('c_tip1=', '')
    st.text('C(短針)の値')
    suuti_c_tip2 = st.text_input('c_tip2=', '')
    st.text('Uの値')
    suuti_u = st.text_input('u=', '')
    st.text('長針のC=0.9に近い値(2個)')
    C_y09_tip1_c = st.text_input('C_y09_tip1_c', '')
    st.text('対応する水深y')
    C_y09_tip1_y = st.text_input('C_y09_tip1_y', '')
    st.text('短針のC=0.9に近い値(2個)')
    C_y09_tip2_c = st.text_input('C_y09_tip2_c', '')
    st.text('対応する水深y')
    C_y09_tip2_y = st.text_input('C_y09_tip2_y', '')
    st.text('u0.9に近い値(長針)')
    u_09_list_tip1 = st.text_input('u_09_list_tip1', '')
    st.text('u0.9に近い値(短針)')
    u_09_list_tip2 = st.text_input('u_09_list_tip2', '')

    st.text('ns=')
    suuti_ns = st.text_input('ns', '')
    st.text('目標の断面')
    target_iteration = st.text_input('target=', '')

    submit_btn = st.form_submit_button('解析開始'),
    cancel_btn = st.form_submit_button('キャンセル')

if submit_btn:
    try:
        # 入力フィールドが空でないかチェックして数値に変換 
        if deg and S and suuti_ns and qw and ur and dX and Cmi:
            #角度
            deg = float(deg)
            rad = (deg / 180) * np.pi

            #流量
            S = float(S)
            qw = float(qw)
            dc = (qw ** 2 / g) ** (1 / 3)

            N = ((14 * (deg ** (-0.65))) * S * (((100 / deg) * S) - 1)) - (0.041 * deg) + 6.27

            T = float(T)

            nu = (7.105482 * (10 ** -18) * (T ** 6)) - (2.51304153 * (10 **-15) * (T ** 5)) + (3.67082783 * (10 ** -13) * (T ** 4)) - (2.97438215 * (10 ** -11) * (T ** 3)) + (1.56879688 * (10 ** -9) * (T ** 2)) - (6.1236331 * (10 ** -8) * T) + (1.79251606 * (10 ** -6))
            Re = qw / nu  #レイノルズ数
            ur = float(ur)

            #計算
            dX = float(dX)

            #IP点
            Cmi = float(Cmi) #Cmi = 0.2(断面平均空気混入率)

            #目標の断面
            target_iteration = float(target_iteration)

            #Xi = input()
            #Dwi = input()

            #Xi = x / dc
            Xi = (5 / ((np.sin(rad)) ** (0.485))) * ((S * np.cos(rad)) ** (-0.455))

            #Dwi = dwi / dc
            Dwi = (0.35 / ((np.sin(rad)) ** (0.3))) * ((S * np.cos(rad)) ** (0.1))

            #疑似空気混入不等流
            #疑似等流の抵抗係数fuの実験式
            #fu = 8 * (dwu/dc) **3 * sin(deg)
            fu = (((-9.2 * deg * ((10)**(-4))) + 0.12) * np.tanh(4 * S)) + (3.8 * (deg ** 2) * (10 **(-5))) + (- 4.4 * deg * (10 ** (-3))) + 0.135

            Dwu = (fu / (8 * np.sin(rad))) ** (1 / 3)

            Cmu = (6.9 / deg - 0.12) * S + 0.656 * (1 - np.exp(-0.0356 * (deg - 10.9))) + 0.073

            small_ko = ur * Dwi * dc * np.cos(rad) / qw
            Ko = (1 / (1 - Cmu)) * (1 / (1 - Cmu) * np.log((1 - Cmi) / (Cmu - Cmi)) - 1 / (1 - Cmi))

            #データを表形式で取得
            data1 = pd.DataFrame({
                'deg':[deg],
                'rad':[rad],
                'S/dc':[S],
                'qw':[qw],
                'dc':[dc],
                'N':[N],
                'T':[T],
                'nu':[nu],
                'Re=qw/nu':[Re],
                'ur':[ur],
                'dX':[dX],
                'Cmi':[Cmi],
                'xi/dc':[Xi],
                'dwi/dc':[Dwi],
                'fu':[fu],
                'dwu/dc':[Dwu],
                'Cmu':[Cmu],
                'small_k0':[small_ko],
                'K0':[Ko]
            })

            # meltメソッドを使用して縦長に変換
            #meltメソッド使用時にvar_name ='variable', value_name='value'のように引数を返すときは文字列で指定する
            df_melt = pd.melt(data1, var_name ='variable', value_name='value')

            st.dataframe(df_melt)

        else:
            st.error("すべてのフィールドに値を入力してください") 
    
    except ValueError: st.error("有効な数値を入力してください")

    if C_y09_tip1_c:
        C_y09_list_1 = [float(i) for i in C_y09_tip1_c.split(',')]

    if C_y09_tip1_y:
        y09_list_1 = [float(i) for i in C_y09_tip1_y.split(',')]

    if C_y09_tip1_c and C_y09_tip1_y and len(C_y09_list_1) == 2 and len(y09_list_1) == 2:
        #傾き
        a_tip1 = ((y09_list_1[1]-y09_list_1[0]) / (C_y09_list_1[1] - C_y09_list_1[0]))
        #切片
        n_tip1 = y09_list_1[0] - a_tip1 * C_y09_list_1[0]

        y09_tip1 = a_tip1 * 0.9 + n_tip1

    else:
        y09_tip1 = None
        st.write('y0.9_tip1が不明です')

    if C_y09_tip2_c:
        C_y09_list_2 = [float(i) for i in C_y09_tip2_c.split(',')]

    if C_y09_tip2_y:
        y09_list_2 = [float(i) for i in C_y09_tip2_y.split(',')]

    if C_y09_tip2_c and C_y09_tip2_y and len(C_y09_list_2) == 2 and len(y09_list_2) == 2:
        #傾き
        a_tip2 = ((y09_list_2[1]-y09_list_2[0]) / (C_y09_list_2[1] - C_y09_list_2[0]))
        #切片
        n_tip2 = y09_list_2[0] - a_tip2 * C_y09_list_2[0]

        y09_tip2 = a_tip2 * 0.9 + n_tip2

    else:
        y09_tip2 = None
        st.write('y0.9_tip2が不明です')
    
    #uのリスト化
    if u_09_list_tip1:
        u_09_list_1 = [float(i) for i in u_09_list_tip1.split(',')]

    if u_09_list_tip2:
        u_09_list_2 = [float(i) for i in u_09_list_tip2.split(',')]

    #u0.9の算出(長針)
    if C_y09_tip1_c and u_09_list_tip1 and len(C_y09_list_1) == 2 and len(u_09_list_1) == 2:
        #傾き
        u_09_a_tip1 = ((u_09_list_1[1]-u_09_list_1[0]) / (C_y09_list_1[1] - C_y09_list_1[0]))
        #切片
        u_09_n_tip1 = u_09_list_1[0] - u_09_a_tip1 * C_y09_list_1[0]

        u09_tip1 = u_09_a_tip1 * 0.9 + u_09_n_tip1
    
    else:
        u09_tip1 = None
        st.write('u0.9_tip1が不明です')

    #u0.9の算出(短針)
    if C_y09_tip2_c and u_09_list_tip2 and len(C_y09_list_2) == 2 and len(u_09_list_2) == 2:
        #傾き
        u_09_a_tip2 = ((u_09_list_2[1]-u_09_list_2[0]) / (C_y09_list_2[1] - C_y09_list_2[0]))
        #切片
        u_09_n_tip2 = u_09_list_2[0] - u_09_a_tip2 * C_y09_list_2[0]

        u09_tip2 = u_09_a_tip2 * 0.9 + u_09_n_tip2

    else:
        u09_tip2 = None
        st.write('u0.9_tip2が不明です')


    st.write('長針y0.9=',y09_tip1)
    st.write('短針y0.9=',y09_tip2)
    st.write('長針u0.9=',u09_tip1)
    st.write('短針u0.9=',u09_tip2)
        
    #データフレーム表示
    data = {}

    #yのリスト化
    if suuti_y:
        y_list = [float(i) for i in suuti_y.split(',')]
        data['y'] = y_list
        if y09_tip1 is not None:         
            data['y/y0.9_tip1'] = [y / y09_tip1 for y in y_list]
            data['y/y0.9_tip2'] = [y / y09_tip2 for y in y_list]

    #Cのリスト化(長針)
    if suuti_c_tip1:     
            C_list_tip1 = [float(i) for i in suuti_c_tip1.split(',')]
            data['C_tip1'] = C_list_tip1

    #Cのリスト化(短針)
    if suuti_c_tip2:    
        C_list_tip2 = [float(i) for i in suuti_c_tip2.split(',')]
        data['C_tip2'] = C_list_tip2

    # uのリスト化 
    if suuti_u:
        u_list = [float(i) for i in suuti_u.split(',')]
        data['u'] = u_list

        if u09_tip1 is not None:
            data['u/u0.9_tip1'] = [u / u09_tip1 for u in u_list]

        else: 
            st.write('u0.9_tip1が設定されていません')

        if u09_tip2 is not None:
            data['u/u0.9_tip2'] = [u / u09_tip2 for u in u_list]

        else:
            st.write('u0.9_tip2が設定されていません')

    if data:
        df = pd.DataFrame(data)
        st.write('データ表')
        st.dataframe(df)

    # 結果を保存するためのデータフレーム
    #pandasを使って繰り返し計算された結果を表形式で格納する
    #Y = y/y0.9, C = C(空気混入率), U = u/u0.9
    data2 = pd.DataFrame(columns=['Y', 'C', 'U','CdY', '(1-C)UdY', '(1-C)U^3dY', '(1-C)UdY', '[(1-C)Y+int_Y^1{(1-C)dY}]', 'UdY'])

    # 計算する前の定義
    Cm = Cmi  #45行目(IP点)のCmi
    Dw = Dwi  #53行目の　dwi/dc
    X = Xi  #50行目の  x/dc

    #データXリスト
    data_X = []
    #データX_Xiリスト
    data_X_Xi = []
    #データD_dashリスト
    data_D_dash = []
    #データk_dashリスト
    data_k_dash = []
    #データCmリスト
    data_Cm = []
    #データCpリスト
    data_Cp = []
    #データCvリスト
    data_Cv = []
    #データDWリスト
    data_Dw = []
    #データdDw/dxリスト
    data_dDwdx = []
    #データDw_Cmリスト
    data_Dw_Cm = []
    #データ(エネルギー水頭)リスト
    data_Es = []
    #データ(断面平均流速)リスト
    data_V_age_Vw = []

    #Y,U,C の取得
    #50回繰り返す場合 => for i in range(int(50 / dX)):
    for i in range(int((50 / dX) + 2)):
        Y = 0
        m = 200
        dY = 1 / m

        D_dash = ((0.848 * Cm) - 0.00302) / (1 + (1.1375 * Cm) - (2.2925 * (Cm ** 2)))
        k_dash = (np.arctanh(0.1 ** 0.5)) + (1 / (2 * D_dash))

        #ループ内でデータを格納するための空の配列を作成する
        #vba上のReDimをpythonのnumpyで変換 
        DataY = np.zeros(m + 1)
        DataC = np.zeros(m + 1)
        DataU = np.zeros(m + 1)

        for j in range(m + 1):
            C = 1 - ((np.tanh(k_dash - (Y / (2 * D_dash)))) ** 2)
            U = Y ** (1 / N)

            DataC[j] = C
            DataU[j] = U
            DataY[j] = Y

            Y += dY

        # 結果をデータフレームに追加
        temp_df = pd.DataFrame({'Y': DataY, 'C': DataC, 'U': DataU})
        
        #空のエントリやすべてがNA(欠損値)のエントリを除外
        temp_df = temp_df.dropna(how='all', axis=1)

        #Cp,Cvの取得

        #d_sumA = CdY, d_sumB = (1-C)UdY, d_sumD = (1-C)U^3dY, sumE = integral_Y^1{(1-C)dY}, d_sumF = [(1-C)Y+int_Y^1{(1-C)dY}]UdY, d_sumG = UdY
        #data3 = pd.DataFrame(columns=['CdY', '(1-C)UdY', '(1-C)U^3dY', 'int_Y^1{(1-C)dY}', '[(1-C)Y+int_Y^1{(1-C)dY}]UdY'])

        Data_d_sumA = np.zeros(m + 1)
        Data_d_sumB = np.zeros(m + 1)
        Data_d_sumD = np.zeros(m + 1)
        Data_sumE = np.zeros(m + 1)
        Data_d_sumF = np.zeros(m + 1)
        Data_d_sumG = np.zeros(m + 1)

        def calculate_Cp_Cv(DataC, DataU, DataY, dY, m): 
            sumA = sumB = sumD = sumE = sumF = sumG = 0 # 初期化 
            for j in range(m):
                d_sumA = (dY * (DataC[j+1] + DataC[j])) / 2 
                d_sumB = (dY * ((1 - DataC[j+1]) * DataU[j+1] + (1 - DataC[j]) * DataU[j])) / 2 
                d_sumD = (dY * ((1 - DataC[j+1]) * (DataU[j+1]) ** 3 + (1 - DataC[j]) * (DataU[j]) ** 3)) / 2 
                d_sumG = (dY * (DataU[j+1] + DataU[j])) / 2 
                    
                sumA += d_sumA 
                sumB += d_sumB 
                sumD += d_sumD 
                sumG += d_sumG 
                
                sumE = 0 # ここでsumEをリセット 
                for k in range(j, m): 
                    if k < m - 1: 
                        d_sumE = (dY * ((1 - DataC[k + 2]) + (1 - DataC[k + 1]))) / 2 
                    
                    else: 
                        d_sumE = 0 
                    
                    sumE += d_sumE 
                    Data_sumE[j] = sumE 
                    
                    
                    if j + 1 < len(DataY):
                        d_sumF = (dY * (((1 - DataC[j + 1]) * DataY[j + 1] + sumE) * DataU[j + 1] + ((1 - DataC[j]) * DataY[j] + sumE) * DataU[j])) / 2 
                    
                    else: 
                        d_sumF = 0 # 安全策としての初期化 
                    sumF += d_sumF 
                    
                    Data_d_sumA[j] = d_sumA 
                    Data_d_sumB[j] = d_sumB 
                    Data_d_sumD[j] = d_sumD 
                    Data_sumE[j] = sumE 
                    Data_d_sumF[j] = d_sumF 
                    Data_d_sumG[j] = d_sumG 
                    # デバッグ用出力 
                    print(f"Iteration {j}: sumA={sumA}, sumB={sumB}, sumD={sumD}, sumE={sumE}, sumF={sumF}, sumG={sumG}") 
                    
                    Cp = sumF / ((1 - sumA) * sumB) 
                    Cv = (((1 - sumA) ** 2) * sumD) / (sumB ** 3) 
                    V_age_Vw = ((1 - sumA) * sumG) / sumB 
                    
                    return Cp, Cv, Data_d_sumA, Data_d_sumB, Data_d_sumD, Data_sumE, Data_d_sumF, sumA, sumB, sumG, Data_d_sumG,V_age_Vw

        Cp, Cv, Data_d_sumA, Data_d_sumB, Data_d_sumD, Data_sumE, Data_d_sumF, sumA, sumB, sumG, Data_d_sumG, V_age_Vw = calculate_Cp_Cv(DataC, DataU, DataY, dY, m)
            
        temp_df = pd.DataFrame({'Y': DataY, 'C': DataC, 'U': DataU, 'CdY': Data_d_sumA, '(1-C)UdY': Data_d_sumB, '(1-C)U^3dY': Data_d_sumD, 'int_Y^1{(1-C)dY}': Data_sumE, '[(1-C)Y+int_Y^1{(1-C)dY}]': Data_d_sumF, 'UdY': Data_d_sumG})
        temp_df = temp_df.dropna(how='all', axis=1)

        #i回目の結果の表示
        if i == target_iteration:
            st.dataframe(temp_df)
            
            if 'y/y0.9_tip1' in df.columns and 'C_tip1' in df.columns:
                buf1 = io.BytesIO()  # バッファ作成
                #グラフの作成
                # Plot the data
                fig1, ax = plt.subplots()
                ax.plot(DataC, DataY, label='C')
                ax.scatter(df['C_tip1'], df['y/y0.9_tip1'], label='C_tip1 vs y/y0.9tip_1')
                ax.set_xlabel('C')
                ax.set_ylabel('y/y0.9')
                ax.set_title('分布グラフ')
                ax.legend()
                st.pyplot(fig1)

            if 'y/y0.9_tip2' in df.columns and 'C_tip2' in df.columns:
                buf2 = io.BytesIO()  # バッファ作成
                # y/y0.9-Cグラフをプロット
                fig2, ax = plt.subplots()
                ax.plot(DataC, DataY, label='C')
                ax.scatter(df['C_tip2'], df['y/y0.9_tip2'], label='C_tip2 vs y/y0.9_tip2')
                ax.set_ylabel('y/y0.9_tip2')
                ax.set_xlabel('C_tip2')
                ax.set_title('分布グラフ')
                ax.legend()
                plt.savefig(buf2, format='png')
                buf2.seek(0)
                st.pyplot(fig2)
            
            if 'y/y0.9_tip1' in df.columns and 'C_tip1' in df.columns and 'y/y0.9_tip2' in df.columns and 'C_tip2' in df.columns:
                buf3 = io.BytesIO()  # バッファ作成
                # y/y0.9-Cグラフをプロット
                fig3, ax = plt.subplots()
                ax.plot(DataC, DataY, label='C')
                ax.scatter(df['C_tip1'], df['y/y0.9_tip1'], label='C_tip1 vs y/y0.9_tip1')
                ax.scatter(df['C_tip2'], df['y/y0.9_tip2'], label='C_tip2 vs y/y0.9_tip2')
                ax.set_ylabel('y/y0.9')
                ax.set_xlabel('C')
                ax.set_title('分布グラフ')
                ax.legend()
                plt.savefig(buf3, format='png')
                buf3.seek(0)
                st.pyplot(fig3)
            
            if 'y/y0.9_tip1' in df.columns and 'u/u0.9_tip1' in df.columns:
                buf4 = io.BytesIO()  # バッファ作成
                fig4, ax = plt.subplots()
                # y/y0.9-u/u0.9グラフをプロット
                ax.plot(DataU, DataY, label='U')
                ax.scatter(df['u/u0.9_tip1'], df['y/y0.9_tip1'], label='u/u0.9_tip1 vs y/y0.9_tip1')
                ax.set_xlabel('u/u0.9_tip1')
                ax.set_ylabel('y/y0.9_tip1')
                ax.set_title('分布グラフ')
                ax.legend()
                plt.savefig(buf4, format='png')
                buf4.seek(0)
                st.pyplot(fig4)

            if 'y/y0.9_tip2' in df.columns and 'u/u0.9_tip2' in df.columns:
                buf5 = io.BytesIO()  # バッファ作成
                fig5, ax = plt.subplots()
                # y/y0.9-u/u0.9グラフをプロット
                ax.plot(DataU, DataY, label='U')
                
                ax.scatter(df['u/u0.9_tip2'], df['y/y0.9_tip2'], label='u/u0.9_tip2 vs y/y0.9_tip2')
                ax.set_xlabel('u/u0.9')
                ax.set_ylabel('y/y0.9')
                ax.set_title('分布グラフ')
                ax.legend()
                plt.savefig(buf5, format='png')
                buf5.seek(0)
                st.pyplot(fig5)


            if 'y/y0.9_tip1' in df.columns and 'u/u0.9_tip1' in df.columns and 'y/y0.9_tip2' in df.columns and 'u/u0.9_tip2' in df.columns:
                buf6 = io.BytesIO()  # バッファ作成
                fig6, ax = plt.subplots()
                # y/y0.9-u/u0.9グラフをプロット
                ax.plot(DataU, DataY, label='U')
                ax.scatter(df['u/u0.9_tip1'], df['y/y0.9_tip1'], label='u/u0.9_tip1 vs y/y0.9_tip1')
                ax.scatter(df['u/u0.9_tip2'], df['y/y0.9_tip2'], label='u/u0.9_tip2 vs y/y0.9_tip2')
                ax.set_xlabel('u/u0.9_tip2')
                ax.set_ylabel('y/y0.9_tip2')
                ax.set_title('分布グラフ')
                ax.legend()
                plt.savefig(buf6, format='png')
                buf6.seek(0)
                st.pyplot(fig6)       

        #ルンゲクッタ法から積分計算
        def calculate_clear_water_depth(Dw, Dwu, Cp, Cv, rad, dX):
            DDwDX = (np.sin(rad) * ((Dw ** 3) - (Dwu ** 3))) / (Cp * (Dw ** 3) * np.cos(rad) - Cv)
        
            k1 = dX * DDwDX 
            k2 = dX * ((np.sin(rad) * ((Dw + k1/2) ** 3 - Dwu ** 3)) / (Cp * ((Dw + k1/2) ** 3) * np.cos(rad) - Cv)) 
            k3 = dX * ((np.sin(rad) * ((Dw + k2/2) ** 3 - Dwu ** 3)) / (Cp * ((Dw + k2/2) ** 3) * np.cos(rad) - Cv)) 
            k4 = dX * ((np.sin(rad) * ((Dw + k3) ** 3 - Dwu ** 3)) / (Cp * ((Dw + k3) ** 3) * np.cos(rad) - Cv)) 
            
            Dw = Dw + (k1 + 2 * k2 + 2 * k3 + k4) / 6

            return Dw, DDwDX
        
        Dw, DDwDX = calculate_clear_water_depth(Dw, Dwu, Cp, Cv, rad, dX)

        #depth_averaged_air_concentration
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

        # Cmの更新
        Cm, count = depth_averaged_air_concentration(Cmi, Cmu, small_ko, X, Xi, Dwi, Ko)
        
        # 再度D_dashとk_dashをCmの更新後に計算
        D_dash = ((0.848 * Cm) - 0.00302) / (1 + (1.1375 * Cm) - (2.2925 * (Cm ** 2))) 
        k_dash = (np.arctanh(0.1 ** 0.5)) + (1 / (2 * D_dash))
        Cp, Cv, d_sumA, d_sumB, d_sumD, sumE, d_sumF, sumA, sumB, sumG, d_sumG, V_age_Vw = calculate_Cp_Cv(DataC, DataU, DataY, dY, m)
        Dw, DDwDX = calculate_clear_water_depth(Dw, Dwu, Cp, Cv, rad, dX)

        def Dw_Cm_caluculate(Dw, Cm):
            Dw_Cm = Dw / (1 - Cm)

            return Dw_Cm
        
        Dw_Cm = Dw_Cm_caluculate(Dw, Cm)

        #energy_caluculate
        Es = (Cp * Dw * np.cos(rad)) + (1 / 2) * Cv * ((Dw) ** -2)

        # Reset arrays for next iteration
        DataY.fill(0)
        DataC.fill(0)
        DataU.fill(0)

        X_Xi = X - Xi

        #それぞれのデータを格納するリスト
        data_X.append(X)
        data_X_Xi.append(X_Xi)
        data_D_dash.append(D_dash)
        data_k_dash.append(k_dash)
        data_Cm.append(Cm)
        data_Cp.append(Cp)
        data_Cv.append(Cv)
        data_Dw.append(Dw)
        data_dDwdx.append(DDwDX)
        data_Dw_Cm.append(Dw_Cm)
        data_Es.append(Es)
        data_V_age_Vw.append(V_age_Vw)

        # Update X
        X += dX

    # 結果をデータフレームに追加
    def dataframe50(data_X,data_X_Xi,data_D_dash,data_k_dash,data_Cm,data_Cp,data_Cv,data_Dw,data_dDwdx,data_Dw_Cm,data_Es,data_V_age_Vw):
        return pd.DataFrame({
            'x/dc':data_X,
            '(x-xi)/dc':data_X_Xi,
            'D_dash':data_D_dash,
            'k_dash':data_k_dash,
            'Cm':data_Cm,
            'Cp':data_Cp,
            'Cv':data_Cv,
            'dw/dc':data_Dw,
            'd(dw/dc)/d(x/dc)':data_dDwdx,
            'y0.9/dc':data_Dw_Cm,
            'Es/dc':data_Es,
            'Vage/Vw':data_V_age_Vw
        })
    data50 = dataframe50(data_X,data_X_Xi,data_D_dash,data_k_dash,data_Cm,data_Cp,data_Cv,data_Dw,data_dDwdx,data_Dw_Cm,data_Es,data_V_age_Vw)

    st.dataframe(data50)

    #グラフの作成
    if 'Cm' in data50.columns and 'dw/dc' in data50.columns and 'y0.9/dc' in data50.columns and '(x-xi)/dc' in data50.columns:
        buf7 = io.BytesIO()  # バッファ作成
        fig7, ax = plt.subplots()
        ax.plot(data_X_Xi, data_Cm, label='Cm')
        ax.plot(data_X_Xi, data_Dw, label='dw/dc')
        ax.plot(data_X_Xi, data_Dw_Cm, label='y0.9/dc')
        ax.set_xlabel('(x-xi)/dc')
        ax.set_ylabel('Cm, dw/dc, y0.9/dc')
        ax.set_title('分布グラフ')
        ax.legend()
        plt.savefig(buf7, format='png')
        buf7.seek(0)
        st.pyplot(fig7)
        

    if '(x-xi)/dc' in data50.columns and 'Cv' in data50.columns:
        buf8 = io.BytesIO()  # バッファ作成
        fig8, ax = plt.subplots()
        ax.plot(data_X_Xi,data_Cv, label='Cv')
        ax.set_xlabel('(x-xi)/dc')
        ax.set_ylabel('Cv')
        ax.set_title('分布グラフ')
        ax.legend()
        plt.savefig(buf8, format='png')
        buf8.seek(0)
        st.pyplot(fig8)

    if '(x-xi)/dc' in data50.columns and 'Cp' in data50.columns:
        buf9 = io.BytesIO()  # バッファ作成
        fig9, ax = plt.subplots()
        ax.plot(data_X_Xi,data_Cp, label='Cp')
        ax.set_xlabel('(x-xi)/dc')
        ax.set_ylabel('Cp')
        ax.set_title('分布グラフ')
        ax.legend()
        plt.savefig(buf9, format='png')
        buf9.seek(0)
        st.pyplot(fig9)       

    if 'Es/dc' in data50.columns and '(x-xi)/dc' in data50.columns:
        buf10 = io.BytesIO()  # バッファ作成
        fig10, ax = plt.subplots()
        ax.plot(data_X_Xi, data_Es, label='Es')
        ax.set_xlabel('(x-xi)/dc')
        ax.set_ylabel('Es/dc')
        ax.set_title('分布グラフ')
        ax.legend()
        plt.savefig(buf10, format='png')
        buf10.seek(0)
        st.pyplot(fig10)
    
    if 'Vage/Vw' in data50.columns and '(x-xi)/dc' in data50.columns:
        buf11 = io.BytesIO()  # バッファ作成
        fig11, ax = plt.subplots()
        ax.plot(data_X_Xi, data_V_age_Vw, label='Vage/Vw')
        ax.set_xlabel('(x-xi)/dc')
        ax.set_ylabel('Vage/Vw')
        ax.set_title('分布グラフ')
        ax.legend()
        plt.savefig(buf11, format='png')
        buf11.seek(0)
        st.pyplot(fig11)
