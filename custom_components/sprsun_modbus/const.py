"""Constants for the SPRSUN Heat Pump Modbus integration."""

DOMAIN = "sprsun_modbus"

# Default values
DEFAULT_NAME = "SPRSUN Warmtepomp"
DEFAULT_PORT = 502
DEFAULT_DEVICE_ADDRESS = 1
DEFAULT_SCAN_INTERVAL = 10  # seconds - balance between responsiveness and load
DEFAULT_TIMEOUT = 30  # seconds - Elfin W11 timeout (must be >= scan_interval + cycle_time)

# Configuration keys
CONF_DEVICE_ADDRESS = "device_address"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_CONTROLLER_TYPE = "controller_type"  # "chico" or "carel"

# Platforms
PLATFORMS = ["sensor", "binary_sensor", "number", "select", "switch", "button"]

# Read-Only Registers (50 parameters) - zgodnie z modbus_reference.md
REGISTERS_READ_ONLY = {
    # System Status
    0x0000: ("compressor_runtime", "Compressor draaiuren", 1, "h", None),
    0x0001: ("cop", "COP", 1, None, None),
    0x0013: ("software_version_year", "Softwareversie (jaar)", 1, None, None),
    0x0014: ("software_version_month_day", "Softwareversie (maand/dag)", 1, None, None),
    0x002C: ("controller_version", "Controllerversie", 1, None, None),
    0x002D: ("display_version", "Displayversie", 1, None, None),
    
    # Input/Output/Status Flags
    0x0002: ("switching_input_symbol", "Schakelingangen (ruw)", 1, None, None),
    0x0003: ("working_status_mark", "Werkstatus (ruw)", 1, None, None),
    0x0004: ("output_symbol_1", "Uitgangen 1 (ruw)", 1, None, None),
    0x0005: ("output_symbol_2", "Uitgangen 2 (ruw)", 1, None, None),
    0x0006: ("output_symbol_3", "Uitgangen 3 (ruw)", 1, None, None),
    
    # Failure/Alarm Flags
    0x0007: ("failure_symbol_1", "Storingsregister 1 (ruw)", 1, None, None),
    0x0008: ("failure_symbol_2", "Storingsregister 2 (ruw)", 1, None, None),
    0x0009: ("failure_symbol_3", "Storingsregister 3 (ruw)", 1, None, None),
    0x000A: ("failure_symbol_4", "Storingsregister 4 (ruw)", 1, None, None),
    0x000B: ("failure_symbol_5", "Storingsregister 5 (ruw)", 1, None, None),
    0x000C: ("failure_symbol_6", "Storingsregister 6 (ruw)", 1, None, None),
    0x000D: ("failure_symbol_7", "Storingsregister 7 (ruw)", 1, None, None),
    
    # Temperature Sensors
    0x000E: ("inlet_temp", "Retourwatertemperatuur", 0.1, "°C", "temperature"),
    0x000F: ("hotwater_temp", "Tapwatertemperatuur", 0.1, "°C", "temperature"),
    0x0011: ("ambient_temp", "Buitentemperatuur", 0.5, "°C", "temperature"),  # SIGNED
    0x0012: ("outlet_temp", "Aanvoerwatertemperatuur", 0.1, "°C", "temperature"),
    0x0015: ("suction_gas_temp", "Zuiggastemperatuur", 0.5, "°C", "temperature"),  # SIGNED
    0x0016: ("coil_temp", "Coiltemperatuur", 0.5, "°C", "temperature"),  # SIGNED
    0x001B: ("exhaust_temp", "Uitlaattemperatuur", 1, "°C", "temperature"),
    0x0022: ("driving_temp", "Aandrijftemperatuur", 0.5, "°C", "temperature"),  # SIGNED
    0x0028: ("evap_temp", "Verdampertemperatuur", 0.1, "°C", "temperature"),  # SIGNED
    0x0029: ("cond_temp", "Condensortemperatuur", 0.1, "°C", "temperature"),
    
    # System Measurements
    0x0017: ("ac_voltage", "AC-spanning", 1, "V", "voltage"),
    0x0018: ("pump_flow", "Flow", 1, "m³/h", None),
    0x0019: ("heating_cooling_capacity", "Thermisch vermogen", 1, "W", "power"),
    0x001A: ("ac_current", "AC-stroom", 1, "A", "current"),
    0x001C: ("eev1_step", "EEV1 stappen", 1, "steps", None),
    0x001D: ("eev2_step", "EEV2 stappen", 1, "steps", None),
    0x001E: ("compressor_frequency", "Compressorfrequentie", 1, "Hz", "frequency"),
    0x0021: ("dc_bus_voltage", "DC-busspanning", 1, "V", "voltage"),
    0x0023: ("compressor_current", "Compressorstroom", 1, "A", "current"),
    0x0024: ("target_frequency", "Doelfrequentie", 1, "Hz", "frequency"),
    0x0026: ("dc_fan1_speed", "DC-ventilator 1 toerental", 1, "rpm", None),
    0x0027: ("dc_fan2_speed", "DC-ventilator 2 toerental", 1, "rpm", None),
    0x002E: ("dc_pump_speed", "DC-pomp toerental", 1, "rpm", None),
    # Pressure sensors: Values in 0.1 PSI, converted to bar (0.1 PSI ÷ 14.5 = 0.0069)
    # REGISTERS ARE SWAPPED IN MANUFACTURER'S DOCUMENTATION!
    # 0x002F labeled "suction" actually shows discharge values (~31 bar)
    # 0x0030 labeled "discharge" actually shows suction values (~5 bar)
    0x002F: ("discharge_pressure", "Persdruk", 0.0069, "bar", "pressure"),  # SWAPPED!
    0x0030: ("suction_pressure", "Zuigdruk", 0.0069, "bar", "pressure"),      # SWAPPED!
    0x0031: ("dc_fan_target", "DC-ventilator doeltoerental", 1, "rpm", None),
    
    # Inverter Status
    0x001F: ("freq_conversion_failure_1", "Inverterstoring 1", 1, None, None),
    0x0020: ("freq_conversion_failure_2", "Inverterstoring 2", 1, None, None),
    0x0025: ("smart_grid_status", "Smart Grid-status", 1, None, None),
    0x002A: ("freq_conversion_fault_high", "Inverterstoring hoog", 1, None, None),
    0x002B: ("freq_conversion_fault_low", "Inverterstoring laag", 1, None, None),
}

