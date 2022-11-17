import numpy as np
import matplotlib.pyplot as plt

OFFSET = -6 - (4.8-2.5) # [cm] -- fluxgate at "0" is really a few cm away from mu metal layer
OFFSET = 0

def readData(file,struct):
    with open(file,"r") as f:
        for line in f:
            parse = line.strip().split()
            dist = float(parse[0])
            ang = int(parse[1])
            it = int(parse[2])
            Bx = float(parse[3])
            By = float(parse[4])
            Bz = float(parse[5])
            

            if dist not in struct[it].keys():
                struct[it][dist] = {} # create nested dict
                struct[it][dist][ang] = [Bx,By,Bz]
            else:
                struct[it][dist][ang] = [Bx,By,Bz]

def fixOffset(struct):
    x = []
    Bx = []
    By = []
    Bz = []
    x_ind = 0
    for dist in struct.keys():
        x.append(int(dist) + OFFSET )
        Bx_off_up = 0
        Bx_off_do = 0
        By_off_up = 0
        By_off_do = 0
        Bz_off_up = 0
        Bz_off_do = 0
        for ang in struct[dist].keys():
            if ang == 0: 
                Bx_off_up = struct[dist][ang][0]
                By_off_up = struct[dist][ang][1]
                Bz_off_up = struct[dist][ang][2]

                Bx.append( struct[dist][ang][0] )
                By.append( struct[dist][ang][1] )
                Bz.append( struct[dist][ang][2] )

            if ang == 180: 
                Bx_off_do = struct[dist][ang][0]
                By_off_do = struct[dist][ang][1]
                Bz_off_do = struct[dist][ang][2]
        
        Bx[x_ind] -= (Bx_off_up + Bx_off_do)/2.
        By[x_ind] -= (By_off_up + By_off_do)/2.
        Bz[x_ind] -= (Bz_off_up + Bz_off_do)/2.
        x_ind+=1

    x = np.asarray(x)
    Bz = np.asarray(Bz)/1e6
    By = np.asarray(By)/1e6
    Bx = np.asarray(Bx)/1e6

    inds = x.argsort()
    x = x[inds]
    Bz = Bz[inds]
    By = By[inds]
    Bx = Bx[inds]

    return x,Bx,By,Bz


data = [{},{},{},{},{},{}]
readData("execs/calibration_flip.txt",data)
BX = []
BY = [] 
BZ = []
BX_160 = []
BY_160 = [] 
BZ_160 = []
for i in range(len(data)):
    x,Bx,By,Bz = fixOffset(data[i])
    if x[0] == 0:
        BX.append(Bx[0])
        BY.append(By[0])
        BZ.append(Bz[0])
        BX_160.append(Bx[1])
        BY_160.append(By[1])
        BZ_160.append(Bz[1])
    else:
        BX_160.append(Bx[0])
        BY_160.append(By[0])
        BZ_160.append(Bz[0])

for i in range(2):
    if i != 0:
        BX = BX_160; BY = BY_160; BZ = BZ_160
    plt.figure(i)
    print(np.std(BX),np.std(BY),np.std(BZ))
    xc,xb = np.histogram(BX,bins=5)
    yc,yb = np.histogram(BY,bins=5)
    zc,zb = np.histogram(BZ,bins=5)
    plt.stairs(xc,xb,label=r'$B_x$',color='green')
    plt.stairs(yc,yb,label=r'$B_y$',color='red')
    #plt.axvline(x=np.average(BY)-np.std(BY),linestyle='--',color='black')
    #plt.axvline(x=np.average(BY)+np.std(BY),linestyle='--',color='black')
    plt.stairs(zc,zb,label=r'$B_z$',color='blue')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel(r'$B_i$ ($\mu$T)',fontsize=20)
    plt.ylabel(r'Counts',fontsize=20)
    plt.legend(numpoints=1,loc='best',fontsize=14)
    plt.tight_layout()
    plt.savefig('offset_reproducibility_%i.pdf' % i ,bbox_inches='tight')

plt.show()
