close all;clear;clc;

purlin1TwN=load('solarPurlin1PinTwNdispYN.out');
purlin1TwP=load('solarPurlin1PinTwPdispYN.out');
purlin2TwN=load('solarPurlin2PinTwNdispYN.out');
purlin2TwP=load('solarPurlin2PinTwPdispYN.out');

%%
figure
plot(purlin1TwN(:,3)/25.4,purlin1TwN(:,1),'k','LineWidth',1.0)
hold on
plot(purlin2TwN(:,3)/25.4,purlin2TwN(:,1),'r--','LineWidth',1.0)

%plot(purlin1TwP(:,3)/25.4,purlin1TwP(:,1),'b','LineWidth',1.0)
%plot(purlin2TwP(:,3)/25.4,purlin2TwP(:,1),'m--','LineWidth',1.0)

%legend('Neg. twist, purlin1','Neg. twist, purlin2','Pos. twist, purlin1','Pos. twist, purlin2')
legend('Neg. twist','Pos. twist')
xlabel('Vertical disp. (in)')
ylabel('Force on one purlin (kip)')
grid on

%%
figure
plot(purlin1TwN(:,4),purlin1TwN(:,1),'k','LineWidth',1.0)
hold on
plot(purlin2TwN(:,4),purlin2TwN(:,1),'r--','LineWidth',1.0)

plot(purlin1TwP(:,4),purlin1TwP(:,1),'b','LineWidth',1.0)
plot(purlin2TwP(:,4),purlin2TwP(:,1),'m--','LineWidth',1.0)

legend('Neg. twist, purlin1','Neg. twist, purlin2','Pos. twist, purlin1','Pos. twist, purlin2')
xlabel('Lateral disp. (mm)')
ylabel('Force on one purlin (kip)')
grid on

%%
figure
plot(purlin1TwN(:,5),purlin1TwN(:,1),'k','LineWidth',1.0)
hold on
plot(purlin2TwN(:,5),purlin2TwN(:,1),'r--','LineWidth',1.0)

plot(purlin1TwP(:,5),purlin1TwP(:,1),'b','LineWidth',1.0)
plot(purlin2TwP(:,5),purlin2TwP(:,1),'m--','LineWidth',1.0)

legend('Neg. twist, purlin1','Neg. twist, purlin2','Pos. twist, purlin1','Pos. twist, purlin2')
xlabel('Twist (rad)')
ylabel('Force on one purlin (kip)')
xlim([-0.02 0.02])
grid on