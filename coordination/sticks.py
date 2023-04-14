import numpy as np
import matplotlib.pyplot as plt
import pdb
import seaborn as sns
from matplotlib.gridspec import GridSpec

joints = ['hip','knee','ankle','foot']
colors = ['tab:blue','tab:orange','tab:green','tab:red']


def makeStickFigure(x,y,dist,angles,dur,\
        fName,cyc_angles,peaks,swing_idx,scale,dest,num_steps=10):
    plt.clf()
    fig = plt.figure(figsize=(20,16))
    gs = GridSpec(3,6,figure=fig,hspace=0.5,wspace=0.5)
    ax = fig.add_subplot(gs[0,:])

    stance_col = 'tab:grey'
    swing_col = 'tab:red'
    ### Plot sticks
    t = np.linspace(0,dur,len(x))[::-1]
    x = x * dist.max(1).reshape(-1,1)/scale + t.reshape(-1,1)
    x = x - (x[:,[-1]] - t.reshape(-1,1))
    plt.plot(x.T,y.T+0.1,'tab:grey',linewidth=0.25)
    plt.plot(x[swing_idx,:].T,y[swing_idx,:].T+0.1,'tab:red',linewidth=0.25)
    plt.stem(t,-0.05*np.ones(len(t)),'tab:grey',markerfmt=" ",basefmt=" ")
    plt.stem(t[swing_idx],-0.05*np.ones(len(swing_idx)),'tab:red',markerfmt=" ",basefmt=" ")

    plt.axis('off')
    plt.ylim([-0.1,1.1])
    t = np.linspace(0,dur,len(angles[0]))[::-1]

    ### Plot instantaneous angles
    ax = fig.add_subplot(gs[1,:3])
#    pdb.set_trace()
    for i in range(len(joints)):
        sns.lineplot(x=t,y=angles[i],label=joints[i])
#    plt.plot(t[peaks],angles[-1][peaks],'o')
    plt.ylim([-5,185])
    plt.xlim([-0.1,dur+1])
    plt.xlabel("Time")
    plt.legend()

    ### Plot angle densities
    ax = fig.add_subplot(gs[1,3:])
    norm=None
    B = 36
    for i in range(len(joints)):
        sns.distplot(angles[i],bins=B,label=joints[i],fit=norm)
    plt.ylim([-0.01,0.11])
    plt.xticks(np.arange(0,190,30))
    ax.legend()
    plt.xlabel("Joint Angle in degrees")

    ### Plot cycle angles per joint
    idx = np.random.permutation(num_steps)
    cyc_angles = [cyc_angles[i][idx] for i in range(4)]
    for i in range(4):
        ax = fig.add_subplot(gs[2,i])
        mAng = cyc_angles[i].mean(0)
        sAng = cyc_angles[i].std(0)
        xAxis = np.linspace(0,1,len(mAng))
        plt.fill_between(xAxis,mAng-sAng,mAng+sAng,alpha=0.2,color=colors[i])
        plt.plot(xAxis,mAng,label=joints[i],color=colors[i])
        plt.ylim([-5,185])
        plt.title(joints[i])

#    pdb.set_trace()
    cyc_angles = np.array(cyc_angles)
    minAng = cyc_angles.min(2)
    maxAng = cyc_angles.max(2)
    diffAng = maxAng - minAng
    ax = fig.add_subplot(gs[2,i+1:])
    plt.boxplot(diffAng.T,showfliers=True)
    plt.xticks(np.arange(5),['']+joints)
    plt.title("Max-Min angle per cycle")
    plt.ylim([-10,130])

    plt.savefig(dest+fName.replace('.avi','_lateral.pdf'))

    return
