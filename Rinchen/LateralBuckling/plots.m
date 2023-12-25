close all;clear;clc;
capAISI=11.6; %length=262 in
%capAISI=19.5; %length=200 in
%capAISI=9.4; %length=300 in
CB_MzP=load('8CS2.5x059Mz262inP.out');
CB_MzP2=load('8CS2.5x059Mz262inPeqDOF.out'); %equal DOF of nodes 10 and 12 for all DOFs
CB_MzN=load('8CS2.5x059Mz262inN.out');
plot(CB_MzN(:,5),CB_MzN(:,1))
hold on
plot(CB_MzP(:,5),CB_MzP(:,1))
plot(CB_MzP2(:,5),CB_MzP2(:,1))
plot([-1 1],[capAISI capAISI],'k--','LineWidth',1)
xlim([-1 1])
% ylim([0 20])
% xticks(-1.5:0.25:1.5)
% yticks(0:2:20)
legend('Negative perturbation','Positive perturbation','Positive perturbation eqDOF','AISI manual')
xlabel('Twist angle at midspan (rad)')
ylabel('Bending moment (kip-in)')