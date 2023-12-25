close all;clear;clc;
ltbAISI=11.6; %length=262 in
yldAISI=93;   %Fy=55 ksi

%% simulation data
purlin1N=load('solarPurlin1N.out');
purlin2N=load('solarPurlin2N.out');

% panel1N=load('solarPanel1N.out');
% panel2N=load('solarPanel2N.out');
% panel1N=load('solarPanel1Nstiff0.1.out');
% panel2N=load('solarPanel2Nstiff0.1.out');
panel1N=load('solarPanel1Nyield.out');
panel2N=load('solarPanel2Nyield.out');

hfig=figure;
plot([-1 1],[ltbAISI ltbAISI],'b-','LineWidth',1)
hold on
plot([-1 1],[yldAISI yldAISI],'b--','LineWidth',1)

plot(purlin1N(:,5),purlin1N(:,1),'k-')
%plot(purlin2N(:,5),purlin2N(:,1),'r--')
plot(panel1N(:,5),panel1N(:,1),'k-o','MarkerIndices',1:100:length(panel1N))
plot(panel2N(:,5),panel2N(:,1),'r--*','MarkerIndices',1:100:length(panel2N))

xlim([-0.1 0])
% ylim([0 20])
% xticks(-1.5:0.25:1.5)
% yticks(0:2:20)
set(gca,'FontSize',8,'FontName','Times New Roman')
legend({'LTB AISI','Yield AISI','Single purlin','Purlin 1 with panel','Purlin 2 with panel'},...
    'FontSize',8,'FontName','Times New Roman')
legend('Location','west')
xlabel('Twist angle at midspan (rad)')
ylabel('Bending moment (kip-in)')

% save figure
figWidth=3.5;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\figures\purlinBuckleN.';
print(hfig,[fileout,'tif'],'-r300','-dtiff');