from chose_phases import *
import pandas as pd
import time
from chose_phases import ask_phases
#import matplotlib.pyplot as plt

@st.cache_data
def koord_spunt(_g_i):
    _g_i.gotostructures()
    koord = []

    try:

        for x in _g_i.Plates[:]:
            plate = x.echo().splitlines()
            line = plate[0].split("on ", 1)[1]
            for y in _g_i.Lines[:]:

                if line == y.info().splitlines()[0]:
                    point_list = y.echo().splitlines()
                    point = point_list[1].split("\"", 2)[1]
                    for z in _g_i.Points[:]:
                        if point == z.info().splitlines()[0]:
                            koord.append(round(z.x.value, 2))

                            time.sleep(0.1)
    except:
        pass

    time.sleep(0.1)
    _g_i.gotostages()
    return koord

def get_plate_results(phases_list, Xplate, g_o):
    ###### henter u_x M,N, V fra plate ###########################################
    plate_Ux_res = []
    plate_Uy_res = []
    plateX_res = []
    plateY_res = []
    plateM_res = []
    plateN_res = []
    plateV_res = []
    plateY_list = []

    for phase in phases_list[0:]:
        # obtain result tables
        plate_Ux = g_o.getresults(phase, g_o.ResultTypes.Plate.Ux, 'node')
        plate_Uy = g_o.getresults(phase, g_o.ResultTypes.Plate.Uy, 'node')
        plateX = g_o.getresults(phase, g_o.ResultTypes.Plate.X, 'node')
        plateY = g_o.getresults(phase, g_o.ResultTypes.Plate.Y, 'node')
        plateM = g_o.getresults(phase, g_o.ResultTypes.Plate.M2D, 'node')
        plateN = g_o.getresults(phase, g_o.ResultTypes.Plate.Nx2D, 'node')
        plateV = g_o.getresults(phase, g_o.ResultTypes.Plate.Q2D, 'node')

        plate_Ux_list = plate_Ux[:]
        plate_Uy_list = plate_Uy[:]
        plateX_list = plateX[:]
        plateY_list = plateY[:]
        plateM_list = plateM[:]
        plateN_list = plateN[:]
        plateV_list = plateV[:]

        plate_Ux_list_2 = []
        plate_Uy_list_2 = []
        plateX_list_2 = []
        plateY_list_2 = []
        plateM_list_2 = []
        plateN_list_2 = []
        plateV_list_2 = []
        for i in range(len(plateX_list)):
            if abs(plateX_list[i] - Xplate) <= 0.0001:
                plate_Ux_list_2.append(plate_Ux_list[i])
                plate_Uy_list_2.append(plate_Uy_list[i])
                plateX_list_2.append(plateX_list[i])
                plateY_list_2.append(plateY_list[i])
                plateM_list_2.append(plateM_list[i])
                plateN_list_2.append(plateN_list[i])
                plateV_list_2.append(plateV_list[i])

                plate_Ux_list_2 = [x for _, x in sorted(zip(plateY_list_2, plate_Ux_list_2))]
                plate_Uy_list_2 = [x for _, x in sorted(zip(plateY_list_2, plate_Uy_list_2))]
                plateX_list_2 = [x for _, x in sorted(zip(plateY_list_2, plateX_list_2))]
                plateM_list_2 = [x for _, x in sorted(zip(plateY_list_2, plateM_list_2))]
                plateN_list_2 = [x for _, x in sorted(zip(plateY_list_2, plateN_list_2))]
                plateV_list_2 = [x for _, x in sorted(zip(plateY_list_2, plateV_list_2))]
                plateY_list_2 = [x for _, x in sorted(zip(plateY_list_2, plateY_list_2))]

        plate_Ux_res.append(plate_Ux_list_2)
        plate_Uy_res.append(plate_Uy_list_2)
        plateX_res.append(plateX_list_2)
        plateY_res.append(plateY_list_2)
        plateM_res.append(plateM_list_2)
        plateN_res.append(plateN_list_2)
        plateV_res.append(plateV_list_2)

    resultater = pd.DataFrame()
    resultater['Y-kordinat'] = plateY_res
    resultater['Ux'] = plate_Ux_res
    resultater['Moment'] = plateM_res
    resultater['Aksial'] = plateN_res
    resultater['shear'] = plateV_res
    return resultater
#    return plateY_res, plate_Ux_res, plateM_res, plateN_res, plateV_res
'''
def plot_results(resultater, i):
    fig, ax1 = plt.subplots()

    ax1.plot(resultater['Ux'][i], resultater['Y-kordinat'][i], color='tab:blue', label='Ux')
    ax1.set_xlabel('Ux')
    ax1.set_ylabel('Y-kordinat', color='tab:blue')

    # Creating the other three y-axes
    offset = 30  # adjust this value as needed
    ax2 = ax1.twiny()
    ax3 = ax1.twiny()
    ax4 = ax1.twiny()

    # Adjusting the positions of the additional y-axes

    ax3.spines['top'].set_position(('outward', offset))
    ax4.spines['top'].set_position(('outward', 2 * offset))

    # Plotting 'Moment', 'Aksial', and 'shear' on their respective y-axes
    ax2.plot(resultater['Moment'][i], resultater['Y-kordinat'][i], color='tab:orange', label='Moment')
    ax2.set_xlabel('Moment', color='tab:orange')

    ax3.plot(resultater['Aksial'][i], resultater['Y-kordinat'][i], color='tab:green', label='Aksial')
    ax3.set_xlabel('Aksial', color='tab:green')

    ax4.plot(resultater['shear'][i], resultater['Y-kordinat'][i], color='tab:red', label='shear')
    ax4.set_xlabel('shear', color='tab:red')


    ax1.legend(loc='best')
    ax2.legend(loc='best')
    ax3.legend(loc='best')
    ax4.legend(loc='best')




    st.pyplot(fig)

    # Show plot
#    plt.show()
'''

def run_spunt_2D(s_o, g_o, s_i, g_i):
    st.title('Plaxis 2D spuntplott')
    col1, col2 = st.columns([0.5, 0.5])

    with st.form("spunt_form"):

        with col1:
            st.header("Velg faser")

            # phases, phase_name =ask_phases(g_o)

            if 'phase_data' not in st.session_state.keys():
                phase_data = [get_phase_screenname(phase) for phase in g_o.Phases[:]]
                st.session_state['dummy_data_phases'] = phase_data
            else:
                phase_data = st.session_state['dummy_data_phases']
            checkbox_container_faser = checkbox_container(phase_data, 'faser')
            phases, phase_name = get_phase_name(get_selected_checkboxes('faser'), g_o)
            save_location_ankerkrefter = st.text_input('mappe for lagring ankerkrefter')

        with col2:
            st.header("Velg spunt")
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
            spunt_data = []
            liste_koordi = koord_spunt(g_i)
            for i in range(len(liste_koordi)):
                spunt_data.append(''.join(str(liste_koordi[i])))

            valgt_spunt = st.selectbox('velg spunt', spunt_data)
            x_plate = float(valgt_spunt)
        submitted_spunt = st.form_submit_button("Hent spuntkrefter og deformasjon")
        if submitted_spunt:

            resultater = get_plate_results(phases, x_plate, g_o)

            #plot_results(resultater)


            #for i in range(len(resultater['Y-kordinat'])):
                #plot_results(resultater, i)






            st.dataframe(resultater, use_container_width=True)





