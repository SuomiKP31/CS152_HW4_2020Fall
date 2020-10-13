from lpt import LPT
from lpt import SPN
from bitarray import bitarray
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Q3
    sbox = [8, 4, 2, 1, 0xc, 6, 3, 0xd, 0xa, 5, 0xe, 7, 0xf, 0xb, 9, 0]

    lpt = LPT(sbox)
    lpt.output_lat()
    for i in range(16):
        for j in range(16):
            if abs(lpt.lat[i][j]) >= 4 and i != 0 and j != 0:
                print("{0},{1} has a bias of {2}".format(i,j,lpt.lat[i][j]/16.0))

    # Q3D
    spn = SPN(sbox)
    #spn.linear_trial(50,3000)

    #Q4
    sbox = [0xe, 2, 1, 3, 0xd, 9, 0, 6, 0xf, 4, 5, 0xa, 8, 0xc, 7, 0xb]
    lpt = LPT(sbox)
    lpt.output_dat()
    
    for i in range(16):
        for j in range(16):
            nd = lpt.ndt[i][j]
            if nd == 6:
                print("{0} has the Rp of 3/8".format((i,j)))
            elif nd == 4:
                print("{0} has the Rp of 1/4".format((i, j)))

    spn = SPN(sbox)
    spn.differential_trial(100,400)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
