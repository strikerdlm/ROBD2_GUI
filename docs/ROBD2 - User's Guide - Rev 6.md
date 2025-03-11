#   Environics

#   Model 6202

#   Reduced Oxygen Breathing Device 2

#   Operator’s Guide

Revision 6

05MAY2010

Software Rev. 6202-0.97-XX

Environics Inc.

69 Industrial Park Road East

Tolland, CT 06084-2805 USA

Phone (860) 872-1111

Web: http://www.environics.com

Fax (860) 870-9333

E-mail: INFO@ENVIRONICS.COM

- --
#   COPYRIGHT

© 2003-2010 Environics Inc. All Rights Reserved. This manual and the software contained within the product(s) described are copyrighted with all rights reserved.

#   TRADEMARKS

Environics is a registered trademark of Environics Inc. All other brand names, company names and product names mentioned are the property of their respective owners.

#   PATENTS

This product is licensed from the U.S. Navy under U.S. Patent Application No. 10/959.764

#   WARRANTY

Environics Inc. warrants this product to be free from defects in material and workmanship for a period of one year from the date of shipment. Environics warrants the following expendable items for 30 days from the date of shipment: fuses, lamps, batteries. During the warranty period, Environics will, at our option, either repair or replace any product that proves to be defective.

To exercise this warranty, contact Environics at the address below for assistance and instructions for returning the products. Repaired or replaced products are warranted for the balance of the original warranty period or at least 30 days.

#   LIMITATION OF WARRANTY

This warranty does not apply to defects resulting from product modification made without Environics’ express written consent, or misuse of any product or part. This warranty also does not apply to software, damage from battery leakage or problems arising from normal wear or failure to follow instructions.

This warranty is in lieu of all other warranties, expressed or implied, including any implied warranty of merchantability or fitness for a particular use. The remedies provided herein are the buyer’s sole and exclusive remedies.

Neither Environics nor any of its employees shall be liable for any direct, indirect, special, incidental or consequential damages arising out of the use of its instruments and software even if Environics has been advised in advance of the possibility of such damages. Such excluded damages shall include, but are not limited to: costs of removal and installation, losses sustained as the result of injury to any person or damage to property.

#   WARNING

READ THIS MANUAL CAREFULLY BEFORE USING THIS INSTRUMENT. FAILURE TO DO SO MAY VOID THE WARRANTY, DAMAGE THE INSTRUMENT OR CAUSE SERIOUS INJURY.

- --
#   ROBD2 Operator’s Guide changes

|Manual Revision # |Software Revision # |Release Date|Enhancements|
|---|---|---|---|
|1|0.93-XX|11/1/2004|Initial release|
|2|0.96-XX|10/26/2005|Added MFC safety feature, changed fitting color codes, reduced maximum altitude to 34K feet, modified self-tests, added purge to pilot test menu, added purge after test altitudes (self calibration). Fixed erroneous information and typographical errors.|
|3|0.96-XX|02/09/2006|Added statement (bottom page 1), Added Breathing loop pressure port (Bottom page 6), Added safety feature (Top page 31).|
|4|0.96-XX|04/26/2006|Modified O2 dump screen (page 29).|
|5|0.96-XX|9/27/2006|Added restrictions to connecting pulse oximeter probe (pages 3, 10 & 12). Added note about powering on the pulse oximeter in Quick start (page 10).|
|6|0.97-xx|5/5/2010|Added O2 DUMP PRESSURE setting to OPTION menu. Modified O2 Dump and O2 Pressure safety feature section. Corrected Patent information.|

- --
#   TABLE OF CONTENTS

- LIST OF FIGURES                                      v

- LIST OF ABBREVIATIONS / ACRONYMS                    vi

- OVERVIEW                                             1

- SYSTEM LAYOUT                                        2

- 
- Front Panel Layout                           2

- Pulse oximeter keys, indicators and icons    4

- Rear Panel Layout                            5

UNPACKING AND INSTALLATION                           7

- 
- Standard packaging and unpacking             7

- Transport case option and unpacking          7

- Installation                                 7

POWER AND GAS CONNECTIONS                            8

- 
- Power Connection                             8

- Gas Connection                               9

QUICK START PROCEDURE                              10

- POWER UP AND SELF-TESTS                            12

- 
- Power up                                   12

- Warmup                                     12

- Self test/calibration                      12

- Self Test Operations                       13

- Self Calibration Operations                15

SYSTEM OPERATION                                   18

- 
- Entering data                              18

- Main Screen 
- Ready mode                   19

- START – Pilot Test mode                    20

- Option menu                                24

SAFETY FEATURES                                    29

- PULSE OXIMETER                                     31

- --
#   LIST OF FIGURES

|FIGURE 1 
- FRONT PANEL LAYOUT|2|
|---|---|
|FIGURE 2 
- PULSE OXIMETER KEYS, INDICATORS AND ICONS|4|
|FIGURE 3 
- REAR PANEL LAYOUT|5|
|FIGURE 4 
- P&ID|36|

- --
#   LIST OF ABBREVIATIONS / ACRONYMS

|AC|Alternating Current|
|---|---|
|EMI|Electromagnetic Interference|
|HZ|Hertz|
|LCD|Liquid Crystal Display|
|LPM|Liters Per Minute|
|MFC|Mass Flow Controller|
|NAG|Nitrogen and Air Generator|
|P&ID|Piping and Instrument Diagram|
|PSIG|Pounds Per Square Inch Gauge|
|RFI|Radio Frequency Interference|
|SUT|Subject Under Test|
|VAC|Volts, Alternating Current|
|VDC|Volts, Direct Current|

- --
#   OVERVIEW

The second generation Reduced Oxygen Breathing Device (ROBD2) is a computerized gas-blending instrument. The system uses Thermal Mass Flow Controllers (MFC) to mix breathing air and nitrogen to produce the sea level equivalent atmospheric oxygen contents for altitudes up to 34,000 feet. The MFCs are calibrated on primary flow standards traceable to the National Institute of Standards and Technology (NIST). NIST is a federal agency whose mission is to develop and promote measurement, standards, and technology to enhance productivity, facilitate trade, and improve the quality of life. Several safety features are built into the ROBD2 to prevent over-pressurization of the Pilot’s mask and to prevent reduced oxygen contents below those being requested for a particular altitude. The software is Menu driven. The main operator’s menu consists of three selections, simplifying the use of the system for the field operator. Built in self-tests verify all system component functionality before the operation of the system can begin. If any self-tests fail, the system will not operate. The system is designed to work with both bottled gases and gases produced by a Nitrogen/Air Generator (NAG).

This manual contains information and guidance for setting up and operating the ROBD2.

