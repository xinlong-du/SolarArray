clear;clc;close all;
%windData = readtable('./Data/dataCT/station_matrix_725046.xlsx');
windData = readtable('./Data/dataCT/station_matrix_725040.xlsx');

%%
spdRaw=windData.Var3;
spd=spdRaw(8:end);
spd=cellfun(@str2num,spd,'UniformOutput',false);
spd=cell2mat(spd);

%% lognormal: do not consider wind speeds below the threshold
methMomentsLognormal(spd);
methMomentsLognormal(spd-min(spd)+1);

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
%% lognormal: consider wind speeds below the threshold
totalHours=11*365*24;
nSmallSpd=totalHours-length(spd);
smallSpd=rand(nSmallSpd,1)*min(spd); %uniform disribution
totalSpd=[spd;smallSpd];
methMomentsLognormal(totalSpd);

%% weibull: do not consider wind speeds below the threshold
parmHat=wblfit(spd-min(spd)+1);
weibullPlot(spd-min(spd)+1,parmHat(1),parmHat(2));

parmHat=wblfit(spd);
weibullPlot(spd,parmHat(1),parmHat(2));

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

dirDiv360=dir/360;
phat = betafit(dirDiv360);
IM=0:0.01:1;
Pf=betapdf(IM,phat(1),phat(2));

figure;
histogram(dirDiv360,'Normalization','pdf')
hold on
plot(IM,Pf,'k-','LineWidth',1)
xlabel('Wind direction (deg/360)')
ylabel('PDF')

%% resovle wind speeds into two directions
spdX=spd.*sin(dir/180*pi);
spdY=spd.*cos(dir/180*pi);
figure;
scatter(spdX,spdY,'.')
xlabel('Vx (mph)')
ylabel('Vy (mph)')
axis equal

%% functions
function []=methMomentsLognormal(totalSpd)
% method of moments
lnSpd=log(totalSpd);
lnTheta=mean(lnSpd);
beta=std(lnSpd);

% plot
IM=0:0.5:60;
Pf=lognpdf(IM,lnTheta,beta);
figure;
histogram(totalSpd,'Normalization','pdf')
hold on
plot(IM,Pf,'k-','LineWidth',1)
xlabel('Wind speed (mph)')
ylabel('PDF')
end

function []=weibullPlot(totalSpd,a,b)
IM=0:0.5:60;
Pf=wblpdf(IM,a,b);
figure;
histogram(totalSpd,'Normalization','pdf')
hold on
plot(IM,Pf,'k-','LineWidth',1)
xlabel('Wind speed (mph)')
ylabel('PDF')
end