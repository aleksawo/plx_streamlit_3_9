import streamlit as st
from plxscripting.easy import *
import pandas as pd
import os
from plaxis_2D_plotter import run_plaxis_model_plotter
#streamlit run your_script.py --server.port 80


tab1, tab2 = st.tabs(["Plott modell", "Hent ankerkrefter"])


with st.sidebar:
    pw = st.text_input('input plaxis passord')
    #pw='?GBz75iy^BwZy/2Y'#input("Passord for remote scripting server: ")
    port_num = st.number_input('port input',value=10000)
    port_num_output = st.number_input('port output',value=10001)
    s_o, g_o = new_server('host.docker.internal', port_num_output, password=pw)
    s_i, g_i = new_server('host.docker.internal', port_num, password=pw)


with tab1:
    run_plaxis_model_plotter(s_o, g_o, s_i, g_i)
