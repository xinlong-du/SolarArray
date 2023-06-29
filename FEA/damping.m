clear;clc;close all;
dataDir='..\..\..\Gartner\Generic Fixed Tilt PV Rack Vibration Test Raw Data 2017\';
files=dir(dataDir);
files(1:3)=[];

%% plot data
% for i=1:length(files)
%     acc=readtable(strcat(dataDir,files(i).name));
%     plotAcc(acc,files(i).name);
% end

%% select data
seleFiles={'17(182657)', '17(182747)', '17(183334)', '18(110257)', '18(111123)', '18(111419)'};
% startTime=[70, 70, 41, 691, 704, 704];
for i=3
    acc=readtable(strcat(dataDir,'Vib2017-08- ',seleFiles{i},'.csv'));
    [time,dX,dY,dZ]=plotAcc(acc,strcat(seleFiles{i},'.csv'));
end

%% calculate damping ratio
figure
plot(time,dZ)

n=6; %number of cycles
pp1=0.00909-(-0.00971);
pp6=0.003917-(-0.001333);
dampingRatio=1/2/pi/6*log(pp1/pp6);

%%
function [time,dX,dY,dZ]=plotAcc(acc,fileName)
time=acc.Var1; %unit: second
accX=acc.Var2; %unit: g
accY=acc.Var3;
accZ=acc.Var4;

vX=cumtrapz(time,accX*9.81);
vY=cumtrapz(time,accY*9.81);
vZ=cumtrapz(time,accZ*9.81);

dX=cumtrapz(time,vX);
dY=cumtrapz(time,vY);
dZ=cumtrapz(time,vZ);

hfig=figure;
subplot(3,1,1)
plot(time,accX)
xlabel('Time (s)')
ylabel('X acceleration (g)')
subplot(3,1,2)
plot(time,accY)
xlabel('Time (s)')
ylabel('Y acceleration (g)')
subplot(3,1,3)
plot(time,accZ)
xlabel('Time (s)')
ylabel('Z acceleration (g)')
% save figure
figWidth=7;
figHeight=9;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout=strcat('.\dampingOutput\',fileName(1:end-4),'1acc.');
print(hfig,[fileout,'tif'],'-r300','-dtiff');

hfig=figure;
subplot(3,1,1)
plot(time,vX)
xlabel('Time (s)')
ylabel('X velocity (m/s)')
subplot(3,1,2)
plot(time,vY)
xlabel('Time (s)')
ylabel('Y velocity (m/s)')
subplot(3,1,3)
plot(time,vZ)
xlabel('Time (s)')
ylabel('Z velocity (m/s)')
% save figure
figWidth=7;
figHeight=9;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout=strcat('.\dampingOutput\',fileName(1:end-4),'2vel.');
print(hfig,[fileout,'tif'],'-r300','-dtiff');

hfig=figure;
subplot(3,1,1)
plot(time,dX)
xlabel('Time (s)')
ylabel('X displacement (m)')
subplot(3,1,2)
plot(time,dY)
xlabel('Time (s)')
ylabel('Y displacement (m)')
subplot(3,1,3)
plot(time,dZ)
xlabel('Time (s)')
ylabel('Z displacement (m)')
% save figure
figWidth=7;
figHeight=9;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout=strcat('.\dampingOutput\',fileName(1:end-4),'3disp.');
print(hfig,[fileout,'tif'],'-r300','-dtiff');
end