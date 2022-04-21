import sys
import os
import time
import subprocess
import wx
import shutil
import time
import json

global compiler_logs
compiler_logs = ''

def build(st_file, platform, port, txtCtrl, update_subsystem):
    global compiler_logs
    compiler_logs = ''
    if (os.path.exists("editor/arduino/bin/iec2c") or os.path.exists("editor/arduino/bin/iec2c.exe")):
        #remove old files first
        if os.path.exists('editor/arduino/src/POUS.c'):
            os.remove('editor/arduino/src/POUS.c')
        if os.path.exists('editor/arduino/src/POUS.h'):
            os.remove('editor/arduino/src/POUS.h')
        if os.path.exists('editor/arduino/src/LOCATED_VARIABLES.h'):
            os.remove('editor/arduino/src/LOCATED_VARIABLES.h')
        if os.path.exists('editor/arduino/src/VARIABLES.csv'):
            os.remove('editor/arduino/src/VARIABLES.csv')
        if os.path.exists('editor/arduino/src/Config0.c'):
            os.remove('editor/arduino/src/Config0.c')
        if os.path.exists('editor/arduino/src/Config0.h'):
            os.remove('editor/arduino/src/Config0.h')
        if os.path.exists('editor/arduino/src/Res0.c'):
            os.remove('editor/arduino/src/Res0.c')
    else:
        compiler_logs += "Error: iec2c compiler not found!\n"
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        return
    
    #Update/setup environment
    if (update_subsystem):
        compiler_logs += "Updating environment...\n"
        cli_command = ''
        if (os.name == 'nt'):
            cli_command = 'editor\\arduino\\bin\\arduino-cli-w32'
        else:
            cli_command = 'editor/arduino/bin/arduino-cli-l64'

        #Setup boards - initial stage
        env_setup = os.popen(cli_command + ' config init 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        #Setup boards - remove 3rd party boards to re-add them later since we don't know if they're there or not
        env_setup = os.popen(cli_command + ' config remove board_manager.additional_urls https://arduino.esp8266.com/stable/package_esp8266com_index.json 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        env_setup = os.popen(cli_command + ' config remove board_manager.additional_urls https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        #Setup boards - add 3rd party boards
        env_setup = os.popen(cli_command + ' config add board_manager.additional_urls https://arduino.esp8266.com/stable/package_esp8266com_index.json 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        env_setup = os.popen(cli_command + ' config add board_manager.additional_urls https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        
        #Update
        env_setup = os.popen(cli_command + ' core update-index 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        env_setup = os.popen(cli_command + ' update 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)

        #Install boards
        env_setup = os.popen(cli_command + ' core install esp8266:esp8266 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        env_setup = os.popen(cli_command + ' core install esp32:esp32 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        env_setup = os.popen(cli_command + ' core install arduino:avr 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        env_setup = os.popen(cli_command + ' core install arduino:samd 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        env_setup = os.popen(cli_command + ' core install arduino:sam 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        env_setup = os.popen(cli_command + ' core install arduino:megaavr 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        env_setup = os.popen(cli_command + ' core install arduino:mbed_portenta 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        env_setup = os.popen(cli_command + ' core install arduino:mbed_nano 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        env_setup = os.popen(cli_command + ' lib install WiFiNINA 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        env_setup = os.popen(cli_command + ' lib install Arduino_MachineControl 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        env_setup = os.popen(cli_command + ' lib install OneWire 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        env_setup = os.popen(cli_command + ' lib install DallasTemperature 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        env_setup = os.popen(cli_command + ' lib install P1AM 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        env_setup = os.popen(cli_command + ' upgrade 2>&1')
        compiler_logs += env_setup.read()
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)

    #Generate C files
    compiler_logs += "Compiling .st file...\n"
    wx.CallAfter(txtCtrl.SetValue, compiler_logs)
    wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
    if (os.name == 'nt'):
        base_path = 'editor\\arduino\\src\\'
    else:
        base_path = 'editor/arduino/src/'
    f = open(base_path+'plc_prog.st', 'w')
    f.write(st_file)
    f.flush()
    f.close()

    time.sleep(0.2) #make sure plc_prog.st was written to disk

    if (os.name == 'nt'):
        compilation = subprocess.Popen(['editor\\arduino\\bin\\iec2c.exe', 'plc_prog.st'], cwd='editor\\arduino\\src', creationflags = 0x08000000, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    else:
        compilation = subprocess.Popen(['../bin/iec2c', 'plc_prog.st'], cwd='./editor/arduino/src', stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    stdout, stderr = compilation.communicate()
    compiler_logs += stdout
    compiler_logs += stderr
    wx.CallAfter(txtCtrl.SetValue, compiler_logs)
    wx.CallAfter(txtCtrl.SetInsertionPoint, -1)

    #Remove temporary plc program
    #if os.path.exists(base_path+'plc_prog.st'):
    #    os.remove(base_path+'plc_prog.st')

    #Generate glueVars.c
    if not (os.path.exists(base_path+'LOCATED_VARIABLES.h')):
        compiler_logs += "Error: Couldn't find LOCATED_VARIABLES.h. Check iec2c compiler output for more information\n"
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        return
    
    located_vars_file = open(base_path+'LOCATED_VARIABLES.h', 'r')
    located_vars = located_vars_file.readlines()
    glueVars = """
#include "iec_std_lib.h"

#define __LOCATED_VAR(type, name, ...) type __##name;
#include "LOCATED_VARIABLES.h"
#undef __LOCATED_VAR
#define __LOCATED_VAR(type, name, ...) type* name = &__##name;
#include "LOCATED_VARIABLES.h"
#undef __LOCATED_VAR

TIME __CURRENT_TIME;
BOOL __DEBUG;
extern unsigned long long common_ticktime__;

//OpenPLC Buffers
#if defined(__AVR_ATmega328P__) || defined(__AVR_ATmega168__) || defined(__AVR_ATmega32U4__) || defined(__AVR_ATmega16U4__)

#define MAX_DIGITAL_INPUT          8
#define MAX_DIGITAL_OUTPUT         8
#define MAX_ANALOG_INPUT           6
#define MAX_ANALOG_OUTPUT          3

#else

#define MAX_DIGITAL_INPUT          24
#define MAX_DIGITAL_OUTPUT         24
#define MAX_ANALOG_INPUT           8
#define MAX_ANALOG_OUTPUT          16

#endif

IEC_BOOL *bool_input[MAX_DIGITAL_INPUT/8][8];
IEC_BOOL *bool_output[MAX_DIGITAL_OUTPUT/8][8];
IEC_UINT *int_input[MAX_ANALOG_INPUT];
IEC_UINT *int_output[MAX_ANALOG_OUTPUT];

void glueVars()
{
"""
    for located_var in located_vars:
        #cleanup located var line
        if ('__LOCATED_VAR(' in located_var):
            located_var = located_var.split('(')[1].split(')')[0]
            var_data = located_var.split(',')
            if (len(var_data) < 5):
                compiler_logs += 'Error processing located var line: ' + located_var + '\n'
                wx.CallAfter(txtCtrl.SetValue, compiler_logs)
                wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
            else:
                var_type = var_data[0]
                var_name = var_data[1]
                var_address = var_data[4]
                var_subaddress = '0'
                if (len(var_data) > 5):
                    var_subaddress = var_data[5]
                
                #check variable type and assign to correct buffer pointer
                if ('QX' in var_name):
                    if (int(var_address) > 2 or int(var_subaddress) > 7):
                        compiler_logs += 'Error: wrong location for var ' + var_name + '\n'
                        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
                        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
                        return
                    glueVars += '    bool_output[' + var_address + '][' + var_subaddress + '] = ' + var_name + ';\n'
                elif ('IX' in var_name):
                    if (int(var_address) > 2 or int(var_subaddress) > 7):
                        compiler_logs += 'Error: wrong location for var ' + var_name + '\n'
                        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
                        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
                        return
                    glueVars += '    bool_input[' + var_address + '][' + var_subaddress + '] = ' + var_name + ';\n'
                elif ('QW' in var_name):
                    if (int(var_address) > 16):
                        compiler_logs += 'Error: wrong location for var ' + var_name + '\n'
                        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
                        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
                        return
                    glueVars += '    int_output[' + var_address + '] = ' + var_name + ';\n'
                elif ('IW' in var_name):
                    if (int(var_address) > 16):
                        compiler_logs += 'Error: wrong location for var ' + var_name + '\n'
                        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
                        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
                        return
                    glueVars += '    int_input[' + var_address + '] = ' + var_name + ';\n'
                else:
                    compiler_logs += 'Could not process location "' + var_name + '" from line: ' + located_var + '\n'
                    wx.CallAfter(txtCtrl.SetValue, compiler_logs)
                    wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
                    return

    glueVars += """
}

void updateTime()
{
    __CURRENT_TIME.tv_nsec += common_ticktime__;

    if (__CURRENT_TIME.tv_nsec >= 1000000000)
    {
        __CURRENT_TIME.tv_nsec -= 1000000000;
        __CURRENT_TIME.tv_sec += 1;
    }
}
    """
    f = open(base_path+'glueVars.c', 'w')
    f.write(glueVars)
    f.flush()
    f.close()

    time.sleep(2) #make sure glueVars.c was written to disk
    
    # Patch POUS.c to include POUS.h
    f = open(base_path+'POUS.c', 'r')
    pous_c = '#include "POUS.h"\n\n' + f.read()
    f.close()

    f = open(base_path+'POUS.c', 'w')
    f.write(pous_c)
    f.flush()
    f.close()

    # Patch Res0.c to include POUS.h instead of POUS.c
    f = open(base_path+'Res0.c', 'r')
    res0_c = ''
    lines = f.readlines()
    for line in lines:
        if '#include "POUS.c"' in line:
            res0_c += '#include "POUS.h"\n'
        else:
            res0_c += line
    f.close()

    f = open(base_path+'Res0.c', 'w')
    f.write(res0_c)
    f.flush()
    f.close()

    #Copy HAL file
    if (os.name == 'nt'):
        source_path = 'editor\\arduino\\src\\hal\\'
        destination = 'editor\\arduino\\src\\arduino.cpp'
    else:
        source_path = 'editor/arduino/src/hal/'
        destination = 'editor/arduino/src/arduino.cpp'

    if platform == 'arduino:avr:uno' or platform == 'arduino:avr:leonardo' or platform == 'arduino:samd:arduino_zero_native' or platform == 'arduino:samd:arduino_zero_edbg':
        source_file = 'uno_leonardo_nano_micro_zero.cpp'
    elif platform == 'arduino:avr:nano' or platform == 'arduino:avr:micro':
        source_file = 'uno_leonardo_nano_micro_zero.cpp'
    elif platform == 'arduino:megaavr:nona4809' or platform == 'arduino:mbed_nano:nano33ble' or platform == 'arduino:samd:nano_33_iot':
        source_file = 'nano_every.cpp'
    elif platform == 'arduino:mbed_nano:nanorp2040connect':
        source_file = 'rp2040.cpp'
    elif platform == 'arduino:avr:mega' or platform == 'arduino:sam:arduino_due_x' or platform == 'arduino:sam:arduino_due_x_dbg':
        source_file = 'mega_due.cpp'
    elif platform == 'arduino:samd:mkrzero' or platform == 'arduino:samd:mkrwifi1010':
        source_file = 'mkr.cpp'
    elif platform == 'arduino:samd:mkrzero-p1am':
        source_file = 'p1am.cpp'
        platform = 'arduino:samd:mkrzero'
    elif platform == 'arduino:mbed_portenta:envie_m7':
        source_file = 'machine_control.cpp'
    elif platform == 'esp8266:esp8266:nodemcuv2' or platform == 'esp8266:esp8266:d1_mini':
        source_file = 'esp8266.cpp'
    elif platform == 'esp32:esp32:esp32' or platform == 'esp32:esp32:esp32s2' or platform == 'esp32:esp32:esp32c3':
        source_file = 'esp32.cpp'

    shutil.copyfile(source_path + source_file, destination)

    #Generate Pin Array Sizes defines
    #We need to write the hal specific pin size defines on the global defines.h so that it is
    #available everywhere

    if (os.name == 'nt'):
        define_path = 'editor\\arduino\\examples\\Baremetal\\'
    else:
        define_path = 'editor/arduino/examples/Baremetal/'
    file = open(define_path+'defines.h', 'r')
    define_file = file.read() + '\n\n//Pin Array Sizes\n'
    hal = open(destination, 'r')
    lines = hal.readlines()
    for line in lines:
        if (line.find('define NUM_DISCRETE_INPUT') > 0):
            define_file += line
        if (line.find('define NUM_ANALOG_INPUT') > 0):
            define_file += line
        if (line.find('define NUM_DISCRETE_OUTPUT') > 0):
            define_file += line
        if (line.find('define NUM_ANALOG_OUTPUT') > 0):
            define_file += line

    #Write defines.h file back to disk
    if (os.name == 'nt'):
        define_path = 'editor\\arduino\\examples\\Baremetal\\'
    else:
        define_path = 'editor/arduino/examples/Baremetal/'
    f = open(define_path+'defines.h', 'w')
    f.write(define_file)
    f.flush()
    f.close()

    #Generate .elf file
    compiler_logs += "Generating binary file...\n"
    wx.CallAfter(txtCtrl.SetValue, compiler_logs)
    wx.CallAfter(txtCtrl.SetInsertionPoint, -1)

    #if (os.name == 'nt'):
    #    compilation = os.popen('editor\\arduino\\bin\\arduino-cli-w32 compile -v --libraries=editor\\arduino --build-property compiler.c.extra_flags="-Ieditor\\arduino\\src\\lib" --build-property compiler.cpp.extra_flags="-Ieditor\\arduino\\src\\lib" --export-binaries -b ' + platform + ' editor\\arduino\\examples\\Baremetal\\Baremetal.ino 2>&1')
        #compilation = subprocess.Popen(['editor\\arduino\\bin\\arduino-cli-w32', 'compile', '-v', '--libraries=..\\..\\', '--build-property', 'compiler.c.extra_flags="-I..\\src\\lib"', '--build-property', 'compiler.cpp.extra_flags="I..\\src\\lib"', '--export-binaries', '-b', platform, '..\\examples\\Baremetal\\Baremetal.ino'], cwd='editor\\arduino\\src', stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    #else:
    #    compilation = os.popen('editor/arduino/bin/arduino-cli-l64 compile -v --libraries=editor/arduino --build-property compiler.c.extra_flags="-Ieditor/arduino/src/lib" --build-property compiler.cpp.extra_flags="-Ieditor/arduino/src/lib" --export-binaries -b ' + platform + ' editor/arduino/examples/Baremetal/Baremetal.ino 2>&1')
    #compiler_logs += compilation.read()
    #wx.CallAfter(txtCtrl.SetValue, compiler_logs)
    #wx.CallAfter(txtCtrl.SetInsertionPoint, -1)

    if (os.name == 'nt'):
        compilation = subprocess.Popen(['editor\\arduino\\bin\\arduino-cli-w32', 'compile', '-v', '--libraries=editor\\arduino', '--build-property', 'compiler.c.extra_flags="-Ieditor\\arduino\\src\\lib"', '--build-property', 'compiler.cpp.extra_flags="-Ieditor\\arduino\\src\\lib"', '--export-binaries', '-b', platform, 'editor\\arduino\\examples\\Baremetal\\Baremetal.ino'], creationflags = 0x08000000, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    else:
        compilation = subprocess.Popen(['editor/arduino/bin/arduino-cli-l64', 'compile', '-v', '--libraries=editor/arduino', '--build-property', 'compiler.c.extra_flags="-Ieditor/arduino/src/lib"', '--build-property', 'compiler.cpp.extra_flags="-Ieditor/arduino/src/lib"', '--export-binaries', '-b', platform, 'editor/arduino/examples/Baremetal/Baremetal.ino'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    stdout, stderr = compilation.communicate()
    compiler_logs += stdout
    compiler_logs += stderr
    if (compilation.returncode != 0):
        compiler_logs += '\nCOMPILATION FAILED!\n'
    wx.CallAfter(txtCtrl.SetValue, compiler_logs)
    wx.CallAfter(txtCtrl.SetInsertionPoint, -1)

    if (port != None and compilation.returncode == 0):
        compiler_logs += '\nUploading program to Arduino board at ' + port + '...\n'
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)
        if (os.name == 'nt'):
            uploading = os.popen('editor\\arduino\\bin\\arduino-cli-w32 upload --port ' + port + ' --fqbn ' + platform + ' editor\\arduino\\examples\\Baremetal/ 2>&1')
        else:
            uploading = os.popen('editor/arduino/bin/arduino-cli-l64 upload --port ' + port + ' --fqbn ' + platform + ' editor/arduino/examples/Baremetal/ 2>&1')
        compiler_logs += uploading.read()
        compiler_logs += '\nDone!\n'
        wx.CallAfter(txtCtrl.SetValue, compiler_logs)
        wx.CallAfter(txtCtrl.SetInsertionPoint, -1)

    time.sleep(1) #make sure files are not in use anymore
    
    #no clean up
    return
    
    #Clean up and return
    if os.path.exists(base_path+'POUS.c'):
        os.remove(base_path+'POUS.c')
    if os.path.exists(base_path+'POUS.h'):
        os.remove(base_path+'POUS.h')
    if os.path.exists(base_path+'LOCATED_VARIABLES.h'):
        os.remove(base_path+'LOCATED_VARIABLES.h')
    if os.path.exists(base_path+'VARIABLES.csv'):
        os.remove(base_path+'VARIABLES.csv')
    if os.path.exists(base_path+'Config0.c'):
        os.remove(base_path+'Config0.c')
    if os.path.exists(base_path+'Config0.h'):
        os.remove(base_path+'Config0.h')
    if os.path.exists(base_path+'Config0.o'):
        os.remove(base_path+'Config0.o')
    if os.path.exists(base_path+'Res0.c'):
        os.remove(base_path+'Res0.c')
    if os.path.exists(base_path+'Res0.o'):
        os.remove(base_path+'Res0.o')
    if os.path.exists(base_path+'glueVars.c'):
        os.remove(base_path+'glueVars.c')