#   REMOTE COMMUNICATIONS

The system has a remote communications port, which allows it to be controlled remotely by a host computer. The host computer communicates with the system through the RS232 port located on the rear panel.

The system will respond to commands issued by the host computer, but will not issue any unsolicited messages to the host, except to acknowledge a command or to return an error code.

#   Interface Specification

The communication interface is a standard RS-232C serial interface, connected via a Male DB-9 connector. The system operates as a DTE (Data Terminal Equipment) device, requiring a null modem cable to connect to a PC.

#   Communication port parameters are:

- 1 Start bit

- 8 data bits

- 1 Stop bit

- No parity bit

The speed of the communications port is fixed at 9600 baud.

#   Data Format

All remote communications use standard ASCII characters. Commands are terminated with either (or both) of these single byte ASCII codes:

- &lt;CR&gt; Carriage Return (ASCII Code 0x0D) 
- This is used to indicate the end of a command.

- &lt;LF&gt; Linefeed (ASCII Code 0x0A) 
- This is used to indicate the end of a command.

#   Command Format

Commands sent to the system must be formatted as follows:

COMMAND FORMAT: COMMAND &lt;CR&gt;&lt;LF&gt;

The system recognizes the end of the command when it sees a &lt;CR&gt; and/or &lt;LF&gt; character. Commands are not case sensitive.

For each command sent, be sure to wait for a valid response from the system before sending a new command.

- --
#   Reply Format

All replies from the system to the host computer will be formatted with one of three formats shown, depending on the type of response required.

#   COMMAND ACCEPTED

If the command received requires no data to be returned, the system will acknowledge that it successfully received and performed the command. This will be indicated by:

RESPONSE:                OK<CR><LF>

#   DATA RETURNED

For commands that require data to be returned, the data will be formatted as follows. If the data consists of a list of values, each value will be separated with a comma.

RESPONSE:                data<CR><LF>
EXAMPLE:                 5000.0<CR><LF>

#   ERROR RETURNED

If the command received contains errors, or cannot be performed by the system, an error code will be returned. The error message is formatted as:

RESPONSE:                ERR(error code)<CR><LF>
EXAMPLE:                 ERR12<CR><LF>

#   Format Of Numeric Data

All numerical values for physical parameters such as Altitude, Pressure, etc. are formatted as floating point values. These values are indicated by the format "x.xxx"

Whole number values (for specifying program step, etc.) must be specified without a decimal point. These values are indicated by the format "n"

- --
#   Remote Command List

#   ROBD2 PROGRAMMING COMMANDS

These commands are used to set up and review the ROBD2 program steps. A total of 20 programs can be created, each with up to 99 steps.

|COMMAND|DESCRIPTION|
|---|---|
|PROG n NAME progname|Assign program name|
|PROG n NAME ?|Get name of program|

Command parameters:

- n = Program #  (1-20)

- progname = Name of program (10 characters max.)

|PROG n s mode alt value|Create a program step.|
|---|---|
|PROG n s ?|Display program step parameters.|

Data is returned as: mode alt value

Command parameters:

- n = Program #  (1-20)

- s = Step #  (1-98) (Step 99 is always END and cannot be changed)

- mode = HLD (hold), CHG (change), or END (end of program)

- alt = Target Altitude (in feet)

- value = Hold Time (in minutes) for a HLD step, -or
- Rate Of Change (in ft/min) for CHG step.

- --
#   ROBD2 OPERATING COMMANDS

These commands are used to control the ROBD2.

