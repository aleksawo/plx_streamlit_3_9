
from chose_phases import *
import pandas as pd
import time
from chose_phases import ask_phases


@st.cache_data
def koordnode_anchor(_g_i):
    _g_i.gotostructures()
    x_koord = []
    y_koord = []
    type_anker = []  # 0 = node-to-noide 1 = fixed
    try:
        for x in _g_i.NodeToNodeAnchors[:]:
            line_list = x.echo().splitlines()
            line = line_list[0].split("on ", 1)[1]
            for y in _g_i.Lines[:]:
                if line == y.info().splitlines()[0]:
                    point_list = y.echo().splitlines()
                    point = point_list[1].split("\"", 2)[1]
                    for z in _g_i.Points[:]:
                        if point == z.info().splitlines()[0]:
                            y_koord.append(round(z.y.value, 2))
                            x_koord.append(round(z.x.value, 2))
                            type_anker.append('node-to-node')
                            time.sleep(0.1)
    except:
        pass
    try:
        for x in _g_i.FixedEndAnchors[:]:
            point_list = x.echo().splitlines()
            point = point_list[0].split("on ", 1)[1]

            for z in _g_i.Points[:]:
                if point == z.info().splitlines()[0]:
                    y_koord.append(round(z.y.value, 2))
                    x_koord.append(round(z.x.value, 2))
                    type_anker.append('fixed-end')
    except:
        pass
    time.sleep(0.1)
    koordinates = list(zip(x_koord, y_koord, type_anker))
    _g_i.gotostages()
    return koordinates
def split_koordinates(chosen_anchors, g_i):
    x_kord = []
    y_kord = []
    type_anker_2 = []

    for i in range(len(chosen_anchors)):
        x_kord.append(float(chosen_anchors[i].strip('(').strip(')').split(", ")[0]))
        y_kord.append(float(chosen_anchors[i].strip('(').strip(')').split(", ")[1]))
        type_anker_2.append(chosen_anchors[i].strip('(').strip(')').split(", ")[2])
    g_i.gotostages()

    return x_kord, y_kord, type_anker_2

