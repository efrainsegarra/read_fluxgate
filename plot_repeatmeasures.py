import numpy as np
import matplotlib.pyplot as plt


def readData(file,struct):
    it = -1
    with open(file,"r") as f:
        for line in f:
            if 'file' in line: 
                it += 1
                continue
            parse = line.strip().split()
            Bz = float(parse[0])/1e6
            
            struct[it].append(Bz)

def reformat(struct):
    for i in range(len(struct)):
        struct[i] = np.asarray(struct[i])

def makeHist(struct):
    c = []
    b = []
    av = []
    std = []
    for i in range(len(struct)):
        av.append( np.average(struct[i]) )
        std.append( np.std(struct[i]) )
        counts, bins = np.histogram(struct[i],bins=16)
        c.append(counts)
        b.append(bins)
    return c,b,av,std


Bz    = [[],[],[],[],[],[],[],[],[],[]] 
readData("execs/repeated_measurements.txt"   ,Bz)
c,b,av,std = makeHist(Bz)

plt.figure(1)
plt.stairs(c[0],b[0],color='blue')
plt.stairs(c[1],b[1],color='red')
plt.stairs(c[2],b[2],color='green')

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel(r'$B_z$ uncorrected ($\mu$T)',fontsize=20)
plt.ylabel(r'Counts (a.u.)',fontsize=20)
#plt.legend(numpoints=1,loc='best',fontsize=15)
plt.tight_layout()
plt.savefig('repeatmeasures.pdf',bbox_inches='tight')

plt.figure(2)
#print(av)
counts,bins = np.histogram(av,bins=3)
plt.stairs(counts,bins)

plt.show()