Step by step instructions are provided for connecting power and gas sources, running the self-tests, running the self-calibration routines and running a pre-programmed sequence of altitudes on the subject under test (SUT).

Descriptions of alarms and safety features are provided along with actions to be taken in the event of an alarm condition.

A piping and instrument diagram (P&ID) is provided on the last page of the manual for an overview of the electrical, pneumatic and electro-pneumatic components contained within the instrument. For a more comprehensive description and illustration of the system components, see the internal layout section of the ROBD2 Programming and Technical guide.

Programming, theory of operation, technical and troubleshooting information are provided in the Programming and Technical Guide.

#   IMPORTANT

The ROBD2 operator should be certified in first-aid and CPR and have access to communication in the event of an emergency.

Prior to participation in ROBD2 training or research, the subject under test should have the equivalent to a FAA physical of any class or military flight physical and be screened for current health status prior to the run.

ROBD2 USER’S GUIDE 1 MAY 2010

- --
#   SYSTEM LAYOUT

#   Front Panel Layout

#   LCD Display

The liquid crystal display (LCD) is a four line, 20 characters display, protected by a clear lens. The display is illuminated when the system is in operation.

#   Function Keys

Three function keys (F1, F2 and F3), located below the display, and are used to make various selections from the menu displayed on the bottom line of the screen. The current function of each key is displayed above each function key on the bottom line of the display. The function of each key will change, depending on the current operating mode.

ROBD2 USER’S GUIDE 2 MAY 2010

- --
#   SYSTEM LAYOUT

#   Advance and Stop keys

The ADVANCE and STOP keys are used while running a program in the Pilot Test Mode (START mode). The STOP key aborts the program immediately upon pressing the key. The ADVANCE key immediately advances the program to the next step upon pressing the key.

#   Numeric Keypad

The numeric keypad is used for data entry of numbers 0 through 9 and a decimal point. Pressing the ENTER key completes the entry of the numeric data selected.

#   Arrow Keys

The arrow keys are used to move the cursor on the display screen to and from different fields located on the different entry screens or to scroll up or down a menu or list of information. Pressing and holding the arrow keys will cause them to repeat.

#   Menu Key

The MENU key has no function while the system is in the Operator’s mode. This key is used to move between multiple menus while the system is in the Administrator (ADMIN) mode. The ADMIN mode is restricted to those who have programming and troubleshooting rights.

#   Oxygen dump switch

This emergency stop switch is used to trigger to supply of 100% O2 to the pilot under test.

#   Breathing mask connector

This female connection port (MS 22058-1), with spring-loaded cover, is for the pilot’s breathing mask connection.

#   Pulse oximeter probe connector

This connector can be used with a finger tip probe or Y sensor with ear clips. The probes should not be connected until after the pulse oximeter has been powered on and runs through its own self test.

ROBD2 USER’S GUIDE 3 MAY 2010

- --
#   SYSTEM LAYOUT

#   Pulse oximeter keys, indicators and icons

|POWER button|Press to turn the monitor on or off:|
|---|---|
|Audio Key|Press to toggle two minute silence (when active). Press and hold for audio disable.|
|Pulse Key|Sets pulse rate alert limits when used with the keys: Press and hold to set auto alert limits.|
|SpOz key|Sets saturation alert limits when used with the keys: Press and hold to set auto alert limits.|
|Increase/decrease keys|Press to set pulse and alert audio level. Sets alert limits when used in conjunction with SpOz and Pulse.|

#   Saturation and pulse rate displays

Saturation and pulse rate values will appear: Status will appear when necessary: Set Troubleshooting on page 37. Arrows indicate alert status that alerts are being set.

Figure 2 
- Pulse oximeter keys, indicators and icons

|AC indicator|Green when the monitor is connected to AC power and rear panel power entry module switch.|
|---|---|
|Battery icon|Green when operating on battery with charged battery. Orange when battery power is diminished. Flashes when battery power is at critical low.|
|Finger probe|Icon flashes red when probe is connected or the probe is off the patient: Red for any sensor errors which occur during monitoring.|
|Hand icon|Yellow when monitor is searching for valid signal and data is being held.|
|Audio disabled icon|Flashes yellow when the audio has been disabled.|
|Two minute silence indicator|Illuminates for two minutes.|
|Signal bar|Pulses with respect to monitored pulse rate. Amplitude corresponds to signal strength.|

#   ROBD2 USER’S GUIDE

MAY 2010

- --
#   SYSTEM LAYOUT

#   Rear Panel Layout

#   Power Input

The power entry module supplies AC power to the internal power supplies. The internal power supplies convert and regulate the AC signal to the five DC voltages required by the system electronics. The power entry module has integrated EMI/RFI filtration and switch one or both hot lines dependent upon 110 or 220 VAC operation. The power entry module also has two replaceable fuses.

#   Gas Inputs

These gas inputs supply source gas to the system components. The optional quick connect fittings for these ports are colored and keyed. The Nitrogen input is black, the Air input is yellow and the oxygen input is green. The Nitrogen and air inputs should be pressurized to a dynamic pressure of 40 PSIG and the oxygen input should be adjusted to a dynamic pressure of 20 PSIG.

ROBD2 USER’S GUIDE 5 MAY 2010

- --
#   ROBD2 USER’S GUIDE

#   SYSTEM LAYOUT

#   RS-232 Port

One 9-pin RS-232 serial port is connected to the embedded controller of the ROBD system. This port is used for remote control of the ROBD2 using a host computer and communications software. Communication protocol is provided in the programming and technical guide. This protocol can be used to develop control and data collection programs using programs such as National Instruments’ Labview.

#   Breathing loop vent port

This port vents the excess flow of gas not used during inhalation and exhalation and also limits the pilot mask pressure.

#   Breathing bag port

This port is used to connect the latex-free neoprene breathing bag. The breathing bag is used to store mixed gas to satisfy the higher than average inhalation and to satisfy short, quick deep breaths.

#   Cooling fan

The cooling fan moves approximately 36 cu/ft per minute of filtered air through the ROBD chassis and out the cooling vents on the top cover of the chassis. The cooling fan should not be obstructed.

#   Breathing loop pressure port

The breathing loop pressure port, on the rear panel of the system, can be used to connect a mechanical pressure gauge or pressure transducer for monitoring breathing loop pressure. This port will normally be plugged when the system is operating and has mainly been installed for troubleshooting and verification purposes. The system has a built in breathing loop pressure transducer. If the plug is not installed during normal operation, then the positive pressure option will not function correctly.

- --
#   UNPACKING AND INSTALLATION

#   Standard packaging and unpacking

