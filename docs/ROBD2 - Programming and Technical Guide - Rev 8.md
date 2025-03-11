# Environics

# ROBD2

# Reduced Oxygen Breathing Device 2

# Programming and Technical Guide

For instrument Serial number 5200 and higher

# Maintenance Manual

Revision 8

23 September 2013

Software rev. 1.00-XX

Environics, Inc.

69 Industrial Park Road East

Tolland, CT 06084-2805 USA

Phone (860) 872-1111

Web: Fax (860) 870-9333

E-mail: INFO@ENVIRONICS.COM

HTTP://WWW.ENVIRONICS.COM
- --
# ROBD2 Programming and Technical Guide changes

|Manual Revision #|Software Revision #|Release Date|Enhancements|
|---|---|---|---|
|1|0.96-XX|02/08/06|Initial release|
|2|0.96-XX|02/09/06|Minor changes for typographical errors|
|3|0.96-XX|01/02/07|New pulse oximeter power supply. Changes to appendices A3, B1, B9, D, E|
|4|0.97-XX|05/10/10|Added new flight simulator remote mode commands|
|5|0.97-XX|10/25/11|Removed appendix B13, made changes for New MFC to appendices B15, B16, E and J|
|6|0.97-XX|03/05/12|Made changes for new pressure sensor, modified appendices A15, B7 E and N. Modified pressure sensor calibration procedure, page 62|
|7|1.00-02|08/30/13|Added SETUP ALTITUDE to SYSTEM menu|
|8|1.00-03|09/23/13|Modified appendices H & M for changes made to the oxygen values.|
- --
# TABLE OF CONTENTS

- LIST OF ABBREVIATIONS / ACRONYMS &nbsp;&nbsp;&nbsp;&nbsp; iv
- LIST OF APPENDICES &nbsp;&nbsp;&nbsp;&nbsp; v
- OVERVIEW &nbsp;&nbsp;&nbsp;&nbsp; 1
- THEORY OF OPERATION &nbsp;&nbsp;&nbsp;&nbsp; 3
- System layout &nbsp;&nbsp;&nbsp;&nbsp; 3
- Instrument illustration drawing &nbsp;&nbsp;&nbsp;&nbsp; 6
- Functional description &nbsp;&nbsp;&nbsp;&nbsp; 7
- Gas inputs &nbsp;&nbsp;&nbsp;&nbsp; 7
- Gas flow and blending &nbsp;&nbsp;&nbsp;&nbsp; 7
- Positive pressure option &nbsp;&nbsp;&nbsp;&nbsp; 9
- Oxygen dump feature &nbsp;&nbsp;&nbsp;&nbsp; 9
- Safety features &nbsp;&nbsp;&nbsp;&nbsp; 10
- ADMINISTRATIVE MODE (ADMIN mode) &nbsp;&nbsp;&nbsp;&nbsp; 11
- Programming the instrument (PROG mode) &nbsp;&nbsp;&nbsp;&nbsp; 12
- System mode &nbsp;&nbsp;&nbsp;&nbsp; 15
- REMOTE COMMUNICATIONS &nbsp;&nbsp;&nbsp;&nbsp; 18
- Interface Specification &nbsp;&nbsp;&nbsp;&nbsp; 18
- Remote Command List &nbsp;&nbsp;&nbsp;&nbsp; 20
- Remote Error Codes &nbsp;&nbsp;&nbsp;&nbsp; 26
- ROUTINE MAINTENANCE &nbsp;&nbsp;&nbsp;&nbsp; 27
- Visual inspection before power up &nbsp;&nbsp;&nbsp;&nbsp; 27
- Packing the system for shipment &nbsp;&nbsp;&nbsp;&nbsp; 27
- Yearly Maintenance &nbsp;&nbsp;&nbsp;&nbsp; 27
- Cleaning the fan filter &nbsp;&nbsp;&nbsp;&nbsp; 28
- Replacing the particle filter element &nbsp;&nbsp;&nbsp;&nbsp; 29
- Cleaning or replacing the final filter (A221) &nbsp;&nbsp;&nbsp;&nbsp; 30
- Replacing the oxygen sensor &nbsp;&nbsp;&nbsp;&nbsp; 31
- Applying Teflon tape to pipe fittings &nbsp;&nbsp;&nbsp;&nbsp; 33
- Calibrating the Mass Flow Controllers &nbsp;&nbsp;&nbsp;&nbsp; 34
- PCB function and TEST POINTS &nbsp;&nbsp;&nbsp;&nbsp; 42
- TROUBLESHOOTING GUIDE &nbsp;&nbsp;&nbsp;&nbsp; 47
- Troubleshooting system problems &nbsp;&nbsp;&nbsp;&nbsp; 47
- Troubleshooting pulse oximeter problems &nbsp;&nbsp;&nbsp;&nbsp; 52
- Main DC power cable pinout &nbsp;&nbsp;&nbsp;&nbsp; 54
- Replacing or updating software &nbsp;&nbsp;&nbsp;&nbsp; 56
- Adjusting the low oxygen pressure switch &nbsp;&nbsp;&nbsp;&nbsp; 57
- Adjusting the internal back pressure regulator A212 &nbsp;&nbsp;&nbsp;&nbsp; 58
- Adjusting needle valve assembly A211 &nbsp;&nbsp;&nbsp;&nbsp; 59
- Testing the pulse oximeter and battery backup &nbsp;&nbsp;&nbsp;&nbsp; 61
- Checking the pressure sensor and O2 sensor ADC &nbsp;&nbsp;&nbsp;&nbsp; 62
- Calibrating adc 11 (pressure sensor) &nbsp;&nbsp;&nbsp;&nbsp; 62
- Leak test &nbsp;&nbsp;&nbsp;&nbsp; 63
- PCB assembly drawings &nbsp;&nbsp;&nbsp;&nbsp; 66
- P&ID &nbsp;&nbsp;&nbsp;&nbsp; 69
- --
# LIST OF ABBREVIATIONS / ACRONYMS

|AC|Alternating|Cu|
|---|---|---|
|EMI|Electromagnetic| |
|FSO|Full|Scale|
|FNPT|Female National Pipe Thread| |
|HZ|Hertz| |
|LCD|Liquid Crystal Display| |
|LPM|Per|Liters Minute|
|MFC|Mass Flow Controller| |
|NAG|Nitrogen and Air Generator| |
|P&ID|Piping|and|
|PWM|Pulse Width Modulation| |
|PSIG|Pounds Per Square Inch Gauge| |
|RFI|Radio Frequency Interference| |
|STP|Standard temperature and pressure| |
|SUT|Subject Under Test| |
|VAC|Volts, Alternating Current| |
|VDC|Volts, Direct Current| |
- --
# LIST OF APPENDICES

- APPENDIX A: Assembly parts list and illustration drawings
- APPENDIX B: Electrical harness drawings
- APPENDIX C: Recommended spare parts list
- APPENDIX D: List of electrical cable connections with E Grade RTV
- APPENDIX E: ROBD2 electrical wiring diagram
- APPENDIX F: Altitude/pressure curve for FSHT and OSFT modes (option)
- APPENDIX G: NSTI/ASTC Altitude/pressure curve for FSHT and OSFT modes
- APPENDIX H: Chart, respiratory physiology and ROBD2 flow rate parameters
- APPENDIX I: Power supply data sheet
- APPENDIX J: Thermal Mass Flow data sheets
- APPENDIX K: Pulse oximeter data sheet
- APPENDIX L: Oxygen sensor data sheet
- APPENDIX M: Performance test data sheet (Available as Excel file with automatic calculation)
- APPENDIX N: Breathing loop pressure transducer data sheet
- APPENDIX O: Schematics and ROBD2 specific signals
- APPENDIX P: Blank flow calibration sheet
- --
# OVERVIEW

Congratulations on your purchase of the second generation Environics’ reduced oxygen breathing device ROBD2. This manual includes information on using the restricted modes of the instrument, programming the ROBD2, communicating remotely via the RS232 port, troubleshooting, parts lists and diagrams. For information on how to run subjects on the instrument for hypoxia testing and operating the pulse oximeter, refer to the operator’s guide.

There are two levels of visible menus on the front panel display. The instrument always powers up into the default OPERATORS menu. This menu is limited to the functions of running programs on subjects and prevents access to programming steps, making changes to existing programs and other modes where system configuration can be changed. The second menu is the ADMIN menu for administrative access. This mode includes all the functionality of the operators menu but does not limit access for programming and other functions. The ADMIN mode is password protected.

The program mode is considered an administrator function and is therefore password protected. This prevents the operator from changing the program and potentially putting the subject under test at risk of becoming hypoxic prematurely or being exposed to levels of O2 below those planned for the profile setup to run for particular individuals.

The remote communication protocol (RS232) allows the ROBD2 to run remotely from a host computer. The operation of the ROBD2 can be controlled as part of an overall process/program consisting of multiple tasks. For example, the ROBD2 could be run along with a flight simulator, the functions of both being controlled by a program on the host computer.

The flexibility of the ROBD2 allows it to run independent of a computer. Its basic menu driven display allows for simple navigation of the modes on a 4 line by 20 character display. All user entered program information is retained in the system by battery backup. Also, all the user settings of the integrated pulse oximeter are backed up.

Before reading this manual, Environics commends re-reading the operator’s guide and having a complete understanding of how to operate the unit, even if it is done so without a subject under test. This allows non-qualified operators to run and understand the unit.

# IMPORTANT

The ROBD2 operator should be certified in first-aid and CPR and have access to communication in the event of an emergency.

Prior to participation in ROBD2 training or research, the subject under test should have the equivalent to a FAA physical of any class or military flight physical and be screened for current health status prior to the run.
- --
# OVERVIEW

IMPORTANT: For the most part, the ROBD2 is fairly maintenance free. Other than some yearly maintenance and calibration, the system should run trouble free for the full period in between. If some type of failure does occur, and parts or assemblies need to be replaced, it is important to note that all of the components that come in contact with 100% oxygen have been cleaned for oxygen service or built as oxygen compatible parts. The goal is to prevent any contamination, including the oils on the skin, from getting onto the wetted surfaces of the gas path. Use some type of rubber or cloth gloves when working on these components. This is for the protection of the operator, subject under test and anyone else in close vicinity to the unit.
- --
# THEORY OF OPERATION

# System layout

Listed below are the major components of the system. Refer to the top view illustration showing each numbered part. Also, refer to the P&ID at the end of this document.

