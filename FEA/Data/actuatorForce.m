close all; clear; clc;
nodeDisp=load('test6PnodeDisp.out');
force=nodeDisp(:,1)/4448.2216153;
disp=sqrt(nodeDisp(:,2).^2+nodeDisp(:,4).^2)*39.3701;
plot(disp,force)
xlabel('Disp/in')
ylabel('Force/kip')
grid on