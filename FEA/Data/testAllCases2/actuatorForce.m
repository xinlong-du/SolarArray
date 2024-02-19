close all; clear; clc;
nodeDisp=load('test6PnodeDispTwist.out');
force=nodeDisp(:,1)/4448.2216153;
disp609=39.3701*nodeDisp(:,4)*cos(30/180*pi)-39.3701*nodeDisp(:,2)*sin(30/180*pi);
disp809=39.3701*nodeDisp(:,10)*cos(30/180*pi)-39.3701*nodeDisp(:,8)*sin(30/180*pi);
disp610=39.3701*nodeDisp(:,16)*cos(30/180*pi)-39.3701*nodeDisp(:,14)*sin(30/180*pi);
disp810=39.3701*nodeDisp(:,22)*cos(30/180*pi)-39.3701*nodeDisp(:,20)*sin(30/180*pi);
disp609m809=disp609-disp809;
disp610m810=disp610-disp810;
rot=disp610m810/42.0-disp609m809/42.0;
plot(rot,force)
xlabel('Twist/rad')
ylabel('Force/kip')
grid on

%% test rig
nodeDisp=load('test6PnodeDispRig.out');
force=nodeDisp(:,1)/4448.2216153;

nodeRec=[607,807,612,812,303,305,403,405]';
nodeDispDiv=cell(length(nodeRec),1);
for i=1:length(nodeRec)
    nodeDispDiv{i}=nodeDisp(:,6*(i-1)+2:6*i+1);
end

disp607=39.3701*nodeDispDiv{1}(:,3)*cos(30/180*pi)-39.3701*nodeDispDiv{1}(:,1)*sin(30/180*pi);
disp303=39.3701*nodeDispDiv{5}(:,3)*cos(30/180*pi)-39.3701*nodeDispDiv{5}(:,1)*sin(30/180*pi);

figure
plot(disp607,force)
xlabel('Disp/in')
ylabel('Force/kip')
grid on

figure
plot(disp303,force)
xlabel('Disp/in')
ylabel('Force/kip')
grid on