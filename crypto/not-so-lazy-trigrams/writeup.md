# rev/not-so-lazy-trigrams Writeup
217 solves | 117 points | Difficulty: Easy  
**TLDR: Decode a ciphertext consisting of 3 seperate substitution ciphers**
## Description
```
Finally got the energy to write a trigram substitution cipher. 
Surely three shuffles are better than one!
```
The challenge consists of a two files: `ct.txt`, which contains the ciphertext and `chall.py`, the encryption program.
## Solve
A trigram substion cipher has a total of 26^3 = 17576 total substitution keys. This corresponds to a keyspace of 17576! total possible trigram substitutions, far larger than the 676! for bigram substitutions and the 26! for simple substitution ciphers. 
```
trigrams = [chr(i)+chr(j)+chr(k) for i in range(97,97+26) for j in range(97,97+26) for k in range(97,97+26)]
shufflei = random.sample(range(97,97+26),26)
shufflej = random.sample(range(97,97+26),26)
shufflek = random.sample(range(97,97+26),26)
sub_trigrams = [chr(i)+chr(j)+chr(k) for i in shufflei for j in shufflej for k in shufflek]
```
However, there's a massive flaw with how the trigram substitution is generated. Rather than shuffle all of the trigrams at random, this substitution instead simply regenerates the trigram pairs with 3 simple substitution ciphers instead. In other words, this is not a trigram substitution, but 3 seperate substitution ciphers where every third character is mapped the same, as well as every third character starting from the second character and every third character starting from the third. This drastically reduces the keyspace from 17576! to just (26!)^3

With the encrypted flag and the flag format `lactf{`, five of the substitutions are known. From here, use typical substitution cipher algorithms and methods to fill out the rest of the plain text and obtain the flag. Some approaches include the hill clombing algorithm, guessing the words from the known wordlengths, using the punctuation to identify words, etc.

The resulting flag is `lactf{still_too_lazy_to_write_a_plaintext_so_heres_a_random_wikipedia_article}`