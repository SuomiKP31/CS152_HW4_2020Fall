from bitarray import bitarray
import random

class LPT:
    def __init__(self, sbox):
        self.sbox = sbox
        self.sbox_len = len(sbox)
        self.lat = []
        self.ndt = []


    def linearApprox(self,input_int,output_int):
        total = 0
        # range over the input
        for x in range(self.sbox_len):
            # for each possible X value
            input_masked = x & input_int # mask by a
            output_masked = self.sbox[x] & output_int # mask by b
            if (bin(input_masked).count("1") - bin(output_masked).count("1")) % 2 == 0:
                total += 1
                # get the number of results compared to 8/16
        result = total - (self.sbox_len // 2)
        if result > 0:
            result = "+" + str(result)
        else:
            result = str(result)

        return result
    def calculateND(self, a, b):
        total = 0
        for x in range(self.sbox_len):
            x_star = a ^ x
            y = self.sbox[x]
            y_star = self.sbox[x_star]
            if b == y ^ y_star:
                total += 1
        return str(total)
    def output_lat(self):
        import sys
        sys.stdout.write("    | ")
        for i in range(self.sbox_len):
            sys.stdout.write(hex(i)[2:].rjust(3) + " ")
        print
        print(" " + "-" * (self.sbox_len * 4 + 4))
        for row in range(self.sbox_len): # rows, i.e. a mask
            sys.stdout.write(hex(row)[2:].rjust(3) + " | ")
            row_lat = []
            # cols, i.e. b mask
            for col in range(self.sbox_len):
                # print the linear approx
                lap = self.linearApprox(row, col)
                sys.stdout.write(lap.rjust(3) + " ")
                row_lat.append(int(lap))
            self.lat.append(row_lat)
            print
    def output_dat(self):
        import sys
        sys.stdout.write("    | ")
        for i in range(self.sbox_len):
            sys.stdout.write(hex(i)[2:].rjust(3) + " ")
        print
        print(" " + "-" * (self.sbox_len * 4 + 4))
        for row in range(self.sbox_len): # a'
            sys.stdout.write(hex(row)[2:].rjust(3) + " | ")
            row_dat = []
            for col in range(self.sbox_len): # b'
                # print ND(a',b')
                dnd = self.calculateND(row,col)
                sys.stdout.write(dnd.rjust(3) + " ")
                row_dat.append(int(dnd))
            self.ndt.append(row_dat)
            print
class SPN:
    def __init__(self,sbox):
        self.sbox = sbox
        self.sbox_len = len(sbox)
        self.rbox = self.reverse_sbox()
        self.keys = self.keygen(5)
        self.printkey()

    def reverse_sbox(self):
        rbox = [0 for x in range(self.sbox_len)]
        for i in range(self.sbox_len):
            rbox[self.sbox[i]] = i
        return rbox

    def rand_gen_plain(self):
        # generate 4 int in [0,15] as plaintext or keys
        plain = []
        for i in range(4):
            plain.append(random.randint(0, 15))
        return plain
    def keygen(self,rounds):
        keys = []
        for i in range(rounds):
            keys.append(self.rand_gen_plain())
        return keys
    def printkey(self):
        print("Keys:")
        for i in range(len(self.keys)):
            print("Key {0}: {1}".format(i,self.keys[i]))
    def addkey(self,round,w):
        next_u = []
        for i in range(4):
            next_u.append(w[i] ^ self.keys[round][i])
        return next_u
    def substitution(self,u):
        v = []
        for i in range(4):
            v.append(self.sbox[u[i]])
        return v
    def permutation(self,v):
        w = []
        v_bitarray = []
        for byte in v:
            ba = bitarray()
            ba.frombytes(chr(byte))
            v_bitarray.append(ba)
        for i in range(4):
            w_byte = bitarray()
            for j in range(4):
                w_byte.append(v_bitarray[j][i+4])
            w.append(int(w_byte.to01(),2))
        return w
    def round_encryption(self,plain,round):
        u = self.addkey(round, plain)
        # print("Key : {0}, next u is {1}".format(self.keys[round], next_u))
        v = self.substitution(u)
        #print("Substitution Yields {0}".format(v))
        w = self.permutation(v)
        #print("Permutation Yields {0}".format(w))

        return w
    def encryption(self,plain):
        #print("Plaintext{0}",plain)
        #print("Key : {0}, next u is {1}".format(self.keys[0], u1))
        for i in range(len(self.keys)-2):
            plain = self.round_encryption(plain,i)
        u4 = self.addkey(3,plain)
        v4 = self.substitution(u4)
        y = self.addkey(4,v4)
        return y

    def linear_attack(self,T):
        counter = []
        for l1 in range(16):
            row = []
            for l2 in range(16):
                row.append(0)
            counter.append(row)
        for t in range(T):
            x = self.rand_gen_plain()
            y = self.encryption(x)
            for l1 in range(16):
                for l2 in range(16):
                    v41 = l1 ^ y[0]
                    v43 = l2 ^ y[2]
                    u41 = self.rbox[v41]
                    u43 = self.rbox[v43]
                    x16 = bitarray()
                    x16.frombytes(chr(x[3]))
                    x16 = x16.tolist()[7]
                    u1 = bitarray()
                    u1.frombytes(chr(int(u41)))
                    u1 = u1.tolist()[4]
                    u2 = bitarray()
                    u2.frombytes(chr(u43))
                    u2 = u2.tolist()[4]
                    z = x16 ^ u1 ^ u2
                    if z == False:
                        counter[l1][l2] += 1
        m = -1
        maxkey = [1,1]
        for l1 in range(16):
            for l2 in range(16):
                c = abs(counter[l1][l2]-T/2)
                if (c > m):
                    m = c
                    maxkey = [l1,l2]
        # print(maxkey)
        return maxkey

    def differential_attack(self,T,x_prime):
        # x_prime needs to be a dedicated input-xor
        counter = []
        for l1 in range(16):
            row = []
            for l2 in range(16):
                row.append(0)
            counter.append(row)
        for t in range(T):
            x = self.rand_gen_plain()
            x_star = [0 for byte in x]
            for i in range(4):
                x_star[i] = x[i] ^ x_prime[i]
            y = self.encryption(x)
            y_star = self.encryption(x_star)
            if (y[2] == y_star[2]) and (y[3] == y_star[3]):
                for l1 in range(16):
                    for l2 in range(16):
                        v41 = l1 ^ y[0]
                        v42 = l2 ^ y[1]
                        u41 = self.rbox[v41]
                        u42 = self.rbox[v42]
                        v41_star = l1 ^ y_star[0]
                        v42_star = l2 ^ y_star[1]
                        u41_star = self.rbox[v41_star]
                        u42_star = self.rbox[v42_star]
                        u41_prime = u41 ^ u41_star
                        u42_prime = u42 ^ u42_star
                        if u41_prime == 1 and u42_prime == 1:
                            counter[l1][l2] += 1
        max = -1
        maxkey = [1,1]
        for l1 in range(16):
            for l2 in range(16):
                if (counter[l1][l2] > max):
                    max = counter[l1][l2]
                    maxkey = [l1,l2]
        # print(maxkey)
        return maxkey

    def linear_trial(self, n, T):
        success = 0.0
        for i in range(n):
            # proceed on n rounds of attack. Switch keys on end of each round
            result = self.linear_attack(T)
            if (result == [self.keys[4][0], self.keys[4][2]]):
                print("Linear attack {0} success!".format(i))
                success += 1
            else:
                print("Linear attack {0} fail!".format(i))
            self.key = self.keygen(5)
        print("Linear attack at T = {0} has the success rate of {1}".format(T,success/n))
    def differential_trial(self,n,T):
        success = 0.0
        for i in range(n):
            # proceed on n rounds of attack. Switch keys on end of each round
            result = self.differential_attack(T,[9,0,0,9])
            if (result == [self.keys[4][0], self.keys[4][1]]):
                print("Differential attack {0} success!".format(i))
                success += 1
            else:
                print("Differential attack {0} fail!".format(i))
            self.key = self.keygen(5)
        print("Differential attack at T = {0} has the success rate of {1}".format(T, success / n))