import numpy as np
import matplotlib.pyplot as plt

OFFSET = -6 - (4.8-2.5) # [cm] -- fluxgate at "0" is really a few cm away from mu metal layer

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
upperguide_data_highres = {}
upperguide_data_amsoff  = {}

readData("execs/lowerguide_highresscan.txt",lowerguide_data_highres)
readData("execs/first_measure.txt",lowerguide_data_initial)
readData("execs/lowerguide_amsoff.txt",lowerguide_data_amsoff)
readData("execs/upperguide_highresscan.txt",upperguide_data_highres)
readData("execs/upperguide_amsoff.txt",upperguide_data_amsoff)

x,Bx,By,Bz = fixOffset(lowerguide_data_highres)
x_amsoff,Bx_amsoff,By_amsoff,Bz_amsoff = fixOffset(lowerguide_data_amsoff)
x_init,Bx_init,By_init,Bz_init = fixOffset(lowerguide_data_initial)

ux,uBx,uBy,uBz = fixOffset(upperguide_data_highres)
ux_amsoff,uBx_amsoff,uBy_amsoff,uBz_amsoff = fixOffset(upperguide_data_amsoff)

uBz_amsoff = uBz_amsoff[:-5]

BS = [Bz,By,Bx]
uBS = [uBz,uBy,uBx]
cols = ['blue','red','green']
lab = [r'$B_z$ ($\mu$T)',r'$B_y$ ($\mu$T)',r'$B_x$ ($\mu$T)']
savelab = ['Bz','By','Bx']

# Plot lowerguide with AMS on using high res scan with all the components
plt.figure(0)
plt.errorbar(x,Bz,color='blue',linestyle='--',marker='o',markersize=7,label=r'$B_z$')
plt.errorbar(x,By,color='red',linestyle='--',marker='o',markersize=7,label=r'$B_y$')
plt.errorbar(x,Bx,color='green',linestyle='--',marker='o',markersize=7,label=r'$B_x$ (no correction)')
plt.grid(True)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel(r'Distance to 1st $\mu$-metal (cm)',fontsize=20)
plt.ylabel(r'$B_i$ ($\mu$T)',fontsize=20)
plt.ylim([-0.8,6.3])
plt.xlim([-15,177])
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
    plt.xlabel(r'Distance to 1st $\mu$-metal (cm)',fontsize=20)
    plt.ylabel(lab[i],fontsize=20)
    plt.ylim([-0.8,6.3])
    plt.xlim([-15,177])
    plt.legend(numpoints=1,loc=1,fontsize=16)
    plt.tight_layout()
    plt.savefig("lowerguide_highres_vs_initial_%s.pdf" % savelab[i],bbox_inches='tight')

# Compare the high res scan to the one with AMS off, component by component
BS_other = [Bz_amsoff,By_amsoff,Bx_amsoff]
for i in range(3):
    plt.figure(i+4)
    plt.errorbar(x,BS[i],color=cols[i],linestyle='--',marker='o',markersize=6,label=r'Lower guide')
    plt.errorbar(x_amsoff,BS_other[i],color=cols[i],linestyle=':',marker='s',markersize=6,label=r'AMS off')
    plt.grid(True)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel(r'Distance to 1st $\mu$-metal (cm)',fontsize=20)
    plt.ylabel(lab[i],fontsize=20)
    plt.ylim([-0.8,6.3])
    plt.xlim([-15,177])
    plt.legend(numpoints=1,loc=1,fontsize=16)
    plt.tight_layout()
    plt.savefig("lowerguide_highres_vs_amsoff_%s.pdf" % savelab[i],bbox_inches='tight')

plt.figure(7)
plt.errorbar(ux,uBz,color='blue',linestyle='--',marker='o',markersize=7,label=r'$B_z$')
plt.errorbar(ux,uBy,color='red',linestyle='--',marker='o',markersize=7,label=r'$B_y$')
plt.errorbar(ux,uBx,color='green',linestyle='--',marker='o',markersize=7,label=r'$B_x$ (no correction)')
plt.grid(True)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel(r'Distance to 1st $\mu$-metal (cm)',fontsize=20)
plt.ylabel(r'$B_i$ ($\mu$T)',fontsize=20)
plt.ylim([-0.8,6.8])
plt.xlim([-15,177])
plt.legend(numpoints=1,loc=1,fontsize=16)
plt.tight_layout()
plt.savefig("upperguide_highres.pdf",bbox_inches='tight')

# Compare component-by-component between the initial scan and the high res scan
BS_other = [Bz,By,Bx]
for i in range(3):
    plt.figure(i+8)
    plt.errorbar(x,BS[i],color=cols[i],linestyle='--',marker='o',markersize=7,label=r'Lower guide')
    plt.errorbar(ux,uBS[i],color=cols[i],linestyle=':',marker='s',markersize=7,label=r'Upper guide')
    plt.grid(True)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel(r'Distance to 1st $\mu$-metal (cm)',fontsize=20)
    plt.ylabel(lab[i],fontsize=20)
    plt.ylim([-0.8,6.8])
    plt.xlim([-15,177])
    plt.legend(numpoints=1,loc=1,fontsize=16)
    plt.tight_layout()
    plt.savefig("lower_vs_upper_%s.pdf" % savelab[i],bbox_inches='tight')

BS_other = [uBz_amsoff,uBy_amsoff,uBx_amsoff]
for i in range(3):
    plt.figure(i+11)
    plt.errorbar(ux,uBS[i],color=cols[i],linestyle='--',marker='o',markersize=6,label=r'Upper guide')
    if i == 0:
        plt.errorbar(ux_amsoff[:-5],BS_other[i],color=cols[i],linestyle=':',marker='s',markersize=6,label=r'AMS off')
    else:
        plt.errorbar(ux_amsoff,BS_other[i],color=cols[i],linestyle=':',marker='s',markersize=6,label=r'AMS off')
    plt.grid(True)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel(r'Distance to 1st $\mu$-metal (cm)',fontsize=20)
    plt.ylabel(lab[i],fontsize=20)
    plt.ylim([-0.8,6.8])
    plt.xlim([-15,177])
    plt.legend(numpoints=1,loc=1,fontsize=16)
    plt.tight_layout()
    plt.savefig("upperguide_highres_vs_amsoff_%s.pdf" % savelab[i],bbox_inches='tight')


plt.show()