|COMMAND|DESCRIPTION|
|---|---|
|RUN READY|Enter PILOT TEST mode Put software into the Pilot Test mode. Equivalent to pushing START from the Main Menu.|
|RUN EXIT|Exit PILOT TEST mode Exit from the Pilot Test mode. Equivalent to pushing EXIT from the Pilot Test Menu.|
|The following RUN commands require the software to be in the Pilot Test mode|The following RUN commands require the software to be in the Pilot Test mode|
|RUN n|Run the specified program n = program #  to run (from 1 to 20)|
|RUN NEXT|Advance to next program step While running a program, this advances the program to the next step. This is equivalent to pressing the ADVANCE key from the front panel.|
|RUN ABORT|Abort current test Abort the current program or test, and return to the Pilot Test menu.|
|SET O2DUMP n|Set the Oxygen Dump state. n=1, turns the Oxygen Dump ON n=0, turns the Oxygen Dump OFF. This command has the same effect as pressing/releasing the O 2 Dump switch on the front panel.|
|RUN O2FAIL|Activate O2 Failure condition This command initiates an O2 FAIL operation. This is equivalent to pressing the O2FAIL button while a program is running. Refer to the RUN PROGRAM section of the manual for more information.|

- --
#   ROBD2 STATUS COMMANDS

These commands are used to get ROBD2 status information.

NOTE: SpO2 and Pulse data is valid only after entering PILOT TEST MODE. Altitude and Elapsed/Remaining Time are valid only while running a Program.

|COMMAND|DESCRIPTION|
|---|---|
|GET RUN O2CONC|Get the O2 Concentration in the breathing loop|
|GET RUN BLPRESS|Get the Breathing Loop Pressure|
|GET RUN SPO2|Get SpO2 reading from Pulse Oximeter|
|GET RUN PULSE|Get Pulse reading from Pulse Oximeter|
|GET RUN ALT|Get the Current Altitude for the current step|
|GET RUN FINALALT|Get the Final Altitude for the current step|
|GET RUN ELTIME|Get the Elapsed Time of the current step|
|GET RUN REMTIME|Get the Remaining Time for the current step|
|GET RUN ALL|Get all run data. Data format is: mm-dd-yy hh-mm-ss, program# , current alt, final alt, o2conc, breathing loop pressure, elapsed time, remaining time, spo2, pulse<cr><lf>|
|GET INFO|Returns the system model number, software revision and serial number|
|GET MFC n|Get the current flow rate for MFC n|
|GET ADC n|Get the voltage for ADC device n|
|GET O2 STATUS|Get the 100% O2 source status. Returns "1" if the 100% O2 source pressure is OK. Returns "0" if the 100% O2 source pressure is LOW.|
|GET STATUS|Returns a 1 if system is not ready (warmup time not expired, low O2 pressure, or self tests not completed). Returns a 0 if system is ready.|

- --
#   FLIGHT SIMULATOR COMMANDS

These commands are used to put the ROBD2 into Flight Simulator Tracking mode. In this mode, the screen will display FLIGHT SIM TRACKING, and the current altitude, O2 concentration, and breathing loop pressure. No keyboard commands are accepted. This mode is intended to be controlled directly by Flight Simulator software.

|COMMAND|DESCRIPTION|
|---|---|
|RUN FLSIM|Puts the system into Flight Simulator Tracking mode. The "RUN READY" command must be sent before RUN FLSIM. To exit from this mode, use the "RUN ABORT" command.|
|SET FSALT nnnnn|Sets the Flight Sim Altitude to nnnnn feet. Altitude value must be &lt;= 34000. NOTE: Sending too many SET FSALT commands will return an ERR99, which means the command buffer for the flight simulator mode has overflowed. The software will store the last 5 altitude commands, but it updates the MFCs only once per second, so sending this command more frequently than once per second should be avoided.|

When in the Flight Simulator mode, the GET RUN ALL command behaves slightly differently:

- Program #  will be 99, to indicate Flight Sim mode.

- Elapsed time will reset to 0 each time a new SET FSALT command is received.

- Remain time will always be 1 second.

- --
#   CURRENT PAGE RAW OCR TEXT

#   DIRECT GAS CONTROL COMMANDS

These commands allow the gas concentration and flow rate of gas to be directly controlled. These commands should not be used while a program is running, or when in Flight Simulator mode.