1. Remove the system from the cardboard box in which it was delivered from the factory.
2. Remove and read any important instructions or notes found within the box.
3. Save and store the box and foam inserts in the event the system needs to be returned to the factory or delivered to another site for operation.
4. If the optional pressure regulators were purchased with the system, they are delivered in a separate box.

#   Transport case option and unpacking

1. The transport case is provided with the ability to be locked. If a lock has been added, remove the lock and undo the rotary latches.
2. Remove the cover and pull the system out by the side handles.
3. If the optional pressure regulators were purchased with the system, they are stored under the area taken up by the ROBD2. The breathing bag is also located in this area as well as other miscellaneous items.

#   Installation

1. Install the system on a table or cart such that the back of the system is flush with the back vertical side of whatever it is installed on. This is due to the fact that the breathing bag hangs below the bottom of the system and needs to hang freely.
2. Remove the plugs/caps in the N2, air and 02 gas ports. Also, remove the red threaded plug from the breathing loop vent port.
3. Remove the red cap from the breathing bag port connector.
4. Be sure to leave the metal hex plug in the breathing loop port. This port is mainly for troubleshooting purposes so that a pressure gauge can be connected to monitor breathing loop pressure.
5. Proceed to the section titled Power and gas connections.

ROBD2 USER’S GUIDE 7 MAY 2010

- --
#   POWER AND GAS CONNECTIONS

After the RODB2 is unpacked, the system should be connected to power and the appropriate gas sources to the gas inlet ports on the rear panel. Environics recommends the use of a power conditioner, as recommended for computers, to eliminate power problems from affecting system operation.

#   WARNING

OPERATING THE ROBD2 AT AN INCORRECT LINE VOLTAGE WILL DAMAGE THE INSTRUMENT AND VOID THE MANUFACTURER’S WARRANTY. CHECK THE LINE VOLTAGE BEFORE YOU PLUG THE INSTRUMENT INTO ANY POWER SOURCE.

#   Power Connection

1. Important: The indicating insert of the power entry module must read either 115 or 230 V dependent upon the actual voltage being used. If it is not set for the voltage being connected, remove the insert, rotate it to the correct setting and reinstall; see below. Set for 115V for 100-120 VAC 50/60 HZ and 230 V for 200-240 VAC 50/60 HZ operation.
2. Insert the standard power cord supplied with the system into the power connector on the rear panel and insert the plug into a properly grounded outlet. The standard unit allows for 110 – 240 VAC (50/60 Hz).
3. Do not turn the power on at this point, proceed to the section titled Gas connection.

Voltage indicator

115v
1Z
115V
115V
KIL

ROBD2 USER’S GUIDE 8 MAY 2010

- --
#   POWER AND GAS CONNECTIONS

#   Gas Connection

#   Input Gas Connections

Input Gas connections are keyed and colored quick connect fittings.

1. On the rear of the ROBD2, connect the air (yellow) and nitrogen (black), at a pressure of 40 PSIG, to the respective ports. Connect the 100% oxygen (green) source at a pressure of 20 PSIG. These pressures may need to be adjusted while the system is flowing. The above listed pressures are dynamic.
2. It is important that the gas pressures stay within the ranges specified for each gas port. Otherwise, the system may produce gas blends that fall outside the accuracy specifications of the system.
3. Connect the pilot mask to the Breathing mask connector on the front panel of the system.
4. Connect the Breathing bag to the Breathing bag port connector on the rear panel. A clip has been provided on the breathing bag to help further secure it to the port.
5. Proceed to the Section titled Power-up and self-tests. As an option the following Quick start procedure can be used. This is a less detailed step by step guide on how to operate the instrument.

ROBD2 USER’S GUIDE 9 MAY 2010

- --
#   QUICK START PROCEDURE

1. Before Powering on the system make sure to perform the steps outlined in the section titled Power and gas connection.
2. Power on the system and pulse oximeter. The system will prompt for the Gas Source. Select either CYL (Pressurized gas cylinders) or NAG (Nitrogen and air generator). Note: the pulse oximeter probe can be connected anytime after the pulse oximeter is powered on.
3. Allow the warm-up time to elapse (10 minutes).
4. Once warm up time has elapsed, press the SELFTST function key. Follow the self-test prompts carefully as errors in following the prompts will cause failures in the self-test. After the self tests have run, the system will perform a self calibration. The 02 sensor will calibrate, followed by cal N2 source (if the NAG is being used), and test altitudes.
DANGER:
During self-tests, gas will be delivered to the mask, breathing bag and vent port. Do not breathe through the mask during the self test or self calibration process, since oxygen will not be present at all times.
5. The pilot’s mask can now be connected.
6. Press the START key to enter the PILOT TEST MENU.
7. To run the Positive Pressure Training, Press the PPT key from the PILOT TEST MENU. Once in the PPT mode, press START. The system will generate a high flow of air at a pressure of approximately 10” H20. Press STOP when finished. The pressure and flow will drop to the same rates as before pressing START. Press EXIT when complete or press START to repeat the test.
8. Enter RUNPRG to run a pre-programmed sequence. Select one of twenty pre-saved programs. The programs are stored as HRT (Hypoxia Recognition Training), FSHT (Flight Simulator Hypoxia Training) or OSFT (Oxygen System Failure Training).
9. Either allow program to complete or select MENU to run a manual altitude. Manual altitude will interrupt the program. Select EXIT to return to the program. If running an OSFT program, press MENU and select 02FAIL to bring the 02 level to that of the sea level equivalent for the desired altitude. Otherwise, air will be delivered to the mask for all altitudes.

ROBD2 USER’S GUIDE 10 MAY 2010

- --
#   QUICK START PROCEDURE

1. Select ADVANCE or STOP keys to perform the respective function. ADVANCE will automatically skip to the next step in the program, STOP will abort the program.
2. If the subject is at risk of becoming hypoxic, press the                       02   DUMP     emergency switch. Once the switch is turned off (turn clockwise) the flow of 100% 02 will stop and the system will generate air only.

ROBD2 USER’S GUIDE                                           11                              MAY 2010

- --
#   POWER UP AND SELF-TESTS

#   Power up

The system power switch is on the rear panel power entry module. Once the system has been powered on, the pulse oximeter can be powered on from the front panel.

IMPORTANT: Do not connect the pulse oximeter probe until powering on the pulse oximeter. The system will prompt for CYL or NAG upon power up. Once the selection is made, the system will subsequently proceed to the Warmup screen. It is important that all gas connections are made before power up. Refer to the section titled Gas connection.

#   Warmup

The system requires a 10 minute warmup period after it is powered up. During the warmup period, the screen will display WARMUP and show a 600 second (10 minute) countdown. During the warmup period, the system cannot be run and no self tests can be performed. The only available function is the OPTION key. After the warmup period, the system will show TEST ERR, indicating that the system self tests have not been run. The SELFTST function key is now available, allowing the system self test to be run.