# Binary Sensors - extracted from bitfield registers
# These are READ-ONLY status indicators

# Working Status Mark (R 0x0003) - operational status
BINARY_SENSOR_BITS = {
    # Working Status Mark (0x0003)
    "hotwater_demand": (0x0003, 0, "Tapwatervraag"),
    "heating_demand": (0x0003, 1, "Verwarmingsvraag"),
    "cooling_demand": (0x0003, 5, "Koelvraag"),
    "antilegionella_active": (0x0003, 4, "Antilegionella actief"),
    "defrost_active": (0x0003, 7, "Ontdooien actief"),
    "alarm_stop": (0x0003, 6, "Alarmstop"),
    
    # Switching Input Symbol (0x0002) - physical input switches
    "ac_linkage_switch": (0x0002, 0, "A/C-koppelschakelaar"),
    "linkage_switch": (0x0002, 1, "Koppelschakelaar"),
    "heating_linkage": (0x0002, 2, "Verwarmingskoppeling"),
    "cooling_linkage": (0x0002, 3, "Koelkoppeling"),
    "flow_switch": (0x0002, 4, "Flowschakelaar"),
    "high_pressure_switch": (0x0002, 5, "Hogedrukschakelaar"),
    "phase_sequence_ok": (0x0002, 6, "Fasevolgorde OK"),
    
    # Output Symbol 1 (0x0004) - main outputs
    "compressor_running": (0x0004, 0, "Compressor"),
    "fan_running": (0x0004, 5, "Ventilator"),
    "valve_4way": (0x0004, 6, "Vierwegklep"),
    "fan_high_speed": (0x0004, 7, "Ventilator hoog toerental"),
    
    # Output Symbol 2 (0x0005) - auxiliary outputs
    "chassis_heater": (0x0005, 0, "Chassisverwarming"),
    "heating_heater": (0x0005, 5, "Verwarmingselement"),
    "valve_3way": (0x0005, 6, "Driewegklep"),
    "hotwater_heater": (0x0005, 7, "Tapwaterelement"),
    
    # Output Symbol 3 (0x0006) - pump outputs
    "ac_pump": (0x0006, 0, "A/C-pomp"),
    "crank_heater": (0x0006, 1, "Carterverwarming"),
    "assistant_solenoid": (0x0006, 5, "Hulpmagneetventiel"),
    "pump_running": (0x0006, 6, "Circulatiepomp"),
    
    # Failure Symbol 1 (0x0007) - sensor failures
    "error_hotwater_sensor": (0x0007, 0, "Fout tapwatersensor"),
    "error_ambient_sensor": (0x0007, 1, "Fout buitensensor"),
    "error_coil_sensor": (0x0007, 2, "Fout coilsensor"),
    "error_outlet_sensor": (0x0007, 4, "Fout aanvoersensor"),
    "error_high_pressure_sensor": (0x0007, 5, "Fout hogedruksensor"),
    "error_phase_sequence": (0x0007, 7, "Fasevolgordefout"),
    
    # Failure Symbol 2 (0x0008) - protection errors
    "error_water_flow": (0x0008, 0, "Waterstromingsfout"),
    "error_high_temp_heating": (0x0008, 2, "Hoge-temp. beveiliging (aanvoer verwarmen)"),
    
    # Failure Symbol 3 (0x0009)
    "error_outlet_gas_temp": (0x0009, 6, "Fout persgastemperatuur"),
    
    # Failure Symbol 4 (0x000A)
    "error_inlet_sensor": (0x000A, 0, "Fout retoursensor"),
    "error_exhaust_high": (0x000A, 1, "Uitlaattemperatuur te hoog"),
    "error_low_temp_cooling": (0x000A, 5, "Lage-temp. beveiliging (aanvoer koelen)"),
    "error_inlet_gas_sensor": (0x000A, 6, "Fout zuiggassensor"),
    
    # Failure Symbol 5 (0x000B) - pressure errors
    "error_low_pressure": (0x000B, 0, "Lagedrukbeveiliging"),
    "error_high_pressure": (0x000B, 1, "Hogedrukbeveiliging"),
    "error_coil_temp_high": (0x000B, 2, "Coiltemperatuur te hoog"),
    "error_high_pressure_sensor2": (0x000B, 6, "Hogedruksensor defect"),
    "error_low_pressure_sensor": (0x000B, 7, "Lagedruksensor defect"),
    
    # Failure Symbol 6 (0x000C) - antifreeze
    "error_antifreeze_secondary": (0x000C, 4, "Secundaire vorstbeveiliging"),
    "error_antifreeze_primary": (0x000C, 5, "Primaire vorstbeveiliging"),
    
    # Failure Symbol 7 (0x000D) - system errors
    "error_ambient_temp_low": (0x000D, 1, "Buitentemperatuur te laag"),
    "error_inverter_module": (0x000D, 4, "Invertermodule defect"),
    "error_dc_fan2": (0x000D, 5, "DC-ventilator 2 defect"),
    "error_dc_fan1": (0x000D, 6, "DC-ventilator 1 defect"),
}