def run_ankerkrefter_2D(s_o, g_o, s_i, g_i):
    st.title('Plaxis 2D ankerkrefter')
    col1, col2 = st.columns([0.5, 0.5])

    with st.form("ankerkrefter_form"):


        with col1:
            st.header("Velg faser")

            #phases, phase_name =ask_phases(g_o)

            if 'phase_data' not in st.session_state.keys():
                phase_data = [get_phase_screenname(phase) for phase in g_o.Phases[:]]
                st.session_state['dummy_data_phases'] = phase_data
            else:
                phase_data = st.session_state['dummy_data_phases']
            checkbox_container_faser=checkbox_container(phase_data, 'faser')
            phases, phase_name = get_phase_name(get_selected_checkboxes('faser'), g_o)
            save_location_ankerkrefter = st.text_input('mappe for lagring ankerkrefter')

        with col2:
            st.header("Velg ankere")
            '''
            if 'anker_data' not in st.session_state.keys():
                anker_data = []
                liste_koordi = koordnode_anchor(g_i)
                for i in range(len(liste_koordi)):
                    anker_data.append(''.join(str(liste_koordi[i])))
    
                
    
                #            anker_data = [koordnode_anchor(g_i)]
                st.session_state['dummy_data_anker'] = anker_data
                            
            else:
                anker_data = st.session_state['dummy_data_anker']
            '''
            anker_data = []
            liste_koordi = koordnode_anchor(g_i)
            for i in range(len(liste_koordi)):
                anker_data.append(''.join(str(liste_koordi[i])))

            valgt_anker = st.multiselect('velg ankere', anker_data)
        submitted_anker = st.form_submit_button("Hent ankerkrefter")
        if submitted_anker:




            #checkbox_container_ankere = checkbox_container(anker_data, 'ankere')
            x_kord, y_kord, type_anker = split_koordinates(valgt_anker, g_i)

            anchor_force = []
            phase_list_names = phase_name
            phases_list = phases

            stivere = []
            anchorF_res = []
            anchorX_res = []
            anchorY_res = []

            for phase in phases_list[0:]:
                #    phase_list_names.append("{}".format(phase.Name))
                anchorF_list_2 = []
                anchorX_list_2 = []
                anchorY_list_2 = []
                #    anchorF_fix_list_2=[]
                #    anchorX_fix_list_2=[]
                #    anchorY_fix_list_2=[]
                for i in range(len(x_kord)):
                    if ('node-to-node') in type_anker[i]:
                        try:
                            anchorF = g_o.getresults(phase, g_o.ResultTypes.NodeToNodeAnchor.AnchorForce2D, 'node')
                            anchorX = g_o.getresults(phase, g_o.ResultTypes.NodeToNodeAnchor.X, 'node')
                            anchorY = g_o.getresults(phase, g_o.ResultTypes.NodeToNodeAnchor.Y, 'node')
                            anchorF_list = anchorF[:]
                            anchorX_list = anchorX[:]
                            anchorY_list = anchorY[:]

                            if y_kord[i] in anchorY_list:
                                for j in range(len(anchorY_list)):
                                    if anchorY_list[j] == y_kord[i] and abs(anchorX_list[j] - x_kord[i]) <= 0.0001:
                                        anchorF_list_2.append(anchorF_list[j])
                                        anchorX_list_2.append(anchorX_list[j])
                                        anchorY_list_2.append(anchorY_list[j])
                            else:
                                anchorF_list_2.append(0)
                                anchorX_list_2.append(x_kord[i])
                                anchorY_list_2.append(y_kord[i])

                        except:
                            anchorF_list_2.append(0)
                            anchorX_list_2.append(x_kord[i])
                            anchorY_list_2.append(y_kord[i])
                    else:
                        try:
                            anchorF_fix = g_o.getresults(phase, g_o.ResultTypes.FixedEndAnchor.AnchorForce2D, 'node')
                            anchorX_fix = g_o.getresults(phase, g_o.ResultTypes.FixedEndAnchor.X, 'node')
                            anchorY_fix = g_o.getresults(phase, g_o.ResultTypes.FixedEndAnchor.Y, 'node')
                            anchorF_fix_list = anchorF_fix[:]
                            anchorX_fix_list = anchorX_fix[:]
                            anchorY_fix_list = anchorY_fix[:]
                            if y_kord[i] in anchorY_fix_list:
                                for j in range(len(anchorY_fix_list)):
                                    if anchorY_fix_list[j] == y_kord[i] and abs(anchorX_fix_list[j] - x_kord[i]) <= 0.0001:
                                        anchorF_list_2.append(anchorF_fix_list[j])
                                        anchorX_list_2.append(anchorX_fix_list[j])
                                        anchorY_list_2.append(anchorY_fix_list[j])
                            else:
                                anchorF_list_2.append(0)
                                anchorX_list_2.append(x_kord[i])
                                anchorY_list_2.append(y_kord[i])

                        except:
                            anchorF_list_2.append(0)
                            anchorX_list_2.append(x_kord[i])
                            anchorY_list_2.append(y_kord[i])

                anchorF_res.append(anchorF_list_2)
                anchorX_res.append(anchorX_list_2)
                anchorY_res.append(anchorY_list_2)

            ######################################lager variabel for endelig tabell

            resultater_node = pd.DataFrame(index=phase_list_names)
            for l in range(len(x_kord)):
                stiver = 'Stiver ' + str(l + 1) + ' (' + str(x_kord[l]) + ', ' + str(y_kord[l]) + ') ' + '[kN]'
                resultater_node[stiver] = 0
            for i in range(len(phases_list)):
                for l in range(len(x_kord)):
                    stiver = 'Stiver ' + str(l + 1) + ' (' + str(x_kord[l]) + ', ' + str(y_kord[l]) + ') ' + '[kN]'
                    resultater_node[stiver][i] = anchorF_res[i][l]

            filname = save_location_ankerkrefter + '''//''' + 'ankerkrefter.xlsx'
            resultater_node.to_excel(filname)

            st.dataframe(resultater_node, use_container_width=True)



    #       resultater_node.to_clipboard(index=True)



