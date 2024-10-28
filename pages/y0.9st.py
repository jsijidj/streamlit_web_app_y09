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
st.caption('これはy0.9とそのグラフ等を計算するテストアプリです')
st.subheader('解析について')
st.text('このサイトでは,あるデータの値を入力することで\n'
        '階段状水路の解析計算の一部ができるようになっています')


st.subheader('解析計算')

with st.form(key='data_form'):
    st.text('deg=')
    deg = st.text_input('deg', '')
    st.text('S/dc=')
    suuti_S = st.text_input('S/dc', '')
    st.text('ns=')
    suuti_ns = st.text_input('ns', '')
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

    submit_btn = st.form_submit_button('解析開始')
    cancel_btn = st.form_submit_button('キャンセル')

if submit_btn:
    new_data = {
        'deg': [deg],
        'S/dc': [suuti_S],
        'ns': [suuti_ns],
    }
    new_df = pd.DataFrame(new_data)
    st.dataframe(new_df)

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
        st.write(y09_tip1)

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
        st.write(y09_tip2)

    else:
        y09_tip2 = None
        st.write('y0.9_tip2が不明です')

    #定数Nの設定
    N = ((14 ** (float(deg) ** (-0.65))) * float(suuti_S) * (100 / float(deg) * float(suuti_S) - 1)) - (0.041 * float(deg)) + 6.27

    st.write('長針y0.9=',y09_tip1)
    st.write('短針y0.9=',y09_tip2)
    #データフレーム表示
    # 入力があればリストに変換

    data = {}

    if suuti_y:
        y_list = [float(i) for i in suuti_y.split(',')]
        data['y'] = y_list
        if y09_tip1 is not None:         
            data['y/y0.9_tip1'] = [y / y09_tip1 for y in y_list]
            data['y/y0.9_tip2'] = [y / y09_tip2 for y in y_list]

    if suuti_c_tip1:     
            C_list_tip1 = [float(i) for i in suuti_c_tip1.split(',')]
            data['C_tip1'] = C_list_tip1

    if suuti_c_tip2:    
        C_list_tip2 = [float(i) for i in suuti_c_tip2.split(',')]
        data['C_tip2'] = C_list_tip2

    if suuti_u:
        u_list = [float(i) for i in suuti_u.split(',')]
        data['u'] = u_list
        if y09_tip1 and y09_tip2 and N is not None:
            data['u/u0.9_tip1'] = [(y / y09_tip1) ** N for y in y_list]
            data['u/u0.9_tip2'] = [(y / y09_tip2) ** N for y in y_list]
    if data:
        df = pd.DataFrame(data)
        st.write('データ表')
        st.dataframe(df)

        if 'y' in df.columns and 'C_tip1' in df.columns:
            buf1 = io.BytesIO()  # バッファ作成
            # y-C散布図をプロット
            fig1, ax = plt.subplots()
            ax.scatter(df['C_tip1'], df['y'], label='C_tip1 vs y')
            ax.set_ylabel('y')
            ax.set_xlabel('C_tip1')
            ax.legend()
            plt.savefig(buf1, format='png')
            buf1.seek(0)
            st.pyplot(fig1)

            st.download_button(
                label="上のグラフをダウンロード",
                data=buf1.getvalue(),
                file_name='y_C_tip1_scatter_plot.png',
                mime='image/png'
            )

        if 'y' in df.columns and 'C_tip2' in df.columns:
            buf2 = io.BytesIO()  # バッファ作成
            # y-C散布図をプロット
            fig2, ax = plt.subplots()
            ax.scatter(df['C_tip2'], df['y'], label='C_tip2 vs y')
            ax.set_ylabel('y')
            ax.set_xlabel('C_tip2')
            ax.legend()
            plt.savefig(buf2, format='png')
            buf2.seek(0)
            st.pyplot(fig2)

            st.download_button(
                label="上のグラフをダウンロード",
                data=buf2.getvalue(),
                file_name='y_C_tip2_scatter_plot.png',
                mime='image/png'
            )

        if 'y/y0.9_tip1' in df.columns and 'C_tip1' in df.columns:
            buf3 = io.BytesIO()  # バッファ作成
            # y/y0.9-Cグラフをプロット
            fig3, ax = plt.subplots()
            ax.scatter(df['C_tip1'], df['y/y0.9_tip1'], label='C_tip1 vs y/y0.9tip_1')
            ax.set_ylabel('y/y0.9_tip1')
            ax.set_xlabel('C_tip1')
            ax.legend()
            plt.savefig(buf3, format='png')
            buf3.seek(0)
            st.pyplot(fig3)
            
            st.download_button(
                label="上のグラフをダウンロード",
                data=buf3.getvalue(),
                file_name='y_y09_tip1_C_tip1_scatter_plot.png',
                mime='image/png'
            )

        if 'y/y0.9_tip2' in df.columns and 'C_tip2' in df.columns:
            buf4 = io.BytesIO()  # バッファ作成
            # y/y0.9-Cグラフをプロット
            fig4, ax = plt.subplots()
            ax.scatter(df['C_tip2'], df['y/y0.9_tip2'], label='C_tip2 vs y/y0.9_tip2')
            ax.set_ylabel('y/y0.9_tip2')
            ax.set_xlabel('C_tip2')
            ax.legend()
            plt.savefig(buf4, format='png')
            buf4.seek(0)
            st.pyplot(fig4)
            
            st.download_button(
                label="上のグラフをダウンロード",
                data=buf4.getvalue(),
                file_name='y_y09_tip2_C_tip2_scatter_plot.png',
                mime='image/png'
            )

        if 'y' in df.columns and 'u' in df.columns:
            buf5 = io.BytesIO()  # バッファ作成
            # y-Uグラフをプロット
            fig5, ax = plt.subplots()
            ax.scatter(df['u'], df['y'], label='u vs y')
            ax.set_ylabel('y')
            ax.set_xlabel('u')
            ax.legend()
            plt.savefig(buf5, format='png')
            buf5.seek(0)
            st.pyplot(fig5)

            st.download_button(
            label="上のグラフをダウンロード",
            data=buf5.getvalue(),
            file_name='y_u_scatter_plot.png',
            mime='image/png'
            )

        if 'y/y0.9_tip1' in df.columns and 'u/u0.9_tip1' in df.columns:
            buf6 = io.BytesIO()  # バッファ作成
            # y/y0.9-u/u0.9グラフをプロット
            fig6, ax = plt.subplots()
            ax.scatter(df['u/u0.9_tip1'], df['y/y0.9_tip1'], label='u/u0.9_tip1 vs y/y0.9_tip1')
            ax.set_ylabel('y/y0.9_tip1')
            ax.set_xlabel('u/u0.9_tip1')
            ax.legend()
            plt.savefig(buf6, format='png')
            buf6.seek(0)
            st.pyplot(fig6)
            
            st.download_button(
            label="上のグラフをダウンロード",
            data=buf6.getvalue(),
            file_name='y_y09_tip1_u_u09_tip1_scatter_plot.png',
            mime='image/png'
            )
            
        if 'y/y0.9_tip2' in df.columns and 'u/u0.9_tip2' in df.columns:
            buf7 = io.BytesIO()  # バッファ作成
            # y/y0.9-u/u0.9グラフをプロット
            fig7, ax = plt.subplots()
            ax.scatter(df['u/u0.9_tip2'], df['y/y0.9_tip2'], label='u/u0.9_tip2 vs y/y0.9_tip2')
            ax.set_ylabel('y/y0.9_tip2')
            ax.set_xlabel('u/u0.9_tip2')
            ax.legend()
            plt.savefig(buf7, format='png')
            buf7.seek(0)
            st.pyplot(fig7)
            
            st.download_button(
            label="上のグラフをダウンロード",
            data=buf7.getvalue(),
            file_name='y_y09_tip2_u_u09_tip2_scatter_plot.png',
            mime='image/png'
            )
    else:
        st.write('値を入力してください')