# Switch entities - Read-Write bitfield controls (persistent state)
# Format: key: (address, bit, name, coil_address_if_available)
REGISTERS_SWITCH = {
    "power_switch": (0x0032, 0, "Aan/uit", 0x0320),  # Parameter marker bit 0: ON/OFF (coil 0x0320)
    "antilegionella_enable": (0x0034, 0, "Antilegionella inschakelen", None),  # Control mark 2 bit 0
    "two_three_function": (0x0034, 1, "Twee/drie-functie", None),  # Control mark 2 bit 1 (0=Two, 1=Three)
}

# Button entities - Read-Write bitfield momentary actions
# Format: key: (address, bit, name, description)
REGISTERS_BUTTON = {
    "failure_reset": (0x0033, 7, "Storing resetten", "Reset alle storingen nadat de oorzaak is verholpen"),  # Control mark 1 bit 7
}

# Select entities - Read-Write mode controls
# Format: address: (key, name, options_dict)
REGISTERS_SELECT = {
    0x0036: ("unit_mode", "Bedrijfsmodus", {  # P06
        0: "Alleen tapwater",
        1: "Alleen verwarmen",
        2: "Alleen koelen",
        3: "Verwarmen + tapwater",
        4: "Koelen + tapwater",
    }),
    0x0190: ("fan_mode", "Ventilatormodus", {  # P07
        0: "Normaal",
        1: "ECO",
        2: "Nacht",
        3: "Test",
    }),
    0x019E: ("pump_mode", "Pompmodus", {  # G02
        0: "Interval",
        1: "Normaal",
        2: "Op aanvraag",
    }),
}

