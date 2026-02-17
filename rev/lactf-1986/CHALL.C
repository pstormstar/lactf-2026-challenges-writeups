
#include <stdio.h>
#include <conio.h>
#include <graph.h>
#include <string.h>
#include <stdint.h>

int i = 0;
unsigned long state; 

unsigned long seed(char *str)
{
    unsigned long s = 0;
    char c;
    while ((c = *str++))
    {
	s = ((s << 6) + (s << 1) + s) + c;
	s = s & 0xFFFFFL;
    }
    return s;
} 

unsigned long lfsr(unsigned long state)
{
    unsigned long bit;
    bit = (state ^ (state >> 3)) & 1;
    state = (state >> 1) | (bit << 19);

    return state & 0xFFFFFL;
}

main()
{
    char flag[0x49] = {0xB6, 0x8C, 0x95, 0x8F, 0x9B, 0x85, 0x4C, 0x5E, 0xEC, 0xB6, 0xB8, 0xC0, 0x97, 0x93, 0x0B, 0x58, 0x77, 0x50, 0xB0, 0x2C, 0x7E, 0x28, 0x7A, 0xF1, 0xB6, 0x04, 0xEF, 0xBE, 0x5C, 0x44, 0x78, 0xE8, 0x99, 0x81, 0x04, 0x8F, 0x03, 0x40, 0xA7, 0x3F, 0xFA, 0xB7, 0x08, 0x01, 0x63, 0x52, 0xE3, 0xAD, 0xD1, 0x85, 0x9F, 0x94, 0x21, 0xD5, 0x2A, 0x5C, 0x20, 0xD4, 0x31, 0x12, 0xCE, 0xAA, 0x16, 0xC7, 0xAD, 0xDF, 0x29, 0x5D, 0x72, 0xFC, 0x24, 0x90, 0x2C};
    char input[0x4A];
    char output[0x49];
    printf("UCLA NetSec presents: LACTF '86 Flag Checker\n");
    printf("Check your Flag: \n");
    fgets(input, sizeof(input), stdin);
    input[strcspn(input, "\n")] = 0;

    if((input[0] != 'l') | (input[1] != 'a') | (input[2] != 'c') | (input[3] != 't') | (input[4] != 'f') | (input[5] != '{'))
    {
        printf("Sorry, the flag must begin with \"lactf{...\"");
        return 0;
    }

    state = seed(input);

    for (i = 0; i < 73; i++)
    {
        state = lfsr(state);
        if(input[i] == 0)
        {
            break;
        }
        output[i] = input[i] ^ (state & 0xFF);
        if(output[i] != flag[i])
        {
            printf("Sorry, that's not the flag.");
            return 0;
        }
    }
    printf("Indeed, that's the flag!");
    return 0;
}



