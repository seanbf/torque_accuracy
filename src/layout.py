import streamlit as st
import getpass

def containers(analysis_toggle, columns):

    report_table = dict()

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
        report_table["Test Name"]           = test_name.text_input("Test Name", key = "test_name")
        report_table["User Name"]           = user.text_input("User", value = getpass.getuser())
        report_table["Test Date"]           = date.date_input("Date", key = "test_date")
        report_table["Test Notes"]          = st.text_area("Test Notes", key = "test_note")

        dyno_fields, software_fields            = st.columns(2)

        #Dyno
        dyno_fields.subheader("Dyno")
        report_table["Dyno"]                    = dyno_fields.selectbox("Dyno", dynos, key = "dyno")
        report_table["Torque Speed Sensor"]     = dyno_fields.selectbox("Torque Speed Sensor",torque_speed_sensors, key = "torque_speed_sensor")
        report_table["Sensor Calibration Date"] = dyno_fields.date_input("Date", key = "sensor_calibration_date")

        #Software
        software_fields.subheader("Software")
        report_table["Software Level"]      = software_fields.selectbox("Level", sw_levels, key = "software_level")
        report_table["Software Location"]   = software_fields.text_input("Location", key = "software_location")
        report_table["Software Notes"]      = software_fields.text_area("Notes", key = "software_note")

        controller_field, motor_field   = st.columns(2)

        #Controllers
        controller_field.subheader("Controller")
        report_table["Controller Manufacturer"] = controller_field.selectbox("Manufacturer", controller_manfactures, key = "controller_manufacturer")

        if report_table["Controller Manufacturer"] == 'Turntide':
            report_table["Controller Model"] = controller_field.selectbox("Model", turntide_controllers, key = "controller_model")
        elif report_table["Controller Manufacturer"] == 'Avid':
            report_table["Controller Model"] = controller_field.selectbox("Model", avid_controllers, key = "controller_model")
        elif report_table["Controller Manufacturer"] == 'Borgwarner':
            report_table["Controller Model"] = controller_field.selectbox("Model", borgwarner_controllers, key = "controller_model")
        elif report_table["Controller Manufacturer"] == 'Cascadia':
            report_table["Controller Model"] = controller_field.selectbox("Model", cascadia_controllers, key = "controller_model")
        elif report_table["Controller Manufacturer"] == 'Other':
            report_table["Controller Model"] = controller_field.text_input("Model")

        report_table["Controller Sample"] = controller_field.selectbox("Sample", samples, key = "controller_sample")
        report_table["Controller Notes"] = controller_field.text_area("Notes", key = "controller_note")

        #Motors
        motor_field.subheader("Motor")
        report_table["Motor Manufacturer"] = motor_field.selectbox("Manufacturer", motor_manufactures, key = "motor_manufacturer")

        if report_table["Motor Manufacturer"] == 'Turntide':
            report_table["Motor Model"] = motor_field.selectbox("Model", turntide_motors, key = "motor_model")
        elif report_table["Motor Manufacturer"] == 'Yasa':
            report_table["Motor Model"] = motor_field.selectbox("Model", yasa_motors, key = "motor_model")
        elif report_table["Motor Manufacturer"] == 'Intergral Powertrain':
            report_table["Motor Model"] = motor_field.selectbox("Model", ipt_motors, key = "motor_model")
        elif report_table["Motor Manufacturer"] == 'Other':
            report_table["Motor Model"] = motor_field.text_input("Model")

        report_table["Motor Sample"] = motor_field.selectbox("Sample", samples, key = "motor_sample")
        report_table["Motor Notes"] = motor_field.text_area("Notes", key = "motor_note")

    with st.sidebar.expander("Test Limits", expanded=True):
        if analysis_toggle == "Output":
            report_table["QM Limit Nm"]         = st.number_input("QM Limit [Nm]",      min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0))
            report_table["QM Limit Pc"]         = st.number_input("QM Limit [%]",       min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0))

        elif analysis_toggle == "Estimated":
            report_table["Estimated Limit Nm"]  = st.number_input("Estimated Limit [Nm]",   min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0))
            report_table["Estimated Limit %"]   = st.number_input("Estimated Limit [%]",    min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0))

        elif analysis_toggle == "Output & Estimated":
            report_table["QM Limit Nm"]         = st.number_input("Output Limit [Nm]",      min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0))
            report_table["QM Limit Pc"]         = st.number_input("Output Limit [%]",       min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0))
            report_table["Estimated Limit Nm"]  = st.number_input("Estimated Limit [Nm]",   min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0))
            report_table["Estimated Limit %"]   = st.number_input("Estimated Limit [%]",    min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0))
    
    with st.sidebar.expander("Signals", expanded=True):
        if analysis_toggle == "Output":
            report_table["Torque Measured"]      = st.selectbox("Torque Measured",list(columns) )
            report_table["Torque Demanded"]      = st.selectbox("Torque Demanded",list(columns) )

        elif analysis_toggle == "Estimated":
            report_table["Torque Measured"]     = st.selectbox("Torque Measured",list(columns) )
            report_table["Torque Estimated"]    = st.selectbox("Torque Estimated",list(columns) )

        elif analysis_toggle == "Output & Estimated":
            report_table["Torque Measured"]     = st.selectbox("Torque Measured",list(columns) )
            report_table["Torque Demanded"]     = st.selectbox("Torque Demanded",list(columns) )
            report_table["Torque Estiamted"]    = st.selectbox("Torque Estimated",list(columns) )

        report_table["DC Voltage"]              = st.selectbox("DC Voltage",list(columns) )
        report_table["DC Current"]              = st.selectbox("DC Current",list(columns) )
        report_table["Speed"]                   = st.selectbox("Speed",list(columns) )
        #report_table["id"]                      = st.selectbox("Id",list(columns) )
        #report_table["iq"]                      = st.selectbox("Iq",list(columns) )
        #report_table["id"]                      = st.selectbox("Ud",list(columns) )
        #report_table["iq"]                      = st.selectbox("Uq",list(columns) )

    return report_table