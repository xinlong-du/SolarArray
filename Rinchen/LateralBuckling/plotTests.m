close all;clear;clc;

purlinTwP=load('6CS2.5x065L262inFY.out');

figure
plot(purlinTwP(:,3)/25.4,purlinTwP(:,1),'k','LineWidth',1.0)
xlabel('Vertical disp. (in)')
ylabel('Force on one purlin (kip)')
grid on

figure
plot(purlinTwP(:,4)/25.4,purlinTwP(:,1),'k','LineWidth',1.0)
xlabel('Lateral disp. (in)')
ylabel('Force on one purlin (kip)')
grid on

figure
plot(purlinTwP(:,5),purlinTwP(:,1),'k','LineWidth',1.0)
xlabel('Twist at midspan (rad)')
ylabel('Force on one purlin (kip)')
grid on