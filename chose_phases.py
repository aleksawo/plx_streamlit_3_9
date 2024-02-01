
import streamlit as st




def project_title(g_i):
    proj_info = g_i.echo()
    proj_info_list = proj_info.splitlines()
    proj_title = proj_info_list[1].split("Title: ", 1)[1]
    proj_title = proj_title[1:-1]
    return proj_title

def get_phase_screenname(_phase):
    return '{} - {}'.format(_phase.Name.value, _phase.Identification.value.split('[')[0].strip())


def checkbox_container(data, string_selection):
    cols = st.columns(3)
    if cols[0].button('Select All'+' '+string_selection):
        for i in data:
            st.session_state[string_selection + i] = True
        st.experimental_rerun()
    if cols[1].button('UnSelect All'+ ' '+string_selection):
        for i in data:
            st.session_state[string_selection + i] = False
        st.experimental_rerun()
    for i in data:
        st.checkbox(i, key=string_selection + i)



    return checkbox_container

def get_selected_checkboxes(string_selection):
    return [i.replace(string_selection ,'') for i in st.session_state.keys() if i.startswith(string_selection) and st.session_state[i]]

def get_phase_name(phasechoices, _g_o):
    phase_list_names = []
    phaselist = []
    if phasechoices:
        for phase in _g_o.Phases[:]:
            if get_phase_screenname(phase) in phasechoices:
                phaselist.append(phase)
                phase_list_names.append(phase.Identification.value)

    phases = phaselist[:]
    phase_name = phase_list_names[:]
    return phases, phase_name

def ask_phases(g_o):
    """ asks the user to specify the phase to get the results for """
    # at first, just one phase, but can be expanded to more phases
    phaselist = []
    choicelist = [get_phase_screenname(phase) for phase in g_o.Phases[:]]
    msg = 'Select one or more phases to generate plate results for'
    # issue with easygui 0.97.4: multchoicebox acts as choicebox
    phasechoices = st.multiselect('select phases', choicelist)

    phase_list_names = []
    phaselist = []
    if phasechoices:
        for phase in g_o.Phases[:]:
            if get_phase_screenname(phase) in phasechoices:
                phaselist.append(phase)
                phase_list_names.append(phase.Identification.value)
    phases = phaselist[:]
    phase_name = phase_list_names[:]
    return phases, phase_name