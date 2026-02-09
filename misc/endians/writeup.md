# misc/endians Writeup
603 solves | 100 points | Difficulty: Baby  
**TLDR: Recover a misencoded (mojibake) flag.**
## Description
```\
I was reading about Unicode character encodings until one day, my flag turned into Japanese! Does little-endian mean the little byte's at the end or that the characters start with the little byte?
```
The challenge consists of 2 files: chall.txt and gen.py.  
chall.txt:
```
氀愀挀琀昀笀㄀开猀甀爀㌀开栀　瀀攀开琀栀㄀猀开搀　攀猀开渀　琀开最㌀琀开氀　猀琀开㄀渀开琀爀愀渀猀氀愀琀椀　渀℀紀
```
gen.py:
```
text = "lactf{REDACTED}"
endian = text.encode(encoding="???").decode(encoding="???")
with open("chall.txt", "wb") as file:
    file.write(endian.encode())
```
## Solve

From the generation script, the flag `text` is passed through an unknown encoding and another unknown decoding before being encoded in utf-8 (the default encoding) before the final bytestream is written to the file. The first step is to decode the string and obtain the codepoints of the characters.
```
>>> with open("chall.txt", "rb") as file:
...     chall = file.read().decode()
...
>>> print(chall)
氀愀挀琀昀笀㄀开猀甀爀㌀开栀　瀀攀开琀栀㄀猀开搀　攀猀开渀　琀开最㌀琀开氀　猀琀开㄀渀开琀爀愀渀猀氀愀琀椀　渀℀紀
>>> print([hex(ord(ch)) for ch in chall])
['0x6c00', '0x6100', '0x6300', '0x7400', '0x6600', '0x7b00', '0x3100', '0x5f00', '0x7300', '0x7500', '0x7200', '0x3300', '0x5f00', '0x6800', '0x3000', '0x7000', '0x6500', '0x5f00', '0x7400', '0x6800', '0x3100', '0x7300', '0x5f00', '0x6400', '0x3000', '0x6500', '0x7300', '0x5f00', '0x6e00', '0x3000', '0x7400', '0x5f00', '0x6700', '0x3300', '0x7400', '0x5f00', '0x6c00', '0x3000', '0x7300', '0x7400', '0x5f00', '0x3100', '0x6e00', '0x5f00', '0x7400', '0x7200', '0x6100', '0x6e00', '0x7300', '0x6c00', '0x6100', '0x7400', '0x6900', '0x3000', '0x6e00', '0x2100', '0x7d00']
```
Notice something interesting about these characters. All of their codepoints end in `00`. This, along with the challenge name and descripton suggests that the upper and lower bytes of each character (aka the endian) has been swapped. One way to fix that would be to decode the bytes using UTF-16BE then reencode them with UTF-16LE. The order doesn't matter, so long as the bytes are decoded and reencoded with UTF16 with different endians.
```
>>> chall.encode(encoding="UTF-16BE").decode(encoding="UTF-16LE")
'lactf{1_sur3_h0pe_th1s_d0es_n0t_g3t_l0st_1n_translati0n!}'
```
From here, the resulting flag is `lactf{1_sur3_h0pe_th1s_d0es_n0t_g3t_l0st_1n_translati0n!}`
## Notes and Observations
- Since the flag only contains ASCII characters, it is not necessary to encode with UTF-16BE. Any ASCII compatible encoding, such as UTF-8 would do as well. The only difference would be that there would be null bytes before each character, but those would be removed by simply printing the resulting string.
```
>>> chall.encode(encoding="UTF-16BE").decode() # Defaults to UTF-8
'l\x00a\x00c\x00t\x00f\x00{\x001\x00_\x00s\x00u\x00r\x003\x00_\x00h\x000\x00p\x00e\x00_\x00t\x00h\x001\x00s\x00_\x00d\x000\x00e\x00s\x00_\x00n\x000\x00t\x00_\x00g\x003\x00t\x00_\x00l\x000\x00s\x00t\x00_\x001\x00n\x00_\x00t\x00r\x00a\x00n\x00s\x00l\x00a\x00t\x00i\x000\x00n\x00!\x00}\x00'
>>> print(chall.encode(encoding="UTF-16BE").decode())
lactf{1_sur3_h0pe_th1s_d0es_n0t_g3t_l0st_1n_translati0n!}
```