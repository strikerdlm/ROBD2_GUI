#   Environics

#   Model 6202-1

#   Reduced Oxygen Breathing Device 2

#   Administrator/ Programming mode addendum

- --
#   ADMINISTRATIVE MODE

#   (ADMIN mode)

The Administrative mode is a limited access mode and is password protected. Access to this mode allows for changing program information, calibration data, and accessing troubleshooting features. Factory set password is 1234, which can be changed in the system menu, once ADMIN mode is activated.

When the system is in the normal operator’s mode (READY screen), the only two menu items, as seen on the bottom line of the display, are START and OPTION. When the system is in the ADMIN mode, a secondary menu appears in the READY screen. The two menu selections are Program (PROG) and System. Toggle back and forth between the operator’s menu and the Admin menu by pressing the MENU key.

Each time the instrument is powered off and on, and the self-tests are run, the system automatically enters the operator’s menu. To enter the ADMIN mode, perform the following:

1. From the ready screen or operator’s menu (shown below), select OPTION (F3).

|(DAY)|(DATE)|(TIME)|
|---|---|---|
|ENVIRONICS ROBD2|READY| |
|START|OPTION| |

Arrow down to ADMIN mode and press ENTER.
Enter the 4 digit numeric password, factory default 1234. This password can be changed once in the ADMIN mode.
ENABLED and automatically. Once exited from the options menu, the display will appear in the ADMIN mode, see below.

|(DAY)|(DATE)|(TIME)|
|---|---|---|
|ENVIRONICS ROBD2|READY|ADMIN|
|START|OPTION| |

- --
#   Programming the instrument (PROG mode)

Once in the ADMIN mode, access is granted to two other menu items. Press the MENU key to display the following screen.

|(DAY)|(DATE)|(TIME)|
|---|---|---|
|ENVIRONICS ROBD2|ENVIRONICS ROBD2|ENVIRONICS ROBD2|
|READY ADMIN|READY ADMIN|READY ADMIN|
|PROG SYSTEM|PROG SYSTEM|PROG SYSTEM|

The program mode is used to create a sequence of up to 99 steps, which later run automatically when selected in the RUNPRG mode. The RUNPRG mode is part of the PILOT TEST menu within the START menu. The system can store up to 20 programs with up to 99 steps each.

Each step can be programmed as either a HOLD or CHANGE step. For a HOLD step, the system will hold at the specified altitude for the specified amount of time, up to 60 minutes in 1 minute increments, and produce the equivalent oxygen content for that altitude. When programming two HOLD steps in a row, the system jumps instantaneously from one altitude to another. To program a hold step for more than 60 minutes, simply insert a second hold step at the same altitude. For a change step, the system decreases or increases the equivalent O2 content, at the specified ascent or descent rate. Using this information, the system determines total step run time for display purposes in the RUN mode.

For a HOLD step, the user must specify the altitude and hold time in minutes or seconds, depending upon how the altitude setup information is set in the system mode.

For a change step, the user must specify the new altitude and rate of change; FT/MIN or FT/SEC, depending upon how the altitude setup information is set in the system mode. If a change step is specified as the first step in a program, the system assumes starting at sea level.

- --
#   Perform the following steps to enter a program of altitudes.

1. Select PROG (F1)
2. A right pointing arrow in the farthest left column will align with the last program number run.
3. To create a new program or to select a program to edit, arrow up or down to the program number (1-20) and select EDIT (F1).
4. To create or edit the program name, use the up and down arrow keys to select the letters/numbers/characters and the right and left arrow keys to select the character position within the program name. Each program can have up to 11 characters, including spaces.
5. Press ENTER to accept the program name or leave the preexisting program name unchanged.
6. When on the row for a program step, the step can either be deleted or a new step can be inserted. Pressing the right arrow key will bring up the edit menu to select hold or change selections. After selecting the hold or change step and altitude, pressing the right arrow key will advance the cursor to the time/rate column. Exiting will automatically save the program.

#   SAMPLE SCREEN IN PROGRAM MODE:

|STEP # |# |ALT|TIME/RATE|
|---|---|---|---|
|1|H|O FT|FOR 20 S|
|2|C|20000 FT|@ 1000 F/S|
|DELETE INSERT EXIT|DELETE INSERT EXIT|DELETE INSERT EXIT|DELETE INSERT EXIT|