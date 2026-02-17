# rev/lactf-1986 Writeup
256 solves | 110 points | Difficulty: Easy  
**TLDR: Reverse a flag-checker program from an x86-16 binary.**
## Description
```
Dug around the archives and found a floppy disk containing a long-forgotten LA CTF challenge. 
Perhaps you may be the first to solve it in decades.
```
The challenge consists of a single file `CHALL.IMG`, which is a floppy disk image.
To run the program, insert the disk image into a DOS emulator and load the program from within.
```
A:\>dir

 Volume in drive A has no label
 Volume Serial Number is 46BA-57E0
 Directory of A:\

CHALL    EXE              9,990 02/02/1986  0:20a CHALL.EXE
    1 File(s)             9,990 Bytes
    0 Dir(s)          1,447,424 Bytes free

A:\chall
UCLA NetSec presents: LACTF '86 Flag Checker
Check your Flag:
hello
Sorry, the flag must begin with "lactf{..."
A:\chall
UCLA NetSec presents: LACTF '86 Flag Checker
Check your Flag:
lactf{hello}
Sorry, that's not the flag.
A:\>
```
## Solve
Extracting the DOS executable `CHALL.EXE` from the disk image using 7zip and opening the program in Ghidra, it can be seen that the program itself consist of three main functions.
- The first function `FUN_1000_0010` is a hashing function that takes in an input string and calculates the hash by multiplying the current hash by 67 (equivalent to `hash << 6 + hash << 1 + hash`), adding the byte value of an input character, and truncating the result to 20 bits for every character in the input going left to right with an initial hash of 0.
- The second function `FUN_1000_007b` is a program that implements a 20-bit LFSR using bits 0 and 3 to determine the next bit.
- The main function `FUN_1000_00b0` asks for the flag as input, calculates the hash using the first function, checks for the input to begin with `lactf{`, then checks if the input character XORed with the current LFSR value truncated to 8 bits matches its corresponding value in a byte array (stored at address `0146` in the data section) for every byte in the input.
To reverse the encryption, find a sequence of LFSR values that when XORed with the byte array gives a valid flag of the form `lactf{...}`

### Solve script
```
flag_bytes = [0xB6, 0x8C, 0x95, 0x8F, 0x9B, 0x85, 0x4C, 0x5E, 0xEC, 0xB6, 0xB8, 0xC0, 0x97, 0x93, 0x0B, 0x58, 0x77, 0x50, 0xB0, 0x2C, 0x7E, 0x28, 0x7A, 0xF1, 0xB6, 0x04, 0xEF, 0xBE, 0x5C, 0x44, 0x78, 0xE8, 0x99, 0x81, 0x04, 0x8F, 0x03, 0x40, 0xA7, 0x3F, 0xFA, 0xB7, 0x08, 0x01, 0x63, 0x52, 0xE3, 0xAD, 0xD1, 0x85, 0x9F, 0x94, 0x21, 0xD5, 0x2A, 0x5C, 0x20, 0xD4, 0x31, 0x12, 0xCE, 0xAA, 0x16, 0xC7, 0xAD, 0xDF, 0x29, 0x5D, 0x72, 0xFC, 0x24, 0x90, 0x2C]

global k
def r():
    global k
    k = (((k) ^ (k >> 3)) & 1) << 19 | (k >> 1)
    return k & 0xff

for hash in range(2**20):
    k = hash
    decrypt = "".join([chr(r() ^ byte) for byte in flag_bytes])
    if decrypt[0:6] == "lactf{" and decrypt[-1] == "}":
        print(decrypt)
        break
```

The resulting flag is `lactf{3asy_3nough_7o_8rute_f0rce_bu7_n0t_ea5y_en0ugh_jus7_t0_brut3_forc3}`