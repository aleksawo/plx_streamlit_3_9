
from chose_phases import *
import pandas as pd



def koordnode_anchor(g_i):
    g_i.gotostructures()
    x_koord = []
    y_koord = []
    type_anker = []  # 0 = node-to-noide 1 = fixed

    try:
        for x in g_i.NodeToNodeAnchors[:]:
            line_list = x.echo().splitlines()
            line = line_list[0].split("on ", 1)[1]
            for y in g_i.Lines[:]:
                if line == y.info().splitlines()[0]:
                    point_list = y.echo().splitlines()
                    point = point_list[1].split("\"", 2)[1]
                    for z in g_i.Points[:]:
                        if point == z.info().splitlines()[0]:
                            y_koord.append(round(z.y.value, 2))
                            x_koord.append(round(z.x.value, 2))
                            type_anker.append('node-to-node')
    except:
        pass
    try:
        for x in g_i.FixedEndAnchors[:]:
            point_list = x.echo().splitlines()
            point = point_list[0].split("on ", 1)[1]

            for z in g_i.Points[:]:
                if point == z.info().splitlines()[0]:
                    y_koord.append(round(z.y.value, 2))
                    x_koord.append(round(z.x.value, 2))
                    type_anker.append('fixed-end')
    except:
        pass

    koordinates = list(zip(x_koord, y_koord, type_anker))
    msg = 'Select one or more anchors to get results for (X,Y-coordinates, type of anchor)'
    # issue with easygui 0.97.4: multchoicebox acts as choicebox
    read = easygui.multchoicebox(msg=msg,
                                 title="name",
                                 choices=koordinates)
    x_kord = []
    y_kord = []
    type_anker_2 = []
    for i in range(len(read)):
        x_kord.append(float(read[i].strip('(').strip(')').split(", ")[0]))
        y_kord.append(float(read[i].strip('(').strip(')').split(", ")[1]))
        type_anker_2.append(read[i].strip('(').strip(')').split(", ")[2])
    g_i.gotostages()

    return x_kord, y_kord, type_anker_2


## #################################################################kjører spørsmål om stivernivåer, x,y kordinater og faser

x_kord, y_kord, type_anker = koordnode_anchor()

anchor_force = []
phase_list_names = []
phases_list = []
phases_list, phase_list_names = ask_phases()

## ###########################lager variabler for plassering av stiverkrefter og lagring av faser- relativ dårlig løsning, burde kunne forbedre

stivere = []

anchorF_res = []
anchorX_res = []
anchorY_res = []
# anchorF_fix_res=[]
# anchorX_fix_res=[]
# anchorY_fix_res=[]

################################################################ get anchor force og plasserer de i riktig variabel
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

resultater_node.to_clipboard(index=True)

msg = "Tabell med resultater fra ankerene er kopiert til clippboard"
choices = ["Ikke trykk Ok før limt inn i excel"]
reply = buttonbox(msg, choices=choices)

'''  
###################################
ym0=1.05
ym1=1.05
ym2=1.25
L=15.5
L_k=L
b=15.5
fy=355000  #kPa
E=210000000 #kPa

rør='Ø610x12,5'

t=rørstiver.loc[rør,'t (mm)']
I=rørstiver.loc[rør,'I (cm4)']
A=rørstiver.loc[rør,'A (cm2)']
alfa=rørstiver.loc[rør,'alfa (-)']
vekt=rørstiver.loc[rør,'w (kN/m)']
V_pl_rd=rørstiver.loc[rør,'Vpl,Rd (kN)']
Wy=rørstiver.loc[rør,'Wpl (cm3)']

Ncr=math.pi**2*E*I/(L_k**2*100**4)
lamba_=(A*fy/(Ncr*100**2))**0.5
tetha=0.5*(1+alfa*(lamba_-0.2)+lamba_**2)
shi=min((1/(tetha+(tetha**2-lamba_**2)**0.5)),1)
#shi=shi.clip(upper=1)

M=L**2*vekt/8
V=L*vekt/2

if V>0.5*V_pl_rd:
    rho=2*V/V_pl_rd
else:
    rho=0
fy_red=(1-rho)*fy
N_b_Rd=shi*A*fy_red/(ym1*100**2)
M_cr
lamba_LT=(Wy*fy/M_cr)**0.5
alfa_LT=0.76

'''


