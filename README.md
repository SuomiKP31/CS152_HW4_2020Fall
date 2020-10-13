# CS152_HW4_2020Fall
 SPN Solution of Cryptography course in ShanghaiTech.
 
 ## Usage
 
This is the code I used for solving question 4.15 and 4.16 in _Cryptography Theory and Practice 4th Edition_, page 134.

It's by no means neat but I tried to make it as clear as possible in case of algorithm.
It can output the linear approximation table and ND value table as the question requested,
as well as store them for use of finding the linear approximation and differential trial.

An SPN network the same as the textbook presented is implemented and tested. (Encryption only)

## Questions

### 4.15 

Suppose that the S-box of Example 4.1 is replaced by the S-box defined by the following substitution:

`sbox = [8, 4, 2, 1, 0xc, 6, 3, 0xd, 0xa, 5, 0xe, 7, 0xf, 0xb, 9, 0]`

(a) Compute the linear approximation table for this S-box.

(b) Find a linear approximation using three active S-boxes, and use the piling-up lemma to
estimate the bias of the random variable X16 + U41 + U49

(c) Describe a linear attack, analogous to Algorithm 4.2, that will nd eight subkey bits in the
last round.

(d) Implement your attack and test it to see how many plaintexts are required in order for
the algorithm to nd the correct subkey bits (approximately 1000-1500 plaintexts should
suffice; this attack is more efficient than Algorithm 4.2 because the bias is larger by a factor
of 2, which means that the number of plaintexts can be reduced by a factor of about 4).

### 4.16

Suppose that the S-box of Example 4.1 is replaced by the S-box defined by the following substitution:

`sbox = [0xe, 2, 1, 3, 0xd, 9, 0, 6, 0xf, 4, 5, 0xa, 8, 0xc, 7, 0xb]`

(a) Compute the table of values ND (as dened in Denition 4.3) for this S-box.

(b) Find a differential trail using four active S-boxes, namely, S1_1 ; S1_4 ; S2_4 , and S3_4 , that has
propagation ratio 27/2048.

(c) Describe a differential attack, analogous to Algorithm 4.3, that will find eight subkey bits
in the last round.

(d) Implement your attack and test it to see how many plaintexts are required in order for the
algorithm to find the correct subkey bits (approximately 100􀀀200 plaintexts should suffice;
this attack is not as effcient as Algorithm 4.3 because the propagation ratio is smaller by
a factor of 2).

## How to Answer

In the case of answering the two question is almost the same. I'll just briefly answer 4.15 here.

(a) The linear approximation table is the output of

    lpt = LPT(sbox)
    lpt.output_lat()
Namely:

             (a)
                |   0   1   2   3   4   5   6   7   8   9   a   b   c   d   e   f  <-(b)
             --------------------------------------------------------------------
              0 |  +8   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0 
              1 |   0  +2  -2   0  +2   0   0  -2  -4  -2  -2   0  +2   0  -4  +2 
              2 |   0  +2   0  +2  -2   0  -2   0  -2   0  +2  -4  -4  -2   0  +2 
              3 |   0   0  +2  +2   0  +4  +2  -2  -2  -2   0   0  +2  -2  +4   0 
              4 |   0  +2   0  -2   0  +2   0  -2  +2  -4  +2   0  -2   0  -2  -4 
              5 |   0  +4  -2  -2  +2  +2   0  +4  -2  +2   0   0   0   0  +2  -2 
              6 |   0   0  +4   0  +2  +2  -2  +2   0   0   0  +4  -2  -2  -2  +2 
              7 |   0  -2  -2   0  +4  -2  +2   0   0  -2  -2   0  -4  -2  +2   0 
              8 |   0  +2  +2   0   0  -2  -2   0  +2   0  -4  -2  +2  -4   0  -2 
              9 |   0   0   0  +4  +2  +2  -2  +2  +2  -2  -2  -2   0  +4   0   0 
              a |   0  +4  +2  +2  -2  -2  +4   0   0   0  -2  +2  -2  +2   0   0 
              b |   0  -2  +4  -2   0  -2   0  +2  -4  -2   0  -2   0  +2   0  -2 
              c |   0   0  +2  +2  +4   0  +2  -2   0  +4  +2  -2   0   0  -2  -2 
              d |   0  -2   0  -2  -2  +4  +2   0   0  +2  -4  -2  -2   0  -2   0 
              e |   0  -2  -2  +4  -2   0   0  +2  -2   0   0  +2   0  -2  -2  -4 
              f |   0   0   0   0   0   0  +4  +4  +2  -2  +2  -2  +2  -2  -2  +2 
              
 Note that the NL value has already been subtracted by 8 for convenience in computing the bias.
 
 (b)
 
 The approximation uses S1_4, S2_1, S3_1, in total 3 S-boxes. The (a,b) values are (1,8), (1,8), (8,10),
 respectively. (Better use the S-box graph on the book if you want to show it clearly)
 
 The bias is +- 1/16.
 
 (c)
 
 Just write it similar to Algorithm 4.2. Replace corresponding parts. `SPN.linear_attack()` implements
 this. The keys and plaintext is completely random, as you want X_16, the plaintext bit, to be
 equally distributed on {0,1}.
 
 (d)
 
` SPN.linear_trial()` performs the linear attack 50 times. At T = 150, it has about 50% potential
to find the correct key, at T = 400, it almost doesn't fail.
 