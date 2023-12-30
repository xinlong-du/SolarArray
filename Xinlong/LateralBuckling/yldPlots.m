close all;clear;clc;
%% obtain yield strength from plot, which is about 80 kip-in
CB_Mz=load('yld100CS75x3Mz6669mmNnoT.out');
plot(CB_Mz(:,3),CB_Mz(:,1))
xlabel('Y displacement at midspan (mm)')
ylabel('Bending moment (kip-in)')