#   Self test/calibration

Pressing the SELFTST key will automatically run all self test and calibration steps sequentially. Some tests require user interface while others do not.

At any time after the system has been powered up and self-tests have run for the first time, these self tests can be run again, either individually or all together, from the OPTION menu. This is useful for troubleshooting purposes to detect a failure that has occurred after the initial power up self-test routine.

Select SELF TEST from the options menu to run the system self tests. Select SELF CALIBRATE to run the system calibration functions, including O2 sensor calibration.

DANGER: During self-tests, gas will be delivered to the mask, breathing bag and vent port. Do not breathe through the mask during the self test or self calibration process, since oxygen will not be present at all times.

ROBD2 USER’S GUIDE 12 MAY 2010

- --
#   POWER UP AND SELF-TESTS

#   Self Test Operations

#   MFC self-test

The system will test each of the MFCs at three points within the full-scale range. The test compares the commanded flow to the MFC to the response from the MFC produced by its own internal PID control loop. When the MFC is controlling properly, the command and response are very close. If any point fails, the system will indicate the failure and stop the test. This will allow for the details of the failure to be recorded by the operator. Pressing OK will allow the remainder of the test to complete.

#   Oxygen sensor test

The oxygen sensor test will check the on-board oxygen sensor accuracy. The system will provide air to the sensor for 20 seconds and report the O2 content as read by the un-calibrated O2 sensor. If the O2 content falls outside the limits set by the test, the test will fail. Click OK to acknowledge the failure.

#   Oxygen dump test (tests the O2 switch, O2 valve and alarm)

This test checks the operation of the emergency oxygen dump switch and the valve that provides the flow of 100% oxygen. The operator will be prompted in this test to activate and de-activate the dump switch. Pay close attention to the prompts. After the switch is tested, the system will verify the operation of the DUMP valve by verifying that the O2 sensor reads 100% O2. Finally, the test will sound the audible oxygen alarm. The operator will be prompted to press OK if the alarm is audible and FAIL if it is not.

#   Oxygen pressure switch test

This test will verify that the oxygen pressure switch works properly. The operator will be prompted to remove pressure from the oxygen port. This can be done by disconnecting the hose at the O2 cylinder. The quick connect fitting on the gas regulator has a check valve. When the hose is removed, the gas regulator is isolated. Be sure to follow the prompts carefully.

#   Pressure sensor test

This test verifies the operation of the pressure transducer that monitors the pressure supplied to the pilot’s mask. The transducer is a 0 to 5 VDC bi-directional sensor which monitors +/
- 20” H2O. The test monitors the pressure sensor at 0” H2O at which the sensor should provide 2.5 VDC.

ROBD2 USER’S GUIDE 13 MAY 2010

- --
#   POWER UP AND SELF-TESTS

#   Pulse Oximeter test

This test verifies that the embedded micro controller of the ROBD2 can communicate with the integrated pulse oximeter. The pulse oximeter has its own built in self-test which runs upon power up. If the pulse oximeter self test fails, the embedded micro-controller of the ROBD2 will not be able to communicate. If the communication link fails, the pulse oximeter self-test displays the failure.

#   Air MFC shutdown test

This test confirms the operation of a safety feature to shut the system down in the event of low input air pressure. The air MFC has an alarm signal that activates if the internal MFC valve opens to maximum capacity. This generally indicates that there is not enough pressure on the MFC to satisfy the required flow rate. This would lead to elevated N2 levels in the breathing loop during normal operation. This feature uses the MFC alarm signal to stop flow and provide 100% oxygen to the breathing loop. The operator must follow the prompts to disconnect and reconnect the air source to confirm the passage of test.

ROBD2 USER’S GUIDE                                           14                         MAY 2010

- --
#   POWER UP AND SELF-TESTS

#   Self Calibration Operations

Before running programs, the system must run through its self calibration routine at the start of each operating day, and every time the system is powered on. These tests will run automatically after the system has warmed up for 10 minutes. If this process is not run, the system will not allow the operator to enter the START mode. At any time after the system has run the automatic self test function, individual self tests or self calibration routines can be run individually from the OPTION menu. To run the self-calibration sequence, select the self calibration menu item from the OPTION menu. Depending upon the gas source being used, the self-calibration process will vary. Either way, no operator interface is required during each self calibration routine.

#   Oxygen sensor calibration

The oxygen sensor calibration is run automatically from the SELFTST key, or can be run separately by selecting CAL O2 SENSOR from the OPTION – SELF CALIBRATE menu.

To calibrate the oxygen sensor, first air is delivered to the oxygen sensor. The O2 content of air is known to be 20.947. The following will be displayed:

|ANALYZING AIR O2|ANALYZING AIR O2|
|---|
|O2 SENSOR CAL|10 REMAINING TIME|
|ACTUAL O2 PERCENT AS READ BY O2 SENSOR|MEASURING O2 AIR|
|O2 = 20.9%|V = .830|
|CANCEL|CANCEL|
|DC VOLTAGE PRODUCED BY O2 SENSOR|DC VOLTAGE PRODUCED BY O2 SENSOR|

ROBD2 USER’S GUIDE 15 MAY 2010

- --
#   POWER UP AND SELF-TESTS

Once the system has calibrated the sensor for air, it will proceed to supplying 100% O2 to the sensor. The following will be displayed:

#   ANALYZING 100% O2

|ACTUAL O2 PERCENT AS READ BY O2 SENSOR|O2 SENSOR CAL|10|REMAINING TIME|
|---|---|---|---|
|MEASURING O2 100%|O2 = 99.5%|V = 3.803|CANCEL|
|DC VOLTAGE PRODUCED BY O2 SENSOR|DC VOLTAGE PRODUCED BY O2 SENSOR|DC VOLTAGE PRODUCED BY O2 SENSOR|DC VOLTAGE PRODUCED BY O2 SENSOR|

Once the sensor has calibrated to 100% O2, the calibration will display complete and automatically move on to the next calibration routine. If any failures occur during this test, refer to the troubleshooting section in the Programming and Technical Guide.

Pressing CANCEL during the process will terminate the calibration process and the new calibration data will not be stored.

#   N2 source calibration

If high pressure gas cylinders are being used for the nitrogen and air sources, then this self-calibration routine will not run. This routine is only run if the NAG is being used. Because of the inefficiency of any filter, some oxygen will be present in the nitrogen source (typically less than 2%). The system will determine the oxygen content during this routine. The amount of oxygen present in the N2 source will be compensated for by adjusting the gas mixture ratio in the pilot test mode. With high pressure cylinders, the amount of oxygen in the nitrogen source is negligible. The routine will monitor the nitrogen source from the NAG for 1 minute. It then stores the value and uses it in other operating modes. From the OPTION menu, select CAL N2 SOURCE. During this calibration, the following will be displayed:

