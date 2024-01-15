close all;clear;clc;
ltbAISI=11.6; %length=262 in
yldAISI=93;   %Fy=55 ksi

%% simulation data without panels
purlin1N=load('solarPurlin1N.out');
purlin2N=load('solarPurlin2N.out');
purlin1P=load('../LateralBuckling/8CS2.5x059Mz262inP.out');
%purlin2P=load('solarPurlin2P.out');

% panel1N=load('solarPanel1N.out');
% panel2N=load('solarPanel2N.out');
% panel1N=load('solarPanel1Nstiff0.1.out');
% panel2N=load('solarPanel2Nstiff0.1.out');

%% plot for the positive moment case
panel1twNmoP=load('solarPanel1yield2OffsetPinTwNmoP.out');
panel2twNmoP=load('solarPanel2yield2OffsetPinTwNmoP.out');
panel1twPmoP=load('solarPanel1yield2OffsetPinTwPmoPdc2.out');
panel2twPmoP=load('solarPanel2yield2OffsetPinTwPmoPdc2.out');

hfig=figure;
plot([-1 1],[ltbAISI ltbAISI],'b-','LineWidth',1)
hold on
plot([-1 1],[yldAISI yldAISI],'b--','LineWidth',1)

plot(purlin1N(:,5),purlin1N(:,1),'m-')
plot(purlin1P(:,5),purlin1P(:,1),'m-')

plot(panel1twNmoP(1:866,5),panel1twNmoP(1:866,1),'k-')
plot(panel2twNmoP(1:866,5),panel2twNmoP(1:866,1),'r--')
plot(panel1twPmoP(:,5),panel1twPmoP(:,1),'k-')
plot(panel2twPmoP(:,5),panel2twPmoP(:,1),'r--')

xlim([-0.3 0.3])
% ylim([0 20])
xticks(-0.3:0.1:0.3)
% yticks(0:2:20)
%set(gca,'FontSize',8,'FontName','Times New Roman')
legend({'LTB','Yield','Single purlin','','Purlin 1 with modules','Purlin 2 with modules'})
legend('Location','west')
legend boxoff
xlabel('Twist angle at midspan (rad)')
ylabel('Bending moment (kip-in)')

% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\figures\purlinBuckle2offsetPinMoP.';
print(hfig,[fileout,'tif'],'-r300','-dtiff');

%% plot for the negative moment case
panel1twNmoN=load('solarPanel1yield2OffsetPinTwNmoN.out');
panel2twNmoN=load('solarPanel2yield2OffsetPinTwNmoN.out');
panel1twPmoN=load('solarPanel1yield2OffsetPinTwPmoN.out');
panel2twPmoN=load('solarPanel2yield2OffsetPinTwPmoN.out');

hfig=figure;
plot([-1 1],[ltbAISI ltbAISI],'b-','LineWidth',1)
hold on
plot([-1 1],[yldAISI yldAISI],'b--','LineWidth',1)

plot(purlin1N(:,5),purlin1N(:,1),'m-')
plot(purlin1P(:,5),purlin1P(:,1),'m-')

plot(panel1twNmoN(1:769,5),panel1twNmoN(1:769,1),'k-')
plot(panel2twNmoN(1:769,5),panel2twNmoN(1:769,1),'r--')
plot(panel1twPmoN(1:953,5),panel1twPmoN(1:953,1),'k-')
plot(panel2twPmoN(1:953,5),panel2twPmoN(1:953,1),'r--')

xlim([-0.3 0.3])
% ylim([0 20])
xticks(-0.3:0.1:0.3)
% yticks(0:2:20)
%set(gca,'FontSize',8,'FontName','Times New Roman')
legend({'LTB','Yield','Single purlin','','Purlin 1 with modules','Purlin 2 with modules'})
legend('Location','west')
legend boxoff
xlabel('Twist angle at midspan (rad)')
ylabel('Bending moment (kip-in)')

% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\figures\purlinBuckle2offsetPinMoN.';
print(hfig,[fileout,'tif'],'-r300','-dtiff');