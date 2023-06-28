clear;clc;close all;
dataDir='..\..\..\Gartner\Generic Fixed Tilt PV Rack Vibration Test Raw Data 2017\';
files=dir(dataDir);
files(1:3)=[];

%% plot data
for i=1:length(files)
    acc=readtable(strcat(dataDir,files(i).name));
    plotAcc(acc,files(i).name);
end

%%
function plotAcc(acc,fileName)
time=acc.Var1; %unit: second
accX=acc.Var2; %unit: g
accY=acc.Var3;
accZ=acc.Var4;

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
fileout=strcat('.\dampingOutput\',fileName(1:end-4),'.');
print(hfig,[fileout,'tif'],'-r300','-dtiff');
end