|COMMAND|DESCRIPTION|
|---|---|
|RUN GAS xx.xx yyyyy|Causes the specified concentration of O2 (xx.xx%) to flow at the specified flow rate of yyyyy ccm The concentration specified must be &lt; 20.94%, unless the system is equipped for hyperoxia operation. To stop gas from flowing, use the command RUN GAS 0 0|
|RUN AIR yyyyy|Causes air to flow at the specified flow rate of yyyyy ccm Acceptable values are from 4000 to 80000 ccm. To stop air from flowing, use the command RUN AIR 0|

- --
#   CONFIGURATION COMMANDS

These commands change/read the configuration and operating parameters of the system. These commands should not be used while a program is running, or when in Flight Simulator mode.

|COMMAND|DESCRIPTION|
|---|---|
|SET MASKFLOW xxxxx|Sets the flow rate of gas delivered to the mask, in units of cc/min. Flow rate must be in the range of 40000-80000 ccm. This command is equivalent to changing the FLOW RATE in the OPTION 
- ROBD CONFIG menu.|
|GET MASKFLOW|Returns the mask flow rate setting, in units of cc/min.|
|SET O2FAILFLOW xxxxx|Sets the flow rate value to be used during an O2 Failure condition, in units of cc/min. Flow rate must be in the range of 4000-80000 ccm. This command is equivalent to changing the O2FAIL FLOW in the OPTION 
- ROBD CONFIG menu.|
|GET O2FAILFLOW|Returns the O2FAIL flow rate setting, in units of cc/min.|

- --
#   Remote Command example:

The following example shows how to program and operate the ROBD2. Commands are shown first with a description of each command. The response from the ROBD2 is shown indented below each command.

PROG 1 NAME TEST001                     Assign name “TEST001” to Program 1
OK
PROG 1 1 HLD 0 1                        Prog 1, Step 1: Hold at 0 feet for 1 min.
OK
PROG 1 2 CHG 5000 5000                  Step 2: Change to 5000 feet at 5000 ft/min.
OK
PROG 1 3 HLD 5000 2                     Step 3: Hold at 5000 feet for 2 min.
OK
PROG 1 4 CHG 30000 10000                Step 4: Change to 30000 feet at 10000 ft/min.
OK
PROG 1 5 END                            Step 5: End of program.
OK
PROG 1 2 ?                              Display Prog 1, Step 2 information.
CHG 5000 5000                        > Change to 5000 ft at 5000 ft/min
GET O2 STATUS                           Get status of 100% O2 source
1                                    >  O 2 pressure is OK
RUN READY                               Enter Pilot Test mode
(required to run a program)
OK
RUN 1                                   Start running Program 1.
OK
GET RUN ALL                             Get Status information
12-31-05 17:55:49,1,0,0,21.04,3.12,3,57,99.2,68
RUN NEXT                                Advance to the next step
OK
GET RUN ALL                             Get Status information
12-31-05 17:56:05,1,975,5000,20.98,3.09,9,51,99.2,67
RUN ABORT                               Abort program
OK
RUN EXIT                                Exit Pilot Test Mode
OK

- --
#   Remote Error Codes

|ERROR|DESCRIPTION|
|---|---|
|4|COMMAND OVERFLOW The input command is too long. Commands are limited to 79 characters.|
|12|UNKNOWN COMMAND An unknown command was received.|
|18|COMMAND ERROR Specified command is recognized but does not match the required format.|
|19|TOO MANY TOKENS Command contained too many data elements to be processed.|
|53|VALUE OUT OF RANGE One of the specified values is out of range.|
|60|UNKNOWN PROGRAM STEP Unknown program step type. Must be HLD, CHG or END|
|98|SYSTEM RUNNING Command cannot be processed when system is already running|
|99|FLIGHT SIMULATOR COMMAND OVERFLOW Too many SET FSALT commands received. Do not send command faster than once per second.|