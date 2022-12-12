clear;clc;close all;
%windData = readtable('./Data/dataCT/station_matrix_725046.xlsx');
windData = readtable('./Data/dataCT/station_matrix_725040.xlsx');

%%
spdRaw=windData.Var3;
spd=spdRaw(8:end);
spd=cellfun(@str2num,spd,'UniformOutput',false);
spd=cell2mat(spd);

%% lognormal: do not consider wind speeds below the threshold
spd2=spd-min(spd)+1;
% method of moments
lnSpd=log(spd2);
lnTheta=mean(lnSpd);
beta=std(lnSpd);
% plot
IM=0:0.5:60;
Pf=lognpdf(IM,lnTheta,beta);
figure;
histogram(spd,30,'Normalization','pdf')
hold on
plot(IM-1+min(spd),Pf,'k-','LineWidth',1)
xlabel('Wind speed (mph)')
ylabel('PDF')

%% wind directions
dirRaw=windData.Var4;
dir=dirRaw(8:end);
dir=cellfun(@str2num,dir,'UniformOutput',false);
dir=cell2mat(dir);

figure;
histogram(dir,36,'Normalization','pdf')
xlabel('Wind direction (deg)')
ylabel('PDF')
xlim([0 360])
xticks(0:60:360)