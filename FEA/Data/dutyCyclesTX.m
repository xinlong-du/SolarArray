close all; clear; clc;
%% load data
filename='../../../WindAnalysis/FiguresDeg30TX/CTspdPb30.txt';
spdDura=load(filename);
duraDiv=floor(spdDura(:,2)/10);      %10 is for 10s duration of simulation data 
duraDiv=floor(duraDiv/min(duraDiv)); %the final counts should multiply 51
duraDiv=reshape(duraDiv,[10,12]);

ndLocYsAll=cell(4,1);
for i=0:30:330
    for j=2:9
        filename=strcat('./testAllcases3/dir',num2str(i),'spd',num2str(j),'nodeDisp.out');
        nodeDisp=load(filename);
        [ndLocYs]=forceDispResp(nodeDisp(251:end,:));
        for k=1:4
            ndLocYsAll{k}=[ndLocYsAll{k};repmat(ndLocYs{k},duraDiv(j+1,i/30+1),1)];
        end
    end
end

%%
[c,hist,edges,rmm,idx] = rainflow(ndLocYsAll{1}*39.37,fs); %convert m to inch

histogram('BinEdges',edges','BinCounts',51*sum(hist,2))
xlabel('Displacement range (in.)','FontSize',8,'FontName','Times New Roman')
ylabel('Cycle counts','FontSize',8,'FontName','Times New Roman')
set(gca,'YScale','log')
set(gca,'FontSize',8,'FontName','Times New Roman')

%% disp at node 1714
fs=1/0.02;
[c,hist,edges,rmm,idx] = rainflow(ndLocYsAll{1}*39.37,fs); %convert m to inch
edges2=0:0.2:2.2;
bins=51*sum(hist,2);
bins2=zeros(11,1);
for i=0:9
    bins2(i+1)=sum(bins(i*100+1:i*100+100));
end
bins2(10+1)=sum(bins(10*100+1:end));

hfig=figure;
histogram('BinEdges',edges2,'BinCounts',bins2)
xlabel('Displacement range (in.)','FontSize',8,'FontName','Times New Roman')
ylabel('Cycle counts','FontSize',8,'FontName','Times New Roman')
set(gca,'YScale','log')
set(gca,'FontSize',8,'FontName','Times New Roman')
% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\figures\nd1714Disp.';
print(hfig,[fileout,'tif'],'-r200','-dtiff');

function [ndLocYs]=forceDispResp(nodeDisp)
nodeRec=[1701:1733,1801:1833,1301:1333,1401:1433,1501:1533]';

nodeDispDiv=cell(length(nodeRec),1);
for i=1:length(nodeRec)
    nodeDispDiv{i}=nodeDisp(:,6*(i-1)+2:6*i+1);
end

%% nodal displacement
nd1714=nodeDispDiv{find(nodeRec==1714)};
nd1717=nodeDispDiv{find(nodeRec==1717)};
nd1814=nodeDispDiv{find(nodeRec==1814)};
nd1817=nodeDispDiv{find(nodeRec==1817)};

nd1714LocY=nd1714(:,3)*cos(30/180*pi)-nd1714(:,1)*sin(30/180*pi);
nd1717LocY=nd1717(:,3)*cos(30/180*pi)-nd1717(:,1)*sin(30/180*pi);
nd1814LocY=nd1814(:,3)*cos(30/180*pi)-nd1814(:,1)*sin(30/180*pi);
nd1817LocY=nd1817(:,3)*cos(30/180*pi)-nd1817(:,1)*sin(30/180*pi);

ndLocYs={nd1714LocY;nd1717LocY;nd1814LocY;nd1817LocY};
end