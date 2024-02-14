import streamlit as st
from plxscripting.easy import *
import pandas as pd
import os
from plaxis_2D_plotter import run_plaxis_model_plotter
from  ankerkrefter_2D import run_ankerkrefter_2D
from spunt_2D_plotter import run_spunt_2D

#streamlit run your_script.py --server.port 80


#tab1, tab2 = st.tabs(["Plott modell", "Hent ankerkrefter"])
#host.docker.internal
def start_server(pw, port_num, port_num_output):
    s_o, g_o = new_server('localhost', port_num_output, password=pw)
    s_i, g_i = new_server('localhost', port_num, password=pw)
    return s_o, g_o, s_i, g_i
#http://host.docker.internal:PORT/ENDPOINT
#requests.get("http://host.docker.internal:PORT/ENDPOINT")
#'http://host.docker.internal'
#'host.docker.internal'




option = st.selectbox('Velg funksjon', ('2D plotter', 'ankerkrefter', 'spunt krefter'))

#st.write('You selected:', option)

if '2D plotter' in option:
    run_plaxis_model_plotter()

if 'ankerkrefter' in option:
    run_ankerkrefter_2D()

if 'spunt krefter' in option:
    run_spunt_2D()



