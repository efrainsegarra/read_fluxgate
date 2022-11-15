import numpy as np
import matplotlib.pyplot as plt

OFFSET = 5.8 # [cm] -- fluxgate at "0" is really 5.8 cm inside the MSR
OFFSET = 0.

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
            

            if dist not in struct.keys():
                struct[dist] = {} # create nested dict
                struct[dist][ang] = [Bx,By,Bz]
            else:
                struct[dist][ang] = [Bx,By,Bz]

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


lowerguide_data_highres = {}
lowerguide_data_initial = {}
lowerguide_data_amsoff  = {}

readData("execs/lowerguide_highresscan.txt",lowerguide_data_highres)
readData("execs/first_measure.txt",lowerguide_data_initial)
readData("execs/lowerguide_amsoff.txt",lowerguide_data_amsoff)

x,Bx,By,Bz = fixOffset(lowerguide_data_highres)
x_amsoff,Bx_amsoff,By_amsoff,Bz_amsoff = fixOffset(lowerguide_data_amsoff)
x_init,Bx_init,By_init,Bz_init = fixOffset(lowerguide_data_initial)


BS = [Bz,By,Bx]
cols = ['blue','red','green']
lab = [r'$B_z$ [$\mu$T]',r'$B_y$ [$\mu$T]',r'$B_x$ [$\mu$T]']
savelab = ['Bz','By','Bx']

# Plot lowerguide with AMS on using high res scan with all the components
plt.figure(0)
plt.errorbar(x,Bz,color='blue',linestyle='--',marker='o',markersize=7,label=r'$B_z$')
plt.errorbar(x,By,color='red',linestyle='--',marker='o',markersize=7,label=r'$B_y$')
plt.errorbar(x,Bx,color='green',linestyle='--',marker='o',markersize=7,label=r'$B_x$ (no correction)')
plt.grid(True)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Distance from MSR [cm]',fontsize=20)
plt.ylabel(r'$B_i$ [$\mu$T]',fontsize=20)
plt.ylim([-0.8,6.3])
plt.xlim([-10,177])
plt.legend(numpoints=1,loc=1,fontsize=16)
plt.tight_layout()
plt.savefig("lowerguide_highres.pdf",bbox_inches='tight')

# Compare component-by-component between the initial scan and the high res scan
BS_other = [Bz_init,By_init,Bx_init]
for i in range(3):
    plt.figure(i+1)
    plt.errorbar(x,BS[i],color=cols[i],linestyle='--',marker='o',markersize=7,label=r'High-res scan')
    plt.errorbar(x_init,BS_other[i],color=cols[i],linestyle=':',marker='s',markersize=7,label=r'Init scan')
    plt.grid(True)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Distance from MSR [cm]',fontsize=20)
    plt.ylabel(lab[i],fontsize=20)
    plt.ylim([-0.8,6.3])
    plt.xlim([-10,177])
    plt.legend(numpoints=1,loc=1,fontsize=16)
    plt.tight_layout()
    plt.savefig("lowerguide_highres_vs_initial_%s.pdf" % savelab[i],bbox_inches='tight')

# Compare the high res scan to the one with AMS off, component by component
BS_other = [Bz_amsoff,By_amsoff,Bx_amsoff]
for i in range(3):
    plt.figure(i+4)
    plt.errorbar(x,BS[i],color=cols[i],linestyle='--',marker='o',markersize=6,label=r'High-res scan')
    plt.errorbar(x_amsoff,BS_other[i],color=cols[i],linestyle=':',marker='s',markersize=6,label=r'AMS off')
    plt.grid(True)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Distance from MSR [cm]',fontsize=20)
    plt.ylabel(lab[i],fontsize=20)
    plt.ylim([-0.8,6.3])
    plt.xlim([-10,177])
    plt.legend(numpoints=1,loc=1,fontsize=16)
    plt.tight_layout()
    plt.savefig("lowerguide_highres_vs_amsoff_%s.pdf" % savelab[i],bbox_inches='tight')


'''
plt.figure(2)
plt.errorbar(x,Bz,color='blue',linestyle='--',marker='o',markersize=7,label=r'$B_z$')
plt.errorbar(x,Bz_init,color='blue',linestyle=':',marker='s',markersize=7,label=r'$B_z + AMS_{static}$')
plt.grid(True)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Distance from MSR [cm]',fontsize=20)
plt.ylabel(r'$B_i$ [$\mu$T]',fontsize=20)
plt.ylim([-0.4,5.2])
plt.xlim([0,170])
plt.legend(numpoints=1,loc=1,fontsize=16)
plt.tight_layout()
plt.savefig("Bz_AMS_initVdynamic.pdf",bbox_inches='tight')

plt.figure(3)
plt.errorbar(x,By,color='red',linestyle='--',marker='o',markersize=7,label=r'$B_y$')
plt.errorbar(x,By_init,color='red',linestyle=':',marker='s',markersize=7,label=r'$B_y + AMS_{static}$')
plt.grid(True)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Distance from MSR [cm]',fontsize=20)
plt.ylabel(r'$B_i$ [$\mu$T]',fontsize=20)
plt.ylim([-0.4,5.2])
plt.xlim([0,170])
plt.legend(numpoints=1,loc=1,fontsize=16)
plt.tight_layout()
plt.savefig("By_AMS_initVdynamic.pdf",bbox_inches='tight')

plt.figure(4)
plt.errorbar(x,Bx,color='green',linestyle='--',marker='o',markersize=7,label=r'$B_x$ (no offset)')
plt.errorbar(x,Bx_init,color='green',linestyle=':',marker='s',markersize=7,label=r'$B_x + AMS_{static}$')
plt.grid(True)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Distance from MSR [cm]',fontsize=20)
plt.ylabel(r'$B_i$ [$\mu$T]',fontsize=20)
plt.ylim([-0.4,5.2])
plt.xlim([-10,160])
plt.legend(numpoints=1,loc=1,fontsize=16)
plt.tight_layout()
plt.savefig("Bx_AMS_initVdynamic.pdf",bbox_inches='tight')
'''
plt.show()

'''
plt.figure(2)
plt.scatter(x,By,color='red')
plt.grid(True)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Distance from MSR [cm]',fontsize=20)
plt.ylabel('By [pT]',fontsize=20)
plt.tight_layout()

plt.figure(3)
plt.scatter(x,Bx,color='green')
plt.grid(True)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Distance from MSR [cm]',fontsize=20)
plt.ylabel('Bx [pT] (no offset)',fontsize=20)
plt.tight_layout()
'''


