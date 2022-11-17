import numpy as np
import matplotlib.pyplot as plt


def readData(file,struct):
    with open(file,"r") as f:
        for line in f:
            parse = line.strip().split()
            Bz = float(parse[0])/1e6
            
            struct.append(Bz)

def reformat(struct):
    struct = np.asarray(struct)

def makeHist(struct):
    counts, bins = np.histogram(struct,bins=16)
    return counts,bins

Bz_0    = [] 
Bz_180  = [] 
readData("execs/individual_measure_0.txt"   ,Bz_0)
readData("execs/individual_measure_180.txt" ,Bz_180)

reformat(Bz_0)
reformat(Bz_180)

Bz_0_counts,Bz_0_bins       = makeHist(Bz_0)
Bz_180_counts,Bz_180_bins   = makeHist(Bz_180)


plt.figure(1)
plt.stairs(Bz_0_counts, Bz_0_bins,color='blue',label=r'0$^\circ$')
plt.stairs(Bz_180_counts, Bz_180_bins,color='red',label=r'180$^\circ$')

plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel(r'$B_z$ uncorrected ($\mu$T)',fontsize=20)
plt.ylabel(r'Counts (a.u.)',fontsize=20)
plt.legend(numpoints=1,loc='best',fontsize=15)
plt.tight_layout()
plt.savefig('offset_calibration.pdf',bbox_inches='tight')

plt.figure(2)
plt.stairs(Bz_0_counts, Bz_0_bins,color='blue')
plt.axvline(x=np.average(Bz_0),linestyle='--',color='black',label='Average')
plt.axvline(x=np.average(Bz_0)+np.std(Bz_0),linestyle='--',color='red',label=r'$\pm 1$std.')
plt.axvline(x=np.average(Bz_0)-np.std(Bz_0),linestyle='--',color='red')

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel(r'$B_z$ uncorrected ($\mu$T)',fontsize=20)
plt.ylabel(r'Counts (a.u.)',fontsize=20)
plt.legend(numpoints=1,loc='best',fontsize=12)
plt.tight_layout()
plt.savefig('individual_measurement.pdf',bbox_inches='tight')


plt.show()