#   ANALYZING N2 SOURCE CONTENT

|N2 SOURCE CAL|MEASURING N2….|N2 = 99.5%|27|REMAINING TIME|
|---|---|---|---|---|
|CANCEL|CANCEL|CANCEL|CANCEL| | | | |

If the content of nitrogen is less than 97.5%, a warning will be shown.

ROBD2 USER’S GUIDE 16 MAY 2010

- --
#   POWER UP AND SELF-TESTS

#   Test altitudes

This routine checks the accuracy of the blending system and the oxygen sensor by running air and nitrogen blends that span the full range of the MFCs. Three altitudes are tested; 5000 feet, 20000 feet and 34000 feet. From the OPTION menu, select TEST ALTITUDES. The following information will be displayed during the testing of each altitude:

|ALTITUDE BEING TESTED|TESTING ALTITUDES|EXPECTED 02 VALUE|
|---|---|---|
|ALT:20000|02: 9.09|MEASURING 02…|

The following information will be displayed after each altitude is tested:

|ALTITUDE BEING TESTED|TESTING ALTITUDES|EXPECTED 02 VALUE|
|---|---|---|
|ALT:20000|02: 9.09|02=9.10|
|RESULT|PASSED|MEASURED 02 VALUE|

ROBD2 USER’S GUIDE 17 MAY 2010

- --
#   SYSTEM OPERATION

#   Entering data

At various times during system operation the operator is required to enter data into the system.

Entry of numeric data is performed by using the numeric keypad. Press the number key(s) representing the desired data values and press ENTER to record the data in the appropriate field. If the numbers entered completely fill the field, the value is automatically accepted and the ENTER key is not required. Pressing an arrow key will also complete the entry and move the cursor to another field. The system automatically adds a decimal point followed by zeros to fill the rest of the field, if required.

For fields requiring alphanumeric data to be entered, the arrow keys may also be used to input data. The following listing shows the order of the alphanumeric and punctuation symbols that can be accessed by pressing the up and down arrow keys:

ABCDEFGHIJKLM NOPQRSTUVWXYZ0123456789.+-/()%# 

Note that the digits 0 – 9 and . can also be entered directly by pressing the corresponding key on the numeric keypad.

To enter alphanumeric data, press the up/down arrow until the desired character is displayed. Then press the ENTER key, or use the left/right arrow keys to position the cursor in the desired location.

The SPACE function key is used to enter a blank space.

The CLEAR function key will clear all data entered.

The ENTER function key will complete the entry of data.

ROBD2 USER’S GUIDE 18 MAY 2010

- --
#   SYSTEM OPERATION

#   Main Screen 
- Ready mode

The ROBD2 was designed with emphasis on simplicity and ease of operation. The system’s menu-driven software guides the operator through all operating routines. The following menu items are available to the user.

|(DAY)|(DATE)|(TIME)|
|---|---|---|
|ENVIRONICS ROBD2|ENVIRONICS ROBD2|ENVIRONICS ROBD2|
|READY|READY|READY|
|START|SELFTST|OPTION|

#   START

The START key is used to enter the Pilot Test mode. The Pilot Test mode is where all pilot testing takes place. The START key is disabled until the warmup time has elapsed, and all self test and calibration operations have completed successfully.

#   SELFTST

The SELFTST key runs the system self test and calibration operations. These operations must be run before the START key can be used to enter the Pilot Test mode. The menu selection disappears after the Self test process has run. Self test and self calibration routines can be run individually or together from the OPTION menu.

#   OPTION

The OPTION key is used to enter the OPTION menu, which is used to set various system options, display self test results and run self test and self calibration. Also, the OPTION menu is used to set time and date, adjust display contrast and view software revision and system serial number.

ROBD2 USER’S GUIDE 19 MAY 2010

- --
#   SYSTEM OPERATION

#   START – Pilot Test mode

#   PILOT TEST MENU

- RUNPRG

- PPT

- EXIT

Standby status in Pilot Test mode

Once in this menu, the operator can select to run a program or the PPT mode.

#   PPT – Positive Pressure Training mode

The Positive Pressure training mode provides high flow and high pressure to the pilot’s mask. This mode supplies air at 95 LPM and a pressure of 10” H0.2. When first entering the PPT mode, the nominal flow rate of standby air is delivered to the mask at 14 LPM. When the START key is pressed, flow and pressure are increased to 95 LPM at a pressure of 10” H0.2. Press the STOP key to return to standby flow and pressure.

The oxygen content and breathing loop pressure (BLP) is displayed on the screen while in the PPT mode.

ROBD2 USER’S GUIDE 20 MAY 2010

- --
#   SYSTEM OPERATION

#   RUNPRG – Running a test program

The RUNPRG mode is used to conveniently recall one of 20 saved programs with up to 99 steps of altitude changes. The program must be setup prior to using the RUN mode (refer to the PROGRAM mode section of the technical manual). When entering the RUNPRG mode, the following screen will appear (Note: program names shown are for example purposes only).

|# |NAME|TYPE|
|---|---|---|
|&gt; 1|BASIC HYPOXIA|HRT|
|2|SIMULATOR|FSHT|
|SELECT| |EXIT|

Using the up and down arrow keys, select the program to run. The highlighted program will have the greater than sign to the left of the program number. NOTE: this mode requires instrument pre-programming. This programming information is in the Programming and technical manual. The following information will be seen in two separate screens. By pressing the MENU key and VIEW, the screens can be toggled.

#   RUNPRG SCREEN 1

|PROGRAM STEP INFO|CHG|34000|@|30000 F/M|
|---|---|---|---|---|
|CURRENT ALTITUDE|ALT = 25000|Elp|=|30 S|
|ELAPSED TIME|ACTUAL 02 PERCENT|02|=|7.11%|
|AS READ BY 02 SENSOR| |Rmn|=|38 S|
|BLP|=|1.30|BREATHING LOOP|PRESSURE “H2O|

#   RUNPRG SCREEN 2

|PROGRAM STEP|CHG|34000|@|30000 F/M|
|---|---|---|---|---|
|CURRENT ALTITUDE|25000| | | |
|ACTUAL 02 PERCENT|7.11%| | | |
|REMAINING TIME|38| | | |

#   TREND BARS

SET ALTITUDE BAR

34000 FEET MAX AS SHOWN

#   CURRENT ALTITUDE BAR