1. PC401/PC412-ROBD2 assembly number A194. The PC401 (1a) is the main micro-controller board and the PC412-ROBD2 is the analog interface board for the analog devices such as the MFCs, pressure transducer and oxygen sensor. For a parts breakdown of this assembly, refer to appendix A.
2. The breathing bag port. The breathing bag is removed for shipping. This bag allows blended gas to collect and be used for individuals with larger than average lung capacity and breath rate.
3. Part number E615-6103, RS232 interface ribbon cable. This cable interconnects the main micro-controller board PC401 to the rear panel RS232 port and to the pulse oximeter PC board on front panel assembly A214 (item # 8). For a detailed illustration drawing of this cable, refer to appendix B.
4. Rear panel assembly number A215. For a parts breakdown of this assembly, refer to appendix A. Referring to the P&ID, parts labeled PS1, FIL-1 and FIL-2 are part of the A215 assembly.
5. Pulse oximeter power supply part number A205. Connects to front panel mounted pulse oximeter via electrical cable E628.
6. Optional pressure control valve assembly number A211. This valve is labeled NV1 in the P&ID.
7. Electrical terminal block assembly A206. This terminal block is used to distribute alike voltage signals +24 VDC and Ground to multiple sources.
8. Front panel assembly number A214.
9. Optional bypass valve number A210. This item as well as item # 6 make up the option to control pressure in the FSHT, OSFT and PPT modes of operation. For basic hypoxia training, as with the HRT mode of operation, these parts are not used. This valve is labeled V2 in the P&ID.
10. Crossover valve number A209. This valve is used to direct air to the MFC normally running Nitrogen. Certain steps of a program and other operating modes in the system require both MFCs to run with air. This valve is labeled V3 in the P&ID.
- --
# THEORY OF OPERATION

1. Air mass flow controller MFC1, part number MAB1-005-25000.
2. Mask particle filter part number A221. This filter prevents particles from getting up into the breathing mask. This part is labeled FIL-3 in the P&ID.
3. Oxygen dump valve part number A208. This valve interrupts the flow of mixed gas, when the O2 dump valve is activated, and provides 100% oxygen to the mask. This part is labeled V1 on the P&ID.
4. Input particle filter number VA-FIL-004. The air port and N2 port are filtered to prevent any particles from entering the system. These parts are labeled FIL-1 and FIL-2 on the P&ID.
5. Nitrogen mass flow controller MFC2, part number MAB1-005-77000.
6. Back pressure regulator assembly A212. This regulator provides stability on the outputs of the MFCs to prevent the pressure fluctuations, of breathing off the mask, from affecting the controlled flow rates. This regulator also serves to control the pressure on the oxygen sensor filtered orifice, to accurately control 150 SCCM of flow into the sensor. This part is labeled BPR1 on the P&ID.
7. Data interface cable, part number E609-ROBD2. This flat ribbon cable carries data to and from the PC401 microcomputer board, the PC406 display board, the PC412-ROBD2 analog interface board and the PC416 solenoid driver I/O board. Refer to appendix B for details of this cable.
8. Oxygen interface PCB, part number SK10-001-PCB. This board conditions the signal from the oxygen sensor, linearizes it and converts it to a voltage scale which is sent to the PC412-ROBD2 analog interface board. A calibration curve is then applied by the software in the system and the result is displayed as an oxygen percentage in various operating modes of the system.
9. Power cable, part number E613-ROBD2. This cable carries the DC voltage power from the system power supply, item 23, to the analog interface board, PC412-ROBD2. A large power resistor has been added to the side panel to ensure proper loading requirements on the power supply to get well regulated voltages.
10. Pulse oximeter speaker, part number AK01-002. This speaker sounds the pulse oximeter alarm features which are configurable from the pulse oximeter key controls on the front panel of the system. The pulse tone and alarms are separately configurable; see the operator’s manual for more details.
- --
# THEORY OF OPERATION

# 21.

Solenoid valve driver and I/O board, part number PC416. This board interfaces with the oxygen dump switch, the low oxygen pressure switch on the oxygen port and the solenoid valves used to isolate and direct the gas flow. This board also powers the fan and has additional I/O for future expansion and options.

# 22.

Breathing loop pressure transducer, part number A215. This sensor monitors the pressure of the gas in the breathing loop which is displayed in various operating modes. This part is labeled PX1 on the P&ID.

# 23.

System power supply, part number PJ02-14-004. This quad output power supply generates the +5 VDC, +/- 15 VDC and 24 VDC voltages necessary to power all the electrical components in the system.
- --
# THEORY OF OPERATION

Instrument illustration drawing

| | | | |1b|1|
|---|---|---|---|---|---|
|3|2| | |8| |
| | | | |6|7|
| |4|5| | | |
| | | | |9| |
| | | | |12|13|
| | | |11|10| |
| | | |15| | |
| | |14| |16| |
|17| | |18|19|20|
| | | | |22|23|
| | | |21| | |
| | | | |6| |
- --
# THEORY OF OPERATION

# Functional description

# Gas inputs

There are three gas inputs on the rear panel of the ROBD2. On the standard instrument, without the hose and regulator option, these inputs are ¼” FNPT.

Environics offers a hose and regulator option. With this option, each gas input has a keyed and colored quick connect fitting both on the back of the instrument and on each gas regulator. The Oxygen port (green) requires 20 PSIG input pressure. The Nitrogen port (black) requires 40 PSIG input pressure. The Air port (yellow) requires 40 PSIG input pressure. These pressures are the same without the hose and regulator option. The gas lines, provided as part of this option, are ten foot 316 stainless steel flexible braided hoses. The pressure regulators provided are dual stage and have the CGA connectors for breathing air (CGA 346), medical grade nitrogen (CGA 580) and medical grade oxygen (CGA 540). When ordering the option, specify HOSE-REG-OPT. To order 20 foot hoses, specify HOSE-REG-OPT-20.

# Gas flow and blending

(refer to P&ID at the end of this document)

Through the rear panel, pressurized air and nitrogen enter each respective port and flow into individual particle filters. These filters remove any condensate and particles larger than .0002”. The individual gases then flow through thermal mass flow controller one (MFC1 for air) and two (MFC2 for nitrogen). Dependent upon the programmed altitude, the system will produce the correct ratio of air to nitrogen flow to produce the correct sea level equivalent oxygen content for that altitude, refer to appendix H. As the programmed altitude increases, the volume of gas delivered to the mask will increase. This increase in flow is in response to increased lung capacity and breaths per minute as the subject under test is deprived of oxygen; reference appendix H.

The gas exits each MFC and mixes in the zone between the outputs of the MFCs and the input to the back pressure regulator (BPR1). BPR1 serves two purposes. The primary function is to control the pressure to the oxygen sensor fixed orifice. At 5 PSIG, the orifice controls the flow to approximately 150 SCCM into the oxygen sensor at all times, regardless of the total flow delivered to the breathing loop. The second purpose of the BPR1 is to control the pressure differential across the MFCs, which buffers the MFCs from the pressure disturbances of the inspiratory and expiratory cycle of the subject under test. Pressure gauge G1 reads the pressure upstream of BPR1 and should always read 5 PSIG. This pressure regulator and pressure gauge are located inside the system. Adjustments to this regulator are rarely needed. The pressure gauge is mainly there for setup, troubleshooting and verification purposes. All gas connections exiting the back pressure regulator are considered to be part of the breathing loop. All of the components in the breathing loop are in direct pneumatic connection with the output port that connects to the pilots mask. Note, the breathing loop is highlighted in red on the attached P&ID.
- --
# THEORY OF OPERATION

Solenoid valve V3, on the input of MFC2, allows certain operating modes to use both MFCs with air only. For instance, the PPT mode provides 95 LPM air to the mask at a pressure of 10” HO. Since this cannot be accomplished with one MFC, both are used together to provide the high flow rate of air. Also, whenever a sea level (zero altitude) step is used in a program, both MFCs are used with air.

Solenoid valve V1 is used to direct either the mix of gases, produced by the MFCs, or 100% oxygen to the breathing loop and breathing mask. 100% O2 is used for the calibration of the O2 sensor and when the O2 dump switch is activated. 100% O2 is also sent to the mask when certain safety features are violated; see safety features below. This valve is also referred to as the oxygen dump valve.

The oxygen pressure switch (PS1), on the input of the oxygen port, is used to detect low O2 tank pressure; see safety features below.

The breathing loop pressure port, on the rear panel of the system, can be used to connect a mechanical pressure gauge or pressure transducer for monitoring breathing loop pressure. This port will normally be plugged when the system is operating and has mainly been installed for troubleshooting and verification purposes. The system has a built In breathing loop pressure transducer. If the plug is not installed during normal operation, then the positive pressure option will not function correctly.

The standard system has been designed to work with a sealed breathing mask. This means that the flow of gas cannot be sent directly to the mask without venting some portion of that flow. The venting portion of the plumbing path allows the breathing loop pressure to remain close to 0” HO during basic hypoxia recognition testing or training (HRT mode). This is accomplished by building up enough pressure internally to inflate the breathing bag. The breathing bag acts as a reserve to accommodate those with larger lung capacities or someone breathing at a higher rate than normal. Once the breathing bag inflates, the excess flow is driven out of the vent port on the rear panel of the system. The inflation of the breathing bag is dependent upon the subject under test having the mask secured to the face.

Check valve CHV1 prevents the breathing loop from ever exceeding 1 PSIG (27” H20).
- --
# THEORY OF OPERATION

# Positive pressure option

Needle valve adjustment NV1 allows each individual system to be setup to produce the positive pressure breathing requirements of the FSHT (Flight Simulator Hypoxia Training), OSFT (Oxygen System Failure Training) and PPT (Positive Pressure Training) modes of the system; see appendix F. These modes are primarily used for training US NAVY fighter pilots.

The pressures generated are consistent with those produced in the pilot’s mask at high altitudes. At a high enough altitude, the partial pressure of the ambient oxygen is insufficient to drive oxygen into the bloodstream from the lungs even if the pilot is breathing 100% oxygen. The application of positive pressure is supplemental to help drive the oxygen from the lungs at high altitudes.

Bypass valve V2 closes for the positive pressure requirements of these modes and opens for the HRT (Hypoxia Recognition Training) mode. When bypass valve V2 is open in the HRT mode, it minimizes the pressure in the breathing loop to approximately 0-2” H2O, altitude dependent. The requirements of the HRT mode are to keep the breathing loop pressure as close to 0” HO as possible. The large orifice bypass valve V2 accomplishes this goal during the HRT mode. By closing V2 for the positive pressure modes, it forces all flow through needle valve NV1. NV1 is set to provide slight positive pressure, in the breathing loop, with increasing altitudes above 28,000 feet.

The 3 liter breathing bag is externally mounted. This breathing bag satisfies the short, deep breaths that the system flow cannot satisfy alone. The vent port will exhaust the gas flow that is not used during the expiratory part of the breathing cycle.

# Oxygen dump feature

Valve V1 controls the flow of 100% oxygen to the pilots mask during an oxygen dump. An oxygen dump is performed when the system operator engages the emergency dump switch on the front panel. This will normally be done when the operator has determined that the subject under test has become hypoxic and needs to recover. The mixing action of the MFCs will stop and the output of the MFCs will be isolated from the pilot’s mask. The .070” orifice will control the flow of 100% oxygen to the pilots mask.
- --
# THEORY OF OPERATION

# Safety features

There are several built-in safety features to either alert the operator or stop the operation of the system and go to a “safe” mode of operation.

# Oxygen pressure switch PS1

The oxygen pressure switch monitors the input pressure on the oxygen port. If this pressure is less than 10 PSIG, the system will not allow the START mode (pilot test menu) to be used. This pressure should normally be set at 20 PSIG. Once the pressure on the oxygen port is restored to above approximately 13 PSIG, the system can be used as normal.

# Oxygen alarm

The O2 alarm will sound for two different scenarios. After pressing the emergency oxygen dump switch, if the O2 has not reached 90% in 5 seconds, the alarm sounds. The alarm will remain active until the emergency switch is turned off. Also, if during an O2 dump, the oxygen content drops below 90%, the alarm will sound. The O2 content, as read by the internal oxygen sensor, is displayed during the oxygen dump routine.

# Oxygen analysis

Using the onboard oxygen sensor, if the oxygen content in any pilot test mode drops below 3.8%, the system will automatically turn on the oxygen dump and display a warning message. 3.8% was selected because the lowest O2 content produced during normal operation is 4.4% at 34,000 feet.

# Overpressure detect

Using the onboard pressure sensor, if the pressure in the breathing loop rises above 20” H2O, the system will turn on the oxygen dump and open the bypass valve, bringing the breathing loop pressure down to zero.

# Pressure relief valve

As a back up to the over pressure detect, this mechanical pressure relief valve prevents the pilot’s mask from exceeding 27” H2O or 1 PSIG.

# Low air flow detect

The air MFC (MFC1) has an alarm signal that activates if the internal MFC valve opens to maximum capacity. This generally indicates that there is not enough pressure on the MFC to satisfy the required flow rate. This would lead to elevated N2 levels in the breathing loop during normal operation. This feature uses the MFC alarm signal to stop flow and provide 100% oxygen to the breathing loop. A message appears indicating the failure.
- --
# ADMINISTRATIVE MODE (ADMIN MODE)

The Administrative mode is a limited access mode and is password protected. Access to this mode allows for changing program information, calibration data, and accessing troubleshooting features.

When the system is in the normal operator’s mode (READY screen), the only two menu items, as seen on the bottom line of the display, are START and OPTION. When the system is in the ADMIN mode, a secondary menu appears in the READY screen. The two menu selections are Program (PROG) and System. Toggle back and forth between the operator’s menu and the Admin menu by pressing the MENU key.

Each time the instrument is powered off and on, and the self tests are run, the system automatically enters the operator’s menu. To enter the ADMIN mode, perform the following:

1. From the ready screen or operator’s menu (seen below), select OPTION.

|(DAY)|(DATE)|(TIME)|
|---|---|---|
|ENVIRONICS ROBD2|READY| |
|START|OPTION| |

Select OPTION (F3), arrow down to ADMIN mode and press ENTER.

Enter the 4 digit numeric password, factory default 1234. This password can be changed once in the ADMIN mode, refer to SYSTEM mode in the index.

Once the 4 digit password has been entered, the screen will display MIN ADMIN MODE ENABLED and automatically exit back out to the ready screen. The display will now appear in the ADMIN mode, see below.

|(DAY)|(DATE)|(TIME)|
|---|---|---|
|ENVIRONICS ROBD2|READY|ADMIN|
|START|OPTION| |
- --
# ADMINISTRATIVE MODE (ADMIN MODE)

Once in the ADMIN mode, access is granted to two other menu items. Press the MENU key to display the following screen.

|(DAY)|(DATE)|(TIME)|
|---|---|---|
|ENVIRONICS ROBD2|READY|ADMIN|
|PROG| |SYSTEM|

# Programming the instrument (PROG mode)

The program mode is used to create a sequence of up to 99 steps, which later run automatically when selected in the RUNPRG mode. The RUNPRG mode is part of the PILOT TEST menu within the START menu. The system can store up to 20 programs with up to 99 steps each.

Each step can be programmed as either a HOLD or CHANGE step. For a HOLD step, the system will hold at the specified altitude for the specified amount of time, up to 60 minutes in 1 minute increments, and produce the equivalent oxygen content for that altitude. When programming two HOLD steps in a row, the system jumps instantaneously from one altitude to another. To program a hold step for more than 60 minutes, simply insert a second hold step at the same altitude. For a change step, the system decreases or increases the equivalent O2 content, at the specified ascent or descent rate. Using this information, the system determines total step run time for display purposes in the RUN mode.

For a HOLD step, the user must specify the altitude and hold time in seconds.

For a change step, the user must specify the new altitude and rate of change. If a change step is specified as the first step in a program, the system assumes starting at sea level.
- --
# ADMINISTRATIVE MODE (ADMIN MODE)

Perform the following steps to enter a program of altitudes.

1. Select PROG F1()
2. A right pointing arrow in the farthest left column will align with the current program number.
3. To create a new program or to select a program to edit, arrow down to the program number (1-20) and select EDIT (F1).
4. To create or edit the program name, use the up and down arrow keys to select the letters/numbers/characters and the right and left arrow keys to select the character position within the program name. Each program can have up to 11 characters, including spaces.
5. Press ENTER to accept the program name.
6. Use the TOGGLE key to select the program mode of operation. HRT (Hypoxia Recognition Training), FSHT (Flight Simulator Hypoxia Training) or OSFT (Oxygen System Failure Training) and select OK (F3).

# Program Modes

# HRT

The basic Hypoxia Recognition Training mode of operation runs altitudes without adjusting the breathing loop pressure, but provides the sea level equivalent O2 for the programmed altitude. The pressure in the breathing loop is maintained close to 0” 2H0. Hold and change altitudes can be programmed. Hold altitudes require a hold time in minutes, change (CHGALT) altitudes require an ascent/descent rate in feet/minute (60000 ft/min max.).

# FSHT

Runs altitudes while adjusting breathing loop pressure above 28,000 feet; reaching a ceiling of 34,000 feet at approximately 4” H0. The sea level O2 equivalent is also adjusted while altitude increases as with HRT. Hold and change altitudes can be programmed. Hold altitudes require a hold time in minutes, change (CHGALT) altitudes require an ascent/descent rate in feet/minute (60000 ft/min max.).

# OSFT

Runs altitudes while adjusting breathing loop pressure above 28,000 feet; reaching a ceiling of 34,000 feet. O2 content remains at 21% until the O2 FAIL key is pressed while in the pilot test mode. Once O2 FAIL is pressed in the pilot test mode, the O2 content will adjust to the sea level equivalent for that altitude while maintaining pressure above 28,000 feet. Hold and change altitudes can be programmed. Hold altitudes require a hold time in minutes, change (CHGALT) altitudes require an ascent/descent rate in feet/minute (60000 ft/min max.).

Refer to appendix F for the altitude to pressure curve for the FSHT and OSFT modes.
- --
# ADMINISTRATIVE MODE (ADMIN MODE)

7. When on the row for a program step, the step can either be deleted or a new step can be inserted. Pressing the right arrow key will bring up the edit menu to select hold or change selections. After selecting the hold or change step and altitude, pressing the right arrow key will advance the cursor to the time/rate column.

# SAMPLE SCREEN IN PROGRAM MODE:

|STEP #|#|ALT|TIME/RATE|
|---|---|---|---|
|1|H|0 FT|FOR 20 S|
|2|C|20000 FT|@ 1000 F/S|
|DELETE|INSERT|EXIT| |

14
- --
# ADMINISTRATIVE MODE  (ADMIN MODE)

# System mode

The system mode contains features that are used by Environics when calibrating the system. Some of these features can be used for advanced troubleshooting under the direction of technical staff. The ADMIN mode password can also be changed in this mode. When troubleshooting a problem, the warm up time and self test routine can be bypassed in this mode.

# Test flow mode

The TEST FLOW mode is used to individually flow each MFC at a particular flow rate. The flow rate is user selectable within the full range of the MFC. This mode is used by the factory for verifying the accuracy of the MFC calibration and can be used as a troubleshooting tool as well. The test flow mode uses the MFC calibration data to provide a corrected accurate flow rate for an STP of 0°C and 14.7 PSIA.

To enter the TEST FLOW mode, select the SYSTEM mode, arrow down to the TEST FLOW menu item and press the ENTER key. The following screen will appear.

|TARGET FLOW SET BY USER|TARGET FLOW SET BY USER|ACTUAL FLOW BASED ON FEEDBACK VOLTAGE FROM MFC| |
|---|---|---|
|FLOW|TARGET| |
|MFC1|0.000 L| |
|MFC2|0.000 L| |
|UPDATE STOP EXIT|UPDATE STOP EXIT| | |

Enter the desired flow rates for one or both MFCs into the target column. Enter the flow rate in LPM. Pressing the update key will begin the flow of gas. MFC1 will flow the gas connected to the AIR port and MFC2 will flow the gas connected to the N2 port. The target flows can be updated while running, without stopping and starting the system. Once flow has stabilized, the flow in the actual column should equal the target flow. The display of actual flow is a function of the feedback voltage from the MFC. The MFC command and response voltages can be monitored on the PC412-ROBD2, refer to the section containing the PCB layout drawings and PCB function and test point section as well.

# WARNING

Never use this mode when a subject is breathing off the mask. 100% N2 will be sent to the breathing loop when flowing MFC2.
- --
# ADMINISTRATIVE MODE (ADMIN MODE)

# Bypass warmup time

The 10 minute warm up time, that counts down after power is applied to the system, can be disabled for trouble shooting purposes.

1. From the system menu, arrow down to BYPASS WARMUP TIME and press the ENTER key.
2. Select YES (F1).
3. This will bypass the warm up time while the instrument is powered on. This procedure needs to be performed each time the system is powered off and on.

# Bypass self tests

Like the Bypass warmup time feature, this feature allows the service technicians to bypass the self test feature for troubleshooting purposes. This feature will disable self tests as long as the instrument is powered on. Once the power is turned off and on again, the feature resets and will need to be disabled again.

1. From the system menu, arrow down to BYPASS SELF TESTS and press the ENTER key.
2. Select YES (F1).

# Setup Altitude

Setup Altitude controls whether feet/min or feet/sec are used as an ascent or descent rate for a change altitude step in a program. Also, hold steps can be set as minutes or seconds. Note: the setting is universal for all programs and program steps. Within this mode, the maximum altitude for programs can be defined.

1. From the system menu, arrow down to Setup Altitude and press the ENTER key.
2. Use the down arrow key to select the line item to change.
3. For Alt Rate and Hold Time, use the right arrow key to toggle.
4. For Max Alt, use the numeric keypad to enter an altitude between 34000 and 40000 feet. The default value is 34000.
5. Press exit when done.
- --
# ADMINISTRATIVE MODE  (ADMIN MODE)

Password protection (change password)

The system mode can be password protected, as this mode contains all the data that impacts the accuracy of the system. The system is shipped with the password set to 1234. A four character numeric password is set within the SYSTEM mode. Upon any attempts to reenter the system mode, after setting a password, the user will be prompted to enter the password to gain entry. Be sure to record this password and keep it in a safe and secure location.

1. Select the SYSTEM mode.
2. Arrow down to CHANGE PASSWORD and press the ENTER key.
3. Enter the 4 digit numeric password and press DONE.
4. EXIT back out of the SYSTEM mode and press the SYSTEM key. A prompt should appear for a password entry.
5. Enter the previously selected 4 digit numeric password to verify the process.

ENTER NEW PASSWORD

OR SELECT         ‘NONE’

PASSWORD: XXXX

DONE          NONE         CANCEL

Calibrate MFC, Calibrate ADC, Pulse Oximeter, Edit Alt flow tbl, Edit alt press tbl and Edit prs ctrl tbl. The latter four modes, within the SYSTEM menu, are currently used by Environics only. However, at some point, as directed by Environics, technical personnel may be directed to enter these modes for advanced troubleshooting. Please refrain from entering these modes, unless under direction from Environics. If data is changed within these modes, system accuracy is compromised. Calibrate MFC mode is covered in the MFC calibration section.

17
- --
# REMOTE COMMUNICATIONS

The system has a remote communications port, which allows it to be controlled remotely by a host computer. The host computer communicates with the system through the RS232 port located on the rear panel.

The system will respond to commands issued by the host computer, but will not issue any unsolicited messages to the host, except to acknowledge a command or to return an error code.

# Interface Specification

The communication interface is a standard RS-232C serial interface, connected via a Male DB-9 connector. The system operates as a DTE (Data Terminal Equipment) device, requiring a null modem cable to connect to a PC.

Communication port parameters are: 1 Start bit, 8 data bits, 1 Stop bit, No parity bit. The speed of the communications port is fixed at 9600 baud.

# Data Format

All remote communications use standard ASCII characters. Commands are terminated with either (or both) of these single byte ASCII codes:

- &lt;CR&gt; Carriage Return (ASCII Code 0x0D) - This is used to indicate the end of a command.
- &lt;LF&gt; Linefeed (ASCII Code 0x0A) - This is used to indicate the end of a command.

# Command Format

Commands sent to the system must be formatted as follows:

COMMAND FORMAT: COMMAND &lt;CR&gt;&lt;LF&gt;

The system recognizes the end of the command when it sees a &lt;CR&gt; and/or &lt;LF&gt; character. Commands are not case sensitive.

For each command sent, be sure to wait for a valid response from the system before sending a new command.
- --
# REMOTE COMMUNICATIONS

# Reply Format

All replies from the system to the host computer will be formatted with one of three formats shown, depending on the type of response required.

# COMMAND ACCEPTED

If the command received requires no data to be returned, the system will acknowledge that it successfully received and performed the command. This will be indicated by:

RESPONSE:         OK<CR><LF>

# DATA RETURNED

For commands that require data to be returned, the data will be formatted as follows. If the data consists of a list of values, each value will be separated with a comma.

RESPONSE:                                data<CR><LF>
EXAMPLE:                            5000.0<CR><LF>

# ERROR RETURNED

If the command received contains errors, or cannot be performed by the system, an error code will be returned. The error message is formatted as:

RESPONSE:         ERR(error code)<CR><LF>
EXAMPLE:                            ERR12<CR><LF>

# Format Of Numeric Data

All numerical values for physical parameters such as Altitude, Pressure, etc. are formatted as floating point values. These values are indicated by the format "x.xxx"

Whole number values (for specifying program step, etc.) must be specified without a decimal point. These values are indicated by the format "n"

19
- --
# REMOTE COMMUNICATIONS

# Remote Command List

# ROBD2 PROGRAMMING COMMANDS

These commands are used to set up and review the ROBD2 program steps. A total of 20 programs can be created, each with up to 99 steps.

|COMMAND|DESCRIPTION|
|---|---|
|PROG n NAME progname|Assign program name|
|PROG n NAME ?|Get name of program|
|PROG n MODE progmode|Assign program operating mode|
|PROG n MODE ?|Get program operating mode|

Command parameters:

- n = Program # (1-20)
- progname = Name of program (10 characters max.)
- progmode = Program operating mode:

|PROG n s mode alt value|Create a program step.|
|---|---|
|PROG n s ?|Display program step parameters.|

Data is returned as: mode alt value

Command parameters:

- n = Program # (1-20)
- s = Step # (1-98) (Step 99 is always END and cannot be changed)
- mode = HLD (hold), CHG (change), or END (end of program)
- alt = Target Altitude (in feet)
- value = Hold Time (in minutes) for a HLD step, -or- Rate Of Change (in ft/min) for CHG step.
- --
# REMOTE COMMUNICATIONS

# ROBD2 OPERATING COMMANDS

These commands are used to control the ROBD2.

|COMMAND|DESCRIPTION|
|---|---|
|RUN READY|Enter PILOT TEST mode Put software into the Pilot Test mode. Equivalent to pushing START from the Main Menu.|
|RUN EXIT|Exit PILOT TEST mode Exit from the Pilot Test mode. Equivalent to pushing EXIT from the Pilot Test Menu.|

The following RUN commands require the software to be in the Pilot Test mode

|COMMAND|DESCRIPTION|
|---|---|
|RUN n|Run the specified program n = program # to run (from 1 to 20)|
|RUN NEXT|Advance to next program step While running a program, this advances the program to the next step. This is equivalent to pressing the ADVANCE key from the front panel.|
|RUN PPT IDLE|Enter POSITIVE PRESSURE TEST Mode Enter the Positive Pressure Breathing test menu. This command is equivalent to pressing PPT from the Pilot Test menu.|
|RUN PPT START|Start POSITIVE PRESSURE TEST Start the Positive Pressure Breathing Test. Flow air to mask at 95 LPM, at a pressure of 10 in. H20.|
|RUN PPT STOP|Stop POSITIVE PRESSURE TEST Stop the Positive Pressure Breathing Test. Mask pressure is reduced back to 0 in. H20, and flow is reduced back to approximately 16 LPM.|
- --
# REMOTE COMMUNICATIONS

# RUN O2FAIL

Toggle the O2 Failure state

For programs configured for OSFT mode, this command toggles the state of the O2 Failure simulation. This is equivalent to pressing the O2FAIL button from the menu while a program is running. Refer to the RUN PROGRAM section of the manual for more information.

# RUN ABORT

Abort current test

Abort the current program or test, and return to the Pilot Test menu.

# SET O2DUMP

Set the Oxygen Dump state.

n=1, turns the Oxygen Dump ON

n=0, turns the Oxygen Dump OFF.

This command has the same effect as pressing/releasing the O2 Dump switch on the front panel.

22
- --
# REMOTE COMMUNICATIONS

# ROBD2 STATUS COMMANDS

These commands are used to get ROBD2 status information.

NOTE: SpO2 and Pulse data is valid only after entering PILOT TEST MODE. Altitude and Elapsed/Remaining Time are valid only while running a Program.

|COMMAND|DESCRIPTION|
|---|---|
|GET RUN O2CONC|Get Concentration in the breathing loop|
|GET RUN BLPRESS|Get the Breathing Loop Pressure|
|GET RUN SPO2|Get SpO2 reading from Pulse Oximeter|
|GET RUN PULSE|Get Pulse reading from Pulse Oximeter|
|GET RUN ALT|Get the Current Altitude for the current step|
|GET RUN FINALALT|Get the Final Altitude for the current step|
|GET RUN ELTIME|Get the Elapsed Time of the current step|
|GET RUN REMTIME|Get the Remaining Time for the current step|
|GET RUN ALL|Get all run data. Data format is: mm-dd-yy hh-mm-ss, program#, current alt, final alt, o2conc, breathing loop pressure, elapsed time, remaining time, spo2, pulse|
|GET INFO|Returns the system model number, software revision and serial number|
|GET MFC n|Get the current flow rate for MFC n|
|GET ADC n|Get the voltage for ADC device n|
|GET O2 STATUS|Get the 100% O2 source status. Returns "1" if the 100% O2 source pressure is OK. Returns "0" if the 100% O2 source pressure is LOW.|
- --
# REMOTE COMMUNICATIONS

# GET STATUS

Returns a 1 if system is not ready (warmup time not expired, low O2 pressure, or self tests not completed) Returns a 0 if system is ready.

# FLIGHT SIMULATOR COMMANDS

# RUN FLSIM

Puts the system into Flight Simulator Tracking mode. You must first issue the "RUN READY" command, just as you would when you want to run any other mode, then RUN FLSIM. When in Flight Simulator mode, the screen will display FLIGHT SIM TRACKING along with the current altitude, o2 conc, and breathing loop pressure. No keyboard commands are accepted. To exit from this mode, use the "RUN ABORT" command, like you normally would for other run modes.

# SET FSALT nnnnn

Sets the Flight Sim Altitude to nnnnn. Value must be <= 34000 Sending too many SET FSALT commands will return an ERR99, which means you've overflowed the command buffer for the flight simulator mode. The software will store the last 5 altitude commands, but since it updates the MFCs only once per second, you shouldn't need to send this command more often than that anyhow.

When in the Flight Sim mode, the GET RUN ALL command will behave as normal, with the following changes:

- Program # will be 99, to indicate Flight Sim mode
- Elapsed time will reset to 0 each time you give a new SET FSALT command
- Remain time will always be 1 second.
- --
# REMOTE COMMUNICATIONS

# Remote Command example:

The following example shows how to program and operate the ROBD2. Commands are shown first with a description of each command. The response from the ROBD2 is shown indented below each command.

PROG 1 NAME TEST001                      Assign name “TEST001” to Program 1
OK
PROG 1 MODE 0                            Set Program mode to HRT mode
OK
PROG 1 1 HLD 0 1                         Prog 1, Step 1: Hold at 0 feet for 1 min.
OK
PROG 1 2 CHG 5000 5000                   Step 2: Change to 5000 feet at 5000 ft/min.
OK
PROG 1 3 HLD 5000 2                      Step 3: Hold at 5000 feet for 2 min.
OK
PROG 1 4 CHG 30000 10000                 Step 4: Change to 30000 feet at 10000 ft/min.
OK
PROG 1 5 END                             Step 5: End of program.
OK
PROG 1 2 ?                               Display Prog 1, Step 2 information.
CHG 5000 5000                         > Change to 5000 ft at 5000 ft/min
GET O2 STATUS                            Get status of 100% O2 source
1                                     >  O2 pressure is OK
RUN READY                                Enter Pilot Test mode
(required to run a program)
OK
RUN 1                                    Start running Program 1.
OK
GET RUN ALL                              Get Status information
12-31-05 17:55:49,1,0,0,21.04,3.12,3,57,99.2,68
RUN NEXT                                 Advance to the next step
OK
GET RUN ALL                              Get Status information
12-31-05 17:56:05,1,975,5000,20.98,3.09,9,51,99.2,67
RUN ABORT                                Abort program
OK
RUN EXIT                                 Exit Pilot Test Mode
OK
- --
# REMOTE COMMUNICATIONS

# Remote Error Codes

|ERROR|DESCRIPTION|
|---|---|
|4|COMMAND OVERFLOW The input command is too long. Commands are limited to 79 characters.|
|12|UNKNOWN COMMAND An unknown command was received.|
|18|COMMAND ERROR Specified command is recognized but does not match the required format.|
|19|TOO MANY TOKENS Command contained too many data elements to be processed.|
|53|VALUE OUT OF RANGE One of the specified values is out of range.|
|60|UNKNOWN PROG STEP Unknown program step type. Must be HLD, CHG or END|
- --
# ROUTINE MAINTENANCE

# Visual inspection before power up

Items to check after removing the instrument and supplemental parts from the transport case. This would be either when receiving the instrument from Environics or during shipment from one location to another.

- Make sure the breathing bag has no rips or punctures.
- Make sure the finger probe has not been damaged.
- Remove the cover from the system and make sure (visually) that all assemblies, electrical cables and tubing connections are secure.
- Make sure that the regulator fittings are clean and free of any packing material.

During power up, the self tests will catch any potential problems. Once the self tests and self calibrations have run, and the system enters the ready mode, plug in the pulse oximeter probe and make sure no errors appear on the pulse oximeter. The finger probe icon should disappear once the probe is connected to the system and placed on the finger. Once removed from the finger, the alarm will sound. Refer to the operator’s guide for pulse oximeter operation.

# Packing the system for shipment

- Pulse oximeter probe should be placed in original package when shipped.
- Regulators should be placed in individual plastic bags for shipping.
- Hose fittings and rear panel fittings should be plugged or capped.
- System should be placed in original plastic bag.
- Breathing bag should be placed in plastic bag.

# Yearly Maintenance

|Environics’ Part Number|Description|Replacement|
|---|---|---|
|FB07-002-FM|Fan filter media, 45 PPI (replace or clean)|1 year|
|MA04-003-005|Filtered orifice, .005", replace with SK10-001|2 years|
|PA04-02-001|Viton tube, Oxygen sensor, replace with SK10-001|2 years|
|SK10-001|Oxygen sensor|2 years|
|VA-FIL-004-E|Filter elements, 5 micron, for input gas filters|1 year|
|RECAL AND TUNE UP|Mfc 21 pt calibration, system performance test|1 year|
- --
# ROUTINE MAINTENANCE

# Cleaning the fan filter

The fan filter should be removed for cleaning at least once per year (more often if it is visibly dirty.) Proceed as follows:

1. Gently pry off the retainer with a screwdriver. Do not unscrew the mounting screws in the guard.
2. Carefully pull out the filter media. You may either vacuum it clean, or wash it gently in warm sudsy water. Be careful not to tear the filter.
3. If the filter has been washed, blot it well between sheets of paper towels, then allow it to dry.
4. Reinstall the filter by holding it in place over the fan opening, then snapping the retaining grid in place.

GUARD

MEDIA

SNAP-FIT RETAINER

28
- --
# ROUTINE MAINTENANCE

# Replacing the particle filter element

# Filter Parts Identification List

|Item#|Description|
|---|---|
|19|Bowl|
|20|Gasket (2)|
|21|Filter Element|
|22|Filter Holder|
|23|Deflector|
|24|O-ring (body to bowl)|
|25|Body|
|26|O-ring (drain to bowl)|
|27|Manual Drain (twist style)|

TORQUE: 12 in-Ibs

Torque Bowl to bottom stop, then back off Bowl 22 to 45. TORQUE finger tight.

Caution: Shut off air supply and exhaust the primary and secondary pressure before dis-assembling the unit. (Units may be serviced without removing them from the air and nitrogen lines.)

# Replacing Filter Element (VA-FIL-004-E)

1. Unscrew the threaded bowl (19) and filter holder (22). The filter element (21), deflector (23) and at least one gasket (20) will drop out with the filter holder.
2. Remove large o-ring (24), deflector (23), filter element (21), and two gaskets (20). Note, top gasket (20) and o-ring (24) may not come out when removing the threaded filter element holder. They may be stuck from compression inside the cap body (25). The gasket (20) and o-ring (24) will be visible up inside the body and can be removed easily.
3. If necessary, clean the bowl (19) before re-assembling the unit. Use a mild soap solution and water only. DO NOT use cleansing agents such as acetone, benzene, carbon tetrachloride, gasoline, toluene, etc., which are damaging to this plastic.
4. Install new deflector, filter element, and new gaskets onto filter holder.
5. Attach element holder to body. Torque from (8 to 12 in-lbs).
6. Replace o-ring (24) onto bowl top. To assist with retaining bowl’s o-ring while installing bowl, lubricate the o-ring with Dupont Krytox lubricant for oxygen compatible parts. Place the o-ring in the outer diameter groove at the very top of the bowl. Do not use the lubricant that comes with the filter element kit.
- --
# ROUTINE MAINTENANCE

# Cleaning or replacing the final filter (A221)

The final filter is meant to capture any particles that may have entered the system during assembly, or during the replacement of a part, and prevent them from entering the breathing mask. The input filters catch any particles entering the system. As a result, this filter should last indefinitely and should only require yearly inspection. An indication that the filter is clogged to the point where it should be cleaned or replaced is that it gets harder and harder to breathe through the mask via the vent port. This can be observed by simply breathing through the mask with the system in the ready mode or powered off altogether.

1. Reference the A221 drawing in Appendix A, page A16. Remove clamp item 10.
2. This will expose the screen filter item 50.
3. Remove the screen filter and inspect.
4. Blow out the filter with compressed air or clean it with a mild soap solution. If necessary, replace the filter. Be sure the filter is dry before reinstalling.
5. Making sure it is properly aligned, reinstall the filter screen and the clamp to the tightness observed in step 1.

CLAMP

CLAMP REMOVED

FILTER SCREEN EXPOSED

A221

30
- --
# ROUTINE MAINTENANCE

# Replacing the oxygen sensor

The average replacement period for the oxygen sensor (Environics’ part number SK10-001) is 2 years. However, an indicator that the oxygen sensor has deteriorated to the point that it needs to be replaced is that the system will not pass the oxygen sensor calibration; refer to the Operator’s Guide section titled Self Calibration operations, oxygen sensor calibration. When replacing the oxygen sensor, Environics highly recommends replacing the filter orifice fitting. This fitting controls the flow into the oxygen sensor at 150 SCCM. This fitting has a built-in mesh filter to prevent particles from clogging the orifice of the fitting. Over time, the filter itself can become clogged by particles. The instructions to replace this fitting are part of the following procedure.

1. Remove the flat ribbon cable from the end of the oxygen sensor, see illustration on the next page.
2. Referencing Appendix A, assembly number A207, locate the two Kept nuts (item 40) on the bottom side of the instrument and remove.
3. Remove the A207 assembly. As the A207 is removed, slide the Viton tube off the blue barbed fitting on the oxygen sensor.
4. Remove the stainless steel safety wire with needle nose pliers or diagonal cutters if it will be replaced.
5. Open the clamp that holds the oxygen sensor in place and remove the oxygen sensor.
6. Referring to appendix A, A207 parts list, tighten the clamp screw (item 20) if necessary.
7. Install the new oxygen sensor in the same orientation as the one that was removed, making sure the blue barb fittings is located in the same orientation.
8. Close the clamp. If necessary, add one or two revolutions of electrical tape onto the sensor to make sure the O2 sensor is held firmly in place.
9. Reattach the safety wire. The installation of the safety wire can be simplified by using a safety wire twisting tool, reference www.mcmaster.com part number 5649A2. The wire can be ordered from Environics using part number RB02-00-00015, specify the number of inches.
10. Place the 02 sensor assembly aside and proceed with replacing the filter-orifice fitting.
11. Using an adjustable or closed end wrench, remove the filter fitting shown in the illustration on the next page.
12. Be sure to remove all Teflon tape fragments from the mating part after the fitting has been removed.
- --
# ROUTINE MAINTENANCE

1. Apply Teflon tape to the new filter fitting (Environics part number MA04-003-005) and screw it into place. Reference the procedure for applying Teflon tape to pipe fittings in this section of the manual. NOTE: this fitting has 1/8” NPT thread and should use 1/8” wide Teflon tape as indicated in the table on the next page.
2. Replace the Viton tube, Environics part number PA04-02-001.
3. Reinstall the oxygen sensor assembly and connect the Viton tube to both the filter fitting and the oxygen sensor.
4. Reinstall the Kept nuts on the bottom panel of the system.
5. Reconnect the flat ribbon cable to the oxygen sensor.
6. Once the system is powered back on and the self tests/ self calibrations are performed, the system will automatically calibrate the new sensor.

|Oxygen sensor|SS Safety wire|Viton tube|
|---|---|---|
|Ribbon cable|8|Filter orifice|
|Clamp| | |

# Oxygen sensor assembly A207
- --
# ROUTINE MAINTENANCE

Applying Teflon tape to pipe fittings Thread tape acts as a lubricant allowing more thread engagement, preventing galling, and filling the gap between the crests and roots of mating taper threads in order to prevent formation of a spiral leak path. Always apply TFE tape to the male taper threaded end. Wrap the tape in the direction of the thread. All ROBD2 fittings are right hand style, meaning the tape must be applied in a clockwise direction. Draw the tape tightly around the thread; be sure the tape does not overhang the first thread otherwise the tape could deteriorate and contaminate the piping system. On stainless steel a double wrap is recommended to minimize any possible galling, while providing a good seal. As shown in the chart below, also ensure that the appropriate minimum number of threads have been wrapped. Press tape firmly into threads, particularly in the overlap area. The taped thread is then ready to assemble to a female thread.

Caution: Use latex type gloves to press tape into threads and also during assembly and disassembly. Most pipe fittings in the ROBD2 have been cleaned for oxygen service. The goal is to prevent any grease, including the oils from the skin, from getting onto the wetted surfaces of the gas path.

|NOMINAL PIPE SIZE|TAPE WIDTH|EFFECTIVE THREAD LENGTH (EXTERNAL)|APPROX: # OF THREADS|
|---|---|---|---|
|Y8|Vs-V4|1/4|7|
|Y4|V4|3/8|7V/3|
|3/8|V4|3/8|7Vz|
|Vz|Va-Vz|Vz|7V2|
|3/4|1a-1/2|916|72/3|
| |Va-1/2|11/16|8|
| | | |33|
- --
# ROUTINE MAINTENANCE

# Calibrating the Mass Flow Controllers

# Equipment Specification and setup (reference illustration on next page)

1. The gas source: Bottle air or clean dry oil-free air from a compressor system can be used for calibration. The input pressure setting for the calibration is the same as the operating pressure, 40 PSIG. Although MFC2 is used for Nitrogen, the properties of air (K factor) allow it to be used as a surrogate gas for calibration. Environics uses air to calibrate both MFCs. However, nitrogen can be used on MFC2.
2. The pressure regulator: Environics uses and recommends the use of dual stage regulators. This is most important if using air from a compressor, to eliminate pressure fluctuations and maintain a drift-free pressure setting.
3. The air feed line to the ROBD2: This line should have minimum I.D. of ¼” and a length no longer than 20 feet. At the maximum calibrated flow of 77 LPM N2, this hose will drop 3 PSIG pressure with a starting pressure of 40 PSIG.
4. ROBD2: Outlined in the following procedure, the input gas connects to each respective port for calibrating the air MFC (MFC1) and the nitrogen MFC (MFC2). Although the normal input ports are used for calibrating the MFCs, the breathing loop is isolated during calibration by interrupting the plumbing of the ROBD2. This is necessary to ensure that cumulative minor leaks in the breathing loop do not impact the calibration of the MFCs.
5. Output hose connection: The minimum I.D. of this hose should be ¼”. It is important to keep this length of hose as short as possible. Running at approximately ambient pressure, this hose will drop more pressure than the equivalent hose running at 40 PSIG, as with the input hoses. The same 20 foot hose will drop 5.5 PSIG when running at ambient pressure.
6. The calibration equipment: The measuring device used for flow calibrating the ROBD2 should be a National Institute for Standards and Technology (NIST) traceable primary standard with an accuracy better than .25% of reading. This calibration procedure assures the best possible precision error, and through traceability, minimizes bias or systematic error, which are more common with secondary or transfer standards. Environics uses a piston prover primary standard flow calibration system Sierra model 101. Environics has three cal benches that are periodically certified and correlated to one another. In addition, Environics cross correlates the benches to ensure accuracy. The STP of the equipment must be set or corrected for 70°F and 29.92 inHg between certifications. These are the standard settings Environics uses and adjusts to during MFC calibration in the ROBD2.
- --
# ROUTINE MAINTENANCE

# Typical calibration setup

|1|LEnvironics"Ro8d? 00|Cal-Bench|
|---|---|---|
|2|Air supply|ROBD2 Under test|
|3| |Primary standard|
|4| | |
|5| | |
|6| | |
- --
# ROUTINE MAINTENANCE

# Removing the MFCs

At some point, it may be more cost effective to remove the MFCs and have them calibrated in an ROBD2 at a central location or by Environics. This will save on shipping charges.

1. Unplug the power cord.
2. Remove the cover from the system.
3. Turn the unit on its side and remove the six screws that hold the MFCs in place. The screws that hold the air flow controller (MFC1) in place are Environics part number HA0113-M400D8MM (4). The screws that hold the nitrogen flow controller (MFC2) in place are Environics part number HA0113-M40012M (2).
4. Turn the unit upright.
5. Unplug the cooling fan from the PC416 and remove the screws in the left side panel.
6. Drop the left side panel. Note never allow the panels to drop to an angle greater than -90 or +90 degrees for the left and right panel respectively. In other words, the panels should always drop to a flat surface that is parallel to the bottom of the system, as shown in the system illustration drawing.
7. Using an open ended or adjustable wrench, disconnect the compression fittings from the plumbing connected to the MFCs. Note, the fittings on the MFCs are not directly accessible, move up or downstream to the most accessible fittings.
8. Remove the MFCs to the point where the MFC cable screws are accessible and remove the cables.
9. Remove the MFCs from the system chassis.
10. Remove any remaining plumbing from the MFC, excluding the brass fittings in the base of the MFC. Loosely assemble the plumbing back into the system, so it does not get misplaced.
11. Acquire and install threaded caps onto the 3/8” MFC compression fittings. Caplug # CD-6 will work.
12. When packing the MFCs, be sure to use plenty of cushion in the shipping box.
13. When the calibrated MFCs return, a calibration certificate should be included. Appendix P illustrates the certificate that will be received from the Environics 21 point calibration.
14. Reinstall the MFCs, using this procedure in reverse order.
- --
# ROUTINE MAINTENANCE

# Calibrating the MFCs in the ROBD2

1. Power the system down, disconnect the power cord and remove the cover from the system.
2. Locate the series of fittings shown in the illustration below, and remove the tube that is called out. These are the fittings that connect to the output or downstream side of the MFCs.
3. A temporary fitting and tube combination will need to be constructed (see below) to connect to the primary standard. The 3/8” union fitting must be a compression fitting (Gyrolok or Swagelok compatible). The TROBD2 uses Gyrolok (Hoke) brass compression fittings. These parts can be ordered from Environics. The union elbow is Environics part number FA110-01-B06 and the 3/8” tube is Environics part number PA15-06-001. The tube must be cut as short as possible. The nuts and ferrules come with the fitting.

Temporary fitting
- --
# ROUTINE MAINTENANCE

1. Install the temporary fitting as shown below. This replaces the tube that was removed in step 2. Rotate the union elbow as required for accessibility to the primary standard connection.
2. Connect the Primary standard to the union elbow as called out above.
3. Plug in the power cord and power the system on. Allow the 10 minute warm up time to elapse.
4. Place the system in the ADMIN mode and enter the SYSTEM mode.
5. Arrow down to CALIBRATE MFC and press ENTER.
6. Enter the MFC number to be calibrated, MFC1 for air (25 LPM full scale) or MFC2 for N2 (77 LPM full scale).
7. Enter the corresponding port number for the MFC. Port 1 for MFC1 and port 2 for MFC2.

Temporary fitting

Connect flow standard here

38
- --
# ROUTINE MAINTENANCE

11. The system will automatically enter the calibration table/mode. This mode is used to both enter the measured flow rates for 20 individual points and is also used to generate uncalibrated (raw) voltages to the MFC from zero to 100% in 5%. This mode is used to generate the flows while they are being measured real time. The following screen is an example of what will be displayed dependent upon the MFC selected and the TRUE (measured) flow data resident in the table.

|FLOW COMMAND|MEASURED FLOW| | |
|---|---|---|---|
|MFC1|__SET__|__TRUE__| |
|CAL POINT #|1= 625.00|651.00| |
| |2= 1250.0|1318.5| |
| |START|INIT|EXIT|

12. Because of the display limitations, only two calibration points (rows) are shown simultaneously. To navigate the table, use the up and down arrow keys for the individual points and the right and left arrow keys to move back and forth between the set and true flow columns. The cursor will move as the arrow keys are depressed.

13. The start key (F1) energizes the MFC, for the respective flow rate, and starts flowing to the primary standard. The init key (F2) initializes the calibration table to the values outlined in step 11. The set point values can be changed independently. It is not necessary to press the init key unless these set point values have been manipulated and it is desirable to recover the factory initialized values of 10-100% in 5% increments. The exit key (F3) exits the calibration mode. If any data has changed, you will be prompted to perform a save or no save data operation. No save will not save the changes that have been made.

14. The next step is where the control of flow actually starts. Ensure that the system is plumbed as outlined in the typical calibration setup illustration above.

15. Arrow down to point number 20, which is 100% FSO for the MFC.
- --
# ROUTINE MAINTENANCE

1. Select start (F1). Gas will start flowing to the primary standard and the following screen (example) will appear. The top line of the display will now show the interpreted flow rate based on the response voltage of the MFC. Since the valves in the MFC use PWM, the response field may fluctuate more at some flow rates than others. The modulation is at a frequency that the flow averages out and these fluctuations are undetectable in the mix. A blinking asterisk in the upper right hand corner identifies that the MFC has been energized. Pressing the view key (F2) will toggle the top line between a set and true flow label to the MFC response. The update key is used after moving the cursor to another row (set point) to update the flow rate consistent with the selected point. The stop key, of course, stops flow and puts the system into the mode shown above. A left pointing arrow in the far right hand column will identify the active row.
2. |MFC1|RESP=|25200|*|
|---|---|---|---|
|19=|23750.|23900.| |
|20=|25000.|25344.|&lt;|
|UPDATE|VIEW|STOP| |

Take several readings on the primary standard to ensure that the flow rate is not drifting. Drifting flow will sometimes indicate that the MFC has not had ample warm up time. It is only necessary to take multiple readings at this point to ensure stability. Once flow has stabilized, take a final measurement and enter that flow rate into the true column opposite the set flow rate. For the example above, a primary standard measurement of 25344 SCCM was measured for an ROBD2 setting of 25000 SCCM.
3. Move the cursor up to the next point and select update (F1). The left facing arrow should move up one row. Allow one minute or so and take a reading. Enter the measured flow rate into the true flow column.
4. Repeat step 18 for all 20 calibration points.
5. After the last calibration point has been recorded, press stop (F3).
6. Scroll the table and ensure all data has been entered correctly.
7. Press exit (F3) and then save (F1). The data has now been saved and this look up table, along with linear interpolation, will be used by the system when running programs.
8. Start at step 8 to calibrate another flow controller, or move onto verifying the flow calibration.
- --
# ROUTINE MAINTENANCE

# Verifying the flow calibration

1. While in the system mode, arrow up to the top line item, TEST FLOW, and press the ENTER key.
2. Cursor down to the MFC to verify, first making sure that the target flow setting for the other MFC is set to zero, and enter the flow rate to verify. Refer to Appendix P for the 5 flow rates that Environics uses for its flow verification. Reference sample display below.
|FLOW|TARGET|ACTUAL|
|---|---|---|
|MFC1=|0.0000|L|
|MFC2=|76.230|L|
|UPDATE VIEW STOP|UPDATE VIEW STOP|UPDATE VIEW STOP|
3. Select update (F1). The system will once again start delivering flow to the primary standard, the difference being that the calibration table is being used to correct the flow. The flow measured by the primary standard should be +/- .5% of the targeted flow rate. The screen will also display the flow rate based on the response voltage from the MFC.
4. Once both MFCs have been calibrated and verified, exit out to the ready mode and power down.
5. Replace the tube taken out in calibration procedure if the MFCs were calibrated in the unit.
6. If the MFCs were calibrated at an outside source, then the calibration table must be changed to reflect the new data.
- --
# PCB FUNCTION AND TEST POINTS

# PC401 function (Microcomputer board)

The PC401 is the microcomputer board. It contains the system EPROM and battery backed up RAM for the storage of all system configuration, calibration and user data. Reference appendix A, assembly A194. This PCB is not field serviceable and should be replaced in the event of failure.

# PC403 and PC404 function (pulse oximeter PCBs)

The PC403 is the main pulse oximeter board containing the display, keypad interface and microprocessor/memory. The PC404 is the RS232 interface card and is connected directly to the PC403. Reference appendix A, assembly A214 (front panel assembly). These PCBs are not field serviceable and should be replaced in the event of failure.

# PC406 function (keypad interface and display PCB)

The PC406 decodes the information entered on the keypad and displays information sent by the microcomputer board, on the front panel 4 line by 20 character LCD display. Also, this PCB contains the beeper circuit for an audible confirmation of keypad data entry. Reference appendix A, assembly A214 (front panel assembly).

# PC406 test points

|TP#|VALUE|
|---|---|
|TP1|5 VDC|
|TP2|GND|
|TP3|.25 to 1.8 VDC as display contrast is adjusted in PREFS mode|
|TP4|See waveform "PC406 TP4" on page 45.|
- --
# PCB FUNCTION AND TEST POINTS

# PC412-ROBD2 FUNCTION (ANALOG BOARD)

This PCB is an interface between all system analog control/feedback components and the microcomputer board (PC401). The analog components include O2 sensor feedback, breathing loop pressure transducer and mass flow controllers (MFCs). This PCB uses 12-bit A/D and D/A converters for high resolution control and read back of the analog devices. Reference appendix A, assembly A194

# PC412-ROBD2 test points

|TP#|VALUE|
|---|---|
|TP1|Command voltage for MFC1; this test point should measure approximately .5 VDC to 5.0 VDC for MFC1 commands between 10 and 100% full-scale flow. This range is approximated due to the MFC calibration table having an affect on the command voltage.|
|TP2|Response voltage for MFC1; this test point should measure approximately -.015 to +.015 VDC with a no flow command or a flow command of zero. When commanding flow, the measurement of this test point should equal TP1 as long as the MFC is flowing and controlling properly.|
|TP3|Command voltage for MFC2; this test point should measure approximately .5 VDC to 5.0 VDC for MFC1 commands between 10 and 100% full-scale flow. This range is approximated due to the MFC calibration table having an affect on the command voltage.|
|TP4|Response voltage for MFC2; this test point should measure approximately -.015 to +.015 VDC with a no flow command or a flow command of zero. When commanding flow, the measurement of this test point should equal TP3 as long as the MFC is flowing and controlling properly.|
- --
# PCB FUNCTION AND TEST POINTS

# PC412-ROBD2 TEST POINTS (CONTINUED)

|TP#|VALUE|
|---|---|
|TP5|Command voltage for optional MFC3; this test point should measure approximately .5 VDC to 5.0 VDC for MFC1 commands between 10 and 100% full-scale flow. This range is approximated due to the MFC calibration table having an affect on the command voltage.|
|TP6|Response voltage for optional MFC3; this test point should measure approximately +.005 to +.015 VDC with a no flow command or a flow command of zero. When commanding flow, the measurement of this test point should equal TP5 as long as the MFC is flowing and controlling properly.|
|TP7(VREF)|+5.00 VDC steady state.|
|TP8(AGND)|Analog ground test point for negative (black) meter lead.|
|TP9(+5A)|+5 VDC steady state.|
|TP10(-5)|-5 VDC steady state.|
|TP11(-12)|-12 VDC steady state.|
|TP12(+12)|+12 VDC steady state.|
|TP13(AGND)|Analog ground test point for negative (black) meter lead.|
|TP14(-15)|-15 VDC steady state.|
|TP15(+15)|+15 VDC steady state.|
|TP16(+5)|+5 VDC steady state.|
|TP17(GND)|Ground test point for negative (black) meter lead when measuring TP16.|
|TP18(PGND)|Ground test point for negative (black) meter lead when measuring TP19.|
|TP19(+24)|+24 VDC steady state.|

( ) Values in parenthesis are as seen on the PCB silkscreen.
- --
# PCB FUNCTION AND TEST POINTS

# PC416 FUNCTION (SOLENOID VALVE DRIVER AND STATUS I/O BOARD)

This PCB is used to activate the solenoid valves used to isolate the gases on the input gas ports. These valves are turned on with 24 VDC and then run at 30% duty cycle or 1/3 power. This allows more efficient use of the internal 24 VDC power supply. This board also controls the input and output status lines currently used to read the low pressure oxygen switch and the emergency dump switch.

# PC416 test points

|TEST POINT|WAVEFORMS|
|---|---|
|TP1(+5)|5 VDC Steady state|
|TP2(GND)|GND meter reference for TP1.|
|TP3(100KHZ)|See waveform "PC416 TP3" on page 45.|
|TP4(PGND)|This is the power (+24VDC) ground test point for the negative (black) meter lead when measuring the +24 VDC test point TP5.|
|TP5(+24)|+24 VDC steady state.|

( ) Values in parenthesis are as seen on the PCB silkscreen.
- --
# PCB FUNCTION AND TEST POINTS

|PC406|TP4|2 V/div|Vp-p(ATJE4 688|Freq(An)=45.66 HZ|Duty CYCATE84|
|---|---|---|---|---|---|
|PC416|TP3|2 V/div|Yp-PCADJ=4.938|Freq(A=13i.4kHz|Duty CYCA1J256 1%|

46
- --
# TROUBLESHOOTING GUIDE

# Troubleshooting system problems

|POWER PROBLEM SYMPTOMS|ACTION/SOLUTION|
|---|---|
|System display does not light up|• Check power cord connection and power source voltage. Environics recommends the use of a power conditioner. • Check fuses in the power entry module on rear panel and replace if necessary. Refer to procedure at the end of this guide. • Check all steady state test points on the PC412-ROBD2. In the absence of voltage at TP14, TP15, TP16 or TP19, check power supply voltages with power cable disconnected from PC412-ROBD2 J7. See power cable wiring diagram on page 53 of this manual. If any of the power supply voltages are absent, replace power supply. If all power supply voltages are present, identify the PCB or component drawing down by disconnecting cables attached to the PC412-ROBD2. Be sure to power off and on again when disconnecting cables. • In the absence of any voltages of other steady state test points, replace PC412-ROBD2. • If the problem is not found by following the directions above, and the problem is not consistent with any other symptom in the troubleshooting guide, contact Environics technical services.|
|Solenoid valves do not actuate| |
|Fan does not run| |
|Self tests fail| |
|Oxygen dump does not activate| |
- --
# TROUBLESHOOTING GUIDE

# FLOW/BLENDING PROBLEM

# SYMPTOMS

Zero or low flow from one or more mfcs.

NOTE: For all flow related problems, always check the steady state test point values on the PC412-ROBD2 first. If there is a problem with TP14, 15, 16 or 19, follow the instructions in the POWER PROBLEM section above.

NOTE: The command test points are found on the PC412-ROBD2, see PCB function and test points.

HINT: use the test flow mode to troubleshoot flow related problems. The DC command voltage measured should be approximately the same percentage of 5 VDC as the commanded flow is a percentage of the full scale flow rate of the MFC. MFC1 for air is 25 LPM and MFC2 for N2 is 77 LPM.

# ACTION/SOLUTION

- Make sure the input pressures are as prescribed.
- If the command voltage for the respective MFC seems correct for the flow rate being commanded, measure corresponding MFC response test point on the PC412-ROBD2. If the response voltage is low or 0, there may either be a problem with the MFC cable, +/- 15 VDC steady state power supply, or the MFC. Try checking the PC412-ROBD2 test points for +/- 15 VDC and swapping the MFC cable.
- If the command voltage is not present, check the calibration data for the MFC in the system mode to ensure that the values have not changed from the last calibration. Environics sends a hardcopy of all data for reference. These values may be slightly different if a follow-up calibration has been done outside Environics. Check TP7 on PC412-ROBD2. This is the reference voltage (+5 VDC) used by the MFC ADC and DAC.
- If these things fail to fix the problem, contact Environics technical services.

48
- --
# TROUBLESHOOTING GUIDE

# FLOW/BLEND PROBLEMS (CONT.)

|Blend or flow is unstable as displayed on the front panel.|ACTION/SOLUTION|
|---|---|
|Flow rate is saturated, regardless of command.|INDICATIONS: O2 concentration is too low (MFC2 saturated) or concentration is too high (MFC1 saturated).|
|Displayed O2 value is not consistent with the altitude|Self calibration fails for test altitudes|

- Measure the MFC response voltage on the PC412-ROBD2.
- If the response voltage is changing at the same rate as the instability of the blend, verify input pressure stability.
- Confirm the stability of the command voltage for the MFC.
- Replace the MFC.
- Check the O2 sensor feedback when running sea altitude only. This will confirm the stability of the O2 sensor.
- This normally indicates a failure within the MFC. However, first check all PC412-ROBD2 steady state voltages. Follow previously recommended procedure (in POWER PROBLEM section) if voltages are not correct.
- Replace MFC.
- Run an O2 sensor calibration and reconfirm.
- Run sea level altitude, O2 value should be approximately 21% on display.
- The voltage read between pins 2 and 3 of SK10-001-PCB should be approximately .7 to .8 VDC for sea level altitude, 21% O2. See appendix E.
- Confirm the +/- 15 VDC power is being supplied to the SK10-001-PCB using appendix E as a guide.
- Replace 2 sensor or O2 sensor PCB.

49
- --
# TROUBLESHOOTING GUIDE

# FLOW/BLEND PROBLEMS (CONT.)

|100% oxygen does not flow to the mask when the emergency dump switch is activated.|• If the dump switch does not illuminate, the internal contacts of the switch may be defective. Use appendix E, point to point wiring, to trace the problem.|
|---|---|
|Dump switch self tests fail|• When pressing the dump switch, audible clicking should be heard from the oxygen dump valve V1 and the bypass valve (if installed) V2. Power is sent to these valves via electrical harness E627 from PC416. Refer to appendix B and E for details.|
|Notes: if the positive pressure option is installed, the bypass valve and oxygen dump valve activate together to provide positive pressure O2.|• Replace the defective component based on the results of monitoring the control signals from the dump switch to the solenoid valves via the PC416.|
|Gas flow is heard immediately upon turning the system power on.|• Make sure the oxygen dump switch is not activated • Measure the command voltage to the MFCs at PC412-ROBD2 test points. If other than zero volts, PC412-ROBD2 may be defective, replace. • If command voltage is zero, MFC or MFC cable may be defective, replace.|
- --
# TROUBLESHOOTING GUIDE

# MISCELLANEOUS PROBLEMS

|Problem|SOLUTION|
|---|---|
|Memory loss| |
|Low O2 message appears when pressure is greater than 15 PSIG.| |
|BLP sensor pressure is not consistent with the normal operating BLP pressure|• Battery on PC401 is low. Battery should be 3 VDC and no less than 2 VDC. • Adjust the pressure switch to close when pressure drops to 10 PSIG. Pressure switch should open when pressure rises to approximately 13 PSIG. See procedure below. • Replace oxygen pressure sensor • Trouble shoot the pressure sensor feedback using appendix E, cable E626. • Replace BLP sensor A215 if necessary|

# Troubleshooting notes:

1. Be sure to use an ESD wrist strap or other static control, when handling electronics.
2. Refer to Appendix E for point to point wiring.
3. Refer to appendix B for complete list of detailed cable drawings and other electrical illustrations.
4. There are other appendices which may be useful for troubleshooting purposes, see list of appendices.
5. If the symptoms are not listed in the troubleshooting guide, contact Environics’ technical services.
6. IMPORTANT: When lowering the left side panel for troubleshooting, be sure to unplug the fan first. This is the only component that does not have a long enough cable to fully extend.
7. IMPORTANT: When disconnecting and working with plumbing parts downstream of the oxygen dump valve and on the oxygen input line, be sure to wear latex type gloves to keep oils off of the wetted surfaces.
- --
# TROUBLESHOOTING GUIDE

# Troubleshooting pulse oximeter problems

Certain conditions may generate special messages in the saturation and pulse rate displays. These displays and the conditions are listed below. Note that “Err” stands for error, but does not necessarily indicate a malfunction. Also, error conditions one and two are internal-only, and are not displayed.

|Low signal strength.|Pulse strength as detected by the sensor is too small for proper monitor operation. This message will disappear when the problem is corrected.|
|---|---|
|Insufficient light.|Sensor is placed on a site too thick (or opaque) for adequate light transmission. This message will disappear when the problem is corrected.|
|Pulse out of range.|Pulse must be within 30 - 250 beats per minute inclusive. This message will disappear when the problem is corrected.|
|Light interference.|Ambient light source (sunlight, warming lights, etc.) are interfering with sensor operation. Shield sensor from these light sources. This message will disappear when the problem is corrected.|
- --
# TROUBLESHOOTING GUIDE

Sensor faulty. Remove sensor from use and replace.

Monitor faulty. Record the error number that appears in the pulse rate display (XX will vary, depending upon the fault). Remove the monitor from use and contact qualified service personnel (report the number that appears in the pulse rate display).

Bad Signal. Monitor not receiving valid signals from sensor. May be caused by excessive motion, cardiac arrhythmia or other situations leading to poor signal. Check subject status, reposition sensor. This message will disappear when the problem is corrected.

If the pulse oximeter will not power on and all other functions of the ROBD2 are working, then the problem may be the pulse oximeter power supply assembly A205, see appendix A.

For a point to point wiring diagram of the A205 power supply, see the wiring diagram, appendix E. The power supply contains its own fuse F302. Check the continuity of this fuse with the power cord of the system disconnected.

The pulse oximeter gets its power directly from the power entry module. It generates 12 VDC which is sent to the pulse oximeter board via cable E628.
- --
# TROUBLESHOOTING GUIDE

# Main DC power cable pinout

| |6|7|
|---|---|---|
|5| |8|
| |4| |
|1|2|3|

CONNECTS TO PC412-ROBD2, J7

|PIN NUMBER|VOLTAGE|
|---|---|
|1|+15 VDC|
|2|-15 VDC|
|3|GND|
|4|GND|
|5|GND|
|6|+5 VDC|
|7|+24 VDC|
|8|NC|

E613-ROBD2 POWER CABLE DIAGRAM
- --
# TROUBLESHOOTING GUIDE

# REPLACING FUSES

Using the troubleshooting guide, for a power related problem, the result may lead to this procedure.

1. Locate the power entry module on the rear panel and turn the power switch off.
2. Remove the power cord from the power entry module.
3. Take note of the voltage indicator position (normally 115 VAC). This module will be removed as part of this procedure and it is very important to reinstall it in the correct orientation.
4. Using a small flathead screwdriver, open the power entry module as shown below.
5. Gently pry out the red fuse holder.
6. Replace the defective fuse(s), reinstall the fuse holder and close the power entry module access door.
7. Reconnect the power cord and power the instrument on.

|FUSE HOLDER|1|II6v|
|---|---|---|
|115V|15V| |
|ACCESS DOOR|FUSE HOUSING|Fuse housing|
| |3AG Type|3AG TYPE|
| |55| |
- --
# TROUBLESHOOTING GUIDE

# Replacing or updating software

1. Locate the power entry module on the rear panel and turn the power off.
2. Remove the power cord from the power entry module.
3. Remove the screws from the instrument cover and remove the cover. Remove the six screws from the right side panel of the instrument.
4. Lower the right side panel so it is parallel to the base of the unit; resting on a table top.
5. Locate the A194 shown in the system illustration drawing at the beginning of this manual. The software is in the PCB labeled 1a in that illustration (PC401). Below is an enlarged view of that part of the illustration drawing.
6. Use an ESD wrist strap when working with electronics. Using a small flat head screwdriver, remove the old software IC, paying close attention to the orientation of the EPROM IC in the socket.
7. The new software chip revision should contain a higher number than the last. Currently, as of the original release date of this manual, the software revision is 0.96-01.
8. Making sure that the pins are even and properly aligned with the socket, press in the new software IC.
9. Return the side panel to its original upright position and screw it into place.
10. Place the cover back onto the instrument and power the unit on, making sure the new software revision has been recognized in the startup screen.
11. Screw the cover into place.

# A194 ASSEMBLY – 1a (PC401), 1b (PC412)
- --
# TROUBLESHOOTING GUIDE

# Adjusting the low oxygen pressure switch

# SETTING THE O2 PRESSURE SWITCH TO 10 PSIG FALLING

1. Remove the two terminal connections on the O2 pressure switch (black and red wires). The pressure switch is connected to the rear panel by a series of fittings. Refer to assembly A213 in appendix A and the illustration above.
2. Connect an ohm meter across the two terminals of the pressure switch.
3. Using an accurate pressure test gauge and pressure relieving regulator, connect oxygen (or air) to the Oxygen port at approximately 10 PSIG. Important: Only use oxygen if the pressure relieving regulator is O2 compatible.
4. Adjust the pressure switch slotted adjustment (top) until the pressure switch turns on (zero ohms) when falling below 10 PSIG and turns off when rising above approximately 12 to 15 PSIG. The key setting is 10 PSIG falling pressure. The 12 to 15 PSIG range is controlled by the dead-band of the pressure switch. Once it is set, adjust the pressure a few times to insure the repeatability of the switch. This adjustment does not lock.

57
- --
# TROUBLESHOOTING GUIDE

# Adjusting the internal back pressure regulator A212

1. Confirm that with the system in standby mode (no flow) the pressure gauge reads zero.
2. In the TEST FLOW mode in the SYSTEM mode, command 25 LPM for MFC1 and press enter.
3. On the internal pressure gauge (G1), make sure BPR1 is set to read 5 PSIG.
4. To adjust, loosen the locking nut on the shaft of the handle and turn the control handle clockwise to increase and counterclockwise to decrease the pressure.
5. Lock down the nut on the shaft of the BPR1.
6. Stop and start MFC1 flow a few times to ensure the setting is repeatable.
7. Exit the TEST FLOW mode.

Pressure Gauge

Back Pressure Regulator

Locking nut

Control handle

A212, BPR1
- --
# TROUBLESHOOTING GUIDE

# Adjusting needle valve assembly A211

Three of four primary operating modes supply varying amounts of pressure to the pilot under test, dependent upon the simulated altitude. This procedure will use one of those modes, the PPT (Positive Pressure Training) mode, to set and lock down the needle valve. The needle valve produces back pressure to the mask in the operating modes.

To run this test, the SELF TEST and SELF CALIBRATION procedure must be completed and the system must be in the ready mode. Gases must be connected and pressurized. Because this test consumes 95 LPM air; clean, dry, oil free air from a compressor system can also be used to conserve bottled breathing air.

1. Remove the cap from the breathing bag port and install the 3 liter breathing bag and breathing bag clamp.
2. With a rubber plug (reference www.mcmaster.com, part number 9545K16) plug the breathing mask connector on the front panel.
3. Make sure the breathing loop pressure port, on the rear panel of the system, is plugged and the plug is removed from the VENT port.
4. If this is a first time adjustment, because the assembly has been replaced, loosen the lower locking nut on the A211 so the T handle moves freely, see diagram below. If this is a readjustment, proceed to step 6.
- --
# TROUBLESHOOTING GUIDE

1. Turn the handle counterclockwise to decrease the adjustment. This prevents overpressure for the next step. This is usually only required for first time adjustment.
2. From the main menu, select START. The system will purge with air for a few seconds.
3. Enter the PPT mode; air will start flowing. The O2 reading on the screen should be approximately 21% and the BLP (Breathing Loop Pressure) should be approximately .5 to .8; BLP is in “HO.2
4. Select START. The system will now flow 95 LPM air. The O2 reading should remain at 21%. If the needle valve is not decreased enough, the system may shutdown and provide 100% O2. This is a built in safety feature to prevent the BLP from getting too high. If this happens, select OK to stop the flow of O2 and rerun steps 5-9.
5. While running 95 LPM in the PPT mode, make sure the command and response voltages to the MFCs are consistent, these voltages can be measured at the PC412. This ensures that the system is delivering the right amount of flow for the needle valve adjustment. The adjustment is very sensitive and can be impacted by varying flow rates. To put it in perspective, once the adjustment is made, the needle valve will produce 10” H2O or .36 PSI back pressure at 95 LPM flow.
6. Increase the needle valve adjustment until the BLP reads between 10 and 10.5 within 5 seconds after pressing START. The pressure should not rise above 11.5” within 1 minute after pressing START. This pressure should remain stable and not fluctuate. Some reasons for fluctuating readings could be a leaking bypass valve (large blue solenoid valve) or an improperly installed A211 (backwards).
7. Tighten the lower locking nut while running. Stop and start the PPT mode a few times to ensure the adjustment generates consistent results.
8. The upper locking nut should be tight against the cap, as provided by the manufacturer.
- --
# TROUBLESHOOTING GUIDE

# Testing the pulse oximeter and battery backup

1. Power on the pulse oximeter.
2. After it has gone through its self-test routine, both the pulse oximeter displays will show 3 dashes.
3. Press SpO2 the key and then the down arrow key once to change the factory default setting from 100 to 99.
4. Press SpO2 key again and then the up arrow key once to change the factory default setting from 85 to 86.
5. Press SpO2 key a third time to put the pulse oximeter in the ready mode.
6. Press the pulse rate key ( ) and then the down arrow key once to change the factory default setting from 150 to 149.
7. Press the pulse rate key again and then the up arrow key once to change the factory default setting from 40 to 41.
8. Press the pulse rate key a third time to put the pulse oximeter back into the ready mode.
9. Turn power to the ROBD2 off for approximately one minute.
10. Turn the ROBD2 power back on.
11. Turn the pulse oximeter power on.
12. After the self test routine, press the SpO2 button once and again to verify the retention of the values 99 and 86.
13. Press the pulse rate key once and again to verify the retention of the values 149 and 41.
14. Press the pulse rate key a third time to put the pulse oximeter back into ready mode.
15. Plug in pulse oximeter finger probe (Environics # XJ007) and attach to pointer finger.
16. Values should appear on the two displays of the pulse oximeter display. The SpO2 number should be in the high 90s and the pulse value will be resting pulse rate.
17. Disconnect the finger probe from the pointer finger and the pulse oximeter alarm should sound.
18. Press the mute ( ) key once to mute the alarm.
- --
# TROUBLESHOOTING GUIDE

# Checking the pressure sensor and O2 sensor ADC

1. Power the unit on and press the CYL key.
2. Select the OPTION mode.
3. Arrow down to the ADMIN mode and press the ENTER key. The message “admin mode enabled” should appear on the top row. If prompted for a password, enter the factory default 1234.
4. Exit and press the MENU key.
5. Enter the SYSTEM mode, arrow down to CALIBRATE ADC and press ENTER.
6. Enter the number 12.
7. On the top line of the calibration table, the “RESP =” value should be in approximate range of .75 and .81 V. This is the Oxygen sensor ADC. This is the voltage read back from the oxygen sensor for 21% O2 (or air).
8. Exit and enter Calibrate ADC again.
9. Enter the number 11.
10. On the top line of the calibration table, the “RESP =” value should be approximately 2.5 V. This is the pressure transducer ADC. The pressure transducer reads back 2.5 VDC for 0” H20.

# Calibrating adc 11 (pressure sensor)

1. Remove the cap from the breathing bag port if present.
2. In ADC 11 cal table, add .003 to the value read in step 10 above and enter that value into column 1 of line one in ADC 11. Also, record this value for the ADC calibration sheet for this device. Line two should always have 5.0 and 25.0 entered into columns one and two respectively. These are the only two lines with data. Exit and save the new data.

# SAMPLE ADC 11 CAL TABLE:

|ADC 11|RESP = 2.501V|
|---|---|
|1 = 2.504|0.000|
|2 = 5.0|25.000|

NOTE: CALIBRATION OF ADC 12 IS PERFORMED BY THE SYSTEM IN THE SELF CALIBRATION ROUTINE. THIS IS DONE IN THE POST CALIBRATION PROCEDURE
- --
# TROUBLESHOOTING GUIDE

# Leak test

# Physical setup

1. Remove the ROBD2 cover, unplug fan, remove the screws from the side panels and fold down both hinged side panels.
2. Connect a back pressure regulator to the vent port as shown in diagram 1, no Teflon tape required. This assembly can be purchased from Environics, or acquire a back pressure regulator that has a range of 0 to 2 PSIG. This type of regulator can be purchased from Control Air Inc. The gauge must read “H0.2.
3. Connect the red shipping cap to breathing bag port as shown in diagram 1.
4. Insert black tapered rubber plug (reference www.mcmaster.com, part number 9545K16) into the breathing mask port as shown in diagram 2.
5. Ensure the metal plug is installed into the breathing loop pressure port, see diagram 3.
6. Make sure the external back pressure regulator is decreased all the way.
7. Install temporary fittings into the air, N2 and oxygen ports and supply air to all three at 30-40 PSIG. Diagram 4 shows a sample setup used by the factory. If the hose and regulator option has been installed onto the system being leak tested, extra fittings can be purchased from Environics for leak testing.

# Performing the leak test

1. Power the unit on and select CYL from front panel menu.
2. Put the system into the ADMIN mode.
3. Exit back to the READY mode.
4. Press the menu key until the SYSTEM mode appears.
5. Enter the SYSTEM mode (F3), arrow to TEST FLOW and press ENTER.
6. Enter 5 LPM for MFC1 and press UPDATE (F1).
7. Adjust the external BPR for 10” H20.
8. Use leak test formula 300 for oxygen systems to ensure bubble tight connections for all threaded fittings and tubing connections. Shake the formula until the top of the bottle fills with bubbles. Pull out the applicator tube until the inside end of the tube is within the envelope of the bubble chamber in top of the bottle. Apply bubbles, not liquid to all plumbing connections. Refer to diagram 5; some parts of the system are at 40 PSIG, others are at 5 PSIG and the remaining parts in the breathing loop are at 10” H20. When using the solution over electrical connections, be sure to use absorbent paper towels to catch any drip. When finished with a connection, wipe away any remaining bubbles.
- --
# TROUBLESHOOTING GUIDE

# BREATHING MASK CONNECTOR

# DIAGRAM 1

# DIAGRAM 2

BREATHING LOOP PRESSURE

0 (

paessuRD

OKYDE

YR

5

# DIAGRAM 3

# DIAGRAM 4

64
- --
# TROUBLESHOOTING GUIDE

# DIAGRAM 5

65
- --
# TROUBLESHOOTING GUIDE

# PCB assembly drawings

|2|28|3|4|
|---|---|---|---|
|R2|LMSS6CNA|82|8|
|8|74HC02|74AC04| |
|SLM324AN|74HC123|5|AD7524|
|5|74AC541|744C245| |
|8|5|22v10| |
|f|PC406|66| |
- --
# TROUBLESHOOTING GUIDE

| |3|$|8| | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|
|1|8|1| | | | | | | | |
|4|8|3|2| | | | | | | |
|2|8|zin|fin|5| | | | | | |
|2|Lz?|82)| | | | | | | | |
| | |2| |8| | | | | | |
|88|(3g|1|1|g| | | | | | |
|9|{|)|(35|8|Sz)|010|2|9z3|3|9813|
| | |8| |8| | | | | | |
|9| | |13|3| | | | | | |
| | | |3|=| | | | | | |
| |0zJ|648|Lla|SlJ|#13| | | | | |
|1|8|6|11| | | | | | | |
|713142|#0|8|sn| | | | | | | |
|2|9|2|Ln|3|&|53|1| | | |
|4|2|zn|8| | | | | | | |
|8|E|2|8|2|@|&|5|En|23| |

Photometer

|MFCT|MFC2|MFC3|
|---|---|---|
|PC412-ROBD2| |67|
- --
# TROUBLESHOOTING GUIDE

| | |C15|C16|C17| | | | |
|---|---|---|---|---|---|---|---|---|
| |U16 8|U17 8|U18|U19| | | | |
| | |8|1|3|2|2|2| |
|1|1|RN3|D29| |D26| | | |
| | | |025|C14|B2z|024|2| |
| | |U12|U13|U14 1| | | | |
|2|2|2|8|F +|C13U91|U10| | |
|5|74HC259|C12| | | | | | |
|8|5|U8| | | | | | |
| |2|8|82|1| | | | |
|8| | |U7| | | | | |
| | |C1| |D12| | | | |
|U6|4|LM3524|1|C9| | | | |
|U4|1|4|5|&|8|U5|8| |
|J2|2|C8|J| | | | | |
|Fan| | |8|PC416|68| | | |
- --
P&ID

 P&ID

       69
- --
# APPENDIX A: Assembly parts list and illustration drawings

- A194, PC412-ROBD2 and PC401-1D - PC boards
- A204 - pulse oximeter battery backup
- A222 - pulse oximeter power supply
- A206 - terminal strip assembly
- A207 - Oxygen sensor assembly
- A208 - Oxygen dump valve assembly (V1 in P&ID)
- A209 - Crossover valve assembly (V3 in P&ID)
- A210 - Bypass valve assembly (option, V2 in P&ID)
- A211 - Needle valve assembly (option, NV1 in P&ID)
- A212 - Back pressure regulator assembly (BPR1 in P&ID)
- A213 - Rear panel assembly
- A213 parts list
- A214 - Front panel assembly
- A214 parts list
- A215 - BLP pressure transducer (PX1 in P&ID)
- A221 - mask particle filter assembly (FIL-3 in P&ID)
- --
            8 8 slsla 6 6 6
                           8 8 slsla
                                    8 8 slsla3 3 3
                                          2
                                           2
                                            2        Q - 8
                                                          Q - 8
                                                               Q - 8   2
                                                                        2
                                                                         2
                          8 8 8 3 3 3 33
                                        3 [
                                           [
                                            [        22
                                                       22
                                                         22
                                                     g 8
                                                        g 8
                                                           g 8
ITTTT
     ITTTT
          ITTTT0 Hhl
                    0 Hhl
                         0 Hhl                       #
                                                      #
                                                       # 4 4 4         8
                                                                       8
                                                                        8
            1 24
                1 24
                    1 24                            1
                                                     1
                                                      1                E
                                                                        E
                                                                         E
 1
  1
   1                          8/8
                                 8/8
                                    8/8              5 5 5
                                                     2 2 2
            2 2 2 8 8 8 7 7 7 8 8 8 de8
                                       8
                                        8            3
                                                      3
                                                       3
            6 6 6 X X X        S
                                S
                                 S
 0
  0
   0        8
             8
              833 de
                    33 de
                33H
                   H
                    H
            3 3 3
    2 2 2M 1
            M 1
               M 1
                                                                            A1
                                                                              A1
                                                                                A1
- --
              2
   8 1 8 I
   2
      8    8l8 [2                   8
              4
      1 sls28                  1    3
 333          7                     5
      3    4
 88
 8 8   53
         c/~
 e8 4  8
    5
                   151 238
              3    8 339
                   0 32 8 3  6
  0 ] J 1            8
 8 6                05
                    3 9
2                                 A2
- --
                                                                                             H
                                                                                              H
                                                                                               H             H
                                                                                                              H
                                                                                                               H
                                                                                                            22
                                                                                                              22
                                                                                                                22
                                                                                            22
                                                                                              22
                                                                                                22
                                                   1 1 1          % 8
                                                                     % 8
                                                                        % 8{ { { 2 1 1 1 2 2 2
                                                                                2
                                                                                 2                              2 1 1 1
                                                                                                                2
                                                                                                                 2
                                                          8
                                                           8
                                                            8              0
                                                                            0
                                                                             0
                                                          o8/
                                                             o8/
                                                                o8/                                                2 2 2
e33
   e33
      e33##A
            ## A
               ## AW
                   W
                    WU
                      U
                       U
         1 1 1
                                 U
                                  U
                                   U
               1 1 1
                                     1 1 1
    3 8 3 8
           3 8 3 8
                  3 8 3 8 1 1 1VH
                                 VH
                                   VH       1 1 1                                                                 1 1 1 1 1 1
                                                                      1 1 1 1 1 1 H 1 1 1 2 2 2                   1 1 1
                    1
                     1
                      1                                            {22
                                                                      {22
                                                                         {22                                      1 1 1
                                 1 6
                                    1 6
                                       1 6                               H
                                                                          H                         A3
                                                                                                      A3
                                                                                                        A3
- --
  3
   3
    3            3
                  3
                   3   slslals
                              slslals
                                     slslals        2
                                                     2
                                                      2
  8
   8
    8                       Fi 2
                                Fi 2
                                    Fi 2                                                                             8
                                                                                                                      8
                                                                                                                       8
                             88 8 #
                                   88 8 #
                                         88 8 #1
                                                1
                                                 1             Jsopo
                                                                    Jsopo
                                                                         Jsopo        7828
                                                                                          7828
                                                                                              7828                   8
                                                                                                                      8
                                                                                                                       8
                                                               5 6 7 8
                                                                      5 6 7 8
                                                                             5 6 7 8  5 6 7 8
                                                                                             5 6 7 8
                                                                                                    5 6 7 8
Hu 9 8 2
        Hu 9 8 2
                Hu 9 8 22 Il
                            2 Il
                                2 Il                                                                                 E
                                                                                                                      E
                                                                                                                       E
                             43
                               43
                                 43
                                            2
                                             2
                                              2
 alzieelz3
          alzieelz3
                   alzieelz3
                  Hk
                    Hk
                      Hk                                  3
                                                           3
                                                            3                                                 6
                                                                                                               6
                                                                                                                6
                                                         6
                                                          6
                                                           6
                                                         8
                                                          8
                                                           8                                                  8
                                                                                                               8
                                                                                                                8
            1
             1
              1              [ [ [                       8
                                                          8
                                                           8                                                 82
                                                                                                               82
                                                                                                                 82
                  2 2 2    1
                            1
                             1
     8 8 8        2 2 2
                  1 1 1                                                                                                   A4
                                                                                                                            A4
                                                                                                                              A4
- --
 alelgksIsle/
             alelgksIsle/
                         alelgksIsle/ 3 3 3
                           2
                            2
                             2
FITIT HH
        FITIT HH
                FITIT HH2
                         2
                          2        #
                                    #
                                     #
 2/
   2/
     2/     0e
              0e
                0e                 I
                                    I
                                     I
                                   1 3 2 2 2
                                            1 3
                                               1 3
            k k
               k k
                  k k              86
                                     86
                                       86
 8
  8
   8? ? ?1 FFe 8
                1 FFe 8
                       1 FFe 88
                               8
                                8     1
                                       1
                                        1
     4
      4
       4    Ff:
               Ff:
                  Ff:
                    3
                     3
                      3     8
                             8
                              8
                    8
                     8
                      8
                                                                           8
                                                                            8
                                                                             8
                                                           2
                                                            2
                                                             2
                                                           8
                                                            8
                                                             8       1
                                                                      1
                                                                       1   8
                                                                            8
                                                                             8
     1 1 1 1 1
              1
               1                                           8
                                                            8
                                                             8       3
                                                                      3
                                                                       3    5
                                                                             5
                                                                              5
               1
                1                                          2
                                                            2
                                                             2       8
                                                                      8
                                                                       8
 2 2 2                                              A
                                                     A
                                                      A         A 2
                                                                   A 2
                                                                      A 2
                                                    4 4 4       4
                                                                 4
                                                                  4
                                                                             A5
                                                                               A5
                                                                                 A5
- --
         &
          &
           &                                                    5 5 53 3 3 8 8 8  0 8 0 2 8
                                                                                           0 8 0 2 8
                                                                                                    0 8 0 2 8885
                                                                                                                885
                                                                                                                   885                        8
                                                                                                                                               8
                                                                                                                                                8
2 2 2 88
        8                      1 elslelel8
                                          1 elslelel8
                                                     1 elslelel8 8 8 8                                                        3
                                                                                                                               3
                                                                                                                                3
2 2 2 8 8 8aea
              aea
                 aeaeel
                       eel
                          eel       8
                                     8
                                      8                                           2 J: J 8 2
                                                                                            2 J: J 8 2
                                                                                                      2 J: J 8 2                   2
                                                                                                                                    2
                                                                                                                                     2       3
                                                                                                                                              3
                                                                                                                                               3
                                                                                             8 8 6
                                                                                                  8 8 6
                                                                                                       8 8 6                       3
                                                                                                                                    3
                                                                                                                                     3
7 7 7 3 3 3 8 8 8                                                                                                                  2
                                                                                                                                    2
                                                                                                                                     2        5
                                                                                                                                               5
                                                                                                                                                5
         a 2 2 2
                a
                 a                                                  1 1 1             1 3 M
                                                                                           1 3 M
                                                                                                1 3 M04
                                                                                                       04
                                                                                                         048
                                                                                                            8
                                                                                                             82
                                                                                                               2
                                                                                                                2
                                                                                      6
                                                                                       6
                                                                                        6
    1 1 1
2 2 2 8 8 8 3 3 3 J J J 8gkk 394/9
                                  gkk 394/9
                                           gkk 394/9
                                                    6 6 6 3 3 3
         8 3 3 3
                8
                 8
    8 8 8      8
                8        co Esld
                                co Esld
                                       co EsldFIA
                                                 FIA
                                                    FIA   c
                                                           c
                                                            c
    J J J     3
               3
                3
               6 6 6                      gjelg/8
                                                 gjelg/8
                                                        gjelg/8
               8 8 8                    ElL
                                           ElL
                                              ElL
                       H
                        H
                         H6
                           6
                            6
                                                                                                                        3
                                                                                                                         3
                                                                                                                          3             3
                                                                                                                                         3
                                                                                                                                          3
                    1 1 1                                                                                                8
                                                                                                                          8
                                                                                                                           8
  8
   8
    8                   6 6 61
                              1
                               1                                                                                        8
                                                                                                                         8
                                                                                                                          8
                                                                                                                        2
                                                                                                                         2
                                                                                                                          2             8
                                                                                                                                         8
                                                                                                                                          8
                                                                                                                                        2
                                                                                                                                         2
                                                                                                                                          2
                                                                                                                                                   A6
                                                                                                                                                     A6
                                                                                                                                                       A6
- --
8 8 3 3 8 8 slsl8 5
                   8 8 3 3 8 8 slsl8 5
                                      8 8 3 3 8 8 slsl8 5 3 3 3
g21138
      g21138
            g21138J
                   J
                    J         2
                               2
                                2                                5
                                                                  5
                                                                   5  8
                                                                       8
                                                                        8
3 38
    3 38
        3 3881 1 8
                  81 1 8
                        81 1 8                                   1
                                                                  1
                                                                   1  3
                                                                       3
                                                                        3
                                                                 8
                                                                  8
                                                                   8
                                                                 2
                                                                  2
                                                                   2
17 0 1 ~12
          17 0 1 ~12
                    17 0 1 ~12                                        E
                                                                       E
                                                                        E
   0 8 3
        0 8 3
             0 8 3         4 1
                              4 1
                                 4 1                             3
                                                                  3
                                                                   3
   1
    1
     1                                                           8
                                                                  8
                                                                   8
            alak
                alak
                    alak                                         2
                                                                  2
                                                                   2
   1 1
      1 1
         1 1sls
               sls
                  sls
2 8
   2 8
      2 8~
          ~
           ~kk aa
                 kk aa
                      kk aa3
                            3
                             33
                               3
                                3
     0
      0
       0S S S
  8
   8
    8
                                                                         A7
                                                                           A7
                                                                             A7
- --
 sigl 3
       sigl 3
             sigl 3alelgleelelzk_
                                 alelgleelelzk_
                                               alelgleelelzk_     8
                                                                   8
                                                                    8
                      2
                       2
                        2         031
                                     031
                                        031
 1
  1
   1   8
        8
         88
           8
            8 8/8 1 2
                     8/8 1 2
                            8/8 1 2
              e2
                e2
                  e2g 1
                       g 1
                          g 1     83 8
                                      83 8
                                          83 8
                                  43
                                    43
                                      43                          3
                                                                   3
                                                                    3
        S
         S
          S                                                       5
                                                                   5
                                                                    5
 3
  3
   38 1 3
         8 1 3
              8 1 3
  1
   1
    1     1 5 3
               1 5 3
                    1 5 3I 2
                            I 2
                               I 21
                                   1
                                    1
813
   813
      8133
          3
           3
  3
   3
    3
  8
   8
    8       8
             8
              8 8
                 8
                  8
  8
   8
    8      3
            3
             3        1
                       1
                        1
           8
            8
             88
               8
                8 8
                   8
                    8
          ELLLL
               ELLLL
                    ELLLL
                                               2
                                                2
                                                 2             2
                                                                2
                                                                 2
  0
   0
    0                                          8
                                                8
                                                 8             6
                                                                6
                                                                 6
        1
         1
          1                                   8
                                               8
                                                8              8
                                                                8
                                                                 8
3
 3
  3  1
      1
       1                                      2
                                               2
                                                2              2
                                                                2
                                                                 2
                                                                 A8
                                                                   A8
                                                                     A8
- --
  slzlala 8 8
             slzlala 8 8
                        slzlala 8 8       g/slalsla 5 5 5
                                                         g/slalsla
                                                                  g/slalsla 3
                                                                             3
                                                                              3
EHHH
    EHHH
        EHHH                                                               2
                                                                            2
                                                                             2
                                                                      2
                                                                       2
                                                                        2
                                                                2 2 2             1 1 1
   2 2 2
                                                     2
                                                      2
                                                       2                          2
                                                                                   2
                                                                                    2     2
                                                                                           2
                                                                                            2
                                                                           1
                                                                            1
                                                                             1           1
                                                                                          1
                                                                                           1
  4
   4
    4
        8
         8
          8                              82 8 8 77
                                                  82 8 8 77
                                                           82 8 8 77                      5
                                                                                           5
                                                                                            5
                                               3
                                                3
                                                 3                               2
                                                                                  2
                                                                                   2
       88
         88
           88                       3
                                     3
                                      3        8
                                                8
                                                 8
        8 ;
           8 ;
              8 ;                   8
                                     8
                                      8        * E 8
                                                    * E 8
                                                         * E 88 3
                                                                 8 3
                                                                    8 3
                                              05
                                                05
                                                  05
  2 2 2 7 1 1 1 1
                 7
                  7    1
                        1                                                                      Ag
                                                                                                 Ag
                                                                                                   Ag
- --
       0 8
          0 8
             0 88
                 8
                  8
                1
                 1
                  1                                                                                                                                     3
                                                                                                                                                         3
                                                                                                                                                          3
        1
         1
          15 1
              5 1
                 5 1
                                                                                   8 8 3 8 gsls
                                                                                               8 8 3 8 gsls
                                                                                                           8 8 3 8 gsls                                 5
                                                                                                                                                         5
                                                                                                                                                          5
                           8
                            8
                             88
                               8
                                8HH 1 FFFIITIIII 2
                                                  HH 1 FFFIITIIII 2
                                                                   HH 1 FFFIITIIII 28
                                                                                     8
                                                                                      88
                                                                                        8
                                                                                         88/8 8/8
                                                                                                 8/8 8/8
                                                                                                        8/8 8/8alelele/a 1 7
                                                                                                                            alelele/a 1 7
                                                                                                                                         alelele/a 1 7   2
                                                                                                                                                          2
                                                                                                                                                           2
                           3
                            3
                             3          0o
                                          0o
                                            0o1 El
                                                  1 El
                                                      1 ElE14 a 1
                                                                 E14 a 1
                                                                        E14 a 1                           Ale Ied 1
                                                                                                                   Ale Ied 1
                                                                                                                            Ale Ied 10
                                                                                                                                      0
                                                                                                                                       06o 8
                                                                                                                                            6o 8
                                                                                                                                                6o 8     2
                                                                                                                                                          2
                                                                                                                                                           2
2 7 1 1 1 1 1 1 17
                  7         8
                             8
                              8  1
                                  1
                                   1                     5
                                                          5
                                                           5
                                                                                                                                                          8
                                                                                                                                                           8
                                                                                                                                                            8
2
 2                    1
                       1  Ee
                            Ee
                              Eeglglg
                                     glglg
                                          glglg    Hsl8 8/xlxlglglglglglglg
                                                                           Hsl8 8/xlxlglglglglglglg
                                                                                                   Hsl8 8/xlxlglglglglglglg
                                                    8 K
                                                       8 K
                                                          8 K                                                                                            2
                                                                                                                                                          2
                                                                                                                                                           2
                                                          6
                                                           6
                                                            6                                                                                             A10
                                                                                                                                                             A10
                                                                                                                                                                A10
- --
              6 6 6
              3 3 3
                  A A A
                   8 8 8
                   3 3 3
                           8
                            8
                             8
8 1
   8 1
      8 1
1 1 1 1 1 1
8 8 8
0; I I I
        0;
          0;               5
                            5
                             5
} 1
   } 1
      } 1                  8
                            8
                             8
                           C
                            C
                             C
                          A11
                             A11
                                A11
- --
                                                                                                                        glals/8 0 0 0
                                                                                                                                     glals/8
                                                                                                                                            glals/83
                                                                                                                                                    3
                                                                                                                                                     3
  N N N                      NJ NJ NJoR
                                       oR
                                         oRH FFHM
                                                 H FFHM
                                                       H FFHM( ( ( N N N          N N N            N N N          N N N            U U U           2
                                                                                                                                                    2
                                                                                                                                                     2
 # 1
    # 1
       # 1                                                                                                 FT
                                                                                                             FT
                                                                                                               FT                            e
                                                                                                                                              e
                                                                                                                                               e
                                 1
                                  1
                                   1
            8
             8
              8        1
                        1
                         1                             2 2 2                                                                 8
                                                                                                                              8
                                                                                                                               891 2
                                                                                                                                    91 2
                                                                                                                                        91 2Ha
                                                                                                                                              Ha
                                                                                                                                                Ha3
                                                                                                                                                   3
                                                                                                                                                    3
0
 0
  0                             FF;| ae 5
                                         FF;| ae 5
                                                  FF;| ae 58 1
                                                              8 1
                                                                 8 1
                                            8
                                             8
                                              8                                                                        37
                                                                                                                         37
                                                                                                                           37                              5
                                                                                                                                                            5
                                                                                                                                                             5
 1 94
     1 94
         1 94
 3 1 3 4
        3 1 3 4
               3 1 3 4
                      U ~
                         U ~
                            U ~W
                                W
                                 W
                             As
                               As
                                 As8/8 6 skwls skkl
                                                   8/8 6 skwls skkl
                                                                   8/8 6 skwls skkl 2 2 2 4 W A A A RH A A A ~KF 1 3+ 4
                                                                                                                       + 4
                                                                                                                          + 44 W RH
                                                                                                                                   4 W RH~KF 1 3
                                                                                                                                                ~KF 1 3   3
                                                                                                                                                           3
                                                                                                                                                            3
 3
  3
   3        %
             %
              %3
                3
                 3          X
                             X
                              X       8]
                                        8]
                                          8]6o
                                              6o
                                                6o     9 X X X X
                                                                9 X X
                                                                     9       X { 8/8 eled
                                                                                         X { 8/8 eled 3 X X X X S
                                                                                                                 X { 8/8 eled 3 X 0 SX X X 3 { 0 SX 01
                                                                                                                                                      1
                                                                                                                                                       1
 3 HL 8
       3 HL 8
             3 HL 8         ~ 3
                               ~ 3
                                  ~ 3                       333s]
                                                                 333s]
                                                                      333s]                                            {
                                                                                                                        {
 3 8 1 8
        3 8 1 8
               3 8 1 8
 3
  3
   3        9
             9
              9             38 8
                                38 8
                                    38 8
                            5
                             5
                              5                             H32
                                                               H32
                                                                  H32
                                                            G6 88
                                                                 G6 88
                                                                      G6 88                                 8
                                                                                                             8
                                                                                                              8        8 slgk
                                                                                                                             8 slgk
                                                                                                                                   8 slgk
       8
        8
         8                  8
                             8
                              8
                            8
                             8
                              8                              8/8
                                                                8/8
                                                                   8/8                                      8
                                                                                                             8
                                                                                                              8        6 8bg
                                                                                                                            6 8bg
                                                                                                                                 6 8bg
                                                                                                                       8
                                                                                                                        8
                                                                                                                         8
                            8
                             8
                              8
                                                                                                                                                               A12
                                                                                                                                                                  A12
                                                                                                                                                                     A12
- --
            2
             2
              2
            3
             3
              3
            5
             5
              5
 6 1
    6 1
       6 1  n
             n
              n
2 2 21 1 1  8
             8
              8  A13
                    A13
                       A13
- --
g
 g
  g       ge/8
              ge/8
                  ge/8                                                                                                      g/alsi8 3 3 3
                                                                                                                                         g/alsi8
                                                                                                                                                g/alsi8
                                                                                      N N N                 U U U N N N     N N N      3 3 3     2
                                                                                                                                                  2
                                                                                                                                                   2
8
 8
  8       a
           a
            a
          82
            82
              82                                                                                                                 8
                                                                                                                                  8
                                                                                                                                   8
                                                                                                                                 8
                                                                                                                                  8
                                                                                                                                   8Uh
                                                                                                                                      Uh
                                                                                                                                        Uh                3
                                                                                                                                                           3
                                                                                                                                                            3
                                                                                                                                                 #
                                                                                                                                                  #
                                                                                                                                                   #
                1 1
                   1 1
                      1 1                                                                                                                                  5
                                                                                                                                                            5
                                                                                                                                                             5
 1
  1
   1                          #F ekk Hel 2 2 2
                                              # F ekk Hel 8
                                                          # F ekk Hel 88
                                                                       8
                                                                        8                                                             8
                                                                                                                                       8
                                                                                                                                        8                 3
                                                                                                                                                           3
                                                                                                                                                            3
                     8
                      8
                       8        33
                                  33
                                    33                     #
                                                            #
                                                             #                                                             8                              3
                                                                                                                                                           3
                                                                                                                                                            3
                                               F
                                                F
                                                 F                                                               8
                                                                                                                  8
                                                                                                                   8                  8
                                                                                                                                       8
                                                                                                                                        8
       D D D                 lu els/3ela-lg sl8 3 3 3
                                                     lu els/3ela-lg sl8
                                                                       lu els/3ela-lg sl8                             3
                                                                                                                       3
                                                                                                                        3        8
                                                                                                                                  8
                                                                                                                                   8
      83
        83
          83                                               5
                                                            5
                                                             5
                                                           aJ 0 Ela e/edq
                                                                          aJ 0 Ela e/edq
                                                                                         aJ 0 Ela e/edq s+l
                                                                                                           s+l
                                                                                                              s+l     5
                                                                                                                       5
                                                                                                                        5        8
                                                                                                                                  8
                                                                                                                                   8                      8
                                                                                                                                                           8
                                                                                                                                                            8
      1
       1
        1                                 Ji
                                            Ji
                                              Ji2 2 2      8
                                                            8
                                                             8                                                                                             3
                                                                                                                                                            3
                                                                                                                                                             33
                                                                                                                                                               3
                                                                                                                                                                3
      g8
        g8
          g8               3
                            3
                             3                                                        8 8 8 8 8 8 8
                                                                                                   8 8 8
                                                                                                        8 8 8
                                                                                      3
                                                                                       3
                                                                                        3
                           1
                            1
                             1                             5
                                                            5
                                                             5                                   2
                                                                                                  2
                                                                                                   2        8
                                                                                                             8
                                                                                                                                                         A14
                                                                                                                                                            A14
                                                                                                                                                               A14
- --
A15
- --
    slel 3
  M0 N NJ2
 8 8  g
        #
071 HE      RL
 5 37       8
 klglgi83
Hege        5
     # 6j            89
                8   3
 E6 1 1 8i3     E
                74
                      A16
- --
# APPENDIX B: Electrical harnesses and diagrams

- B1: E402-ROBD2, AC power entry cable
- B2: E609-ROBD2, data interface ribbon cable
- B3: E613-ROBD2, power supply cable, low voltage DC
- B4: E615-ROBD2, RS232 interface cable
- B5: E616-ROBD2, PC416 power interconnect cable
- B6: E625, Oxygen dump switch cable
- B7: E626, Oxygen and pressure sensor cable
- B8: E627, Solenoid valve cable
- B9: E628, Pulse oximeter power supply cable
- B10: E629, PC412-ROBD2 misc. power cables
- B11: E630, Oxygen alarm cables
- B12: E631, E625 interface to terminal block
- B13: OBSOLETE
- B14: I418, MFC1 (air) signal and power cable
- B15: I417, MFC2 (N2) signal and power cable
- B16: I397 Sheet 1, Terminal block wiring diagram
- B17: I397 Sheet 2, Oxygen pressure switch wiring diagram
- B18: A216, low oxygen alarm
- --
                                             08
                                               08
                                                 08
                                             38
                                               38
                                                 38
                                            2
                                             2
                                              2
                                                                1 #
                                                                   1 #
                                                                      1 #3
                                                                          3
                                                                           3                           3
                                                                                                        3
                                                                                                         3    {53
                                                                                                                 {53
                                                                                                                    {53      A
                                                                                                                              A
                                                                                                                               A
                                                                                                             28
                                                                                                               28
                                                                                                                 28
                                                      4
                                                       4
                                                        4
                                                      3
                                                       3
                                                        3                                                                     2
                                                                                                                               2
                                                                                                                                2  1
                                                                                                                                    1
                                                                                                                                     1
                                                                          8 8 8                                                    8
                                                                                                                                    8
                                                                                                                                     8
                                                     1
                                                      1
                                                       1                                   1 1 1                       8
                                                                                                                        8
                                                                                                                         8
                                                                                                                       7
                                                                                                                        7
                                                                                                                         7
                                                           Ag
                                                             Ag
                                                               Ag
                                                           9
                                                            9
                                                             9                                                                          1
                                                                                                                                         1
                                                                                                                                          1
                                                                   8
                                                                    8
                                                                     8        M
                                                                               M
                                                                                M3
                                                                                  3
                                                                                   3 3
                                                                                      3
                                                                                       3
                                                                   8
                                                                    8
                                                                     88
                                                                       8
                                                                        8         01
                                                                                    01
                                                                                      01                                                       3
                                                                                                                                                3
                                                                                                                                                 3
                                                 1
                                                  1
                                                   1                                                                  3
                                                                                                                       3
                                                                                                                        3                     1
                                                                                                                                               1
                                                                                                                                                1
             0
              0
               0                                                          @UCK (22 Ao)
                                                                                      @UCK (22 Ao)
                                                                                                  @UCK (22 Ao)1 23
                                                                                                                  1 { { { 23
                                                                                                                            1 23
                  Ja
                    Ja
                      Ja                                                                                              1
                                                                                                                       1
                                                                                                                        1                    2
                                                                                                                                              2
                                                                                                                                               2
                  3
                   3
                    3 03
                        03
                          030
                             0
                              0                                                  8
                                                                                  8
                                                                                   8
    0
     0
      0     1
             1
              1                 @
                                 @
                                  @    8
                                        8
                                         8                                       8
                                                                                  8
                                                                                   8                                                           0
                                                                                                                                                0
                                                                                                                                                 0
       1
        1
         1                A
                           A
                            A           3
                                         3
                                          3                                      2
                                                                                  2
                                                                                   2
1
 1
  1               J0 {
                      J0 {
                          J0 {3 8
                                 3 8
                                    3 8
                          8
                           8
                            8          1
                                        1
                                         1
                                                                                                                                               B1
                                                                                                                                                 B1
                                                                                                                                                   B1
- --
                                                                   {
                                                                    {
                                                                     {
                                                                   8
                                                                    8
                                                                     88
                                                                       8
                                                                        8
                               6
                                6
                                 6                                 8
                                                                    8
                                                                     8
                               4
                                4
                                 4
                               8
                                8
                                 8
                               8
                                8
                                 8
                               5
                                5
                                 5                                         @
                                                                            @
                                                                             @
                               3
                                3
                                 3
                                                                            3
                                                                             3
                                                                              3
                                                                           8
                                                                            8
                                                                             8
                                                                           8
                                                                            8
                                                                             8
                                                              @
                                                               @
                                                                @           =
                                                                             =
                                                                              =
                                                         @
                                                          @
                                                           @  3
                                                               3
                                                                3
                                                              8
                                                               8
                                                                8
                                    28
                                      28
                                        28
                                    22
                                      22
                                        222 2 2          5
                                                          5
                                                           5
                                                         8
                                                          8
                                                           8  S
                                                               S
                                                                S
                        I I I                            2
                                                          2
                                                           2
                       0
                        0
                         0                               3
                                                          3
                                                           3
                                                 @
                                                  @
                                                   @
1 1 11 2 1 1 1 1 8
    1
     1   2
          23
            3
             3
              3
               3
                35 5 51 8
                         1 8                     3
                                                  3
                                                   3
                                                 6
                                                  6
                                                   63
                                                     3
                                                      3
                                                                                     1 1 11 1 1
                                                 6
                                                  6
                                                   6                         B2
                                                                               B2
                                                                                 B2
              3
               3
                3                                                                      3 3 3
- --
                                            8
                                             8
                                              8                      1
                                                                      1
                                                                       1                           JJ
                                                                                                     JJ
                                                                                                       JJ
                                                                                                   Ij
                                                                                                     Ij
                                                                                                       Ij
                                                   2 2 2             @
                                                                      @
                                                                       @
                                                   2 2 2             E
                                                                      E
                                                                       E1
                                                                         1
                                                                          1                        Ii;
                                                                                                      Ii;
                                                                                                         Ii;
                                                   1 1 1                                            7 7 7 1 1 1 1 1 1
                                                   6 6 6
                                                                                                    1 1 1
                                                                           5 5 5
                                                                                  2 2
                                                                                     2 2
                                                                                        2 2         8 8 8
                                                                                  [
                                                                                   [
                                                                                    [
                                                 82 82 82
                                                                                    2
                                                                                     2
                                                                                      2
                            8 8 8
                          0
                           0
                            0      1 1 1                                             A @
                                                                                        A @
                                                                                           A @
                                   E E E                    3
                                                             3
                                                              3
    1 1 1 0 H H H 10
                    0 J J J 1
          82
            82
              82                                           J
                                                            J
                                                             J                       2 3
                                                                                        2 3
                                                                                           2 33
                                                                                               3
                                                                                                3            1 1 1
                                                                                                             1 1 1
                2i
                  2i
                    2i3 3 31                               2 >
                                                              2 >
                                                                 2 >                       S
                                                                                            S
                                                                                             S
1 1 1                                2 2 2                  @
                                                             @
                                                              @
                                                           S
                                                            S
                                                             S
                                                                                        B3
                                                                                          B3
                                                                                            B3
- --
 8 8 8
1 1 1      1 1 1
           0 0 0                                                                              1 1 1
 3 3 3                          8 8 8            2 2 2
 1 1 1                          3 3 3            8 8 8   ke
                                                           ke
                                                             ke           2
                                                                           2
                                                                            28 8 8
 8 8 8                          3
                                 3
                                  3                         3 3 3 8 8 8
                                                          3 3 3 J J J 1 1 1 8 8 8    8 8 8
 1 1 1     1 1 1                1 1 1                                     3 8 8 8 1
                                                                          3 1
                                                                             3 1             IE
                                                                                               IE
                                                                                                 IE
1
 1
  1                                               3 3 3                   1
                                                                           1
                                                                            1
                          A
                           A
                            A
                          {
                           {
                            {                                                                HE
                                                                                               HE
                                                                                                 HE
                                        { { {
                                        8 8 8 3
                                        3
                                         3
          ha
            ha
              haI 6j 1 1 1                                                                    1 1 1
              I 6j
                  I 6j
                           9
                            9
                             9         1
                                        1
                                         1
                           0
                            0
                             0         9
                                        9
                                         9                                                  1 1 1E
                                                                                                  E
                                                                                                   E
8 0 1 1 1 1
           8 0 1
                8 0 1                                                                       08
                                                                                              08
                                                                                                08
                           3
                            3
                             3                                        2
                                                                       2
                                                                        2                   1 1 1
8
 8
  8                                                                   D
                                                                       D
                                                                        D
                 Ie
                   Ie
                     Ie
                                                                                                 B4
                                                                                                   B4
                                                                                                     B4
- --
         2
          2
           2             8
                          8
                           8        8
                                     8
                                      8  8
                                          8
                                           8  1
                                               1
                                                1            0 1
                                                                0 1
                                                                   0 12 2 22
                                                                            2
                                                                             2                             @
                                                                                                            @
                                                                                                             @
                                                                                                           3
                                                                                                            3
                                                                                                             3
                                                             2
                                                              2
                                                               2                                           3
                                                                                                            3
                                                                                                             3
                                                                                                           8
                                                                                                            8
                                                                                                             8
                                                                                         2 1
                                                                                            2 1
                                                                                               2 1
                                                                    {<
                                                                      {<
                                                                        {<              82
                                                                                          82
                                                                                            82
                                                                    Ssss
                                                                        Ssss
                                                                            Ssss                8
                                                                                                 8
                                                                                                  8
                                                                    WWll
                                                                        WWll
                                                                            WWll
                                                                   2882
                                                                       2882
                                                                           2882
                                                   g
                                                    g
                                                     g              WWww
                                                                        WWww
                                                                            WWwwJJ
                                                                                  JJ
                                                                                    JJ          8
                                                                                                 8
                                                                                                  8
                       8
                        8
                         8                                            2
                                                                       2
                                                                        2
                                                        0
                                                         0
                                                          0           W
                                                                       W
                                                                        W: 2
                                                                            : 2
                                                                               : 2
2 6
   2 6
      2 6
         8 8 1 E
                8 8 1 E
                       8 8 1 E                          5
                                                         5
                                                          5           4 2 2 2
                                                                      4
                                                                       4
                            li
                              li
                                li                      3
                                                         3
                                                          3           '1
                                                                        '1
                                                                          '1
                                                                           8
                                                                            8
                                                                             8
                                                        S
                                                         S
                                                          S
                                                                                                     B5
                                                                                                       B5
                                                                                                         B5
- --
                                                                                                     0
                                                                                                      0
                                                                                                       0W
                                                                                                         W
                                                                                                          W
HHWH 3 3 3 L L L
                HHWH
                    HHWH1 1 1 0 0 0 ! ! ! HL L L H J J J 2 2 2H88
                                                                 88
                                                                   88  3 1
                                                                          3 1
                                                                             3 1
                                                                       A
                                                                        A
                                                                         A                            8
                                                                                                       8
                                                                                                        8
 h 1 1 1 539 k 1 1 1 2 2 2
 h 539 k 2 J} 1 1 1
                   h 539 k 2 J}2 J}                         1
                                                             1
                                                              1         D
                                                                         D
                                                                          D 2
                                                                             2
                                                                              2
  533 1 1 1 # 1 1 1
  533 # 1 1 1
  533 #
  Bxx 1 1 1 4 4 4
                 Bxx
                    Bxx: : :
                                            8 64 E
                                                  8 64 E
                                                        8 64 E
                                            W
                                             W
                                              W        Q
                                                        Q
                                                         Q                        n 4
                                                                                     n 4
                                                                                        n 4
                                                                                  3
                                                                                   3
                                                                                    30 A
                                                                                        0 A
                                                                                           0 A
              2 2 283
                     83
                       83                   2
                                             2
                                              2        7
                                                        7
                                                         7                                 @
                                                                                            @
                                                                                             @
                                            4 2 8 0
                                                   4 2 8 0
                                                          4 2 8 0
                                            8
                                             8
                                              8    0 2 3
                                                        0 2 3
                                                             0 2 3                              3
                                                                                                 3
                                                                                                  3
       8 8 8 0 ] ] ] 1 1 1
       1 1 10
             01
               1
                1           I I I 5               0 0 6
                                                       0 0 6
                                                            0 0 6
                                                   0
                                                    0
                                                     09 0
                                                         9 0
                                                            9 0
                                                       2
                                                        2
                                                         2                                                       1 1 1
  8
   8
    8                         5
                               5
                                                                                                         B6
                                                                                                           B6
                                                                                                             B6
- --
                                                                                                            R
                                                                                                             R
                                                                                                              R jel
                                                                                                                   jel
                                                                                                                      jel
       2
        2
         2                            2
                                       2
                                        2                                 H
                                                                           H
                                                                            H
                                                                             <
                                                                              <
                                                                               <          222222?
                                                                                                 222222?
                                                                                                        222222?4 4 4 000000
                                                                                                                           000
       3
        3
         3                            3
                                       3
                                        3                                                                       2 2
                                                                                                                   2 2
                                                                                                                      2 2
                                                                          2 2
                                                                             2 2
                                                                                2 2                             la
                                                                                                                  la
                                                                                                                    la
    1 2/
        1 2/
            1 2/                       1 1 1                                                                     3
                                                                                                                  3
                                                                                                                   3   8
                                                                                                                        8
                                                                                                                         8
    8 1 8 g
           8 1 8 g
                  8 1 8 g
    8 8 8
               6 6 6                   1 1 1                               #
                                                                            #
                                                                             #                                   3
                                                                                                                  3
                                                                                                                   3
       2 ? 3
            2 ? 3
                 2 ? 3              81
                                      81
                                        81                                 2
                                                                            2
                                                                             2                                   8 8 8
    3 9
       3 9
          3 9      3 5 9
                        3 5 9
                             3 5 9
 8 8 8
      8 8 8
           8 8 88
                 8
                  88 3
                      8 3
                         8 3                4
                                             4
                                              4                                                                    4
                                                                                                                    4
                                                                                                                     4
                                                                                                                   8
                                                                                                                    8
                                                                                                                     8
                         88
                           88
                             88                                                      8
                                                                                      8
                                                                                       8                           3
                                                                                                                    3
                                                                                                                     3
       3
        3
         3                88
                            88
                              88                                                     2
                                                                                      2
                                                                                       2                           22
                                                                                                                     22
                                                                                                                       22
                         88
                           88
                             88                  9
                                                  9
                                                   9
                                                 3
                                                  3
                                                   3
                6j
                  6j
                    6j                                4
                                                       4
                                                        4  G
                                                            G
                                                             G       2
                                                                      2
                                                                       2
                                                      3
                                                       3
                                                        3  2
                                                            2
                                                             2       3
                                                                      3
                                                                       3
                                                                     2
                                                                      2
                                                                       2
8 8
   8 8
8   8 1 1 1 11
              1                                               H
                                                               H
                                                                H
                                                              83
                                                                83
                                                                  83
         1 1 1
                                                                                                                     B7
                                                                                                                       B7
                                                                                                                         B7
- --
     0 0 01
           1
            1          0
                        0
                         0  I I I      0 0 01
                                             1
                                              1   8 8 8
     0 0 0             1
                        1
                         1             1 1 1
     8
      8
       8  1
           1
            1    1 1 1      1
                             1
                              1   1 1 1    1 1 1  1
                                                   1
                                                    1
     1 1 1             1
                        1
                         1             1 1 1
                 1 1 1            1 1 1           0 0 0 8
                                                  8
                                                   8
                                                  e
                                                   e
                                                    e
                       6
                        6
                         6                        7 1 1 1 3
                                                  7 3
                                                     7 3     2
                                                              2
                                                               2
                                                                @
                                                                 @
                                                                  @  3 E
                                                                        3 E
                                                                           3 E
                                                                     5
                                                                      5
                                                                       5 3
                                                                          3
                                                                           3
                                                                                  8
                                                                                   8
                                                                                    8
                                                                                HE
                                                                                  HE
                                                                                    HE8
                                                                                       8
                                                                                        8
               H
                H
                 H
               6j
                 6j
                   6j
E
 E
  E           1
               1
                1                                                                          B8
                                                                                             B8
                                                                                               B8
- --
  8
   8
    8
  8
   8
    8                       8
                             8
                              8
                            8
                             8
                              8
                            3
                             3
                              3
                            8
                             8
                              8
 3: 8
     3: 8
         3: 8
 8 0
    8 0
       8 0 R
            R
             R
 2
  2
   2       3
            3
             3
 1
  1
   1      8
           8
            8
                                       2
                                        2
                                         2
            2
             2
              2                        2 2 2
                                       8
                                        8
                                         8
            2
             2
              2                       2
                                       2
                                        2
   H
    H
     H      5
             5
              5
            w
             w
              w
8 1 1 1 1 1 1
             8 1 1 1
                    8# # #                  1 1 1E E E
 1 1 1                           B9
                                   B9
                                     B9
- --
                                                                [
                                                                 [
                                                                  [          8 0
                                                                                8 0
                                                                                   8 0
                                                                              <
                                                                               <
                                                                                <
                                       +
                                        +
                                         +                      3
                                                                 3
                                                                  3
                               8
                                8
                                 8     83
                                         83
                                           83                                     2
                                                                                   2
                                                                                    2
                                                                5
                                                                 5
                                                                  5
   Ji 58 9 1 1 1 1 1 1 8 e e e 3 3 3                            2
                                                                 2
                                                                  2          2
                                                                              2
                                                                               2
  Ii 1 1 1
          Ii
            Ii 1 1 1 ! ! ! 8
   Ji 58 9 8                                               s
                                                            s
                                                             s
   38 # 2 2 2 } 7 7 7 1 1 1
   Ji 58 9 0 0 0 } }              3
                                   3
                                    3     d 3
                                             d 3
                                                d 3
                                          A
                                           A
                                            A              L
                                                            L
                                                             L
   38 # 0 0 0
             38 #                 8
                                   8
                                    8     8 8
                                             8 8
                                                8 8
       0 0 01 1 11 1
                    1 1
                       1 1
   E33 22 1
           E33 22 1
   E33
      Bxx 1 1 1 22 1
   Bxx
      Bxx
                83
                  83
                    834
                       4
                        4
                              S
                               S
                                SN
                                  N
                                   N
                                          6
                                           6
                                            6N
                                              N
                                               N
                                                           5
                                                            5
                                                             5            8
                                                                           8
                                                                            8<
                                                                              <
                                                                               <0
                                                                                 0
                                                                                  0
          Ie
            Ie
              Ie
               1 1 1          9
                               9
                                9        9
                                          9
                                           9         6
                                                      6
                                                       6   L
                                                            L
                                                             L                2
                                                                               2
                                                                                2
                              3
                               3
                                3         3
                                           3
                                            3                        [
                                                                      [
                                                                       [
" " "   8 8 8 7 1 1 1 1 1 17
                            7                         =
                                                       =
                                                        =
                                                      5
                                                       5
                                                        5                 2
                                                                           2
                                                                            2
        1 1 1 1 81 8
                    1 8                               2
                                                       2
                                                        2            3
                                                                      3
                                                                       3
                                                                     5
                                                                      5
                                                                       5
   8
    8
     8                   Ie
                           Ie
                             Ie                                      2
                                                                      2
                                                                       2
                                                                          B10
                                                                             B10
                                                                                B10
- --
                                                                                                  2
                                                                                                   2
                                                                                                    2
                                                        2
                                                         2
                                                          2                    8
                                                                                8
                                                                                 8               0
                                                                                                  0
                                                                                                   0
                                                        9
                                                         9
                                                          9+
                                                            +
                                                             +   [
                                                                  [
                                                                   [            2 3
                                                                                   2 3
                                                                                      2 3         2 2
                                                                                                     2 2
                                                                                                        2 2
 li 1 1 1 1 W 3 3 31 W
                      1 W                              3
                                                        3
                                                         3      c
                                                                 c
                                                                  c                         3
                                                                                             3
                                                                                              3
 li
   li 1 1 1 58 8 2 2 2 } } } ] ] ] 8 8 8                        <
                                                                 <
                                                                  <                         8
                                                                                             8
                                                                                              8
X k F2 J
X
 X58 8 k F2 J
             58 8 k F2 J                                                                   3
                                                                                            3
                                                                                             3        3
                                                                                                       3
                                                                                                        3
                                                                                                      1
                                                                                                       1
                                                                                                        1
     : : :1 1 1                                                           3
                                                                           3
                                                                            3
                                                                          S
                                                                           S
                                                                            S
 Bexl 1 1 1 83
              Bexl
                  Bexl
                      533 2 2 2 4 4 4 1
  533 E 83
          533 E E 831
                     1                                           1
                                                                  1
                                                                   1     1
                                                                          1
                                                                           1                          2
                                                                                                       2
                                                                                                        2
                                          2
                                           2
                                            2                                                         3
                                                                                                       3
                                                                                                        3
                                          U
                                           U
                                            U
                                          9
                                           9
                                            9                    3
                                                                  3
                                                                   3
                                          S
                                           S
                                            S
  > #
     > #
        > #
      5 5 51 1 11 ] ] ] J J J I
                               1 I
                                  1 I    1 85
                                             1 85
                                                 1 85           x
                                                                 x
                                                                  x   2
                                                                       2
                                                                        2
                                                                      {
                                                                       {
                                                                        {                        88
                                                                                                   88
                                                                                                     882
                                                                                                        2
                                                                                                         2
                                                                                                         8
                                                                                                          8
                                                                                                           8    F
                                                                                                                 F
                                                                                                                  F
                                                                                                                 1 1 1
  8
   8
    8                                                                 2
                                                                       2
                                                                        2                        32
                                                                                                   32
                                                                                                     32
                                                                                                     B11
                                                                                                        B11
                                                                                                           B11
- --
                                         2
                                          2
                                           2
                                         3
                                          3
                                           3    2
                                                 2
                                                  2
                                         8
                                          8
                                           8    3
                                                 3
                                                  3
                                                ~
                                                 ~
                                                  ~
                                                8
                                                 8
                                                  8
                                           2
                                            2
                                             2
                                           3
                                            3
                                             3
                            8
                             8
                              8           8
                                           8
                                            8    58
                                                   58
                                                     58
                                                       4
                                                        4
                                                         4
                                    3
                                     3
                                      3
                            2
                             2
                              2     x
                                     x
                                      x          88
                                                   88
                                                     88
                           8
                            8
                             8                   33
                                                   33
                                                     33
                                                       88
                                                         88
                                                           88
                           8
                            8
                             8
                                  3 3 3                  I 28
                                                             I 28
                                                                 I 28
                                 2
                                  2
                                   2                          23
                                                                23
                                                                  23
                                                         9 2 8
                                                              9 2 8
                                                                   9 2 8
                                                        22
                                                          22
                                                            22
                                                         3
                                                          3
                                                           3        1
                                                                     1
                                                                      1
E E E 3 1
         3 1
            3 11 1 1; ; ;                                                 B12
                                                                             B12
                                                                                B12
- --
 3 3 3 9 9 9 1 1 1
                  28
                    28
                      28                         1
                                                  1
                                                   1
                                                 8
                                                  8
                                                   8                 [
                                                                      [
                                                                       [
                                                 0
                                                  0
                                                   0
                9
                 9
                  9
                1
                 1
                  1
         1 1 1  J
                 J
                  J          1 1 1 2 2 2 1
                                          1
                                           1  82 8 8 8
                                              82
                                                82
                                              2 32
                                                  2 32
                                                      2 32
                8
                 8
                  8                           8 8 8
                3
                 3
                  3       IPEFFE
                                IPEFFE
                                      IPEFFE                6
                                                             6
                                                              6
6 6 6 FT 1
          FT 1
              FT 1
  8
   8
    8
    3
     3
      3         8
                 8
                  8
                                                p
                                                 p
                                                  p8 8 8             I6
                                                                       I6
                                                                         I61 1 1
                                                2 2 2
                                                                 B14
                                                                    B14
                                                                       B14
- --
                6                  [
                                   1
                                   4
                                   5
                                   3
                              8
                               8
      3       3
                        ~
                            7
8                        @ 8
                         3
3        188       2 6
                   8         E
 7 1     08        8         88
                             7
 E
                              B15
- --
                 +           8 282
li T8 1 W 7 !8 J 28            2
F 1 588 k E! J} Lh   823 2 2 82 8
  0    1 1             S       2
 8 #xe 4
         0       02    28        2
                 2   8925 8 2 8
                       22
                       33N     8 2N  ei3 8 #
                                      Bi23 _          3
                                              02
   IR 12                                              5 %5 #
   8                                                  HH
3           5                                        #8
                                                         3
                                                B16
- --
                                      28
                                        28
                                          28                                                                           8 8
                                                                                                                          8 8
                                                                                                                             8 83
                                                                                                                                 3
                                                                                                                                  3
                                       8 4
                                          8 4
                                             8 4                   SNa
                                                                      SNa
                                                                         SNa      2 2 2                3 3 3   3
                                                                                                                3
                                                                                                                 3     2 2
                                                                                                                          2 2
                                                                                                                             2 2
                                                                                                                       8
                                                                                                                        8
                                                                                                                         8
                                                                                                                             2
                                                                                                                              2
                                                                                                                               2
                                       1
                                        1
                                         1                                                                             0
                                                                                                                        0
                                                                                                                         0
                                                                6
                                                                 6
                                                                  6                                            2 8 8
                                                                                                                    2 8 8
                                                                                                                         2 8 8s9
                                                                                                                                s9
                                                                                                                                  s9
                                                      810
                                                         810
                                                            810        Lin
                                                                          Lin
                                                                             Lin
                                                                      5lJ
                                                                         5lJ
                                                                            5lJ          9inl
                                                                                             9inl
                                                                                                 9inl
                                       2
                                        2
                                         2                                                                             2
                                                                                                                        2
                                                                                                                         2
                                                                                                                       3
                                                                                                                        3
                                                                                                                         3
3 I 3 I 5
         3 I 3 I 5I 3 I I I I 507
                                 07
                                   07      28
                                             28
                                               28
                                           8 3
                                              8 3
                                                 8 3                                                                     8
                                                                                                                          8
                                                                                                                           8
38 8 8    3
           3
            3                                  8
                                                8
                                                 8                                                            03;
                                                                                                                 03;
                                                                                                                    03;
             2
              2
               2                                0
                                                 0
                                                  0                                                                      01
                                                                                                                           01
                                                                                                                             01
                                                                                                                          @
                                                                                                                           @
                                                                                                                            @
                                                                                                                         9
                                                                                                                          9
                                                                                                                           9
                                                                                                                                     B17
                                                                                                                                        B17
                                                                                                                                           B17
- --
                                     J3 8N
           8             9            183
           88            335 ~
WA J 1
li 1 1 1Vb L 0H 2 1                     5
 528 2 ]   2             Ye           2 2
 1                              8     3
    F2                           8    8
 3[ #[ 1 3                            3
 0 4                 2                1
  I "82        8     {
    J          8                      2
               8                      2
                        38 #               1
  1                     {a  1
  8                     22
2      I                   52
                                    B18
- --
# APPENDIX C: ROBD2 RECOMMENDED SPARE PARTS LIST

PRICES EFFECTIVE: 2/24/2006

REVISION: 1

|ITEM #|QUANTITY|ENVIRONICS #|DESCRIPTION|UNIT PRICE|
|---|---|---|---|---|
|1|1|A204|BATTERY BACKUP ASSEMBLY| |
|2|1|A222|PULSE OXIMETER POWER SUPPLY ASSEMBLY| |
|3|1|A209|3-WAY SOLENOID VALVE ASSEMBLY, MFC CROSSOVER| |
|4|1|A210|2-WAY BYPASS VALVE ASSEMBLY (LARGE BLUE SOLENOID)| |
|5|1|A215|BREATHING LOOP PRESSURE SENSOR WITH HARNESS| |
|6|1|A216|O2 ALARM WITH HARNESS| |
|7|1|A221|FILTER, SS WIRE, 60 MESH, 02 CLEANED| |
|8|2|AK01-002|PULSE OXIMETER SPEAKER (TAPE NOT INCLUDED)| |
|9|5|CA01-001-16|BREATHING HOSE AND BREATHING BAG CLAMPS| |
|10|1|FB07-002-FM|FAN FILTER MEDIA, 45 PPI| |
|11|2|FB09-002|3 LITER BREATHING BAG| |
|12|10|FJ02-002-0022|FUSE, SLO-BLO, 2.0 AMP 250 VAC (2 PER ROBD)| |
|13|2|MA04-003-005|FILTERED ORIFICE, .005", OXYGEN SENSOR FLOW CONTROL| |
|14|2|MAB1-005-25000|AIR MASS FLOW CONTROLLER FACTORY CALIBRATED W/CERT| |
|15|2|MAB1-005-77000|N2 MASS FLOW CONTROLLER FACTORY CALIBRATED W/CERT| |
|16|10|PA00-16-001|BREATHING HOSE (7.5 FEET PER ROBD2)| |
|17|1|PA04-02-001|VITON TUBE, OXYGEN SENSOR, REPLACED WITH SK10-001| |
|18|1|PC401-1C|MICROCOMPUTER PC BOARD (DOES NOT INCLUDE EPROM)| |
|19|1|PC403-1D|MAIN PULSE OXIMETER PC BOARD| |
|20|1|PC404-1D|PULSE OXIMETER PC BOARD, ANALOG/RS232| |
|21|1|PC406-1D|KEYBOARD/DISPLAY INTERFACE PC BOARD| |
|22|1|PC412-1D|ANALOG INTERFACE PC BOARD| |
|23|1|PC416-1D|SOLENOID VALVE DRIVER PC BOARD| |
|24|1|PJ02-14-004|MAIN POWER SUPPLY W/O COVER| |
|25|1|SA06-010-02|3-WAY OXYGEN DUMP SOLENOID VALVE (W/O PINS)| |
|26|1|SJ04-001-351|OXYGEN DUMP SWITCH| |
|27|1|SK10-001|OXYGEN SENSOR| |
|28|1|SK10-001-PCB|OXYGEN SENSOR PC BOARD| |
|29|1|SK11-001G010|OXYGEN PRESSURE SWITCH, 0-10 PSIG, PRESET FOR 10 PSIG| |
|30|1|UK18-009|EPROM FOR PC401 (MUST BE PROGRAMMED BY FACTORY)| |
|31|4|VA-FIL-004-E|FILTER ELEMENTS, 5 MICRON, FOR INPUT GAS FILTERS| |
|32|1|VA-G-005|PRESSURE GAUGE, 0-15 PSIG, O2 CLEANED| |
|33|1|VA-PRR-001|OPTIONAL PRESSURE REGULATOR FOR AIR| |
|34|1|VA-PRR-002|OPTIONAL PRESSURE REGULATOR FOR NITROGEN| |
|35|1|VA-PRR-003|OPTIONAL PRESSURE REGULATOR FOR OXYGEN| |
|36|2|XJ007|PULSE OXIMETER FINGER PROBE| |
- --
# Appendix D

# GE RTV 167 FOR ROBD2 CONNECTORS

Application: 1/8” dab of RTV on center of connectors. Any connectors having more than 10 pins, apply 2 dabs, one at each end. In hard to reach locations, first apply dab to tie wrap end then to connectors. Be sure to cover both mating connectors. 14 total connections

# PC401- Micro-controller Board

Connectors H1 (inputs), H3 (RS232) and H5 (Data bus).

# PC403 – Main Pulse Oximeter Board

Connectors J402 (keypad), J404 (power in) and J407 speaker.

# PC404 – Secondary Pulse Oximeter Board (smaller)

J401 (RS232 cable)

# PC406 – Front panel

J2 (keypad)

# PC412 – Analog Board

Connectors J5 and J13

# PC416 – Status/solenoid valve driver PCB

J5 (solenoid valves)

# Main power supply

Connector TB1 (power input)

# SK10-001-PCB – Oxygen sensor PCB

J1
- --
 92831 I        9
                8 2 0       7931         g 3
                                         8 2{    28        3           8 1 1 {1 1 11 0 1
                                                                                   8
                                                                                   1     8           J
   3                   8                 9 8
 3 3            g 9                                        3                                         N
   3             9                        3 21     6 IW    2
 I 31              1                                  2 I                                       J
                                                                                                8 2
                                                      31                      93            4
             8                                                                              8
                          8                                             0 08
  8    8   +                                                            5 22622             81
      2   83       13                 1 2                              8e3    93              3
                   1 3                                                   82                       8 28
   8   8           1                  1
  2       8 8                                        2
  1   3                                              &
                                                     1            3 2
                                                                  287                            1 33
                                                                                                   1
      9    9
      3    8          1                                                     4
                      2/glg                                                  1
8 ; 1 8 1            G4 N1 8                    9      8
1     E3     8         3 8        3  8 ? 3                    823              R 38
1       1H 6             3             1 G      1 Be            0               20
                                                   8            8
- --
# APPENDIX F: ALTITUDE VERSUS PRESSURE CURVE FOR FSHT, OSFT AND PPT MODES

|Altitude (X1000 Ft)|Pressure (inH2O)|
|---|---|
|25|1.04|
|28|2.4|
|30|3.34|
|34|4|
|50|10|

PPT test

15

13

11

9

7

5

3

1

- 120

25 30 35 40 45 50 55

natural pressure

Altitude (1000 ft)

Note: The system can only be programmed to ascend to a ceiling of 34000 feet max. Pressure (inches of water)
- --
# APPENDIX G: NAVALSURVIVAL TRAINING INSTITUTE (NSTI/ASTC) FLOW, ALTITUDE PRESSURE CURVE

# FSHT AND OSFT MODES OF OPERATION

|ALTITUDE|MASK FLOW LPM|BLP ("H20)|
|---|---|---|
|0|50.0|1.60|
|5000|30.0|0.57|
|10000|37.0|0.88|
|13000|42.0|1.10|
|15000|46.0|1.30|
|18000|50.0|1.60|
|20000|50.0|1.60|
|22000|50.0|1.60|
|25000|50.0|1.60|
|28000|56.0|2.00|
|28999|59.0|2.14|
|29000|50.0|2.70|
|30000|52.0|2.90|
|34000| |4.00|

BLP "H20

4.00

3.50

3.00

2.50

2.00

1.50

1.00

0.50

0.00

0   5000   10000   13000   15000   18000   20000   22000   25000   28000   28999   29000   30000   34000   ALTITUDE
- --
# Appendix H: Respiratory physiology and ROBD2 flow rate parameters

|% O2|ALTITUDE|TIDAL VOLUME (ml)|BREATHS/MIN|MASK FLOW LPM|AIR MFC LPM|N2 MFC LPM|
|---|---|---|---|---|---|---|
|21|0|500|14|50.0|50.0|0.0|
|17.27|5000|500|14|30.0|24.7|5.3|
|14.05|10000|536|14|37.0|24.8|12.2|
|12.34|13000|536|14|42.0|24.7|17.3|
|11.28|15000|536|14|46.0|24.7|21.3|
|9.81|18000|593|14|50.0|23.4|26.6|
|8.91|20000|700|15|50.0|21.2|28.8|
|8.06|22000|800|16|50.0|19.2|30.8|
|6.89|25000|825|19|50.0|16.4|33.6|
|5.86|28000|850|23|56.0|15.6|40.4|
|5.22|30000|900|27|52.0|12.9|39.1|
|4.09|34000|933|30|56.0|10.9|45.1|
- --
# Appendix I: Power supply data sheet

Specifications are maximum 25°C unless otherwise stated and are subject to change without notice.

# OUTPUT SPECIFICATIONS

Total Output Power

- 100W Convection Cooled
- 125W Convection Cooled
- 150W 300 LFM Forced Air

# Features

- Emissions Per EN 55022,11
- Output Voltage Centering
- Universal 85-264 VAC Input
- Optional Power Fail Signal
- Standard "U" Shaped Chassis
- 2 Year Warranty

# Output Specifications

|Output 1:|0.5% (0-100% Load Change)|
|---|---|
|Output 2:|0.25% (Xoxx)|
|Output 3:|2.0% (0-100% Load Change)|
|Output 4:|2.0% (0-100% Load Change)|

# SAFETY SPECIFICATIONS

Protection (Optional): Input to restart

- Voltage Category: Protection Class
- Pollution Degree: auto recovery

# INPUT SPECIFICATIONS

- Source Voltage: 85 - 264 Volts AC
- Frequency Range: 47-63 Hz
- Source Current: 3A at 85V Input

# MODEL LISTING

|MODEL|OUTPUT 1|OUTPUT 2|OUTPUT 3|OUTPUT 4|Power Factor|
|---|---|---|---|---|---|
|CE-150-4001|+3.3/15A|+5V/15A|+12V/2A| |0.90 (150 watts, 230V)|
|CE-150-4002|+5V/15A|+3.3V/5A|+12V/2A| |0.90 (150 watts, 230V)|
|CE-150-4003|+5V/15A|+3.3V/5A|+12V/2A| |0.90 (150 watts, 230V)|

# GENERAL SPECIFICATIONS

Dielectric Strength: 5656 VDC, Primary to Secondary; 2121 VDC, Primary to Ground; 707 VDC, Secondary to Ground.

Leakage Current: <300 µA Earth Leakage Current; <100 µA Patient Leakage Current.

# POWER DESIGNS

Integrated

Ph: 570-824-4856 Fx: 570-824-4843
- --
# CE-150 SERIES MECHANICAL SPECIFICATIONS

7.09 (177.8)

6.00 (152.4)

(12.7)

BYGESUNTING HOLES

PowcR FAIL ReTuRN

REKOTC

ADJUST

3.00 (76.2)

# MULTIPLE Output

MODEL

OuIPUTOutpUT

OUIPVT

400 (101.6)

Outputs| outPUTDuput

outpuT

Outrmt

OutPUT

OuipuI

QutPUT

Ground

7.00 (177.8)

6.00 (152.4)

(12.7)

ADJUST

REMOTE BEMOTE

S.c0 (76.2)

# SINGLE OUTPUT MODEL

Power Fail ReiurMPowER FaIL

(~) DC OutpuT

(+) DC Qutput

CRound

50 (12.7)

(152.4)

1-84CUNTING HOLES

(44.5)

L.Co (25.4)

# DIMENSIONS

# CONNECTORS

AC Input Connector P1:

.156 inch friction lock header mates with Molex 09-50-3031 or equivalent

crimp terminal housing with Molex 08-50-0189 or equivalent crimp terminal

DC Output Connector P2: (Single Output)

6-32 screw down terminal mates with # 6 ring tongue terminal:

DC Output Connector P2: (Multi Output)

'156 inch friction lock header mates with Molex 09-50-3121 or equivalent

crimp terminal housing with Molex 08-50-0189 or equivalent crimp terminal

Ground Connector

Ground mates with .187 inch quick disconnect terminal.

Option/Sense Connector P3: (Single Output)

100 inch friction lock header mates with Molex 22-01-2067 or equivalent

crimp terminal housing with Molex type 6459 or equivalent crimp terminal.

Option Connector P3: (Multi Output)

crimp terminal housing with Molex type 6459 or equivalent crimp terminal

'100 inch friction lock header mates with Molex 22-01-2047 or equivalent

Optional cover increases height dimension from 1.75 to 92 inches.

# INTEGRATED POWER DESIGNS

Ph; 570-824-4666 Fx 570-824-4843

# ELECTROMAGNETIC COMPATIBILITY SPECIFICATIONS

|Electrostatic Discharge|EN 61000-4-2|6kV Contact Discharge|
|---|---|---|
|Radiated Electromagnetic Field|EN 61000-4-3|SVM , 26-1000 MHz|
|EFT/Bursts|EN 61000-4-4|2kV|
|Surges|EN 61000-4-5|1kV Differential Mode|
| | |2 kV Common Mode|
|Conducted Immunity|EN 61000-4-6|3V, 150KHz-80MHZ|
|Voltage Dips|EN 61000-4-11|30% Reduction, 10ms|
| | |60% Reduction, 100ms|
|Voltage Interruptions|EN 61000-4-11|95% Reduction, 500ms|
|Radiated Emissions|EN 55011|Class|
| |EN 55022|Class|
|Conducted Emissions|EN 55011| |
| |EN 55022|Class|
| | |Class|
|Harmonic Current Emissions|EN 61000-3-2| |

Specifications are typical across product line and may vary by model:

# APPLICATIONS INFORMATION

Consult factory for alternate output configurations.

Consult factory for positive, negative, floating outputs:

Specify optional overvoltage protection; remote on/off; power fail signal or cover when ordering:

125 or 150 watts as determined by the cooling method.

Each output can deliver its rated current but total output power must not exceed 100,

Rated 20 amps maximum when convection cooled only:

Free air convection cooling; 100 watts maximum output power:

Base plate cooled rating of 125 watts requires one square foot .09" thick aluminum area attached to bottom four mounting holes.

Forced air cooling rating of 150 watts requires an air speed of 300 linear feet per minute point .one inch above the main isolation transformer:

This product is intended for use as a professionally installed component within medical and information technology equipment:

A minimum load of 10% is required on output one to ensure proper regulation of 250mV (single output models only).

The use of Remote sense terminals (Figure may be used to compensate for cable losses up to decoupling capacitor Cp (0.1-10uF) and twisted pair is recommended as well as the load side capacitor CL of 100uF/Amp connected across.

Peak to peak output ripple and noise is measured directly at the output terminals of the power supply; without the use of the probe ground lead or retractable tip.

This power supply has been safety approved and final tested using strength test: Please consult factory before performing an AC dielectric strength test: DC dielectric.

The input circuit includes only one fuse in the "line" conductor: In consideration to paragraph 57.6 of UL 2601-1 be added to the neutral conductor in the end product when used in medical applications; fuse should.

Maximum screw penetration into chassis mounting holes is .250 inches.

# Maximum Output Power vs: Ambient Temperature

|150| |
|---|---|
|140|FORCED AIR COOLING|
|120|BASEPLATE COOLING|
|100|CONVECTION COOLING|
|80| |
|70| |

Ambient Temperature, (C)

# OuT

# TwiSTed PAIR

# Out 0

Figure 1 Output sense connections
- --
# APPENDIX J

# MFC1 & MFC2

# FLUID CONTROL SYSTEMS

# Mass Flow Controller (MFC) for Gases

Direct flow measurement for nominal (N) flow rates in MEMS technology from 10 ml/min to 80 ml/min.

High accuracy and repeatability. Short settling time.

Type 8711 can be combined with:

- Type 8619
- Type 0330
- Type 6013
- Type 6606

Multichannel 2/2 or 3/2-way solenoid valve.

Type 8711 controls the mass flow of gases that is relevant for most applications in process technologies. The measured value provided by the chip will be compared in the digital control electronics with the predefined set point according to the signal; if control difference is present; the control value output to the proportional valve will be modified using PI-control algorithm.

Due to the fact that the sensor is directly in contact with the gas, very fast response time of the MFC is reached. In this way, the mass flow can be maintained at a fixed value or predefined profile regardless of pressure variations or other changes in the system.

# Technical Data

|Nominal flow range|10 ml/min to 80 ml/min (N)|
|---|---|
|Voltage tolerance|110/90|
|Residual ripple|290|
|Turn-down ratio|1:50, higher turn-down ratio on request|
|Power consumption|Max 3.5-14 W|
|Operating gas|Neutral, non-contaminated gases (depending on proportional valve used)|
|Input signal|0-5 V, 0-10 V, 0-20 mA or 4-20 mA|
|Calibration gas|Operating gas or air with conversion factor|
|Input impedance|20 kΩ (voltage)|
|Max. operating pressure|10 bar (145 psi)|
|Output signal|0-5 V, 0-10 V, 0-20 mA or 4-20 mA|
|Gas temperature|10 to +70°C (10 to +80°C with oxygen)|
|Max current (voltage)|10 mA|
|Ambient temperature|10 to +50°C|
|Max load (current)|600 Ω|
|Accuracy|±0.390 FS; 10.89 min; warm up time|
|Digital communication|via adapter possible; RS232 Modbus RTU (via RS adapter), RS485, RS422 or USB|
|Settling time (t95%)|300 ms|
|Repeatability|±0.190 FS|
|Fieldbus option|(see accessories table on p. 3) PROFIBUS-DP DeviceNet; CANopen|
|Materials|Protection class IP40|
|Body|Aluminium or stainless steel|
|Seals|FKM; EPDM|
|Total weight|500 g (aluminium body)|
|Port connection|NPT 1/4, G 1/4 screw-in fitting or flange|
|Installation|horizontal or vertical, others on request|
|Light emitting diodes|Indication for power|
|Regulating unit|Normally closed (default functions, Limit with analog signals)|
|Valve orifice|0.05 to 4.0 mm|
|Binary inputs|Two|
|kvs value|0.0006 to 0.32 m³/h|
|Electrical connection|Additionally with fieldbus; D-Sub 15-pin|
|Power supply|24V DC (default functions, Limit setpoint not reached)|

The nominal flow range defines the range of nominal flow rates (full scale values) possible. Index N: Flow rates referred to available which refers to 1.013 bar and 20°C.

Alternatively, there is an Index for 1.013 bar and 80°C.

www.burkert.com

P. 1/8
- --
# APPENDIX J

# MFC1 & MFC2

# burkert

# Measuring Principle

The actual flow rate is detected by sensor. This operates according to thermal principle which has the advantage of providing the mass flow which is independent on pressure and temperature: A small part of the total gas stream is diverted into a small, specifically designed bypassing channel which ensures laminar flow conditions; The sensor element is a chip immersed into the wall of this flow channel; The chip, produced in CMOS technology, contains a heating resistor and two temperature sensors (thermopiles) which are arranged symmetrically voltage of the upstream and downstream of the heater: The differential thermopiles measure the mass flow rate passing the flow sensor; The calibration procedure effectuates a unique assignment of the sensor signal to the total flow rate through the device:

# 1. Nominal Flow Range of Typical Gases (other gases on request)

|Gas|Min|Max: Q|
|---|---|---|
|Argon|0.01|[min]|
|Helium|0.01|500|
|Carbon dioxide|0.02| |
|Air|0.01| |
|Methane|0.01| |
|Oxygen|0.0| |
|Nitrogen|0.01| |
|Hydrogen|0.01|500|

# 2. Notes Regarding the Configuration

For the proper choice of the actuator orifice within the MFC not only the pressures directly before and after the MFC should be known; if these should be unknown, please use the request for quotation form on p. 8 to indicate the required maximum flow rate Qrom' but also the pressure values directly before and after the MFC (P,P) at this flow rate should be known; or not accessible to measurement; estimates are to be made by taking into account the approximate pressure drops over the flow resistors before and after the MFC respectively at a flow rate of Q. In addition, please quote the maximum inlet pressure Puma to be encountered; This data is needed to make sure the actuator is able to provide a close-tight function within all the specified modes of operation: The request form on page 8 contains the relevant fluid specification. Using the experience of Burkert engineers already in the design phase provide us with a copy of the request containing the necessary data together with your inquiry or order:
- --
# APPENDIX J

# MFC1 & MFC2

# Pin Assignment

|Pin|Assignment|
|---|---|
|1|Analogue Control|
|2|Bus control|
|3|Relay opener|
|4|Relay shutter|
|5|Relay middle contact|
|6|GND for 24v|
|7|24V-Supply|
|8|12V-Output (only for internal company use)|
|9|Set value input GND|
|10|Set value input|
|11|Actual value output GND|
|12|Actual value output|
|13|DGND (for RS232)|
|14|Binary input|
|15|RS232 RxD (without driver)|

Note: Optional Pin and with bus version as transmitter input possible

The cable length for RS232/Setpoint and actual value signal limited to 30 meters

Driving RS232 interface only by RS232 adapter including an adaption of TL levels

# PROFIBUS DP

# With Fieldbus Version:

|Pin|Assignment|
|---|---|
|1|VDD|
|2|RxDI TxD N (A-Line)|
|3|DGND|
|4|RxDl TxD P (B-Line)|

# DeviceNet, CANopen

# Plug M12

|Pin|Assignment|
|---|---|
|1|Shield|
|2|NC|
|3|DGND|
|4|CAN_H|
|5|CAN_L|

Optional configuration with 24V DC possible for power supply via fieldbus connector. With this no power supply connection on round M12 plug needed.
- --
# APPENDIX K: PULSE OXIMETER DATA SHEET

# Specifications

Below are specifications for the Respironics Novametrix Model 51SB Pulse Oximeter: These specifications are listed for informational purposes only, and are subject to change without notice.

# Pulse Oximeter

# Principle of Operation

RedInfrared absorption

# Spoz (Oxygen Saturation)

|Range:|0-100%|
|---|---|
|Accuracy:|(for 1 standard deviation or 68% of sample distribution)|
|#29 SpOz (for 80-100% SpO2)|unspecified for 0-79%|
|Display Resolution:|1%|
|Averaging:|& seconds|
|Audio:|Pitch of pulse tone varies with SpOz value|

# Pulse Rate

|Range:|30-250 beats per minute (bpm)|
|---|---|
|Accuracy:|+ % of full scale (for 1 standard deviation or approximately 68% of readings)|
|Display Resolution:|1 bpm|
|Averaging time:|& seconds|

# Sensors

Reusable Y-SensorTM (can be disinfected and used with all patient populations) and reusable adult finger sensor

Neonatal/Pediatric and Pediatric/Adult Single Patient Use SpOz Sensors

# General Specifications

# Alerts

|Limits:|Automatic and adjustable limits for SpOz and Pulse Rate. Values are retained in memory when the monitor is turned off, or can be reset to factory defaults when the monitor is turned on.|
|---|---|
|Audio:|Adjustable volume, 2-minute silence or OFF (LED indicators)|
|Visual:|Flashing numerics for violated limit(s) and red Alert Bar" with limit (high or low) violation indicator;|
- --
# Messages

Icons for sensor disconnected, sensor off patient: Numeric codes for low signal, insufficient light; light interference, pulse out of range, sensor faulty, monitor faulty, bad signal:

# DisplayNumerics

7-Segment LED'
- --
# UFO-130-2 Oxygen Sensor

# Appendix L

2x2 inch

PC Board

# UFO 130

# ULTRA 'SENSOR

7100018

history of developing unique solutions for challenging applications

Teledyne Analytical Instruments has long

# Ultra-Fast Oxygen Sensor (UFO)

Ideally suited for use in Metabolic and Critical Care Monitors, the UFO is also a welcome addition to Clinical Exercise and Sports Medicine as well as other applications where Breath by Breath analysis is critical.

The 2-year Ultra Fast Oxygen sensor (UFO-130-2) is a prime example of this capability.

Specifically developed as a reliable and economical alternative to expensive paramagnetic sensors, the Teledyne UFO utilizes fuel cell technology and optical sensors, which is inherently rugged and forgiving.

Available with a 2 X 2 inch PC board and weighing only 4.0 ounces, the UFO can be mounted in almost any location:

Since the UFO already meets ISO 7767 (1997), ASTM F1462-93, and CE Medical Devices Directives; very little additional work is needed to integrate the sensor into new or existing products.

Unlike other sensors, the UFO is insensitive to shock, vibration, and position, and will operate without damage.

With a response time of 100 milliseconds, the UFO is one of the fastest sensors ever developed for this application.

For additional information on this or other Teledyne oxygen sensors; please contact us using the information noted on this data sheet.

Built for reliability and performance.
- --
# UFO-130-2 Specifications

Output: 3.4 - +0.4V at 100% oxygen, ATM

Range: 1 - 100% oxygen

Accuracy: Less than #1.0% oxygen at constant temperature and pressure, when calibration in air and 100% oxygen

Resolution: 0.1 oxygen

Response time:

- 10 ~ 90% OS step change in &lt;130 MS @200 +100 CC (min gas flow rate)
- Response time will degrade at slower flow rate

Cross interference:

- Referenced to ISO7767 (May; 1997)
- ASTM-F1462/93

Operating humidity: 0 ~ 99% RH (non-condensing)

Operating ambient pressure: 550 - 800 mmHg

Operating relative pressure:

- Continuous: 100 to +100 mmHg to ambient pressure
- Intermittent: Up to -200 mmHg for less than 5 seconds

Operating temperature:

- Continuous: 15 - 40°C
- Intermittent: Up to 50°C for less than 2 hours per day

# TELEDYNE ANALYTICAL INSTRUMENTS

A Teledyne Technologies Company

City of Industry; California 91748, USA

16830 Chestnut Street

TEL: 626-934-1500

FAX: 626-934-1651

TOLL FREE: 888-789-8168

Visit Our Web Site at: wwW.teledyne-ai.com

2004 Teledyne Analytical Instruments Teledyne Technologies Company

All rights reserved. Printed in the USA

Power supply:

- +11.8 VDC to +16.0 VDC
- -11.8 VDC to -16.0 VDC

Power consumption: Less than 200 mW

Weight:

- Sensor: &lt;2.5 oz
- Electronics board: &lt;1.5 oz

Dimensions:

- Sensor: 2 5/8" L x 1 3/16" W
- Electronics Board: 2" x 2"

Sensor life expectancy: 24 months in air at 25°C 50% RH

Sensor storage temperature: 0 - 40°C

Gas inlet connection: 1/16" OD tube

Gas outlet connection: Luer connector

Standard: Meets ISO7767 (May, 1997) ASTM F1462/93

# Warranty

Sensor is warranted for 2 years against defects in material workmanship

NOTE: Specifications and features will vary with application: The above are established and validated during design, but are not to be construed as test criteria for every product specifications and features are subject to change without notice.

CERTIFIED ISO 9001 2000 ANSI - Rab 0rs accredited by the Council to: Accreditation (HvAl) Nation | Accreditation Program
- --
# APPENDIX M: BLANK PERFORMANCE DATA SHEET

|SERIAL NUMBER| |DATE| |
|---|---|---|---|
|ROBD PERFORMANCE TESTING|NA|NA|NA|

|STEP #|ALTITUDE (FEET)|DESIRED % O2|ACTUAL % O2|ERROR %|O2 RANGE ALLOWED|BLP ("H2)|
|---|---|---|---|---|---|---|
|1|0|21|21|0.000|20.9 TO 21.1| |
|2|5000|17.27|17.27|0.00|17.0 to 17.5| |
|3|10000|14.05|14.05|0.00|13.8 to 14.3| |
|4|13000|12.34|12.34|0.00|12.2 to 12.5| |
|5|15000|11.28|11.28|0.00|11.1 to 11.4| |
|6|18000|9.81|9.81|0.00|9.66 to 10.0| |
|7|20000|8.91|8.91|0.00|8.76 to 9.06| |
|8|22000|8.06|8.06|0.00|7.9 to 8.2| |
|9|25000|6.89|6.89|0.00|6.74 to 7.05| |
|10|28000|5.86|5.86|0.00|5.73 to 6.0| |
|11|30000|5.22|5.22|0.00|5.1 to 5.35| |
|12|34000|4.09|4.09|0.00|4.0 to 4.2| |

# Instructions

1. Select program 20 or program the instrument with the altitudes identified above for FSHT mode.
2. Plug the mask port.
3. Run an oxygen sensor calibration.
4. Run program 20 and record the oxygen and pressure data.

NOTE: The breathing bag must be connected.
- --
# Model 265

# Very Low Differential Pressure Transducer

Ranges: 0.25 to 100 in. W.C./±0.1 to ±50 in. W.C.

Air or Non-Conducting Gas

# Also Offered with Model 265

24 VAC Excitation

w/0-5 or 0-10 VDC Output5,0 in Wc

Conduit enclosure is available as an option.

Setra Systems 265 pressure transducers sense differential or gauge (static) pressures and convert this pressure difference to a proportional electrical output. The 265 is offered with a high level 0-5 VDC output or a 4-20 mA output. The change in capacitance is detected and converted to a linear DC electrical signal by Setra’s unique electronic circuit.

It is also offered with 0-5 or 0-10 VDC output in the 24 VAC excitation version. The micro-tig welded tension sensor allows up to 10 PSI overpressure (range dependent) with no damage to the unit. In addition, the sensor parts have thermally matched coefficients, which promote improved temperature performance and excellent long-term stability.

# Pressure Ranges

|Bidirectional Pressure|Unidirectional Pressure|
|---|---|
|Pressure| |
|0 to 0.25 in. WC|0 to ±0.1 in. WC|
|0 to 0.5 in. WC|0 to ±0.25 in. WC|
|0 to 1 in. WC|0 to ±0.5 in. WC|
|0 to 2.5 in. WC|0 to ±1 in. WC|
|0 to 5 in. WC|0 to ±2.5 in. WC|
|0 to 10 in. WC|0 to ±5 in. WC|
|0 to 25 in. WC|0 to ±10 in. WC|
|0 to 50 in. WC|0 to ±25 in. WC|
|0 to 100 in. WC|0 to ±50 in. WC|

Proof Pressure for all ranges: up to 10 PSI

NOTE: Setra quality standards including ISO 9001 are based on ANSI-Z540-1. The calibration of this product is NIST traceable.

U.S. Patent Nos. 5442962, 6019002, 6014800 and other Patents Pending.

# Applications

- Heating, Ventilating and Air Conditioning (HVAC)
- Energy Management Systems
- Variable Air Volume and Fan Control (VAV)
- Environmental Pollution Control
- Static Duct and Clean Room Pressures
- Oven Pressurization and Furnace Draft Controls

# Benefits

- Up to 10 PSI Proof Pressure (Range Dependent)
- 24 VDC or 24 VAC Excitation
- High Level 0-5 VDC, 0-10 VDC or 2-Wire 4-20 mA Analog Outputs are Compatible with All Energy Management Systems
- Fully Protected Against Reverse Wiring
- Internal Regulation Permits Use with Unregulated DC Power Supplies
- 1% Accuracy Improves Variable Air Volume System Performance.
- Optional Accuracies as High as 0.25% FS
- Fire Retardant Case (UL 94 V-0 Approved)
- Meets CE Conformance Standards

Visit Setra Online: http://www.setra.com

159 Swanson Rd., Boxborough, MA 01719/Telephone: 978-263-1400/Fax: 978-264-0292 800-257-3872
- --
# Model 265 Specifications

# Performance Data

|Standard|Optional|
|---|---|
|Accuracy RSS*|±1.0% FS|
|Non-Linearity (BFSL)|±0.98% FS|
|Hysteresis|0.10% FS|
|Non-Repeatability|0.05% FS|
|Thermal Effects**| |

# Environmental Data

|Temperature|Operating*°F (°C)|Storage °F (°C)|
|---|---|---|
| |0 to +150 (-18 to +65)|-40 to +185 (-40 to +85)|

# Electrical Data (Current)

|Circuit|2-Wire|
|---|---|
|Output*|4 to 20 mA**|
|Electrical Load|0 to 800 Ohms|
|Minimum loop supply voltage (VDC)|9 + 0.02 x (Resistance of receiver plus line)|
|Maximum loop supply voltage (VDC)|30 + 0.004 x (Resistance of receiver plus line)|

# Physical Description

|Case|Weight|
|---|---|
|Fire Retardent Glass Filled Polyester (UL 94 V-0 Approved)|3 ounces|

# Ordering Information

Code all blocks in table. SSP265 Rev.D 11/10/2008 Example: Part No. 26512R5WD11T1C for a 265 Transducer 0 to 2.5” WC Range, 4 to 20 mA Output, Terminal Strip Electrical Connection, and ±1% Accuracy.

# Ranges

|Model|Differential|Bidirectional|Excitation/Output|Elec. Termination|Accuracy|
|---|---|---|---|---|---|
|2651 = 265|R25WD = 0 to 0.25” WC|0R1WB = ±0.1” WC|Standard|T1 = Terminal Strip|C = ±1% FS|
| |0R5WD = 0 to 0.5” WC|R25WB = ±0.25” WC|11 = 24 VDC/ 4-20 mA| |Optional (w/Cal. Cert.)|
| |001WD = 0 to 1” WC|0R5WB = ±0.5” WC|2B = 24VDC/ 0-5 VDC| |Optional (w/Cal. Cert.)|
| |2R5WD = 0 to 2.5” WC|001WB = ±1” WC|AB = 24 VAC/ 0-5 VDC|A1 = 1/2” Conduit|E = ±0.4% FS|
| |005WD = 0 to 5” WC|2R5WB = ±2.5” WC|AC = 24 VAC/ 0-10 VDC| |F = ±0.25% FS|
| |010WD = 0 to 10” WC|005WB = ±5” WC| | |G = ±1% FS|
| |025WD = 0 to 25” WC|010WB = ±10” WC| | | |
| |050WD = 0 to 50” WC|025WB = ±25” WC| | | |
| |100WD = 0 to 100” WC|050WB = ±50”WC| | | |

# Contact Information

While we provide application assistance on all Setra products, both personally and through our literature, it is the customer’s responsibility to determine the suitability of the product in the application.

159 Swanson Road, Boxborough, MA 01719/Tel: 978-263-1400; Toll Free: 800-257-3872; Fax: 978-264-0292; email: sales@setra.com
- --
# Appendix O: PCB Schematics

- ROBD2 specific signals
- PC406
- PC412 sheet 1
- PC412 sheet 2
- PC416 sheet 1
- PC416 sheet 2
- --
# ROBD2 SPECIFIC PCB SIGNAL CONNECTION POINTS

| | | |SIGNAL ORIGINATES| | |SIGNAL TERMINATES| | |
|---|---|---|---|---|---|---|---|---|
|PART|J#|PIN#|CABLE|FUNCTION|PART|J#|PIN#|CABLE|
|PC416|J5|15&16|E627|V1, O2 DUMP VALVE|V1 (A208)|N/A|N/A|E627|
|PC416|J5|17&18|E627|V2, BYPASS VALVE|V2 (A210)|N/A|N/A|E627|
|PC416|J5|3&4|E627 1|V3, CROSSOVER VALVE|V3, (A209)|N/A|N/A|E6271|
|A206|N/A|GND 2|E631|GND SIGNAL FOR O2 DUMP SWITCH LAMP|SJ04-001-351|N/A|X1|E625|
|A206|N/A|GND 1|E631|GND SIGNAL FOR O2 DUMP SWITCH|SJ04-001-351|N/A|3|E625|
|A206|N/A|+24VDC 1|E631|+24 VDC SIGNAL FOR O2 DUMP SWITCH LAMP|SJ04-001-351|N/A|J72|X2|
|SJ04-001-351|N/A|4|E631|GROUNDS THE INPUT LINE ON PC416, O2 DUMP|PC416|N/A|131|E625|
|A206|N/A|GND 5 23|N/A|GND SIGNAL SUPPLY TO O2 PRESSURE SWITCH|SK11-001G010|N/A|N/A| |
|SK11-001G010|N/A| |N/A|GROUNDS INPUT LINE ON PC416, LOW O2 PRESSURE|PC416|N/A|5|N/A|
|PC412|J9|1|E629|+24 VDC SUPPLY WIRE TO TERMINAL BLOCK A206|A206|N/A|+24VDC 4|E629|
|PC412|J9|2|E629|GND SUPPLY WIRE TO TERMINAL BLOCK A206| | |2ND GND SUPPLY WIRE TO TERMINAL BLOCK A206|A206|
|PC412|J10|2|E629| |A206|N/A|GND 4|E629|
|A206|N/A|GND 6|N/A|GND WIRE FOR PC401 HIGH CURRENT DRIVERS| | |+15 VDC SUPPLY FOR A216 OXYGEN ALARM4|PC401|
|PC412|J13|4|E630| |A216|N/A|1|E630|
|PC401|J2|3|E630|PULLED TO GND VIA PC401 HIGH CURRENT DRIVERS|A216|N/A|2|E630|
|PC412|J6|1|E626|+15 VDC SUPPLY VOLTAGE FOR SK10-001-PCB|SK10-001-PCB|J1|5|E626|
|PC412|J6|2|E626|-15 VDC SUPPLY VOLTAGE FOR SK10-001-PCB|SK10-001-PCB|J1|251|E6265|
|PC412|J6|4|E626|GND SIGNAL FOR PRESSURE SENSOR A215|A215|N/A| |E626|
|PC412|J6|5|E626|ANALOG GND FOR SK10-001-PCB|SK10-001-PCB|J1|2|E626|
|PC412|J6|7|E626|+24VDC FOR PRESSURE SENSOR A215|A215|N/A|1|E626|
|A215|N/A|3|E626|PRESSURE SENSOR ANALOG OUTPUT SIGNAL|PC412|J5|9|E626|
|SK10-001-PCB|J1|3|E626|I4186 OXYGEN SENSOR OUTPUT SIGNAL|PC412|J5|7|E6266|
|PC412|J5|19| |+24 VDC POWER TO MFC1|MFC1|N/A|5|I418|
|PC412|J5|20|I418|GND WIRE FOR MFC1|MFC1|N/A|4|I418|
|PC401|H1|13|I418|GND SIGNAL FOR MFC LIMIT ERROR RELAY|MFC1|N/A|3|I418|
|MFC1|N/A|2|I418|GROUNDS INPUT PIN ON PC401 I/O CONNECTOR H1|PC401|H1|1|I418|

# Footnotes

1. E631 INTERCONNECTS WITH E625, REFERENCE APPENDIX B FOR ELECTRICAL DRAWINGS.
2. SOLDER SIDE OF J7 ON PC416, REFER TO APPENDIX B, PAGE B17
3. PART HAS NO PIN NUMBERS, REFER TO APPENDIX B, PAGE B17 FOR CONNECTIONS
4. FOR A216, LOW OXYGEN ALARM, REFERENCE APPENDIX B, PAGE B19. A216 CONNECTS TO E630.
5. A215 CONNECTS TO E626 WITH INTERCONNECT PIN NUMBERS FOR A215 REFER TO THE 6-PIN INTERCONNECT.
6. ILLUSTRATION DRAWING I418 (PAGE B14 OF APPENDIX B) SHOWS MFC1 WIRING WITH RESPECT TO THESE SPECIFIC SIGNALS
7. FIELDS FOR ALIKE OR GROUPED WIRES/SIGNALS ARE SHADED
8. REFERENCE APPENDIX E FOR POINT TO POINT WIRING DIAGRAM E205
9. +24 VDC AND GND ARE CONNECTIONS ON THE A206 TERMINAL BLOCK ASSEMBLY. THESE COLORS ARE REFERENCES FROM APPENDIX E POINT TO POINT WIRING DIAGRAM.
- --
|BD7|BD6|BD5|BD4|BD3|BD2|BD1|BD0|BD7|BD6|BD5|BD4|BD3|BD2|BD1|BD0|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | |D0|D1|D2|D3|D4|D5|D6|D7| |

# HOLD

- BS1
- BS2
- EDGE
- IEN CONTRAST*
- BD0 BEEP
- BD1 KEYPAD*
- BD2 INT*
- BD3

| | | | |ROW9|ROW8|ROW7|COL1|COL2|ROW6|COL3|ROW5|ROW4|ROW3|ROW2|ROW1|COL4|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|A0|A1|DISPLAY|R/W*|D4|D3|D2|D1|D0| | | | | | | | |

# STB*

- BA3
- BA2
- BA1

BD6
BD7
BD4
BD5
BD2
BD3
BD0
BD1

# BWR*

- LCD
- BRD*
- BA0

# PC406

SHM
- --
# BD7BD6BD5BD4BD3BD2BD1BD0


|D7|VREF|
|---|---|
|D6| |
|D5| |
|D4| |
|D3|O3COMMAND|
|D2| |
|D1| |
|D0| |

|BD7|D7|
|---|---|
|BD6|D6|
|BD5|D5|
|BD4|D4|
|BD3|D3|
|BD2|D2|
|BD1|D1|
|BD0|D0|

|OE*|DACLSB*|DACMSB*|DACLD*|D7|
|---|---|---|---|---|
|BD0|MUX*| | | |
|BD1|ADC*| | | |
|BD2|IRQ*| | | |
|BD3| | | | |
|D7| | | | |
|D6| | | | |
|D5| | | | |
|D4| | | | |
|D3| | | | |
|D2| | | | |
|D1| | | | |
|D0| | | | |

|A2|A1|
|---|---|
|RD*|WR*|

# Measurements

- Lamp Temp.
- Phot. Flow
- Phot. Pressure
- Phot. Temp
- O3 Lamp Drive
- O3 Pressure
- O3 Response
- O3 Block Temp.
- Spare
- O3 Flow
- Spare

|IRQ*|VIN|STB*|
|---|---|---|
|BA3| |D3|
|BA2| |D2|
|BA1| |D1|
|BA0| |D0|

# Control Signals

|BD6|BD7|BD4|BD5|BD2|BD3|BD0|BD1|
|---|---|---|---|---|---|---|---|
| |BWR*|LCD*|BRD*|BA0| | | |

# PC412  SHM
- --
# Ozonator

# O3COMMAND

# Photometer

|IRQ*|VIN|STB*|
|---|---|---|
|BA3|BA2|BA1|
|BD6|BD7|BD4|
|BD5|BD2|BD3|
|Spare|BD0|BD1|
|BWR*|LCD*|BRD*|
|BA0|Spare|Spare|

# Photo.

# Ozonator

# PC412

# SHM
- --
# D29

# 1N4148

# D28

BD7BD6BD5BD4BD3BD2BD1BD0
BD7BD6BD5BD4BD3BD2BD1BD0
1N4148
# D27

# 1N4148

# D26

# D7  1N4148

|BD7|D7|D6|
|---|---|---|
|BD6|D6|D5|
|BD5|D5|D4|
|BD4|D4|D3|
|BD3|D3|D2|
|BD2|D2|D1|
|BD1|D1|D0|
|BD0|D0| |

# D25

# 1N4148

# D24

# 1N4148

# D23

# 1N4148

# D22

# 1N4148

|OE*|STATUSRD*|
|---|---|
|BS1|BS2|
|PORT*|ENGAGE*|
|BD7|BD0|
|FULLPWR*|STATUSWR*|
|BD1|RESET*|
|BD2|PWRSAV*|
|BD3| |

# D7

# D2

# D1

# D0

# STB*

# BA3

# BA2

# BA1

BD6
BD7
BD4
BD5
BD2
BD3
BD0
BD1
# BWR*

# BRD*

# BA0

# PC416  SHM
- --
# Solenoids 11-20

| |FULLPWR*|RESET*|PORT*|PWRSAV*|ENGAGE*| |
|---|---|---|---|---|---|---|
| |D7|D4|D3|D2|D1|D0|

# Solenoids 1-10

D7
D4
D3
D2
D1
D0

# Chasis Temperature Sensor

PC416 SHM
- --
# Appendix P

# ROBD2 FLOW CALIBRATION SHEET (CALIBRATION EQUIPMENT S/N #)

|ROBD2 SERIAL#|SYSTEM MODEL#|ROBD2|
|---|---|---|
|DATE:|STP 70oF, 29.92”HG|ROBD2 SOFTWARE REVISION:|

MFC1 : 25 SLPM SERIAL#:
MFC2: 77 SLPM SERIAL#:
|SET FLOW RATE|MEASURED FLOW RATE|SET FLOW RATE|MEASURED FLOW RATE|
|---|---|---|---|
|100%|25000|100%|77000|
|95%|23750|95%|73150|
|90%|22500|90%|69300|
|85%|21250|85%|65450|
|80%|20000|80%|61600|
|75%|18750|75%|57750|
|70%|17500|70%|53900|
|65%|16250|65%|50050|
|60%|15000|60%|46200|
|55%|13750|55%|42350|
|50%|12500|50%|38500|
|45%|11250|45%|34650|
|40%|10000|40%|30800|
|35%|8750|35%|26950|
|30%|7500|30%|23100|
|25%|6250|25%|19250|
|20%|5000|20%|15400|
|15%|3750|15%|11500|
|10%|2500|10%|7700|
|5%|1250|5%|3850|
|2.5%|625|2.5%|1925|

CAL DATE:
BY:
CAL DATE:
BY:
# VERIFICATION OF MFC CALIBRATION (ACCEPTABLE TOLERANCE OF 0.5% SET POINT)

|SET FLOW RATE|MEASURED FLOW RATE|SET FLOW RATE|MEASURED FLOW RATE|
|---|---|---|---|
|99%|24750|99%|76230|
|85%|21250|85%|65450|
|55%|13750|55%|42350|
|25%|6250|25%|19250|
|10%|2500|10%|7700|
|5%|1250|5%|3850|

MFC FLOW VERIFICATION DATE:
.
MFC FLOW VERIFICATION DATE: