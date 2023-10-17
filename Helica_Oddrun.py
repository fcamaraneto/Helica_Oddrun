import streamlit as st
from PIL import Image # create page icon

import pandas as pd
import numpy as np
#import scipy.io as spio
#import scipy.special as spios
#import plotly.express as px
#import plotly.graph_objects as go

# shortcuts
divide = np.divide
pi = np.pi
log = np.log
sqrt = np.sqrt
print = st.markdown

#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
#                                     SETTINGS
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
icon=Image.open('dnv_logo.jpg')
st.set_page_config(page_title="HELICA Multiphysics", layout="centered", page_icon=icon)

#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
#                                     SIDEBAR
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.postimg.cc/wvSYBKsj/DNV-logo-RGB-Small.png);
                background-repeat: no-repeat;
                margin-left: 20px;
                padding-top: 100px;
                background-position: 1px 1px;
            }
            [data-testid="stSidebarNav"]::before {
              # content: "My Company Name";
              #  margin-left: 2px;
              #  margin-top: 2px;
              #  font-size: 3px;
              #  position: relative;
              #  top: 1px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

url='https://i.postimg.cc/NjhVmdYR/helica-logo.png'

st.markdown(f"""
        <style>
            [data-testid="stSidebarNav"] + div {{
                position:relative;
                bottom: 0;
                height:60%;
                background-image: url({url});
                background-size: 40% auto;
                background-repeat: no-repeat;
                background-position-x: center;
                background-position-y: bottom;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# '📊 📉 📈 📧 🗂️ 📂 📈  🖥️🗄️  '

add_logo()
#st.sidebar.image('aau_logo.png', width=150)

#st.sidebar.markdown("HELICA Cable Rating module complies with IEC 60287 and IEC 60949 ... ")

#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
#                                     INPUT DATA
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
st.title("Current Rating")
#st.title("Interface")
#st.markdown('The Cable Rating module ... ')
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
tab1, tab2, tab3, tab5 = st.tabs([
    "🖥️ Cross-Section", "🖥️ Design Basis", "📊 Current Rating", "Report"])
    #"📊 Electrical Parameters", "Export Parameters"])
#tab1, tab2, tab3, tab4, tab5 = st.tabs([
#    "🖥️ Design Basis", "🖥️ Cable Design", "🖥️ Cross-Section", "🖥️ Current Rating",
#    "🖥️ Electrical Parameters"])

#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
#  1 - DESIGN BASIS
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
with tab2: #1-DESIGN BASIS

    col0, col1, col2, col3 = st.columns([.75, .75, .9, .75])
    with col0:
        '**SYSTEM DATA**'
    with col1:
        '**RATED VOLTAGE**'
        U_temp = st.number_input('Design Voltage [kV]', format="%.1f", value=30., step=10., min_value=0.001)
        U0 = U_temp * 1e3 / sqrt(3)
    with col2:
        '**TYPE OF SYSTEM**'
        system = st.selectbox("Cable Type", options=["HVAC Three-core"]) #, "HVAC Single-Core", "HVDC Single-Core"])
    with col3:
        '**FREQUENCY**'
        if system != 'HVDC Single-Core':
            freq = st.selectbox("System Frequency (Hz)", options=["50 Hz"])#, "60 Hz"])
        else:
            freq = st.selectbox("System Frequency (Hz)", options=["0 Hz - DC"])
        if freq == "50 Hz":
            f = 50
        if freq == "60 Hz":
            f = 60
        if freq == "0 Hz - DC":
            f = 0
        omega = 2 * pi * f
    line = st.write("-" * 34)  # horizontal separator line




    # '**INSTALLATION CONDITIONS**'
    col0, col1, col2, col3 = st.columns([1.25, 1.1, 1, 1.])
    with col0:
        '**OPERATION CONDITIONS**'
    with col1:
        '**INSTALLATION**'
        x1 = st.selectbox("Installation Method", options=["Buried"])#, 'On the Seabed', 'J-Tube'])
        x2 = st.selectbox("External Media", options=["Seabed"])#, "Sea", 'Air', "Soil"])
    with col2:
        '**BURRIAL DEPTH**'
        L_temp = st.number_input('L [m]', format="%.2f", value=1., step=1., min_value=.001)
        L_burrial = L_temp
    with col3:
        '**TEMPERATURE**'
        theta_0 = st.number_input('Ambient Temp. [°C]', format="%.1f", value=15., step=.1, min_value=.001)
        theta_1 = st.number_input('Operation Temp. [°C]', format="%.1f", value=90., step=1.)
        theta_2 = st.number_input('Maximum Temp. [°C]', format="%.1f", value=250., step=1.)
    line = st.write("-" * 34)  # horizontal separator line

#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
#  2 - CROSS-SECTION
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
with tab1: #2-CROSS-SECTION

    layer3c = ['Conductor', 'Tape', 'Conductor Screen', 'Insulation', 'Insulation Screen', 'Water blocking', 'Swelling tape', '', '', '']
    layer3s = ['Conductor', 'Sheath Screen', 'Bedding', 'Swelling tape', 'Insulation', 'Insulation Screen', 'Water blocking']
    layer3a = ['Fillers', 'Binding', 'Bedding', 'Conductor', 'Cover', '', '', '']

    conductors = ['', 'Copper', 'Lead', 'Steel', 'Aluminum']
    materials = ['', 'Polyethylene', 'XLPE', 'Polypropylene', 'PVC']

    conductors_core = ['Copper', 'Lead', 'Steel', 'Aluminum']
    materials_core = ['', 'Polyethylene', 'Polyethylene', 'XLPE', 'Polyethylene', 'Polyethylene', 'Polypropylene', '', '', '', '', '', '', '']
    conductors_sheath = ['Lead', 'Copper', 'Steel', 'Aluminum']
    materials_sheath = ['Polyethylene', 'Polyethylene', 'Polyethylene', 'Polyethylene', 'Polypropylene', '', '', '', '', '', '', '', '']
    conductors_armour = ['Steel', 'Steel', '', '', '']
    materials_armour = ['Polypropylene', 'Polypropylene', 'Polypropylene', '', 'Polypropylene', '', '', '', '', '', '', '', '']



    core_240mm = [18.1, 18.6, 20.6, 38.6, 40.4, 42.6, 0.001]
    sheath_240mm = [47.1, 52.2, 0.001]
    armour_240mm = [125.0, 125.4, 127.4, 139.4, 145.4, 0.001]

    core_300mm = [20.4, 20.9, 22.9, 40.9, 42.7, 44.9, 0.001]
    sheath_300mm = [49.4, 54.5, 0.001]
    armour_300mm = [127.3, 127.7, 129.7, 141.7, 147.7, 0.001]


    core_400mm = [23.2, 23.7, 25.7, 43.7, 45.5, 47.7, 0.001]
    sheath_400mm = [52.2, 57.3, 0.001]
    armour_400mm = [130.1, 130.5, 132.5, 144.5, 150.5, 0.001]

    core_500mm = [26.2, 26.7, 28.7, 46.7, 48.5, 50.7, 0.001]
    sheath_500mm = [55.2, 60.3, 0.001]
    armour_500mm = [133.1, 133.5, 135.5, 147.5, 153.5, 0.001]

    core_630mm =   [  30.0,  30.5,  32.5,  48.5,  50.3,  52.5, 0.001]#, 0.001, 0.001, 0.001, 0.001, 0.001]
    sheath_630mm = [  57.1,  62.1, 0.001]#, 0.001, 0.001, 0.001, 0.001]
    armour_630mm = [ 134.9, 135.3, 137.3, 149.3, 155.3, 0.001]#, 0.001, 0.001, 0.001]

    core_800mm =   [  33.7,  34.2,  36.2,  54.2,  56.0,  58.2, 0.001]#, 0.001, 0.001, 0.001, 0.001, 0.001]
    sheath_800mm = [  62.7,  67.8, 0.001]#, 0.001, 0.001, 0.001, 0.001]
    armour_800mm = [ 140.6, 141.0, 143.0, 155.0, 161.0]#, 0.001, 0.001, 0.001, 0.001]

    core_1000mm =   [  37.9,  38.4,  40.4,  58.4,  60.2,  62.4, 0.001]#, 0.001, 0.001, 0.001, 0.001, 0.001]
    sheath_1000mm = [  66.9,  72.0, 0.001]#, 0.001, 0.001, 0.001, 0.001]
    armour_1000mm = [ 144.8, 145.2, 147.2, 159.2, 165.2]#, 0.001, 0.001, 0.001, 0.001]



    cols1 = [.7, 1, 1, 1]
    cols0 = [.5, .7, 1.1, .8, 1]


    col1, col2, col3 = st.columns([.4,.3,.6])
    with col1:
        #'**CROSS-SECTION AREA**'
        #''
        #''
        #'SELECT CABLE TYPE:'
    #with col1:
        type = st.selectbox("SELECT CABLE TYPE:",
                            options=["3 x 240 mm2", "3 x 300 mm2",  "3 x 400 mm2",  "3 x 500 mm2",
                                     "3 x 630 mm2", "3 x 800 mm2", "3 x 1000 mm2"])

        if type == "3 x 240 mm2":
            core_mm = core_240mm
            sheath_mm = sheath_240mm
            armour_mm = armour_240mm
        if type == "3 x 300 mm2":
            core_mm = core_300mm
            sheath_mm = sheath_300mm
            armour_mm = armour_300mm
        if type == "3 x 400 mm2":
            core_mm = core_400mm
            sheath_mm = sheath_400mm
            armour_mm = armour_400mm
        if type == "3 x 500 mm2":
            core_mm = core_500mm
            sheath_mm = sheath_500mm
            armour_mm = armour_500mm
        if type == "3 x 630 mm2":
            core_mm = core_630mm
            sheath_mm = sheath_630mm
            armour_mm = armour_630mm
        if type == "3 x 800 mm2":
            core_mm = core_800mm
            sheath_mm = sheath_800mm
            armour_mm = armour_800mm
        if type == "3 x 1000 mm2":
            core_mm = core_1000mm
            sheath_mm = sheath_1000mm
            armour_mm = armour_1000mm


    st.write("-" * 34)  # horizontal separator line
    '**CROSS-SECTION DESIGN**'
    #line = st.write("-" * 34)  # horizontal separator line

    # DESIGN - CORE
    with st.expander('CONDUCTOR', expanded=False):

        # DESIGN - CONDUCTOR
        col1, col2, col3, col4  = st.columns(cols1)
        #with col0:
        #    '**DESIGN**'
        with col1:

            '**CONDUCTOR**'
            nc = st.number_input('Layers----', value=6, min_value=1, max_value=7, step=1)
            layer_c = ['' for i in range(0, nc)]
            material_c = ['' for i in range(0, nc)]
            D_c = ['' for i in range(0, nc)]
            rho_c = ['' for i in range(0, nc)]
            with col2:
                '**LAYER**'
            with col4:
                '**MATERIAL**'
            with col3:
                '**DIAMETER**'

            for k in range(0, nc):
                with col2:
                    layer_c[k] = st.selectbox('Layer ' + str(k + 1), layer3c, index=k)
                with col4:
                    if layer_c[k] == 'Conductor':
                        material_c[k] = st.selectbox(str(layer_c[k]), conductors_core, index=k)
                    else:
                        material_c[k] = st.selectbox(str(layer_c[k]), materials_core, index=k)
                with col3:
                    D_c[k] = st.number_input('D' + str(k+1) + ' [mm]', value=core_mm[k], min_value=.001, step=1., format="%.1f")

    


    # DESIGN - SHEATH
    with st.expander('SHEATH', expanded=False):

        col1, col2, col3, col4 = st.columns(cols1)
        with col1:
            '**SHEATH**'
            ns = st.number_input('Layers-----', value=2, min_value=1, max_value=3, step=1)
            layer_s = ['' for i in range(0, ns)]
            material_s = ['' for i in range(0, ns)]
            D_s = ['' for i in range(0, ns)]
            rho_s = ['' for i in range(0, ns)]
            with col2:
                '**LAYER**'
            with col4:
                '**MATERIAL**'
            with col3:
                '**DIAMETER**'

            for k in range(0, ns):
                with col2:
                    layer_s[k] = st.selectbox('Layer ' + str(nc + k + 1), layer3s, index=k)
                with col4:
                    if layer_s[k] == 'Conductor':
                        material_s[k] = st.selectbox('Material (Layer ' + str(nc + k + 1) + ')', conductors_sheath, index=k)
                    else:
                        material_s[k] = st.selectbox('Material (Layer ' + str(nc + k + 1) + ')', materials_sheath, index=k)
                with col3:
                    D_s[k] = st.number_input('D' + str(nc + k + 1) + ' [mm]', value=sheath_mm[k], min_value=.001, step=1., format="%.1f")
    


    # DESIGN - ARMOUR
    with st.expander('ARMOUR', expanded=False):

        col1, col2, col3, col4 = st.columns(cols1)
        with col1:
            '**ARMOUR**'
            na = st.number_input('Layers-a', value=5, min_value=1, max_value=6, step=1)
            layer_a = ['' for i in range(0, na)]
            material_a = ['' for i in range(0, na)]
            D_a = ['' for i in range(0, na)]
            rho_a = ['' for i in range(0, na)]

            with col2:
                '**LAYER**'
            with col4:
                '**MATERIAL**'
            with col3:
                '**DIAMETER**'

            for k in range(0, na):
                with col2:
                    layer_a[k] = st.selectbox('Layer ' + str(nc + ns + k + 1), layer3a, index=k)
                with col4:
                    if layer_a[k] == 'Conductor':
                        material_a[k] = st.selectbox('Material (Layer ' + str(nc + ns + k + 1) + ')', options=['Steel'])#, index=k)
                    else:
                        material_a[k] = st.selectbox('Material (Layer ' + str(nc + ns + k + 1) + ')', materials_armour, index=k)
                with col3:
                    D_a[k] = st.number_input('D' + str(nc + ns + k + 1) + ' [mm]', value=armour_mm[k], min_value=.001, step=1., format="%.1f")

    line = st.write("-" * 34)  # horizontal separator line



    '**WIRE DATA**'
    with st.expander('"RADIUS"', expanded=False):

        col0, col1, col2, col3 = st.columns([.7, 1, 1, 1])
        #with col0:
        #    '' #'**WIRE DIMENSIONS**'
        with col1:
            '**CONDUCTOR**'
        with col2:
            '**SHEATH**'
        with col3:
            '**ARMOUR**'
        with col1:
            rc_in = st.number_input('Radius [mm]', format="%.2f", value=5., step=1., min_value=.001)
            rc = rc_in * 1.e-3
        with col2:
            rs_in = st.number_input('Radius [mm] ', format="%.2f", value=5., step=1., min_value=.001)
            rs = rs_in * 1.e-3
            ns = st.number_input('Wires', value=30, step=1, min_value=1)
        with col3:
            ra_in = st.number_input('Radius [mm]  ', format="%.2f", value=6., step=1., min_value=.001)
            ra = ra_in * 1.e-3
            na1 = st.number_input('Wires (Layer 1)', value=71, step=1, min_value=1)
            #na2 = st.number_input('Wires (Layer 2)', value=71, step=1, min_value=1)

    line = st.write("-" * 34)  # horizontal separator line


    '**MISCELLANEOUS**'
    with st.expander('"ADDITIONAL DATA"', expanded=False):

        col0, col1, col2, col3 = st.columns([.7, 1, 1, 1])

        with col1:
            laylength_temp = st.number_input('Core Lay-up [mm]', format="%.0f", value=2152., step=1.)
            laylength = laylength_temp * 1e-3
            #
            epsilon = st.number_input('Permittivity εr (XLPE)', format="%.1f", value=2.5, step=.1)
            #ts_temp = st.number_input('Sheath thickness [mm]', format="%.2f", value=2.3, step=.1)
            #ts_sheath = ts_temp * 1e-3
        with col2:
            laylength_a_temp = st.number_input('Armour Lay-up [mm]', format="%.0f", value=1785., step=1.)
            laylength_a = laylength_a_temp * 1e-3
            tgdelta = st.number_input('Tan Delta 𝛿 (XLPE)', format="%.5f", value=40e-4, step=1.)
       # with col3:
            #input1 = theta
            #theta_2 = st.number_input('Maximum Temperature [°C]', format="%.2f", value=250.00, step=1.)

    line = st.write("-" * 34)  # horizontal separator line




    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  CROSS-SECTION
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    # source    https://plotly.com/python/shapes/

    D1 = D_c[0] * 1.e-3
    theta_s = 360 / ns
    theta_a1 = 360 / na1
    #theta_a2 = 360 / na2

    if (D1 == rc):
        layers = 0
        nc = [1]
        theta_c = [0]
        R1c = [0]
    else:
        layers = int(np.floor(((D1 + 1.e-5) / rc) - np.floor(0.5 * (D1 + 1.e-5) / rc)) - 1)
        nc = np.zeros(layers)
        nc = [1] + [(i * 6) for i in range(1, layers + 1)]
        theta_c = [0] + [(360 / nc[i]) for i in range(1, layers + 1)]
        R1c = [2 * rc * i for i in range(0, layers + 1)]

    xc = np.zeros(sum(nc), dtype='float32')
    yc = np.zeros(sum(nc), dtype='float32')

    D8 = D_s[1] * 1.e-3

    Xoffset = D8
    Yoffset = 2 * (D8 * np.sqrt(3) / 2) + rs;
    dum = 2 * Yoffset / 3
    baricentro = Yoffset - dum

    for k in range(0, layers + 1):
        a = sum(nc[0:k])
        b = sum(nc[0:k + 1])

        xc[a:b] = [R1c[k] * np.cos(i * (theta_c[k] * np.pi / 180)) for i in range(1, nc[k] + 1)]
        yc[a:b] = [R1c[k] * np.sin(i * (theta_c[k] * np.pi / 180)) for i in range(1, nc[k] + 1)]

    D2 = D_s[1] * 1.e-3
    D3 = D_a[3] * 1.e-3
    xs = [D2 * np.cos(i * (theta_s * np.pi / 180)) for i in range(0, ns)]
    ys = [D2 * np.sin(i * (theta_s * np.pi / 180)) for i in range(0, ns)]
    xa = [D3 * np.cos(i * (theta_a1 * np.pi / 180)) for i in range(0, na1)]
    ya = [D3 * np.sin(i * (theta_a1 * np.pi / 180)) for i in range(0, na1)]

    xc1 = [xc[i] + Xoffset + rc for i in range(0, sum(nc))]
    xs1 = [xs[i] + Xoffset + rs for i in range(0, ns)]

    xc2 = [xc[i] - Xoffset - rc for i in range(0, sum(nc))]
    xs2 = [xs[i] - Xoffset - rs for i in range(0, ns)]

    xc3 = [xc[i] for i in range(0, sum(nc))]
    yc3 = [yc[i] + Yoffset + rc for i in range(0, sum(nc))]
    xs3 = [xs[i] for i in range(0, ns)]
    ys3 = [ys[i] + Yoffset + rs for i in range(0, ns)]

    xa1 = [xa[i] for i in range(0, na1)]
    ya1 = [ya[i] + baricentro + ra * .5 for i in range(0, na1)]

    # print(xc1)
    # xc=xc1
    # xs=xs1

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #                      PLOT cross-section
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -


#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# 3 - CURRENT RATING
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
with tab3: #3-CURRENT RATING
    # - - - - - - - - - -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #                            CODE
    # - - - - - - - - - -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    D_c_ = [  30.0,  30.5,  32.5,  48.5,  50.3,  52.5 ]
    D_s_ = [  57.1,  62.1 ]
    D_a_ = [ 134.9, 135.3, 137.3, 149.3, 155.3 ]


    # shortcuts
    divide = np.divide
    pi = np.pi
    log = np.log
    sqrt = np.sqrt
    print = st.markdown

    De = D_s[1] * 1.e-3  #62.1e-3
    Lcore = laylength
    dc_c = D_c[0] * 1.e-3 #30.3e-3
    #S = 75.5e-3

    Di = D_c[3] * 1.e-3
    dc2 = D_c[2] * 1.e-3
    s = D_s[1] * 1.e-3
    dc = D_c[0] * 1.e-3

    input1 = theta_1
    input2 = theta_0
    dtheta = input1 - input2

    # - - - - - - - - - -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #                       RESULTS INDEPENDENT OF THE TEMPERATURE
    # - - - - - - - - - -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #epislon = 2.5
    #tgdelta = 0.004



    # 1 -- Calculation of lay-up factor of the cores
    def flayup(D_e, L_core):
        return sqrt(1 + (pi * 1.29 * D_e / L_core) ** 2)


    flayup = flayup(De, Lcore)  # print(flayup)

    # - - - Capacitance (semi-conducting layers or tapes excluded)
    C_core = divide(epsilon, 18 * log(divide(Di, dc2))) * 1e-9
    C = C_core * flayup  # print(C)
    # - - - Calculationn of dielectric losses
    Wd = omega * C * U0 * U0 * tgdelta  # print(Wd)

    # SHEATH: Calculation of cross-sectional area of the sheath
    Dsh = D_c[5] * 1.e-3 #52.5e-3
    ts = (D_s[0]-D_c[5]) *0.5* 1.e-3 #2.3e-3
    As = pi * ts * (Dsh + ts)  # print(As*1e6)
    # SHEATH: calculation of the sheath reactance
    d = Dsh + ts  # print(d*1e3)
    X1c = 2 * omega * log(divide(2 * s, d)) * 1e-7  # print(X1c*1e5)
    X = flayup * X1c  # print(X*1e5)

    # Rac_s -- Electrical resistance of the metal sheath at 20°C
    # AC Resistance of the screen at 20oC per unit length of 3-core cable is
    # calculated by taken into consideration the lay-up factor
    rho20_s = 21.4e-8
    alpha20_s = 4.0e-3
    Rs20 = flayup * (rho20_s / As)  # print(rho20_s)    #print(Rs20*1e4)


    # - - - - - - - - - -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #                       THERMAL RESISTANCE
    # - - - - - - - - - -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    def rhoT(rho, d2, d1):
        return (divide(rho, 2 * pi) * log(d2 / d1))


    D_c_ = [  30.0,  30.5,  32.5,  48.5,  50.3,  52.5 ]
    D_s_ = [  57.1,  62.1 ]
    D_a_ = [ 134.9, 135.3, 137.3, 149.3, 155.3 ]


    # Thermal resistance T1 between conductor and screen
    Dwb = D_c[5] * 1.e-3 #52.5e-3  # External diameter of sc water blocking tape(s)
    Dsi = D_c[4] * 1.e-3 #50.3e-3  # External diameter of sc insulation screen
    dwb_con = D_c[1] * 1.e-3 #30.5e-3  # External diameter over the sc tape of the conductor
    dsc = D_c[2] * 1.e-3 #32.5e-3  # External diameter of sc conductor screen
    rhot_sc_t = 6  # Thermal resistivity of semiconducting tapes
    rhot_sc = 2.5  # Thermal resistivity of sc screen
    rhot_i = 3.5  # Thermal resistivity of insulation
    rhot_wb = 12  # Thermal resistivity of water blocking tapes
    T1_wbcon = rhoT(rhot_sc_t, dwb_con, dc)  # Thermal resistance of sc tape over conductor
    T1_csc = rhoT(rhot_sc, dsc, dwb_con)  # Thermal resistance of sc conductor screen
    T1_i = rhoT(rhot_i, Di, dsc)  # Thermal resistance of insulation
    T1_isc = rhoT(rhot_sc, Dsi, Di)  # Thermal resistance of sc insulation screen
    T1_wbt = rhoT(rhot_wb, Dwb, Dsi)  # Thermal resistance of sc water blocking tape
    # Thermal resistance between conductor and screen per core length
    T1_core = T1_wbcon + T1_csc + T1_i + T1_isc + T1_wbt
    T1 = T1_core / flayup  # Thermal resistance between conductor and screen per cable length

    # Thermal resistance T2 of the sheath around each core, fillers and bedding
    De = D_s[1] * 1.e-3 #62.1e-3  # External diameter of sc PE sheath
    rhot_scPE = 2.5  # Thermal resistivity of sc PE sheath
    rhot_fil_bt = 6  # Thermal resistivity of fillers and binding tapes
    Ds = D_s[0] * 1.e-3 #57.1e-3  # External diameter of metallic sheath
    T2p_core = rhoT(rhot_scPE, De, Ds)  # Thermal resistance of the sheath around each core per core length
    T2p = T2p_core / flayup  # Thermal resistance of the sheath around each core per cable length
    # Calculation of geometric factor G
    Dcable = D_a[0] * 1.e-3 #134.9e-3  # Diameter over assembled three cores
    Darm = D_a[2] * 1.e-3 #137.3e-3
    Xg = divide(divide(Darm - Dcable, 2), De)
    # As 0 < X < 0,03
    G = 2 * pi * (0.00022619 + 2.11429 * Xg - 20.4762 * Xg ** 2)
    rhot_filler = 6  # Thermal resistance of fillers
    T2pp = divide(rhot_filler * G, 6 * pi)  # Thermal resistance of fillers and bending under the armour
    T2 = T2p / 3 + T2pp  # The thermal resistance T2 is equal to:

    # Thermal resistance T3 of outer covering
    Dap = D_a[3] * 1.e-3 #149.3e-3  # External diameter of the armour
    t3 = (D_a[4]-D_a[3]) *0.5* 1.e-3 #3e-3  # Thickness of the serving
    rhot_cov = 6  # Thermal resistivity of outer covering
    T3 = divide(rhot_cov, 2 * pi) * log(1 + divide(2 * t3, Dap))  # print(T3)

    # External thermal resistance T4
    De = D_a[4] * 1.e-3 #155.3e-3  # External diameter of one cable
    L = L_burrial #1000e-3  # Distance from the surface of the ground to the cable axis
    rhot_soil = 0.7  # Thermal resistivity of the soil
    u = 2 * L / De
    T4 = divide(1, 2 * pi) * rhot_soil * (log(u + sqrt(u ** 2 - 1)))

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #                     RESULTS DEPENDENT OF THE TEMPERATURE
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # *** ASSUMPTION: CORE CONDUCTOR 90 DEGREES ***    #
    # Rac: Calculation of of the conductor Rac at operation temperature
    # DC resistance of conductor - - - - - - - - - - - - - - - - - -
    Rdc20_c = 28.3e-6
    alpha20_c = 3.93e-3
    Rdc_c = Rdc20_c * (1 + alpha20_c * (input1 - 20))  # print(Rdc_c)
    # - - - Skin effect factor - - -  - - -  - - -  - - -  - - -  - - -
    ks = 1
    xs2 = (8 * pi * f / Rdc_c) * 1e-7  # print(xs2)
    xs = sqrt(xs2)
    # for 0 < xs <= 2.8:
    ys = divide(xs2 ** 2, 192 + 0.8 * xs2 ** 2)  # print(ys)
    # - - - Proximity effect factor - - -  - - -  - - -  - - -  - - -  - - -
    kp = 1
    xp2 = (8 * pi * f / Rdc_c) * 1e-7 * kp  # print(xp2)
    xp = sqrt(xp2)
    dum1 = divide(xp2 ** 2, 192 + 0.8 * xp2 ** 2) * divide(dc, s) ** 2
    dum2 = 0.312 * divide(dc, s) ** 2
    dum3 = divide(1.18, divide(xp2 ** 2, 192 + 0.8 * xp2 ** 2) + 0.27)
    yp = dum1 * (dum2 + dum3)  # print(yp)
    # - - - AC resistance of conductor
    # Note: The impact of armour wires in the conductor losses is taken into consideration
    # with the factor 1.5 in the equation above. See Section 2.5.4 in the guidance chapter.
    Rac = Rdc_c * (1 + 1.5 * (ys + yp))  # print(Rac)

    # *** LOOP INITIALIZATION ***
    errorI = 1e-4
    errorT = 1e-4
    Iguess = 1000
    dt0 = 10  # deltaT for the first iteration

    theta_c = input1
    theta_s = theta_c - dt0
    theta_a = theta_s - dt0
    # Tj_guess =

    # Lead sheath AC resistance at operating temperature 𝜃𝑠
    Rs = Rs20 * (1 + alpha20_s * (theta_s - 20))  # print(Rs*1e4)

    # ARMOUR AC resistance at operating temperature 𝜃a
    da = (D_a[2]+D_a[3]) *0.5* 1.e-3 #143.3e-3  # Mean diameter of the armour 𝑑𝐴 143,3 mm Cable data sheet
    n1 = na1 #71  # Number of armour wires
    df = ra #6e-3  # Diameter of armour wires
    laylength_a = laylength_a #1785e-3  # Lay Length of the armour
    rho20_a = 13.8e-8  # Armour resistivity at 20oC
    alpha20_a = 4.5e-3  # Armour temperature coefficient at 20oC per Kelvin
    S = D_s[1] * 1.e-3 #62.1e-3  # Distance between conductor axes/Diameter over single core
    # Calculation of cross-sectional area of the armour
    Aa = n1 * pi * divide(df, 2) ** 2  # print(Aa*1e6)
    # Ratio of the length of the wires to the length of the cable
    flayup_a = sqrt(1 + (pi * da / laylength_a) ** 2)  # print(flayup_a)
    # DC Resistance of armour at 20oC
    # According to [3] section 2.4.2.1 the AC resistance of armour wire varies
    # from about 1,2 times the DC resistance of 2 mm up to 1,4 times the DC resistance
    # for 5 mm wires. As this diameter exceeds the diameter of 5 mm the suitable factor
    # is found with the use of linear interpolation as it is referred in Guidance Point 34.
    Raa20 = rho20_a / Aa
    k = (0.2 / 3) * (df * 1e3 - 2) + 1.2
    Ra20 = k * Raa20 * flayup_a  # print(Ra20*1e4)
    # The operating temperature 𝜃𝑎𝑟 (oC) of the armour
    # Steel wire armour AC resistance at operating temperature 𝜃𝑎
    Ra = Ra20 * (1 + alpha20_a * (theta_a - 20))
    # print(Ra*1e4)
    note4 = ('Note: Ra with wrong result (R𝑎 = 1,2798804135 x10-4): ' + str(Ra * 1e4))

    # LOSS FACTOR FOR SHEATH
    # Loss factor "lambda1p" caused by circulating currents on the sheath
    # Note: The impact of armour wires in the conductor losses is taken into consideration with the
    # factor 1.5 in the equation
    lambda1p = divide(Rs, Rac) * divide(1.5, 1 + divide(Rs, X) ** 2)  # print(lambda1p)
    # Loss factor "lambda1pp" caused by eddy currents on the sheath
    m = (omega / Rs) * 1e-7
    lambda0 = 3 * divide(m ** 2, 1 + m ** 2) * divide(d, 2 * s) ** 2  # print(lambda0)
    delta1 = (1.14 * m ** 2.45 + 0.33) * divide(d, 2 * s) ** (0.92 * m + 1.66)  # print(delta1)
    beta1 = sqrt(divide(4 * pi * omega, 1e7 * rho20_s * (1 + alpha20_s * (theta_s - 20))))  # print(beta1)
    gs = 1 + ((divide(ts, Ds)) ** 1.74) * (beta1 * Ds * 1e-3 - 1.6)  # print(gs)
    note1 = str('Note: gs with wrong result (𝑔𝑠 = 1.00226113355):' + str(gs))
    delta2 = 0
    dum5 = gs * lambda0 * (1 + delta1 + delta2)
    dum6 = divide((beta1 * ts) ** 4, 12e12)
    lambda1pp = divide(Rs, Rac) * (dum5 + dum6)  # print(lambda1pp)
    note2 = ('Note: 𝜆1" with wrong result (𝜆1" = 0,02208098453): ' + str(lambda1pp))
    M = Rs / X
    N = M  # print(M)
    dum8 = 4 * (M ** 2) * (N ** 2) + (M + N) ** 2
    dum9 = 4 * (M ** 2 + 1) * (N ** 2 + 1)
    F = divide(dum8, dum9)  # print(F)
    lambda1 = lambda1p + F * lambda1pp  # print(lambda1)

    # LOSS FACTOR FOR ARMOUR
    # Calculation of the value c which is the distance between the axis of conductors
    # and the axis of the cable for three core cables (refer to Guidance Point 33)
    c = Dcable / 2 - S / 2
    # print(c*1e3)
    # Loss factor 𝜆2 of the armour, refer to Guidance Point 37
    dum11 = 1.23 * (Ra / Rac) * ((2 * c / da) ** 2)
    dum12 = divide(1, divide(2.77 * Ra * 1e6, omega) ** 2 + 1)
    dum13 = 1 - Rac * lambda1p / Rs
    lambda2 = dum11 * dum12 * dum13  # print(lambda2)
    note5 = ('Note: 𝜆2 with wrong result (𝜆2 = 0.4206526837): ' + str(lambda2))

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #                               ITERATIVE PROCESS
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # 10 - Permissible current rating
    n = 3
    dum21 = dtheta - Wd * (0.5 * T1 + n * (T2 + T3 + T4))
    dum22 = Rac * T1 + n * Rac * (1 + lambda1) * T2 + n * Rac * (1 + lambda1 + lambda2) * (T3 + T4)
    I = sqrt(divide(dum21, dum22))
    note6 = ('Note: I with wrong result (I = 838.339973933 ): ' + str(I))

    delta_I = 9999
    delta_Ts = 9999
    delta_Ta = 9999

    nITER = 10
    results = np.zeros((nITER, 7))

    results[0, 0] = 0
    results[0, 1] = theta_s
    results[0, 2] = delta_Ts
    results[0, 3] = theta_a
    results[0, 4] = delta_Ta
    results[0, 5] = I
    results[0, 6] = delta_I

    # Losses in conductor / sheath / armour
    Wc = n * Rac * I ** 2
    Ws = n * lambda1 * Rac * I ** 2
    Wa = n * lambda2 * Rac * I ** 2
    Wdt = n * Wd  # print(Wc)    #print(Ws)    #print(Wa)    #print(Wdt)

    theta_s_new = theta_1 - (Rac * I ** 2 + 0.5 * Wdt) * T1  # print('𝜃s : ' + str(theta_s))
    theta_a_new = theta_1 - (Rac * I ** 2 + 0.5 * Wdt) * T1 - (
                Rac * I ** 2 * (1 + lambda1)) * n * T2  # print('𝜃a : ' + str(theta_a))
    note3 = ('Note: 𝜃𝑎 with wrong result (𝜃𝑎 = 71.308546665890 oC): ' + str(
        theta_a_new))  # print(theta_s)    #print(theta_a)

    delta_I = abs(I - Iguess)  # print('delta_I: ' + str(delta_I))
    delta_Ts = abs(theta_s - theta_s_new)  # print('delta_Ts: ' + str(delta_Ts))
    delta_Ta = abs(theta_a - theta_a_new)  # print('delta_Ta: ' + str(delta_Ta))    #delta_Tj = abs(theta_j - Tj_guess)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #                               ITERATIVE PROCESS
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    for ITER in range(1, nITER):

        if delta_I > errorI and delta_Ts > errorT and delta_Ta > errorT:  # and delta_Tj > errorT:

            Rs = Rs20 * (1 + alpha20_s * (theta_s - 20))
            Ra = Ra20 * (1 + alpha20_a * (theta_a - 20))

            # LOSS FACTOR FOR SHEATH
            lambda1p = divide(Rs, Rac) * divide(1.5, 1 + divide(Rs, X) ** 2)
            m = (omega / Rs) * 1e-7
            lambda0 = 3 * divide(m ** 2, 1 + m ** 2) * divide(d, 2 * s) ** 2
            delta1 = (1.14 * m ** 2.45 + 0.33) * divide(d, 2 * s) ** (0.92 * m + 1.66)
            beta1 = sqrt(divide(4 * pi * omega, 1e7 * rho20_s * (1 + alpha20_s * (theta_s - 20))))
            gs = 1 + ((divide(ts, Ds)) ** 1.74) * (beta1 * Ds * 1e-3 - 1.6)
            delta2 = 0
            dum5 = gs * lambda0 * (1 + delta1 + delta2)
            dum6 = divide((beta1 * ts) ** 4, 12e12)
            lambda1pp = divide(Rs, Rac) * (dum5 + dum6)
            M = Rs / X
            N = M
            dum8 = 4 * (M ** 2) * (N ** 2) + (M + N) ** 2
            dum9 = 4 * (M ** 2 + 1) * (N ** 2 + 1)
            F = divide(dum8, dum9)
            lambda1 = lambda1p + F * lambda1pp

            # LOSS FACTOR FOR ARMOUR
            dum11 = 1.23 * (Ra / Rac) * ((2 * c / da) ** 2)
            dum12 = divide(1, divide(2.77 * Ra * 1e6, omega) ** 2 + 1)
            dum13 = 1 - Rac * lambda1p / Rs
            lambda2 = dum11 * dum12 * dum13

            # CURRENT RATING
            dum21 = dtheta - Wdt * (0.5 * T1 + n * (T2 + T3 + T4))
            dum22 = Rac * T1 + n * Rac * (1 + lambda1) * T2 + n * Rac * (1 + lambda1 + lambda2) * (T3 + T4)
            I_new = sqrt(divide(dum21, dum22))
            # print('Iteration '+ str(ITER) + ': ' + str(I))

            Wc = n * Rac * I ** 2
            Ws = n * lambda1 * Rac * I ** 2
            Wa = n * lambda2 * Rac * I ** 2
            Wdt = n * Wd

            theta_s_new = theta_1 - (Rac * I ** 2 + 0.5 * Wdt) * T1
            theta_a_new = theta_1 - (Rac * I ** 2 + 0.5 * Wdt) * T1 - (Rac * I ** 2 * (1 + lambda1)) * n * T2

            delta_I = abs(I - I_new)
            delta_Ts = abs(theta_s - theta_s_new)
            delta_Ta = abs(theta_a - theta_a_new)
            # delta_Tj= abs(theta_j - Tj_guess)

            I = I_new
            theta_s = theta_s_new
            theta_a = theta_a_new
            # Tj_guess = theta_j

            results[ITER, 0] = ITER
            results[ITER, 1] = theta_s
            results[ITER, 2] = delta_Ts
            results[ITER, 3] = theta_a
            results[ITER, 4] = delta_Ta
            results[ITER, 5] = I
            results[ITER, 6] = delta_I

        else:
            break

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    # RESULTS
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    line = st.write("-" * 34)  # horizontal separator line

    # '**RESULTS** '
    st.metric("Current Rating [A]", value=str(float("{:.1f}".format(I))) + str(' A'))
    # st.metric("Current Rating [A]", value=str(float("{:.1f}".format(I))) + str(' A'))

    col1, col2, col3 = st.columns(3)
    col1.metric("Core Temperature [°C]", value=str(float("{:.1f}".format(input1))) + str(' °C'))
    col2.metric("Sheath Temperature [°C]", value=str(float("{:.1f}".format(theta_s))) + str(' °C'))
    col3.metric("Armour Temperature [°C]", value=str(float("{:.1f}".format(theta_a))) + str(' °C'))
    # col3.metric("Jacket Temperature [°C]", value=str(float("{:.1f}".format(theta_a))) + str(' °C'))

    # st.markdown('Convergence: ' + str(ITER) + ' iterations')
    # ''
    # ''
    # '** ELECTRICAL PARAMETERS ** '
    # col1, col2, col3 = st.columns(3)
    # col1.metric("Resistance", value=str(float("{:.4f}".format(1e6*Rac))) + str(' μΩ/m'))
    # col2.metric("Capacitance", value=str(float("{:.2f}".format(1e12 * C))) + str(' pF/m'))
    # col3.metric("Reactance", value=str(float("{:.2f}".format(1e6 * X))) + str(' μΩ/m'))

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    line = st.write("-" * 34)  # horizontal separator line

    col1, col2, col3 = st.columns([.5, .75, .5])
    with col2:
        # print('Case study 2: 30 kV submarine array cable')
        image3 = Image.open('cigre_TB880_2.png')
        st.image(image3, caption='Reference: 33 kV submarine array cable', width=300)


#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# MoM-SO: ELECTRICAL PARAMETERS
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
#with tab4:
    



#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# EXPORT PARAMETERS
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
with tab5:

    #st.plotly_chart(fig)

    #st.subheader('Interface with circuit solvers')
    #st.markdown(' Interfacing with circuit solvers contains matlab scripts which demonstrate'
    #        ' how to interface rational function-based models with time domain circuit solvers '
    #        'via a Norton equivalent. The procedure is shown for models representing '
    #        'Y-parameters, Z-parameters, S-parameters, and general transfer functions that '
    #        'do not interact with the circuit.')

    #col = st.selectbox("Select Software:",
    #                   options=["PSCAD", "EMTP", "PowerFactory", "ATP"])

    import time
    localtime = time.asctime(time.localtime(time.time()))
    dum = time.strftime("Date:%d-%m-%Y  Time:%H:%M:%S", time.localtime())


    st.write("")

    st.download_button(
        label="Download Data",
        data='Universal Cable Constants (UCC) \n\n' + dum,
        file_name='cable_parameters.csv',
        mime='text/csv')

    st.download_button(
        label="Download Report",
        data='Universal Cable Constants (UCC) \n\n' + dum,
        file_name='cable_parameters.txt',
        mime='text/csv')
















