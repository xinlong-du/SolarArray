close all;clear;clc;
CB_Nx=load('CB_Nx300.out');
plot(CB_Nx(:,5),CB_Nx(:,1))
xlim([0 1.8])
ylim([0 30])
xticks(0:0.2:1.8)
yticks(0:2:30)
xlabel('Twist angle at midspan (rad)')
ylabel('Compressive force (kN)')