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
seleData=cell(6,1);
for i=1:length(seleFiles)
    acc=readtable(strcat(dataDir,'Vib2017-08- ',seleFiles{i},'.csv'));
    seleData{i}=acc;
    time=acc.Var1; %unit: second
    accX=acc.Var2; %unit: g
    accY=acc.Var3;
    accZ=acc.Var4;
    plotAcc(time,accX,accY,accZ,strcat(seleFiles{i},'.csv'));
end

%% calculate damping ratio 17(182657)
time=seleData{1}.Var1;
accZ=seleData{1}.Var4;
figure
plot(time,accZ)

n=4; %number of cycles
pp1=0.008318-(-0.01203);
ppn=0.006067-(-0.004601);
dampingRatio1=1/(2*pi*n)*log(pp1/ppn);

%% calculate damping ratio 17(182747)
time=seleData{2}.Var1;
accZ=seleData{2}.Var4;
figure
plot(time,accZ)

n=5; %number of cycles
pp1=0.0088-(-0.007823);
ppn=0.00543-(-0.002988);
dampingRatio2=1/(2*pi*n)*log(pp1/ppn);

%% calculate damping ratio 17(183334)
time=seleData{3}.Var1;
accZ=seleData{3}.Var4;
figure
plot(time,accZ)

n=4; %number of cycles
pp1=0.5919-(-0.4969);
ppn=0.1652-(-0.1339);
dampingRatio3=1/(2*pi*n)*log(pp1/ppn);

%% calculate damping ratio 18(110257)
time=seleData{4}.Var1;
accZ=seleData{4}.Var4;
figure
plot(time,accZ)

n=4; %number of cycles
pp1=0.1574-(-0.1204);
ppn=0.04195-(-0.04712);
dampingRatio4=1/(2*pi*n)*log(pp1/ppn);

%% calculate damping ratio 18(111123)
time=seleData{5}.Var1;
accZ=seleData{5}.Var4;
figure
plot(time,accZ)

n=10; %number of cycles
pp1=0.02417-(-0.02038);
ppn=0.007971-(-0.006178);
dampingRatio5=1/(2*pi*n)*log(pp1/ppn);

%% calculate damping ratio 18(111419)
time=seleData{6}.Var1;
accY=seleData{6}.Var3;
figure
plot(time,accY)

n=8; %number of cycles
pp1=0.09457-(-0.06537);
ppn=0.009734-(-0.00889);
dampingRatio6=1/(2*pi*n)*log(pp1/ppn);

%%
function plotAcc(time,accX,accY,accZ,fileName)
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