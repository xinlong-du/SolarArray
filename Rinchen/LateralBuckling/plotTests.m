close all;clear;clc;

purlinTwP=load('6CS2.5x065L262inFY.out');
purlinTwN=load('6CS2.5x065L262inFYtwN.out');

figure
plot(purlinTwP(:,3)/25.4,purlinTwP(:,1),'k','LineWidth',1.0)
hold on
plot(purlinTwN(:,3)/25.4,purlinTwN(:,1),'r--','LineWidth',1.0)
legend('Positive initial twist','Negative initial twist')
xlabel('Vertical disp. (in)')
ylabel('Force on one purlin (kip)')
grid on

figure
plot(purlinTwP(:,4)/25.4,purlinTwP(:,1),'k','LineWidth',1.0)
hold on
plot(purlinTwN(:,4)/25.4,purlinTwN(:,1),'r--','LineWidth',1.0)
legend('Positive initial twist','Negative initial twist')
xlabel('Lateral disp. (in)')
ylabel('Force on one purlin (kip)')
grid on

figure
plot(purlinTwP(:,5),purlinTwP(:,1),'k','LineWidth',1.0)
hold on
plot(purlinTwN(:,5),purlinTwN(:,1),'r--','LineWidth',1.0)
legend('Positive initial twist','Negative initial twist')
xlabel('Twist at midspan (rad)')
ylabel('Force on one purlin (kip)')
grid on