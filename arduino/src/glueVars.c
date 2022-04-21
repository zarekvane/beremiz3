
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
    bool_output[0][0] = __QX0_0;
    int_output[0] = __QW0;

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
    