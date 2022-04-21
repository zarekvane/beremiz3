#include <stdlib.h>
extern "C" {
#include "openplc.h"
}
#include "Arduino.h"

//OpenPLC HAL for Arduino Nano form factor (Nano Every, Nano 33 BLE, Nano 33 IoT)

/******************PINOUT CONFIGURATION***********************
Digital In:  2, 3, 4, 5, 6                  (%IX0.0 - %IX0.4)
Digital Out: 7, 8, 10, 11, 12, 13           (%QX0.0 - %QX0.5)
Analog In: A1, A2, A3, A4, A5, A6, A7       (%IW0 - %IW6)
Analog Out: 9, 14                           (%QW0 - %QW1)
**************************************************************/

//Define the number of inputs and outputs for this board (mapping for the Arduino UNO)
#define NUM_DISCRETE_INPUT          5
#define NUM_ANALOG_INPUT            7
#define NUM_DISCRETE_OUTPUT         6
#define NUM_ANALOG_OUTPUT           2

//Create the I/O pin masks
uint8_t pinMask_DIN[] = {2, 3, 4, 5, 6};
uint8_t pinMask_AIN[] = {15, 16, 17, 18, 19, 20, 21};
uint8_t pinMask_DOUT[] = {7, 8, 10, 11, 12, 13};
uint8_t pinMask_AOUT[] = {9, 14};

void hardwareInit()
{
    for (int i = 0; i < NUM_DISCRETE_INPUT; i++)
    {
        pinMode(pinMask_DIN[i], INPUT);
    }
    
    for (int i = 0; i < NUM_ANALOG_INPUT; i++)
    {
        pinMode(pinMask_AIN[i], INPUT);
    }
    
    for (int i = 0; i < NUM_DISCRETE_OUTPUT; i++)
    {
        pinMode(pinMask_DOUT[i], OUTPUT);
    }

    for (int i = 0; i < NUM_ANALOG_OUTPUT; i++)
    {
        pinMode(pinMask_AOUT[i], OUTPUT);
    }
}

void updateInputBuffers()
{
    for (int i = 0; i < NUM_DISCRETE_INPUT; i++)
    {
        if (bool_input[i/8][i%8] != NULL) 
            *bool_input[i/8][i%8] = digitalRead(pinMask_DIN[i]);
    }
    
    for (int i = 0; i < NUM_ANALOG_INPUT; i++)
    {
        if (int_input[i] != NULL)
            *int_input[i] = (analogRead(pinMask_AIN[i]) * 64);
    }
}

void updateOutputBuffers()
{
    for (int i = 0; i < NUM_DISCRETE_OUTPUT; i++)
    {
        if (bool_output[i/8][i%8] != NULL) 
            digitalWrite(pinMask_DOUT[i], *bool_output[i/8][i%8]);
    }
    for (int i = 0; i < NUM_ANALOG_OUTPUT; i++)
    {
        if (int_output[i] != NULL) 
            analogWrite(pinMask_AOUT[i], (*int_output[i] / 256));
    }
}