- --
#   SYSTEM OPERATION

#   RUNPRG EXAMPLE

1. HOLD AT 34000 FEET FOR 2 MINUTES
2. CHANGE TO 0 FEET AT 18000 FT/MIN
3. HOLD AT 0 FEET FOR 1 MINUTE
4. CHANGE TO 20000 FEET AT 30000 FT/MIN
5. END OF PROGRAM

#   STEP 1: SCREEN 1

|HLD|34000|FOR|2 MIN| | |
|---|---|---|---|---|---|
|ALT = 34000|Elp = 50S|34000| | | |
|02 = 4.4%|Rmn = 70S| |4.40%| | |
| |BLP = 1.35|70| | | |

#   STEP 2: SCREEN 1

|CHG|0|@|18000 F/M| |
|---|---|---|---|---|
|ALT = 34000|Elp = 20 S|34000| | |
|02 = 4.37%|Rmn = 113 S|4.37%| | |
| |BLP = 1.20|113| | |

#   STEP 3: SCREEN 1

|HLD|0|FOR|1 MIN|
|---|---|---|---|
|ALT = 0|Elp = 10S|0| |
|02 = 21.2%|Rmn = 50S|21.2%| |
| |BLP = 1.25|50| |

#   STEP 4: SCREEN 1

|CHG|20000|@|30000 F/M|
|---|---|---|---|
|ALT = 13000|Elp = 26S|13000| |
|02 = 12.42%|Rmn = 14S|12.42%| |
| |BLP = 1.42|14| |

ROBD2 USER’S GUIDE 22 MAY 2010

- --
#   SYSTEM OPERATION

While in the RUNPRG mode, pressing the STOP key will abort the program.

Pressing the ADVANCE key while in the run mode will advance the program to the next step, regardless of how much time remains in the current step.

Pressing the 02 DUMP switch will cause the program to shut down and the system will supply 100% 02 to the SUT. O2 will continue to flow until the dump switch is disengaged by turning it clockwise.

Pressing the MENU key while in the run mode will toggle the screens back and forth between the two run mode display screens. One screen contains the bar graph representation of desired altitude, actual altitude and a running trend of altitude. The other display screen gives more detailed information, including breathing loop pressure, elapsed step time, remaining step time, actual 02 content as read by the onboard oxygen sensor, desired altitude, current altitude and the actual program step information.

#   Manual altitude override

While in the RUNPRG mode, you can manually override a program step and go directly to any desired altitude. Entering a manual altitude will pause the current program and ascend or descend to the new altitude entered.

To enable manual altitude control while running a program, press the MENU key, then select MANUAL. Enter the new altitude and press ENTER.

You can enter new altitude values as often as desired. You can also increase or decrease the current altitude in increments of 1000 ft., but pressing the up or down arrow keys.

To resume the program from where it was interrupted, press EXIT.

ROBD2 USER’S GUIDE 23 MAY 2010

- --
#   SYSTEM OPERATION

#   Option menu

The OPTION menu is used to run self-test and self-calibration functions, and to change various system settings.

Pressing the OPTION key will bring up the following display.

> TEST RESULTS
SELF TEST
SELF CALIBRATE
EXIT

The OPTION menu contains a menu with the following items:

TEST RESULTS
SELF TEST
SELF CALIBRATE
GAS SOURCE
O2 DUMP PRESSURE
ADMIN MODE
SET TIME/DATE
ADJUST CONTRAST
SYSTEM INFO

Select the desired function by using the arrow keys, then press ENTER.

ROBD2 USER’S GUIDE                                   24                          MAY 2010

- --
#   SYSTEM OPERATION

#   TEST RESULTS

The Test Results function displays the results of all Self Test and Self Calibrate functions. The test item is listed on the left, with the result shown on the right. Below is a sample test result display:

|TEST RESULTS| |
|---|---|
|MFCS|
- OK|
|PULSE OXIM|
- OK|
|O2 DUMP VALVE|
- OK|
|O2 DUMP SWITCH|
- FAIL|
|O2 DUMP ALARM|
- OK|
|O2 PRESS SW|
- OK|
|O2 SENSOR|
- OK|
|PRESS SENSOR|
- OK|
|O2 SENSOR CAL|
- SKIP|
|N2 SOURCE CAL|
- SKIP|
|ALTITUDE TEST|
- SKIP|
|AIR MFC SHUTDN|
- FAIL|

"OK" indicates that the test has been run and completed successfully.

"FAIL" indicates that the test has been run but has failed.

"SKIP" indicates that the test has been skipped and has not yet been run.

The software will not allow access to the PILOT TEST menu until all tests show "OK".

Press the EXIT key to return to the OPTION menu.

#   SELF TEST

The Self Test function allows various self tests to be run, either all at once or individually. The available menu items are shown below.

TEST ALLTEST MFCSTEST O2 SENSORTEST O2 DUMPTEST O2 PRESS SWTEST PRESS SENSORTEST PULSE OX.TEST MFC SHUTDOWN

To run all Self Tests, position the cursor on TEST ALL and press ENTER. For each self test, the software will ask you to confirm that you want to run the test. Select YES to run the test, or NO to skip to the next test.

ROBD2 USER’S GUIDE 25 MAY 2010

- --
#   SYSTEM OPERATION

To run an individual self test, position the cursor on the desired test and press ENTER.

While a test is running, you may be prompted to perform various actions. Be sure to follow the prompts carefully, otherwise the test may fail. In the event that a test fails, you will be prompted with "TEST FAILED. REPEAT TEST?". Press YES to rerun the test, otherwise press NO.

#   SELF CALIBRATE

The Self Calibrate function allows various self calibration checks to be run, either all at once or individually. The available menu items are shown below.

CAL ALLCAL O2 SENSORCAL N2 SOURCETEST ALTITUDES
To run all Self Calibrations, position the cursor on CAL ALL and press ENTER. For each test, the software will ask you to confirm that you want to run the test. Select YES to run the test, or NO to skip to the next test.

To run an individual test, position the cursor on the desired test and press ENTER.

While a test is running, you may be prompted to perform various actions. Be sure to follow the prompts carefully, otherwise the test may fail. In the event that a test fails, you will be prompted with "TEST FAILED. REPEAT TEST?". Press YES to rerun the test, otherwise press NO.

#   GAS SOURCE

The GAS SOURCE function is used to select the source for gases to the ROBD2. This can be either high pressure gas cylinders, or the NAG.

When using gas cylinders, select CYL. This will set the N2 source gas concentration to 100%.

When using the NAG, select NAG. This tells the system that the N2 Source calibration needs to be run during the Self Calibration process. N2 source calibration measures the O2 content of the nitrogen gas source to determine the concentration of nitrogen in the gas.

