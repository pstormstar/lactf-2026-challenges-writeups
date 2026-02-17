# rev/the-fish Writeup
306 solves | 105 points | Difficulty: Baby  
**TLDR: Reverse an encoding system written in an esolang.**
## Description
```
The fish asks you for the flag. Unfortunately, it can only describe it to you in its own words.
```
The challenge consists of a single file `fish.py`, which is the entire challenge.
## Solve
`fish.py` is an interpreter for the [Fish (><>)](https://esolangs.org/wiki/Fish) esolang, a stack-based language. It asks for an input, stores it in `flag`, then writes the values of the characters in `flag` into the intial stack, and calls the interpreter on the ><> program stored in `fisherator`.
The program differs from the original interpreter in two ways:
- The division instruction `,` does integer division, not float division
- The instruction to print the top of stack as a number `n` instead checks if the number on the top of the stack matches a hard-coded number (the output of the program initialized with the flag) and prints the appropriate output.

Here's a breakdown of the `fisherator` program:
```
  v 2,0             25,0 v    v 30,0                                 v 69,0            v 87,0
r0!&4:*:**+&5:*0l2=?.~~20."W"01&:&1=}@{?.{2*"E"0&:&2%0=?.&3*1+&}}1+{{.&2,:&}@{1=?.{56*0.n;

Initialization:
r0!
r   Reverses the stack (the first character in the input is now the top of the stack)
 0  Adds a 0 to the stack
  ! Skips the following instruction, starting the first loop from "4"

The first loop:
&4:*:**+&5:*0l2=?.~~20.
&                       Pops the value from the register into the stack (skipped on the first loop)
 4:*:*                  Push 256 to the stack (equivalent to (4*4)*(4*4))
      *+&               Multiplies the top of the stack by 256 then adds the value underneath it and stores it in the register
         5:*0           Push 25 (5*5) and 0 to the stack
             l2=?.      Jumps to 25,0 on the program if there are only 2 values in the stack, otherwise skip
                  ~~20. Pops the 25 and 0 off the stack and jumps to 2,0 on the program
Note that jumping skips the instruction at the jump address, so execution continues from the instruction after the jump.

The second loop:
"W"01&:&1=}@{?.{2*"E"0&:&2%0=?.&3*1+&}}1+{{.&2,:&}@{1=?.{56*0.n;

Initialization:
"W"01
"W"01                           Push 87 (ord("W")), 0, and 1 on the stack
If condition:
&:&1=}@{?.{2*"E"0&:&2%0=?.
&:&1=                           Push whether the value in register is 1
     }@{?.                      Jumps to 87,0 if so
          {2*                   Doubles the value of the initial 1 in the stack
             "E"0               Pushes 69 (ord("E")) and 0 to the stack
                 &:&2%0=?.      Checks if the number in the register is even, goes to 69,0 if so
Handling the Register:
&3*1+&}}1+{{.&2,:&}@{1=?.{56*0.
&3*1+&                          Multiplies the register value by 3 and adds 1
      }}1+{{                    Increments the value of the initial 1 in the stack
            .                   Jumps to 69,0 (does nothing since the pointer is already at 69,0)
             &2,:&              Divides register value by 2
                  }@{1=?.       Jumps to 87,0 if the register value is 1
                         {56*0. Jumps to 30,0

Ending:
n;                              Compares the final value and exits
```
In short, the program converts a string into a base-256 big-endian integer, then tracks its sequence down to 1, where the next number is (3n+1)/2 if the current number is odd anf n/2 if it's even. It builds a binary sequence starting with 1, where each appended 0 is an even number and each 1 is an odd number. This final string is compared to the hardcoded integer.

So obtain the flag, sinply reverse this process by taking the hardcoded integer, and read all but the first bit from right to left, multiplying by 2 for each 0 and multiplying by 2, subtracting 1, and dividing by 3 for each 1.

### Solve script
```
flag_val = 996566347683429688961961964301023586804079510954147876054559647395459973491017596401595804524870382825132807985366740968983080828765835881807124832265927076916036640789039576345929756821059163439816195513160010797349073195590419779437823883987351911858848638715543148499560927646402894094060736432364692585851367946688748713386570173685483800217158511326927462877856683551550570195482724733002494766595319158951960049962201021071499099433062723722295346927562274516673373002429521459396451578444698733546474629616763677756873373867426542764435331574187942918914671163374771769499428478956051633984434410838284545788689925768605629646947266017951214152725326967051673704710610619169658404581055569343649552237459405389619878622595233883088117550243589990766295123312113223283666311520867475139053092710762637855713671921562262375388239616545168599659887895366565464743090393090917526710854631822434014024
def solve(flag_val):
    acc = 1
    curr = flag_val
    while curr != 1:
        acc *= 2
        if curr % 2 != 0:
            acc -= 1
            acc //= 3 
        curr //= 2
    byte_len = (acc.bit_length() + 7) // 8
    flag_bytes = acc.to_bytes(byte_len, byteorder='big')
    print(flag_bytes.decode('utf-8'))
solve(flag_val)
```

The resulting flag is `lactf{7h3r3_m4y_83_50m3_155u35_w17h_7h15_1f_7h3_c011472_c0nj3c7ur3_15_d15pr0v3n}`