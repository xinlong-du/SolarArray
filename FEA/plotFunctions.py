# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 16:20:46 2023

@author: xinlo
"""
import matplotlib.pyplot as plt
import matplotlib as mpl

#%% Plot parameters------------------------------------------------------------
big_fig_size = (6,10);
plt_line_width = 0.5; 
fig_font_size = 8;

#%% plot forces between purlin and mudule at joint (local system of purlin)
def localForcePlot(timeVec,nodeForces,nodeID):
    fig = plt.figure(figsize=big_fig_size)
    ax0 = fig.add_subplot(611)
    ax1 = fig.add_subplot(612)
    ax2 = fig.add_subplot(613)
    ax3 = fig.add_subplot(614)
    ax4 = fig.add_subplot(615)
    ax5 = fig.add_subplot(616)
    plt.rc('xtick', labelsize=fig_font_size)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=fig_font_size)    # fontsize of the tick labels
    ax0.tick_params(direction="in")
    ax1.tick_params(direction="in")
    ax2.tick_params(direction="in")
    ax3.tick_params(direction="in")
    ax4.tick_params(direction="in")
    ax5.tick_params(direction="in")
    ax0.plot(timeVec,nodeForces[:,0]*0.0002248, linewidth=plt_line_width)
    ax1.plot(timeVec,nodeForces[:,1]*0.0002248, linewidth=plt_line_width)
    ax2.plot(timeVec,nodeForces[:,2]*0.0002248, linewidth=plt_line_width)
    ax3.plot(timeVec,nodeForces[:,3]*0.0007375623, linewidth=plt_line_width)
    ax4.plot(timeVec,nodeForces[:,4]*0.0007375623, linewidth=plt_line_width)
    ax5.plot(timeVec,nodeForces[:,5]*0.0007375623, linewidth=plt_line_width)
    ax0.set_ylabel('Fx (kips)',fontsize=fig_font_size)
    ax1.set_ylabel('Fy (kips)',fontsize=fig_font_size)
    ax2.set_ylabel('Fz (kips)',fontsize=fig_font_size)
    ax3.set_ylabel('Mx (kips*ft)',fontsize=fig_font_size)
    ax4.set_ylabel('My (kips*ft)',fontsize=fig_font_size)
    ax5.set_ylabel('Mz (kips*ft)',fontsize=fig_font_size)
    ax5.set_xlabel('Time (s)',fontsize=fig_font_size)
    plt.savefig('./Data/nodeForces'+nodeID+'.tif', transparent=False, bbox_inches='tight', dpi=100)

#%% plot displacements at joint (global system)
def globalDispPlot(timeVec,jointDisp,nodeID):
    fig = plt.figure(figsize=big_fig_size)
    ax0 = fig.add_subplot(611)
    ax1 = fig.add_subplot(612)
    ax2 = fig.add_subplot(613)
    ax3 = fig.add_subplot(614)
    ax4 = fig.add_subplot(615)
    ax5 = fig.add_subplot(616)
    plt.rc('xtick', labelsize=fig_font_size)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=fig_font_size)    # fontsize of the tick labels
    ax0.tick_params(direction="in")
    ax1.tick_params(direction="in")
    ax2.tick_params(direction="in")
    ax3.tick_params(direction="in")
    ax4.tick_params(direction="in")
    ax5.tick_params(direction="in")
    ax0.plot(timeVec,jointDisp[:,0]*39.3701, linewidth=plt_line_width)
    ax1.plot(timeVec,jointDisp[:,1]*39.3701, linewidth=plt_line_width)
    ax2.plot(timeVec,jointDisp[:,2]*39.3701, linewidth=plt_line_width)
    ax3.plot(timeVec,jointDisp[:,3], linewidth=plt_line_width)
    ax4.plot(timeVec,jointDisp[:,4], linewidth=plt_line_width)
    ax5.plot(timeVec,jointDisp[:,5], linewidth=plt_line_width)
    ax0.set_ylabel('dX (in)',fontsize=fig_font_size)
    ax1.set_ylabel('dY (in)',fontsize=fig_font_size)
    ax2.set_ylabel('dZ (in)',fontsize=fig_font_size)
    ax3.set_ylabel('rX (rad)',fontsize=fig_font_size)
    ax4.set_ylabel('rY (rad)',fontsize=fig_font_size)
    ax5.set_ylabel('rZ (rad)',fontsize=fig_font_size)
    ax5.set_xlabel('Time (s)',fontsize=fig_font_size)
    plt.savefig('./Data/nodeDisp'+nodeID+'.tif', transparent=False, bbox_inches='tight', dpi=100)

#%% plot y displacements at joint (local system of purlin)
def localYdispPlot(timeVec,nd10xxLocY,nd18xxLocY,nd11xxLocY,nd10xx,nd18xx,nd11xx):
    fig = plt.figure(figsize=(6,10))
    ax0 = fig.add_subplot(611)
    ax1 = fig.add_subplot(612)
    ax2 = fig.add_subplot(613)
    ax3 = fig.add_subplot(614)
    ax4 = fig.add_subplot(615)
    ax5 = fig.add_subplot(616)
    plt.rc('xtick', labelsize=fig_font_size)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=fig_font_size)    # fontsize of the tick labels
    ax0.tick_params(direction="in")
    ax1.tick_params(direction="in")
    ax2.tick_params(direction="in")
    ax3.tick_params(direction="in")
    ax4.tick_params(direction="in")
    ax5.tick_params(direction="in")
    ax0.plot(timeVec,nd10xxLocY*39.3701, linewidth=plt_line_width)
    ax1.plot(timeVec,nd18xxLocY*39.3701, linewidth=plt_line_width)
    ax2.plot(timeVec,nd11xxLocY*39.3701, linewidth=plt_line_width)
    ax3.plot(timeVec,(nd18xxLocY-nd10xxLocY)*39.3701, linewidth=plt_line_width)
    ax4.plot(timeVec,(nd18xxLocY-nd11xxLocY)*39.3701, linewidth=plt_line_width)
    ax5.plot(timeVec,(nd10xxLocY-nd11xxLocY)*39.3701, linewidth=plt_line_width)
    ax0.set_ylabel('N'+nd10xx+' (in)',fontsize=fig_font_size)
    ax1.set_ylabel('N'+nd18xx+' (in)',fontsize=fig_font_size)
    ax2.set_ylabel('N'+nd11xx+' (in)',fontsize=fig_font_size)
    ax3.set_ylabel('N'+nd18xx+' - N'+nd10xx+' (in)',fontsize=fig_font_size)
    ax4.set_ylabel('N'+nd18xx+' - N'+nd11xx+' (in)',fontsize=fig_font_size)
    ax5.set_ylabel('N'+nd10xx+' - N'+nd11xx+' (in)',fontsize=fig_font_size)
    ax5.set_xlabel('Time (s)',fontsize=fig_font_size)
    plt.savefig('./Data/nodeDisp'+nd10xx+'to'+nd11xx+'LocY.tif', transparent=False, bbox_inches='tight', dpi=100)
    
#%% plot force-deformation responses of springs
def springResPlot(springRes):
    fig = plt.figure(figsize=big_fig_size)
    ax0 = fig.add_subplot(321)
    ax1 = fig.add_subplot(322)
    ax2 = fig.add_subplot(323)
    ax3 = fig.add_subplot(324)
    ax4 = fig.add_subplot(325)
    ax5 = fig.add_subplot(326)
    plt.rc('xtick', labelsize=fig_font_size)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=fig_font_size)    # fontsize of the tick labels
    ax0.tick_params(direction="in")
    ax1.tick_params(direction="in")
    ax2.tick_params(direction="in")
    ax3.tick_params(direction="in")
    ax4.tick_params(direction="in")
    ax5.tick_params(direction="in")
    ax0.plot(springRes[:,1],springRes[:,7],linewidth=plt_line_width)
    ax1.plot(springRes[:,2],springRes[:,8],linewidth=plt_line_width)
    ax2.plot(springRes[:,3],springRes[:,9],linewidth=plt_line_width)
    ax3.plot(springRes[:,4],springRes[:,10],linewidth=plt_line_width)
    ax4.plot(springRes[:,5],springRes[:,11],linewidth=plt_line_width)
    ax5.plot(springRes[:,6],springRes[:,12],linewidth=plt_line_width)
    ax0.set_xlabel('Disp. (m)',fontsize=fig_font_size)
    ax0.set_ylabel('Force (N)',fontsize=fig_font_size)
    ax1.set_xlabel('Disp. (m)',fontsize=fig_font_size)
    ax1.set_ylabel('Force (N)',fontsize=fig_font_size)
    ax2.set_xlabel('Disp. (m)',fontsize=fig_font_size)
    ax2.set_ylabel('Force (N)',fontsize=fig_font_size)
    ax3.set_xlabel('Rotation (m)',fontsize=fig_font_size)
    ax3.set_ylabel('Moment (N)',fontsize=fig_font_size)
    ax4.set_xlabel('Rotation (m)',fontsize=fig_font_size)
    ax4.set_ylabel('Moment (N)',fontsize=fig_font_size)
    ax5.set_xlabel('Rotation (m)',fontsize=fig_font_size)
    ax5.set_ylabel('Moment (N)',fontsize=fig_font_size)