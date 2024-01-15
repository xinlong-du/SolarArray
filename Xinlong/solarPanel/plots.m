close all;clear;clc;
ltb=14.6; %length=262 in
yld=81.0;

%% simulation data of single purlin
purlin1N=load('../LateralBuckling/100CS75x3Mz6669mmNnoT.out');

%% fully restrained joints
panel1N=load('solarPanel1yield2OffsetFRTwNmoN.out');
panel2N=load('solarPanel2yield2OffsetFRTwNmoN.out');

hfig=figure;
plot([-1 1],[ltb ltb],'b-','LineWidth',1)
hold on
plot([-1 1],[yld yld],'b--','LineWidth',1)
plot(purlin1N(:,5),purlin1N(:,1),'m-')
plot(panel1N(:,5),panel1N(:,1),'k-')
plot(panel2N(:,5),panel2N(:,1),'r--')

xlim([-0.3 0])
% ylim([0 20])
% xticks(-1.5:0.25:1.5)
% yticks(0:2:20)
%set(gca,'FontSize',8,'FontName','Times New Roman')
legend({'LTB','Yield','Single purlin','Purlin 1 with modules','Purlin 2 with modules'})
legend('Location','west')
legend boxoff
xlabel('Twist angle at midspan (rad)')
ylabel('Bending moment (kip-in)')

% save figure
figWidth=3.5;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\figures\purlinBuckle2offsetFRTwNmoN.';
print(hfig,[fileout,'tif'],'-r300','-dtiff');

%% pin joints
panel1N=load('solarPanel1yield2OffsetPinTwNmoN.out');
panel2N=load('solarPanel2yield2OffsetPinTwNmoN.out');

hfig=figure;
plot([-1 1],[ltb ltb],'b-','LineWidth',1)
hold on
%plot([-1 1],[yld yld],'b--','LineWidth',1)
plot(purlin1N(:,5),purlin1N(:,1),'m-')
plot(panel1N(:,5),panel1N(:,1),'k-')
plot(panel2N(:,5),panel2N(:,1),'r--')

xlim([-0.3 0])
% ylim([0 20])
% xticks(-1.5:0.25:1.5)
% yticks(0:2:20)
%set(gca,'FontSize',8,'FontName','Times New Roman')
legend({'LTB','Single purlin','Purlin 1 with modules','Purlin 2 with modules'})
legend('Location','west')
legend boxoff
xlabel('Twist angle at midspan (rad)')
ylabel('Bending moment (kip-in)')

% save figure
figWidth=3.5;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\figures\purlinBuckle2offsetPinTwNmoN.';
print(hfig,[fileout,'tif'],'-r300','-dtiff');

%% nonlinear spring joints
panel1N=load('solarPanel1yield2OffsetPinSpringTwNmoN3.out');
panel2N=load('solarPanel2yield2OffsetPinSpringTwNmoN3.out');

hfig=figure;
plot([-1 1],[ltb ltb],'b-','LineWidth',1)
hold on
plot([-1 1],[yld yld],'b--','LineWidth',1)
plot(purlin1N(:,5),purlin1N(:,1),'m-')
plot(panel1N(:,5),panel1N(:,1),'k-')
plot(panel2N(:,5),panel2N(:,1),'r--')

xlim([-0.3 0])
% ylim([0 20])
% xticks(-1.5:0.25:1.5)
% yticks(0:2:20)
%set(gca,'FontSize',8,'FontName','Times New Roman')
legend({'LTB','Yield','Single purlin','Purlin 1 with modules','Purlin 2 with modules'})
legend('Location','west')
legend boxoff
xlabel('Twist angle at midspan (rad)')
ylabel('Bending moment (kip-in)')

% save figure
figWidth=3.5;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\figures\purlinBuckle2offsetSpringTwNmoN.';
print(hfig,[fileout,'tif'],'-r300','-dtiff');