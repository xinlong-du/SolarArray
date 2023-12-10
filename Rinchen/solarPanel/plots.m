close all;clear;clc;
CB_MzP=load('solarPurlin1N.out');
CB_MzN=load('solarPurlin2N.out');
plot(CB_MzN(:,5),CB_MzN(:,1),'k-')
hold on
plot(CB_MzP(:,5),CB_MzP(:,1),'r--')
xlim([-1 1])
% ylim([0 20])
% xticks(-1.5:0.25:1.5)
% yticks(0:2:20)
xlabel('Twist angle at midspan (rad)')
ylabel('Bending moment (kip-in)')