It is very important to select the correct gas source, otherwise significant O2 concentration errors may result.

ROBD2 USER’S GUIDE 26 MAY 2010

- --
#   SYSTEM OPERATION

#   O2 DUMP PRESSURE

The O2 Dump Pressure setting determines whether or not the subject under test receives pressurized O2 during an O2 dump cycle.

When ENABLED, the SUT will receive pressurized O2 during an O2 dump cycle. This is the default setting. When DISABLED, the breathing loop pressurization solenoid will remain open, and the SUT will receive unpressurized O2 during an O2 dump cycle.

Press the TOGGLE key to toggle the setting between ENABLED and DISABLED. After selecting the desired setting, press EXIT to return to the previous menu. The selected setting will be retained in memory even after power to the ROBD system has been turned off.

#   ADMIN MODE

The ADMINinstrator MODE allows access to Administrator level functions, which include programming of test routines (PROG mode) and system functions (SYSTEM mode) such as MFC calibration.

To enter ADMIN mode, select ADMIN MODE from the menu and press ENTER. If there is an Administrator password, you will be prompted to enter it. If there is no password, the system will automatically switch to ADMIN mode.

To exit ADMIN mode, select ADMIN MODE from the menu, and press ENTER. The system will disable administrator mode, regardless of any password setting. When the system is in Admin mode, "ADMIN" will be displayed on the main menu screen.

#   SET TIME/DATE

The SET TIME/DATE function allows you to set the Time and Date displayed on LCD screen. Three fields to display the day, date and time will appear.

With the left/right arrow keys, move the cursor to the desired date or time field to be changed and press the up and down arrow keys to set the correct time and/or date. Note: the day of the week is calculated by the system automatically.

When the correct time and date are entered, press the EXIT function key to return to the OPTION menu.

ROBD2 USER’S GUIDE 27 MAY 2010

- --
#   SYSTEM OPERATION

#   ADJUST CONTRAST

The contrast of the LCD display is affected somewhat by the angle at which the display is viewed as well as the ambient temperature. To adjust the contrast for optimum results:

1. Using the up and down arrow keys, move the pointer cursor down to the line that reads ADJUST CONTRAST and press the ENTER key. The following screen appears:

ADJUST CONTRASTCONTRAST = 100K/L TO CHANGEDONE

Press the up arrow to increase the contrast on the screen. When increasing the contrast, the contrast number will increase to a maximum 100. Use the down arrow to decrease the contrast on the screen. When decreasing the contrast, the contrast number will decrease to a minimum value of 0. The numerical value is shown for reference since the user may not detect a change in contrast on the screen. The contrast value will change in increments of five.
After reaching the desired contrast setting, press DONE to return to the OPTION menu.

#   SYSTEM INFO

Selecting System Info will bring up a display of the system model number, serial number and software version.

ROBD2 USER’S GUIDE 28 MAY 2010

- --
#   SAFETY FEATURES

There are a number of built-in safety features to either alert the operator or stop the operation of the system and go to a “safe” mode of operation.

#   Oxygen dump switch

An emergency Oxygen Dump switch has been provided to supply 100% oxygen on demand as the subject under test (SUT) becomes hypoxic. The emergency switch is activated by depressing it, which starts the flow of oxygen. Once the SUT has recovered as determined by pulse oximeter analysis, turning the switch clockwise will stop the flow of 100% O2.

When the O2 dump switch is pressed, the following screen appears, assuming a program is running. Data displayed will be dependent upon altitude:

= = = T E S T A B O R T E D = = =
A LT = 2 80 00               El p= 4S
O X Y G E N D U M P P R ES S E D
DELIVERING 100% O2

The concentration of oxygen read by the internal O2 sensor will be displayed. If the concentration of oxygen is not above 90% within 5 seconds, an internal alarm will sound. Also, if the concentration of O2 drops below 90% after 5 seconds, the alarm will sound. The alarm is deactivated at the time the O2 dump switch is disengaged and the system will go into standby status in the pilot Test Menu.

#   Oxygen pressure switch

The oxygen pressure switch monitors the input pressure on the oxygen port. This prevents operation of the system if there is insufficient pressure to supply enough O2 to the SUT when the O2 Dump Switch is activated.

This pressure should normally be set between 15 and 20 PSIG. If this pressure is less than 10 PSIG, the system will not allow any Pilot Test operations. If Low O2 Pressure is detected in the Ready mode, the system will display LOW O2 instead of READY, on the screen.

ROBD2 USER’S GUIDE 29 MAY 2010

- --
#   SAFETY FEATURES

In the Pilot Test Menu, if any of the Pilot Test keys (RUNPRG or PPT) are pressed during a Low O2 Pressure condition, the system will display the following screen and prevent the system from running in the Pilot Test Menu.

|PILOT TEST MENU|PILOT TEST MENU|PILOT TEST MENU|
|---|
|*LOW 02 PRESSURE*|*LOW 02 PRESSURE*|*LOW 02 PRESSURE*|
|*CANNOT RUN TEST*|*CANNOT RUN TEST*|*CANNOT RUN TEST*|
|RUNPRG|PPT|EXIT|

The system will once again function when pressure is restored above 12 PSIG.

#   Oxygen alarm

The O2 alarm will sound for two different scenarios. The 02 alarm is only active for the O2 dump feature. After pressing the emergency oxygen dump switch, if the 02 has not reached 90% in 5 seconds, the alarm sounds. The alarm will remain active until the emergency switch is turned off. Also, if during an O2 dump, the oxygen content drops below 90%, the alarm will sound.

#   Oxygen analysis

Using the onboard oxygen sensor, if the oxygen content in any pilot test mode drops below 3.8%, the system will automatically turn on the oxygen dump and display a warning message.

#   Overpressure detect

Using the onboard pressure sensor, if the pressure to the mask rises above 20” H0,2 the system will turn on the oxygen dump and open the bypass valve, bringing the breathing loop pressure down to zero.

#   Pressure relief valve

As a back up to the over pressure detect, this mechanical pressure relief valve prevents the pilot’s mask from exceeding 27” H0 or 1 PSIG.

#   Low air flow detect

The Air MFC (MFC1) has an alarm signal that activates if the internal MFC valve opens to maximum capacity. This generally indicates that there is not enough pressure on the MFC to satisfy the required flow rate. This would lead to elevated N2 levels in the breathing loop during normal operation. This feature uses the MFC alarm signal to stop flow and provide 100% oxygen to the breathing loop. A message appears indicating the failure.

ROBD2 USER’S GUIDE 30 MAY 2010

- --
#   PULSE OXIMETER

#   SpO2 and Pulse Rate Displays