# Numbers - Read-Write registers (according to modbus_reference.md)
# Format: address: (key, name, scale, unit, min, max, step, device_class)
REGISTERS_NUMBER = {
    # Basic Configuration - P parameters
    0x00CC: ("heating_setpoint", "Setpoint verwarmen", 0.5, "°C", 10, 55, 0.5, "temperature"),  # P01
    0x00CB: ("cooling_setpoint", "Setpoint koelen", 0.5, "°C", 12, 30, 0.5, "temperature"),  # P02
    0x00CA: ("hotwater_setpoint", "Setpoint tapwater", 0.5, "°C", 10, 55, 0.5, "temperature"),  # P04
    0x00C6: ("temp_diff_heating_cooling", "Hysterese verwarmen/koelen", 1, "°C", 2, 18, 1, "temperature"),  # P03
    0x00C8: ("temp_diff_hotwater", "Hysterese tapwater", 1, "°C", 2, 18, 1, "temperature"),  # P05
    
    # Economic Mode - Heating (E01-E04, E13-E16)
    # NOTE: E01-E04 are SIGNED (can be negative for winter ambient temps)
    0x0169: ("econ_heat_ambi_1", "ECO verwarmen buiten 1", 1, "°C", -30, 50, 1, "temperature"),  # E01 SIGNED
    0x016A: ("econ_heat_ambi_2", "ECO verwarmen buiten 2", 1, "°C", -30, 50, 1, "temperature"),  # E02 SIGNED
    0x016B: ("econ_heat_ambi_3", "ECO verwarmen buiten 3", 1, "°C", -30, 50, 1, "temperature"),  # E03 SIGNED
    0x016C: ("econ_heat_ambi_4", "ECO verwarmen buiten 4", 1, "°C", -30, 50, 1, "temperature"),  # E04 SIGNED
    0x0175: ("econ_heat_temp_1", "ECO verwarmen doel 1", 0.5, "°C", 10, 55, 0.5, "temperature"),  # E13
    0x0176: ("econ_heat_temp_2", "ECO verwarmen doel 2", 0.5, "°C", 10, 55, 0.5, "temperature"),  # E14
    0x0177: ("econ_heat_temp_3", "ECO verwarmen doel 3", 0.5, "°C", 10, 55, 0.5, "temperature"),  # E15
    0x0178: ("econ_heat_temp_4", "ECO verwarmen doel 4", 0.5, "°C", 10, 55, 0.5, "temperature"),  # E16
    
    # Economic Mode - Hot Water (E05-E08, E17-E20)
    # NOTE: E05-E08 are SIGNED (can be negative for winter ambient temps)
    0x016D: ("econ_water_ambi_1", "ECO tapwater buiten 1", 1, "°C", -30, 50, 1, "temperature"),  # E05 SIGNED
    0x016E: ("econ_water_ambi_2", "ECO tapwater buiten 2", 1, "°C", -30, 50, 1, "temperature"),  # E06 SIGNED
    0x016F: ("econ_water_ambi_3", "ECO tapwater buiten 3", 1, "°C", -30, 50, 1, "temperature"),  # E07 SIGNED
    0x0170: ("econ_water_ambi_4", "ECO tapwater buiten 4", 1, "°C", -30, 50, 1, "temperature"),  # E08 SIGNED
    0x0179: ("econ_water_temp_1", "ECO tapwater doel 1", 0.5, "°C", 10, 55, 0.5, "temperature"),  # E17
    0x017A: ("econ_water_temp_2", "ECO tapwater doel 2", 0.5, "°C", 10, 55, 0.5, "temperature"),  # E18
    0x017B: ("econ_water_temp_3", "ECO tapwater doel 3", 0.5, "°C", 10, 55, 0.5, "temperature"),  # E19
    0x017C: ("econ_water_temp_4", "ECO tapwater doel 4", 0.5, "°C", 10, 55, 0.5, "temperature"),  # E20
    
    # Economic Mode - Cooling (E09-E12, E21-E24)
    # NOTE: E09-E12 are SIGNED (can be negative for winter ambient temps)
    0x0171: ("econ_cool_ambi_1", "ECO koelen buiten 1", 1, "°C", -30, 50, 1, "temperature"),  # E09 SIGNED
    0x0172: ("econ_cool_ambi_2", "ECO koelen buiten 2", 1, "°C", -30, 50, 1, "temperature"),  # E10 SIGNED
    0x0173: ("econ_cool_ambi_3", "ECO koelen buiten 3", 1, "°C", -30, 50, 1, "temperature"),  # E11 SIGNED
    0x0174: ("econ_cool_ambi_4", "ECO koelen buiten 4", 1, "°C", -30, 50, 1, "temperature"),  # E12 SIGNED
    0x017D: ("econ_cool_temp_1", "ECO koelen doel 1", 0.5, "°C", 12, 30, 0.5, "temperature"),  # E21
    0x017E: ("econ_cool_temp_2", "ECO koelen doel 2", 0.5, "°C", 12, 30, 0.5, "temperature"),  # E22
    0x017F: ("econ_cool_temp_3", "ECO koelen doel 3", 0.5, "°C", 12, 30, 0.5, "temperature"),  # E23
    0x0180: ("econ_cool_temp_4", "ECO koelen doel 4", 0.5, "°C", 12, 30, 0.5, "temperature"),  # E24
    
    # General Configuration - G parameters
    0x0181: ("comp_delay_hotwater", "Tapwater bijstook-vertraging", 1, "min", 1, 60, 1, None),  # G08
    0x0182: ("comp_delay_heating", "Verwarming bijstook-vertraging", 1, "min", 1, 60, 1, None),  # G06
    0x0183: ("hotwater_heater_ext_temp", "Tapwater bijstook buitentemp.", 1, "°C", -30, 30, 1, "temperature"),  # G07 SIGNED
    0x0184: ("heating_heater_ext_temp", "Verwarming bijstook buitentemp.", 1, "°C", -30, 30, 1, "temperature"),  # G05 SIGNED
    0x0185: ("pump_cycle", "Pomp intervalcyclus", 1, "min", 1, 120, 1, None),  # G03
    0x018D: ("dc_pump_temp_diff", "DC-pomp temp.verschil", 1, "°C", 5, 30, 1, None),  # G04
    0x0191: ("mode_control_enable", "Moduskoppeling inschakelen", 1, None, 0, 1, 1, None),  # G09
    0x0192: ("ambient_switch_setpoint", "Buitentemp. omschakelpunt", 1, "°C", -20, 30, 1, "temperature"),  # G10 SIGNED
    0x0193: ("ambient_switch_diff", "Buitentemp. omschakelhysterese", 1, "°C", 1, 10, 1, "temperature"),  # G11
    
    # Antilegionella Configuration
    0x019A: ("antilegionella_temp", "Antilegionella temperatuur", 1, "°C", 30, 70, 1, "temperature"),
    0x019B: ("antilegionella_weekday", "Antilegionella weekdag", 1, None, 0, 6, 1, None),  # 0=Sun, 6=Sat
    0x019C: ("antilegionella_start_hour", "Antilegionella startuur", 1, "h", 0, 23, 1, None),
    0x019D: ("antilegionella_end_hour", "Antilegionella einduur", 1, "h", 0, 23, 1, None),
}

# Weekday mapping for antilegionella
WEEKDAY_MAP = {
    0: "Zondag",
    1: "Maandag",
    2: "Dinsdag",
    3: "Woensdag",
    4: "Donderdag",
    5: "Vrijdag",
    6: "Zaterdag",
}
