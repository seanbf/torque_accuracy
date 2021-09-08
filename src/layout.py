import streamlit as st
import getpass

def test_details():

    controller_manfactures = [
        "Turntide",
        "Avid",
        "Cascadia",
        "BorgWarner",
        "Other",
    ]

    turntide_controllers = [
        "Gen 5 Oxford",
        "Gen 5",
        "Gen 4 Size 10",
        "Gen 4 Size 8"
    ]

    avid_controllers = [
        "Placeholder A",
        "Placeholder B",
        "Placeholder C"
    ]

    cascadia_controllers = [
        "Placeholder A",
        "Placeholder B",
        "Placeholder C"
    ]

    borgwarner_controllers = [
        "Placeholder A",
        "Placeholder B",
        "Placeholder C"
    ]

    samples = [
        "A0",
        "A1",
        "A2",
        "A3",
        "A4",
        "B0",
        "B1",
        "B2",
        "B3",
        "B4",
        "C0",
        "C1",
        "C2",
        "C3",
        "C4",
        "D0",
        "D1",
        "D2",
        "D3",
        "D4",
    ]

    motor_manufactures = [
        "Turntide",
        "Yasa",
        "Intergral Powertrain",
        "Other"
    ]

    turntide_motors = [
        "Placeholder A",
        "Placeholder B",
        "Placeholder C"
    ]

    yasa_motors = [
        "Oxford"
    ]

    ipt_motors = [
        "Bowfell",
    ]

    dynos = [
        "Dyno 1",
        "Dyno 2",
        "Dyno 3",
        "Dyno 4",
        "Dyno 5",
        "Dyno 6",
        "Other"
    ]

    sw_levels = [
        "Branch",
        "Tag",
        "Trunk",
        "Release Candidate",
        "Other"
    ]

    torque_speed_sensors =[
        "HBM T40 (SN:XX)",
        "HBM T20 (SN:XX)",
        "Sensor Technologies (SN:XX)"
    ]

    with st.expander("Test Details", expanded=False):

        test_name, user, date               = st.columns(3)

        #Report Details
        test_name.text_input("Test Name", key = "Test Name")
        user.text_input("User", value = getpass.getuser(), key = "User")
        date.date_input("Date", key = "Test Date")
        st.text_area("Test Notes", key = "Test Note")

        dyno_fields, software_fields            = st.columns(2)

        #Dyno
        dyno_fields.subheader("Dyno")
        dyno_fields.selectbox("Dyno", dynos, key = "Dyno")
        dyno_fields.selectbox("Torque Speed Sensor",torque_speed_sensors, key = "Torque Speed Sensor")
        dyno_fields.date_input("Date", key = "Sensor Calibration Date")

        #Software
        software_fields.subheader("Software")
        software_fields.selectbox("Level", sw_levels, key = "Software Level")
        software_fields.text_input("Location", key = "Software Location")
        software_fields.text_area("Notes", key = "Software Notes")

        controller_field, motor_field   = st.columns(2)

        #Controllers
        controller_field.subheader("Controller")
        controller_field.selectbox("Manufacturer", controller_manfactures, key = "Controller Manufacturer")

        if st.session_state["Controller Manufacturer"] == 'Turntide':
            controller_field.selectbox("Model", turntide_controllers, key = "Controller Model")

        elif st.session_state["Controller Manufacturer"] == 'Avid':
            controller_field.selectbox("Model", avid_controllers, key = "Controller Model")

        elif st.session_state["Controller Manufacturer"] == 'Borgwarner':
            controller_field.selectbox("Model", borgwarner_controllers, key = "Controller Model")

        elif st.session_state["Controller Manufacturer"] == 'Cascadia':
            controller_field.selectbox("Model", cascadia_controllers, key = "Controller Model")

        elif st.session_state["Controller Manufacturer"] == 'Other':
            controller_field.text_input("Model")

        controller_field.selectbox("Sample", samples, key = "Controller Sample")
        controller_field.text_area("Notes", key = "Controller Notes")

        #Motors
        motor_field.subheader("Motor")
        motor_field.selectbox("Manufacturer", motor_manufactures, key = "Motor Manufacturer")

        if st.session_state["Motor Manufacturer"] == 'Turntide':
            motor_field.selectbox("Model", turntide_motors, key = "Motor Model")

        elif st.session_state["Motor Manufacturer"] == 'Yasa':
            motor_field.selectbox("Model", yasa_motors, key = "Motor Model")

        elif st.session_state["Motor Manufacturer"] == 'Intergral Powertrain':
            motor_field.selectbox("Model", ipt_motors, key = "Motor Model")

        elif st.session_state["Motor Manufacturer"] == 'Other':
            motor_field.text_input("Model")

        motor_field.selectbox("Sample", samples, key = "Motor Sample")
        motor_field.text_area("Notes", key = "Motor Notes")

    return