The measured SpO2 will appear in the display at the upper left of the front panel, the pulse rate in the display at the lower left. The oximeter ensures that only valid pulsatile signals are processed. Bad or invalid data causes alerts to occur and may also cause the displays to show “
- 
- -” and “
- 
- -” in the SpO2 and pulse rate displays respectively.

SpO2 display

Pulse Bar 888

Pulse Display

The displays are updated once per second as the monitor is acquiring data. If the monitor cannot detect a regular and rhythmic pulsatile signal for periods longer than 45 seconds, the display will blank out and “
- 
- -” will be displayed in the SpO2 and Pulse rate displays. If the signal should return and regular and rhythmic pulsatile data is detected, the display will update with the new values. When the oximeter detects a pulsatile signal that is too low to be processed, after previously receiving an acceptable signal and displaying data, the icon will illuminate. This indicates that the SpO2 and pulse rate data has been held since the last acceptable signal. If an acceptable signal is not detected within 30 seconds, dashes will be displayed, the icon will flash, and the appropriate status code will appear. When the monitor is not detecting a valid signal, the display will react to the condition that exists. If the monitor is operating normally and no probe is connected, or if a probe is connected but not attached to a subject, the displays will show dashes “
- 
- -” and the icon will also flash.

ROBD2 USER’S GUIDE 31 MAY 2010

- --
#   PULSE OXIMETER

#   Pulse Activity Bar

The signal bar or pulse activity bar is derived from the pulsatile signal that is measured by the monitor. The height of the bar with each pulse beat is proportional to the strength of the signal for low to medium signals, and is adjusted to fit the graph for large signals. This pulse activity bar represents the subject’s pulse and should show regular rhythmic movement. Erratic or non-rhythmic movement may indicate a poorly positioned or applied sensor, or may be indicative of excessive subject movement at the sensor site.

#   SpO2 and Pulse Rate Alerts

#   Alert Limit Violations

When the oximeter detects SpO2 or pulse rate values that exceed either the high or low limits, both an audible alert tone and visual alerts are generated. The audible alert volume can be adjusted, or an alert can be muted for two minutes or disabled (see “Muting the alert”). The visual alerts are the limit arrows (high or low), and the out-of-range numeric value. A limit arrow, either high or low, will flash in the violated parameter window, either SpO2 or pulse rate. The numeric value, which is out-of-range, will also flash. If the alert condition no longer exists, the alerts will stop, however the limit arrow will flash until acknowledged (by pressing the alert reset key).

#   High Low indicators

1

ROBD2 USER’S GUIDE 32 MAY 2010

- --
#   PULSE OXIMETER

#   Setting SpO2 alarm alert limits

Press the key once for setting the upper alert limit:

To advance to setting the lower alert limit without adjusting the upper limit, proceed to step 4.

The SpO2 display will show the currently set upper alert limit.

The indicator in the SpO2 display area will illuminate red indicating that the upper alert limit can be adjusted. The SpO2 upper alert limit can be adjusted from 100-55.

Press the key to increase the alert limit; or key to decrease the alert limit.

Press the key again for setting the lower alert limit.

The indicator in the SpO2 display area will illuminate red indicating that the lower alert limit can be adjusted. The SpO2 low alert limit can be adjusted from 95-50.

Press the key to increase the alert limit; or key to decrease the alert limit.

Press the key again to exit the alert limits mode, or the monitor will automatically return to normal display mode after ten seconds.

#   Setting pulse rate alarm limits

Press the key once for setting the upper alert limit:

To advance to setting the lower alert limit without adjusting the upper limit, proceed to step 4.

The pulse rate display will show the currently set upper alert limit.

Press the key to increase the alert limit; or key to decrease the alert limit.

The indicator in the pulse rate display area will illuminate red indicating that the upper alert limit can be adjusted. The Pulse Rate upper alert limit can be adjusted from 250-35.

Press the key again for setting the lower alert limit:

The indicator in the pulse rate display area will illuminate red indicating that the lower alert limit can be adjusted. The Pulse rate lower alert limit can be adjusted from 245-30.

Press the key to increase the alert limit; or key to decrease the alert limit.

Press the key again to exit the alert limits mode, or the monitor will automatically return to normal display mode after ten seconds.

ROBD2 USER’S GUIDE 33 MAY 2010

- --
#   PULSE OXIMETER

#   Muting the alert

To mute the audible alert for two minutes:

Press the key:

The icon flashes yellow and any audible alerts sounding are muted:

To cancel two minute mute:

Press the key:

The icon is off. Any alerts that are active will sound an alarm tone.

To disable alert audio:

Press and hold the key until the icon illuminates, approximately three seconds.

To enable alert volume:

Press the key; and the icon will turn off.

#   Adjusting the alert volume

Press the key to display the current alert volume level.

The SpOz window will display "ALr" (for alert), and the pulse window will display the alert volume level that is currently selected.

Press key to increase or key to decrease the alert volume level. Each time the key or key is pressed, a short sample tone will sound at the new volume level. The sample tones will not occur if the audible alert is disabled (4 illuminated).

The Model 515B will return to normal display mode ten seconds after the last key or key press, or sooner by pressing the key or key:

The new value will remain in effect even after the monitor is turned off. This parameter is stored in battery-backed memory and will be reset to default value if the monitor is reset to factory defaults. See "Resetting to Factory Defaults" on page 19.

NOTE: If the key and key are pressed while the monitor is sounding an alert; they will only set the alert volume. Pulse volume cannot be adjusted when the monitor is alerting.

ROBD2 USER’S GUIDE 34 MAY 2010

- --
#   PULSE OXIMETER

#   Pulse beep volume control

To adjust the pulse beep volume:

Press the key to display the current pulse volume level:

The SpOz window will display PUL (for pulse), and the pulse window will display the pulse volume level that is currently selected.

Press to increase or to decrease the pulse volume level. Each time the or key is pressed, a short sample tone will sound at the current volume level. The sample tones will not occur if the audible alert is disabled illuminated.

The Model 515B will return to normal display mode ten seconds after the last oximeter or key press; or sooner by pressing the E0 or keys.

The new value will remain in effect even after the monitor is turned off: This parameter is stored in battery-backed memory and will be reset to the default value if the monitor is reset to factory defaults. See Resetting to Factory Defaults on page 19.

NOTE: If the ad keys are pressed while the monitor is sounding an alert, they will only set the alert volume. Pulse volume cannot be adjusted when the monitor is alerting:

ROBD2 USER’S GUIDE 35 MAY 2010

- --
#   PULSE OXIMETER

#   Figure 4 
- P&ID

#   ROBD2 USER’S GUIDE

36  MAY 2010