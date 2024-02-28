from chose_phases import *
import pandas as pd
import time
from chose_phases import *
import matplotlib.pyplot as plt
from plxscripting.easy import *
import numpy as np
import math

@st.cache_data
def koord_spunt(pw, port_num, port_num_output):
    s_o, g_o, s_i, g_i = start_server(pw, port_num, port_num_output)
    g_i.gotostructures()
    koord = []
    try:
        for x in g_i.Plates[:]:
            plate = x.echo().splitlines()
            line = plate[0].split("on ", 1)[1]
            for y in g_i.Lines[:]:

                if line == y.info().splitlines()[0]:
                    point_list = y.echo().splitlines()
                    point = point_list[1].split("\"", 2)[1]
                    for z in g_i.Points[:]:
                        if point == z.info().splitlines()[0]:
                            koord.append(round(z.x.value, 2))
                            time.sleep(0.1)
    except:
        pass

    time.sleep(0.1)
    g_i.gotostages()
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
#                plate_Ux_list_2.append(plate_Ux_list[i])
                plate_Ux_list_2.append(plate_Ux_list[i]*100)
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
 #   resultater['Ux_cm']=resultater['Ux'].multiply(100)
    return resultater
#    return plateY_res, plate_Ux_res, plateM_res, plateN_res, plateV_res

def round_up(number):
  """Rounds a number up to the nearest specified value based on its range.

  Args:
      number: The number to be rounded.

  Returns:
      The rounded number.
  """
  if 0 <= number <= 100:
    return math.ceil(number / 10) * 10  # Round up to nearest 10th [[1](https://realpython.com/python-rounding/)]
  elif 100 <= number <= 300:
    return math.ceil(number / 20) * 20  # Round up to nearest 20th
  elif 300 <= number <= 800:
    return math.ceil(number / 50) * 50  # Round up to nearest 50
  else:
    return math.ceil(number / 100) * 100  # Round up to nearest 100



def plot_results_separate(resultater, i, phase_name, save_location, spacing_dybde=1, figsize=(6, 10)):

    quantities = {'Ux', 'Moment', 'Aksial', 'shear'}
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']

    label = ['Aksial (kN)', 'Skjær (kN)', 'Ux (cm)', 'Moment (kNm)']

    # Create figure and subplots (2 rows, 2 columns)
    fig, axs = plt.subplots(2, 2, figsize=figsize)

    max_values = {quantity: np.abs(resultater[quantity][i]).max().round(1) for quantity in quantities}

    # Iterate through quantities and subplots
    for (j, quantity), ax, color, label in zip(enumerate(quantities), axs.flat, colors, label):
        y = resultater['Y-kordinat'][i]
        x = resultater[quantity][i]

#        max_val_str = f"{quantity}: {max_values[quantity]}"
#        max_val_str = f"{max_values[quantity]}"
        max_val_str = f"maks: {max_values[quantity]}"

        # Plot on the current subplot
        ax.plot(x, y, color=color, label=quantity+' '+max_val_str)

        # Customize labels and grid
        ax.set_xlabel(label)
        ax.set_ylabel('Y-kordinat')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend(loc='best')
        locator = plt.MultipleLocator(spacing_dybde)
        ax.yaxis.set_major_locator(locator)
        ax.set_xticks(np.linspace(-round_up(abs(min(x))), round_up(max(x)), 5))

        # Optional annotations for max values (you can add them)
        # ...

    # Adjust layout and show
    plt.tight_layout()
    plt.suptitle(phase_name[i])
    plt.subplots_adjust(top=0.95)

    st.pyplot(fig)
    name_plot = save_location + '''//''' + phase_name[i] + '' + '.png'
    plt.savefig(name_plot)


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

def start_server(pw, port_num, port_num_output):
    s_o, g_o = new_server('localhost', port_num_output, password=pw)
    s_i, g_i = new_server('localhost', port_num, password=pw)
    return s_o, g_o, s_i, g_i

def run_spunt_2D():
    st.title('Plaxis 2D spuntplott')

    if st.button("Clear Cache - Trykk for ny modell"):
        koord_spunt.clear()  # Properly clears the cache of my_function
        get_phase_data_list.clear()

    col1, col2 = st.columns([0.5, 0.5])

    with st.form("spunt_form"):
        with st.sidebar:
            # pw = st.text_input('input plaxis passord')
            pw = '?GBz75iy^BwZy/2Y'  # input("Passord for remote scripting server: ")
            port_num = st.number_input('port input', value=10000)
            port_num_output = st.number_input('port output', value=10001)

        phase_data = get_phase_data_list(pw, port_num, port_num_output)
        liste_koordi = koord_spunt(pw, port_num, port_num_output)

        with col1:

            st.header("Velg faser")

            if 'phase_data' not in st.session_state.keys():
                st.session_state['dummy_data_phases'] = phase_data
            else:
                phase_data = st.session_state['dummy_data_phases']
            checkbox_container_faser = checkbox_container(phase_data, 'faser')

            save_location_spuntplot = st.text_input('mappe for lagring av plott')

        with col2:
            st.header("Velg spunt")

            spunt_data = []
            for i in range(len(liste_koordi)):
                spunt_data.append(''.join(str(liste_koordi[i])))

            valgt_spunt = st.selectbox('velg spunt', spunt_data)
            x_plate = float(valgt_spunt)

        submitted_spunt = st.form_submit_button("Hent spuntkrefter og deformasjoner")

        if submitted_spunt:
            s_o, g_o, s_i, g_i = start_server(pw, port_num, port_num_output)
            phases, phase_name = get_phase_name(get_selected_checkboxes('faser'), g_o)

            resultater = get_plate_results(phases, x_plate, g_o)

            #resultater['Ux']=resultater['Ux'].mul(100)

            #plot_results(resultater)


            for i in range(len(resultater['Y-kordinat'])):
                #plot_results(resultater, i)
                plot_results_separate(resultater, i, phase_name, save_location_spuntplot, spacing_dybde=1, figsize=(6, 10))



            st.dataframe(resultater, use_container_width=True)





