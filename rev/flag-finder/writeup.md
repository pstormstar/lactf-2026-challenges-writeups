# rev/flag-finder Writeup
168 solves | 132 points | Difficulty: Medium  
**TLDR: Decode a regex that implements a nonogram puzzle.**
## Description
```
No flag? No problem! My Flag Finder is here to help!

flag-finder.chall.lac.tf
```
The challenge consists of a website with some text, what appears to be a large textbox, and a button that says "Find flag".
![Challenge webpage](<webpage screenshot.png>)
## Solve
Upon attempting to select the "textbox", rather than allowing text to be entered, a black box appears where it was clicked. Upon opening the page in inspect, it's revealed that this is actually a large grid of checkboxes, 19 boxes tall and 101 boxes wide. Examining the `script.js` file reveals the following code:
```
const fullInput = document.getElementById('fullInput');
const find = document.getElementById('find');
const result = document.getElementById('result');
const len = 1919;
const theFlag = /^(?=(?=(?:.{91}\..{9})*(?:.{91}#.{9}){4}(?:.{91}\..{9})+...
function createInput() {
    for (let i = 0; i < len; i++) {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `box-${i}`;
        checkbox.className = 'grid-box';
        fullInput.appendChild(checkbox);
    }
}
function match() {
    const boxes = document.querySelectorAll('.grid-box');
    let input = "";
    boxes.forEach(box => {
        input += box.checked ? "#" : ".";
    });
    result.className = 'status';
    if (theFlag.test(input)) {
        result.textContent = "✅ Flag found!";
        result.classList.add('success');
    } else {
        result.textContent = "❌ Flag not found.";
        result.classList.add('error');
    }
}
createInput();
find.addEventListener('click', match);
```
The script waits for the "Find flag" button to be pressed, then takes all the checkboxes in the page, concates their states into a single string, `.` for ever unchecked box and `#` for every checked box, then checks whether the resulting string matches the regex stored in `theFlag` and outputs the result.

Thus, the challenge is to figure out what string of 1919 (101*19) `.`s and `#`s would match the regex. The regex itself can be broken down into 3 parts: the vertical constraints, the input constraint, and the horizontal constraints.
- The vertical constraints are of the form  
`(?=(?:.{n}\..{100-n})* ... (?:.{n}\..{100-n})*)`  
which are lookaheads that check if the entire string can be grouped into strings of 101 characters such that the n+1th character of each group is a `.` or a `#`.  
As an example, the first such constraint 
```
(?=
    (?:.{91}\..{9})*
    (?:.{91}#.{9}){4}
    (?:.{91}\..{9})+
    (?:.{91}#.{9}){5}
    (?:.{91}\..{9})+
    (?:.{91}#.{9}){4}
    (?:.{91}\..{9})*
)
```
checks whether the 92nd character of each 101 character group consists of some number of `.`s, followed by 4 `#`s, followed by at least 1 `.`, followed by 5 `#`s, followed by at least 1 `.`, followed by 4 more `#`s, followed by any number of `.`s.  
There are a total of 101 vertical constaints, 1 for each of the 101 columns.
- The length constaint is the simple lookahead `(?=^.{1919}$)` which checks that the entire string is exactly 1919 characters long and nothing else.
- The horizontal constraints are of the form  
`(\.* ... \.*)(?<=.{n*101})(?<!.{n*101+1})`  
which are capturing groups that check whether the n+1th set of exactly 101 characters matches a specific number and grouping of `#`s.
As an example the 8th such constraint
```
(
    \.*
    #{2}\.+
    #{2}\.+
    #{3}\.+
    #{3}\.+
    #\.+
    #\.+
    #{3}\.+
    #{2}\.+
    #{3}\.+
    #\.+
    #\.+
    #\.+
    #\.+
    #\.*
)
(?<=.{808})
(?<!.{809})
```
checks whether the 8th group of 101 characters consists of `#`s of groups 2, 2, 3, 3, 1, 1, 3, 2, 3, 1, 1, 1, 1, and 1 where there's at least 1 `.` between each group and there can be any number of `.`s at the start and end of the group and that there are exactly 101 characters matched in this new group.
There are a total of 19 horizontal constraints, 1 for each of the 19 rows.

Given that these constaints are idential to those of a [nonogram](https://en.wikipedia.org/wiki/Nonogram) puzzle, the solve consists of converting the regex into nonogram clues and solving the nonogram puzzle. Write a script to parse the regex as a series of nonogram clues (the inverse of `regexer.py`) and run them through a nonogram solver such as with z3 to get the valid nonogram.

When the solution regex is rearranged into 19 lines of 101 characters, the flag is revealed.
```
.....................................................................................................
.##...........#...##..##.#.#.#...#.#.###.......#..##..........##..........##.###.###.........#...###.
..#..##...##.###..#..##..#.#.##..#.#...#......##.#.#.....#.#.#.#.#.#.....#.....#...#.....#.#.##....#.
..#...##.#....#..###.#...###.#.#.###..#......#.#.#.#.....#.#.#.#.#.#.....###.###...#.....###.#.#.###.
..#..#.#.#....#...#..##..###.#.#...#.#.......#.#.#.#.....###.#.#.#.#.....#.#...#...#.....###.#.#...#.
.###.###..##..##..#...##.#.#.#.#...#.#...###..##.###.###...#.###..##.###.###.###...#.###.###.#.#.###.
.........................................................###.........................................
..............##..................##.###.###.....#.#.........###..##.###.........#.#.......#.....#.#.
.##......#.#.#.#.#.#......##.###.#.#.#...#.......#.#.....###...#.#.....#.#.#.....#.#.##...##.....#.#.
.#.#.....#.#.#.#.#.#.....#...#.#.#.#.###.###.....###.....#.#.###.###.###..#......###.#.#.#.#.....###.
.#.#.....###.#.#.#.#.....#...#...#.#...#...#.......#.....#.....#.#.#...#..#........#.#.#.#.#.......#.
.#.#.###...#.###..##.###..##.#...###.##..##..###...#.###.#...###.###.###.#.#.###...#.#.#..##.###...#.
.........###.........................................................................................
..........##......##..##.....#.#.....###.....#.#.........###..##.###......##..##.....#.#......#..##..
.....##..#.#.##..#.#.#...###.#.#.###...#.....#.#.....###...#.#.....#.#.#.#.#.#...###.#.#.###..#...##.
.....#.#.#.#.#.#.#.#.###.#.#.###.###..#......###.....#.#.###.###.###..#..#.#.###.#.#.###.###..#....#.
.....#.#.#.#.#.#.#.#.#.#.#.....#.###...........#.....#.....#.#.#...#..#..#.#.#.#.#.....#.###......##.
.###.#.#.###.#.#.###.###.#.....#.#.#..#..###...#.###.#...###.###.###.#.#.###.###.#.....#.#.#..#..##..
.....................................................................................................
```
The flag is more legible when reentered into the original page:
![Webpage solve](<webpage solve.png>)
The flag is not the easiest to read, expecially the 6 which looks like a G and the 0 looking like an O, but carefully paying attention to the flag format and the distinguishing features (such as W being taller than w) will reveal the resulting flag `lactf{Wh47_d0_y0u_637_wh3n_y0u_cr055_4_r363x_4nd_4_n0n06r4m?_4_r363x06r4m!}`