def limits(analysis_toggle):

    if analysis_toggle == "Output":
        st.subheader("Output Limits")
        st.number_input("QM Limit [Nm]",      min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0), key = "Output Limit [Nm]")
        st.number_input("QM Limit [%]",       min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0), key = "Output Limit [%]")

    else:
        col_output, col_estimated = st.columns(2)
        col_output.subheader("Output Limits")
        col_output.number_input("Output Limit [Nm]",      min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0), key = "Output Limit [Nm]")
        col_output.number_input("Output Limit [%]",       min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0), key = "Output Limit [%]")
        col_estimated.subheader("Estimated Limits")
        col_estimated.number_input("Estimated Limit [Nm]",   min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0), key = "Estimated Limit [Nm]")
        col_estimated.number_input("Estimated Limit [%]",    min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0), key = "Estimated Limit [%]")
    return

def signals(analysis_toggle, columns, t_demanded, t_estimated, t_measured, speed, vdc, idc):

    torque_measured_signals = [
        "Transducer_Torque_IOP",
        "Transducer_Torque_MCP",
        "Transducer_Trq_IOP",
        "Transducer_Trq_MCP"
    ]

    speed_signals = [
        "Transducer_Speed_IOP",
        "Transducer_Speed_MCP",
        "tesInputData.L2mPosSpdArb_RotorSpd_MCP",
        "tesInputData.L2mPosSpdArb_RotorSpd_IOP"
    ]

    torque_demanded_signals = [
        " TesOp_B.L2m_TarTrq_MCP",
        "TesOp_B.L2m_TarTrq_MCP",
        " TesOp_B.L2m_TarTrq_IOP",
        "TesOp_B.L2m_TarTrq_IOP"
    ]

    torque_estimated_signals = [
        " tesOutputData.L2mTes_EstTrq.val_MCP",
        "tesOutputData.L2mTes_EstTrq.val_MCP",
        " tesOutputData.L2mTes_EstTrq.val_IOP",
        "tesOutputData.L2mTes_EstTrq.val_IOP"
    ]

    dc_voltage_signals = [
        " sensvdcOutputData.L2mSensVdc_Vdc.val_MCP",
        "sensvdcOutputData.L2mSensVdc_Vdc.val_MCP",
        " sensvdcOutputData.L2mSensVdc_Vdc.val_IOP",
        "sensvdcOutputData.L2mSensVdc_Vdc.val_IOP"
    ]

    dc_current_signals = [
        " sensidcOutputData.L2mSensIdc_Idc.val_MCP",
        "sensidcOutputData.L2mSensIdc_Idc.val_MCP",
        " sensidcOutputData.L2mSensIdc_Idc.val_IOP",
        "sensidcOutputData.L2mSensIdc_Idc.val_IOP"
    ]


    # Torque measured auto-select
    for signals in torque_measured_signals:
        if signals in columns:
            list_index = list(columns).index(signals)
            st.selectbox("Torque Measured",list(columns),  key = t_measured, index=list_index)
            break
        elif signals not in columns: 
            st.selectbox("Torque Measured",list(columns),  key = t_measured, index = 0)
            break

    # Torque demanded auto-select
    for signals in torque_demanded_signals:
        if signals in columns:
            list_index = list(columns).index(signals)
            st.selectbox("Torque Demanded",list(columns), key = t_demanded, index=list_index)
            break
        else: 
            st.selectbox("Torque Demanded",list(columns), key = t_demanded )
            break

    if analysis_toggle == "Output & Estimated":
            # Torque estimated auto-select
        for signals in torque_estimated_signals:
            if signals in columns:
                list_index = list(columns).index(signals)
                st.selectbox("Torque Estimated",list(columns), key = t_estimated, index=list_index)
                break
            else: 
                st.selectbox("Torque Estimated",list(columns), key = t_estimated)
                break

    # Speed auto-select
    for signals in speed_signals:
        if signals in columns:
            list_index = list(columns).index(signals)
            st.selectbox("Speed",list(columns), key = speed, index=list_index)
            break
        else: 
            st.selectbox("Speed",list(columns), key = speed, index = 0)
            break
        
    # DC Voltage auto-select
    for signals in dc_voltage_signals:
        if signals in columns:
            list_index = list(columns).index(signals)
            st.selectbox("DC Voltage",list(columns), key = vdc, index=list_index)
            break
        else: 
            st.selectbox("DC Voltage",list(columns), key = vdc )
            break

    # DC Current auto-select
    for signals in dc_current_signals:
        if signals in columns:
            list_index = list(columns).index(signals)
            st.selectbox("DC Current",list(columns), key = idc, index=list_index)
            break
        else: 
            st.selectbox("DC Current",list(columns), key = idc )
            break
    
    return