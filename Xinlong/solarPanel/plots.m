close all;clear;clc;
ltbAISI=13.9; %length=262 in

%% simulation data
purlin1N=load('../LateralBuckling/100CS75x3Mz6669mmNnoT.out');

panel1N=load('solarPanel1yield2OffsetPinTwNmoP.out');
panel2N=load('solarPanel2yield2OffsetPinTwNmoP.out');

hfig=figure;
plot([-1 1],[ltbAISI ltbAISI],'b-','LineWidth',1)
hold on
plot(purlin1N(:,5),purlin1N(:,1),'k-')
plot(panel1N(:,5),panel1N(:,1),'k-o','MarkerIndices',1:100:length(panel1N))
plot(panel2N(:,5),panel2N(:,1),'r--*','MarkerIndices',1:100:length(panel2N))

% xlim([-0.1 0])
% ylim([0 20])
% xticks(-1.5:0.25:1.5)
% yticks(0:2:20)
set(gca,'FontSize',8,'FontName','Times New Roman')
legend({'LTB AISI','Single purlin TwN','Purlin 1 with panel','Purlin 2 with panel'},...
    'FontSize',8,'FontName','Times New Roman')
legend('Location','west')
xlabel('Twist angle at midspan (rad)')
ylabel('Bending moment (kip-in)')

% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\figures\purlinBuckle2offsetPinTwNmoP.';
print(hfig,[fileout,'tif'],'-r300','-dtiff');