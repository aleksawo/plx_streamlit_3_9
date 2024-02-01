
import streamlit as st
from plxscripting.easy import *
import pandas as pd
import os
from chose_phases import *


def run_plaxis_model_plotter(s_o, g_o, s_i, g_i):
    st.title('Plaxis 2D plotter')
    col1, col2 = st.columns([0.5, 0.5])

    with st.form("my_form"):
        with col1:
            st.header("Velg faser")
            #    phases, phase_name = ask_phases()

            if 'phase_data' not in st.session_state.keys():
                phase_data = [get_phase_screenname(phase) for phase in g_o.Phases[:]]
                st.session_state['dummy_data'] = phase_data
            else:
                phase_data = st.session_state['dummy_data']
            checkbox_container_faser = checkbox_container(phase_data, 'faser')

            # st.write('You selected:')
            # st.write(get_selected_checkboxes())

            phases, phase_name = get_phase_name(get_selected_checkboxes('faser'), g_o)

            # st.write(phase_name)

            save_location = st.text_input('mappe for lagring plott')
        # save_location= r'C:\Users\alew\Documents\Jobbting\Plaxis\Test_plott'

        # type_plot = st.multiselect('Velg plott', ['Utot','U_inc',3])



        with col2:
            type_plot = st.multiselect('Velg plot', ['U_tot', 'U_inc', 'delta_y_s', 'tot_y_s'])

            brukerdefinert_zoom = st.checkbox('Brukerdefinert zoom på plottene')
            if brukerdefinert_zoom:
                st.markdown(
                    'Skriv inn 2 kordinater som angir kvadrated som skal plottes - ofte y1 og y2 som styrer zoom nivå, og snitt av x1 og x2 blir senter')
                col5, col6, col7, col8 = st.columns([0.25, 0.25, 0.25, 0.25])

                with col5:
                    x1 = st.number_input('x_1')
                with col6:
                    y1 = st.number_input('y_1 ')
                with col7:
                    x2 = st.number_input('x_2')
                with col8:
                    y2 = st.number_input('y_2')

        submitted = st.form_submit_button("Plott faser")

        if submitted:
            # g_o.Plots[-1].zoom(-10, 10, 10, 40)
            os.chdir(save_location)

            for plot_type in type_plot:
                if plot_type == 'U_tot':
                    result_type = g_o.ResultTypes.Soil.Utot
                elif plot_type == 'U_inc':
                    result_type = g_o.ResultTypes.Soil.dUtot
                elif plot_type == 'delta_y_s':
                    result_type = g_o.ResultTypes.Soil.IncrementalDeviatoricStrain
                elif plot_type == 'tot_y_s':
                    result_type = g_o.ResultTypes.Soil.TotalDeviatoricStrain

                for phase in phases[0:]:
                    newest_plot = g_o.Plots[-1]
                    newest_plot.Phase = g_o.Phases[int(phase.Number.echo().split(' ')[-1])]
                    newest_plot.ResultType = result_type
                    newest_plot.PlotType = 'shadings'
                    max_value_result_type = max(g_o.getresults(phase, result_type, 'node'))
                    newest_plot.LegendSettings.MaxValue = max_value_result_type
                    name_plot = save_location + '''//''' + phase.Identification.value + '_' + plot_type + '.png'
                    if brukerdefinert_zoom:
                        newest_plot.zoom(x1, y1, x2, y2)
                    newest_plot.export(name_plot, 1200, 800)
                    st.image(phase.Identification.value + '_' + plot_type + '.png')


            '''
            if 'Utot' in type_plot:
                for phase in phases[0:]:
                    newest_plot = g_o.Plots[-1]
                    newest_plot.Phase = g_o.Phases[int(phase.Number.echo().split(' ')[-1])]
                    newest_plot.ResultType = g_o.ResultTypes.Soil.Utot
                    newest_plot.PlotType = 'shadings'
                    max_disp = max(g_o.getresults(phase, g_o.ResultTypes.Soil.Utot, 'node'))
                    newest_plot.LegendSettings.MaxValue = max_disp
                    name_plot = save_location + '''//''' + phase.Identification.value + '_Utot.png'
                    #    name_plot = phase.Identification.value + '_Utot.png'
                    if brukerdefinert_zoom:
                        newest_plot.zoom(x1, y1, x2, y2)

                    newest_plot.export(name_plot, 1200, 800)
                    st.image(phase.Identification.value + '_Utot.png')
                    # st.image(name_plot)

            if 'U_inc' in type_plot:
                for phase in phases[0:]:
                    newest_plot = g_o.Plots[-1]
                    newest_plot.Phase = g_o.Phases[int(phase.Number.echo().split(' ')[-1])]
                    newest_plot.ResultType = g_o.ResultTypes.Soil.dUtot
                    newest_plot.PlotType = 'shadings'
                    max_disp = max(g_o.getresults(phase, g_o.ResultTypes.Soil.dUtot, 'node'))
                    newest_plot.LegendSettings.MaxValue = max_disp
                    name_plot = save_location + '''//''' + phase.Identification.value + '_Uinc.png'
                    #    name_plot = phase.Identification.value + '_Utot.png'
                    if brukerdefinert_zoom:
                        newest_plot.zoom(x1, y1, x2, y2)
                    newest_plot.export(name_plot, 1200, 800)
                    st.image(phase.Identification.value + '_Uinc.png')
                    # st.image(name_plot)

            if 'delta_y_s' in type_plot:
                for phase in phases[0:]:
                    newest_plot = g_o.Plots[-1]
                    newest_plot.Phase = g_o.Phases[int(phase.Number.echo().split(' ')[-1])]
                    newest_plot.ResultType = g_o.ResultTypes.Soil.IncrementalDeviatoricStrain
                    newest_plot.PlotType = 'shadings'
                    max_disp = max(g_o.getresults(phase, g_o.ResultTypes.Soil.IncrementalDeviatoricStrain, 'node'))
                    newest_plot.LegendSettings.MaxValue = max_disp
                    name_plot = save_location + '''//''' + phase.Identification.value + '_delta_y_s.png'
                    #    name_plot = phase.Identification.value + '_Utot.png'
                    if brukerdefinert_zoom:
                        newest_plot.zoom(x1, y1, x2, y2)
                    newest_plot.export(name_plot, 1200, 800)
                    st.image(phase.Identification.value + '_delta_y_s.png')
                    # st.image(name_plot)

            if 'tot_y_s' in type_plot:
                for phase in phases[0:]:
                    newest_plot = g_o.Plots[-1]
                    newest_plot.Phase = g_o.Phases[int(phase.Number.echo().split(' ')[-1])]
                    newest_plot.ResultType = g_o.ResultTypes.Soil.TotalDeviatoricStrain
                    newest_plot.PlotType = 'shadings'
                    max_disp = max(g_o.getresults(phase, g_o.ResultTypes.Soil.TotalDeviatoricStrain, 'node'))
                    newest_plot.LegendSettings.MaxValue = max_disp
                    name_plot = save_location + '''//''' + phase.Identification.value + '_tot_y_s.png'
                    #    name_plot = phase.Identification.value + '_Utot.png'
                    if brukerdefinert_zoom:
                        newest_plot.zoom(x1, y1, x2, y2)
                    newest_plot.export(name_plot, 1200, 800)
                    st.image(phase.Identification.value + '_tot_y_s.png')
                    # st.image(name_plot)
            '''











