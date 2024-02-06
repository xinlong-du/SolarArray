close all; clear; clc;
%% load data
filename='../../../WindAnalysis/FiguresDeg30TX/CTspdPb30.txt';
spdDura=load(filename);
spdVec=spdDura(:,1);
spdMat=reshape(spdVec,[10,12]);
duraDiv=floor(spdDura(:,2)/10);      %10 is for 10s duration of simulation data 
duraDiv=floor(duraDiv/min(duraDiv)); %the final counts should multiply 51
duraDiv=reshape(duraDiv,[10,12]);

ndLocYsAll=cell(8,1);
for i=0:30:330
    for j=2:9
        filename=strcat('./testAllcases3/dir',num2str(i),'spd',num2str(j),'nodeDisp.out');
        nodeDisp=load(filename);
        [ndLocYs]=forceDispResp(nodeDisp(251:end,:));
        for k=1:8
            ndLocYsAll{k}=[ndLocYsAll{k};repmat(ndLocYs{k},duraDiv(j+1,i/30+1),1)];
        end
    end
end

ndLocYsAllAll=cell(8,1);
for i=0:30:330
    for j=0:9
        filename=strcat('./testAllcases3/dir',num2str(i),'spd',num2str(j),'nodeDisp.out');
        nodeDisp=load(filename);
        [ndLocYs]=forceDispResp(nodeDisp(251:end,:));
        for k=1:8
            ndLocYsAllAll{k}=[ndLocYsAllAll{k};repmat(ndLocYs{k},duraDiv(j+1,i/30+1),1)];
        end
    end
end

%% duty cycles for bending
fs=1/0.02;
nd1814m1815=ndLocYsAllAll{3}*39.37-ndLocYsAllAll{7}*39.37;
nd1816m1817=ndLocYsAllAll{8}*39.37-ndLocYsAllAll{4}*39.37;
rot18xx=nd1814m1815/20.63-nd1816m1817/20.63;
figure
rainflow(rot18xx,fs)

[c,hist,edges,rmm,idx] = rainflow(rot18xx,fs);
figure
histogram('BinEdges',edges','BinCounts',51*sum(hist,2))
set(gca,'YScale','log')

edges2=0:0.0002:0.0052;
bins=51*sum(hist,2);
bins2=zeros(26,1);
for i=0:24
    bins2(i+1)=sum(bins(i*100+1:i*100+100));
end
bins2(25+1)=sum(bins(25*100+1:end));

hfig=figure;
histogram('BinEdges',edges2,'BinCounts',bins2)
xlabel('Displacement range (in.)','FontSize',8,'FontName','Times New Roman')
ylabel('Cycle counts','FontSize',8,'FontName','Times New Roman')
set(gca,'YScale','log')
set(gca,'FontSize',8,'FontName','Times New Roman')
xticks(0:0.0004:0.0052)
yticks([1 10 1e2 1e3 1e4 1e5 1e6 1e7 1e8])
% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\figures\bendingRot.';
print(hfig,[fileout,'tif'],'-r200','-dtiff');

%%
meanLocY=(ndLocYsAllAll{1}+ndLocYsAllAll{2}+ndLocYsAllAll{3}+ndLocYsAllAll{4})*39.37/4.0; %convert m to inch
%plot(meanLocY)
[c,hist,edges,rmm,idx] = rainflow(meanLocY,fs);
figure
histogram('BinEdges',edges'/2,'BinCounts',51*sum(hist,2))
set(gca,'YScale','log')

edges2=0:0.05:0.95;
bins=51*sum(hist,2);
bins2=zeros(19,1);
for i=0:17
    bins2(i+1)=sum(bins(i*100+1:i*100+100));
end
bins2(18+1)=sum(bins(18*100+1:end));

hfig=figure;
histogram('BinEdges',edges2,'BinCounts',bins2)
xlabel('Displacement (in.)','FontSize',8,'FontName','Times New Roman')
ylabel('Cycle counts','FontSize',8,'FontName','Times New Roman')
set(gca,'YScale','log')
set(gca,'FontSize',8,'FontName','Times New Roman')
xticks(0:0.1:1.0)
yticks([1 10 1e2 1e3 1e4 1e5 1e6 1e7 1e8])
% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\figures\bendingDisp.';
print(hfig,[fileout,'tif'],'-r200','-dtiff');

%% duty cycles for twist
nd1714m1814=ndLocYsAllAll{1}*39.37-ndLocYsAllAll{3}*39.37;
nd1717m1817=ndLocYsAllAll{2}*39.37-ndLocYsAllAll{4}*39.37;
rot1417=nd1714m1814/42.0-nd1717m1817/42.0;

[c,hist,edges,rmm,idx] = rainflow(rot1417,fs);
hfig=figure;
histogram('BinEdges',edges','BinCounts',sum(hist,2))
xlabel('Rotation range (rad)','FontSize',8,'FontName','Times New Roman')
ylabel('Cycle counts','FontSize',8,'FontName','Times New Roman')
set(gca,'YScale','log')
set(gca,'FontSize',8,'FontName','Times New Roman')
%xticks(0:0.0006:0.0036)
% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\figures\rot1417.';
print(hfig,[fileout,'tif'],'-r200','-dtiff');

twistDisp=rot1417/2.0*21.0; %displacement for one actuator
[c,hist,edges,rmm,idx] = rainflow(twistDisp,fs);
figure
histogram('BinEdges',edges'/2,'BinCounts',51*sum(hist,2))
set(gca,'YScale','log')

edges2=0:0.0015:0.02;
bins=51*sum(hist,2);
bins2=zeros(13,1);
for i=0:11
    bins2(i+1)=sum(bins(i*100+1:i*100+100));
end
bins2(12+1)=sum(bins(12*100+1:end));

hfig=figure;
histogram('BinEdges',edges2,'BinCounts',bins2)
xlabel('Displacement (in.)','FontSize',8,'FontName','Times New Roman')
ylabel('Cycle counts','FontSize',8,'FontName','Times New Roman')
set(gca,'YScale','log')
set(gca,'FontSize',8,'FontName','Times New Roman')
%xticks(0:0.1:1.0)
yticks([1 10 1e2 1e3 1e4 1e5 1e6 1e7 1e8])
% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\figures\twistDisp.';
print(hfig,[fileout,'tif'],'-r200','-dtiff');

%% disp at node 1714
fs=1/0.02;
[c,hist,edges,rmm,idx] = rainflow(ndLocYsAll{1}*39.37,fs); %convert m to inch
[cA,histA,edgesA,rmmA,idxA] = rainflow(ndLocYsAllAll{1}*39.37,fs); %convert m to inch
figure
histogram('BinEdges',edges','BinCounts',51*sum(hist,2))
set(gca,'YScale','log')
figure
histogram('BinEdges',edgesA','BinCounts',51*sum(histA,2))
set(gca,'YScale','log')

edges2=0:0.1:2.2;
bins=51*sum(hist,2);
bins2=zeros(22,1);
for i=0:20
    bins2(i+1)=sum(bins(i*50+1:i*50+50));
end
bins2(21+1)=sum(bins(21*50+1:end));

edgesA2=0:0.1:2.2;
binsA=51*sum(histA,2);
binsA2=zeros(22,1);
for i=0:20
    binsA2(i+1)=sum(binsA(i*100+1:i*100+100));
end
binsA2(21+1)=sum(binsA(21*100+1:end));

hfig=figure;
histogram('BinEdges',edgesA2,'BinCounts',binsA2)
hold on
histogram('BinEdges',edges2,'BinCounts',bins2)
xlabel('Displacement range (in.)','FontSize',8,'FontName','Times New Roman')
ylabel('Cycle counts','FontSize',8,'FontName','Times New Roman')
set(gca,'YScale','log')
set(gca,'FontSize',8,'FontName','Times New Roman')
xticks(0:0.2:2.2)
yticks([1 10 1e2 1e3 1e4 1e5 1e6 1e7 1e8])
% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\figures\nd1714DispComp.';
print(hfig,[fileout,'tif'],'-r200','-dtiff');

%% disp at node 1717
fs=1/0.02;
[c,hist,edges,rmm,idx] = rainflow(ndLocYsAll{2}*39.37,fs); %convert m to inch
[cA,histA,edgesA,rmmA,idxA] = rainflow(ndLocYsAllAll{2}*39.37,fs); %convert m to inch
figure
histogram('BinEdges',edges','BinCounts',51*sum(hist,2))
set(gca,'YScale','log')
figure
histogram('BinEdges',edgesA','BinCounts',51*sum(histA,2))
set(gca,'YScale','log')

edges2=0:0.09:2.43;
bins=51*sum(hist,2);
bins2=zeros(27,1);
for i=0:25
    bins2(i+1)=sum(bins(i*30+1:i*30+30));
end
bins2(26+1)=sum(bins(26*30+1:end));

edgesA2=0:0.09:2.43;
binsA=51*sum(histA,2);
binsA2=zeros(27,1);
for i=0:25
    binsA2(i+1)=sum(binsA(i*90+1:i*90+90));
end
binsA2(26+1)=sum(binsA(26*90+1:end));

hfig=figure;
histogram('BinEdges',edgesA2,'BinCounts',binsA2)
hold on
histogram('BinEdges',edges2,'BinCounts',bins2)
xlabel('Displacement range (in.)','FontSize',8,'FontName','Times New Roman')
ylabel('Cycle counts','FontSize',8,'FontName','Times New Roman')
set(gca,'YScale','log')
set(gca,'FontSize',8,'FontName','Times New Roman')
xticks(0:0.18:2.43)
yticks([1 10 1e2 1e3 1e4 1e5 1e6 1e7 1e8])
% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\figures\nd1717DispComp.';
print(hfig,[fileout,'tif'],'-r200','-dtiff');

%% disp at node 1814
fs=1/0.02;
[c,hist,edges,rmm,idx] = rainflow(ndLocYsAll{3}*39.37,fs); %convert m to inch
[cA,histA,edgesA,rmmA,idxA] = rainflow(ndLocYsAllAll{3}*39.37,fs); %convert m to inch
figure
histogram('BinEdges',edges','BinCounts',51*sum(hist,2))
set(gca,'YScale','log')
figure
histogram('BinEdges',edgesA','BinCounts',51*sum(histA,2))
set(gca,'YScale','log')

edges2=0:0.1:1.6;
bins=51*sum(hist,2);
bins2=zeros(16,1);
for i=0:14
    bins2(i+1)=sum(bins(i*50+1:i*50+50));
end
bins2(15+1)=sum(bins(15*50+1:end));

edgesA2=0:0.1:1.6;
binsA=51*sum(histA,2);
binsA2=zeros(16,1);
for i=0:14
    binsA2(i+1)=sum(binsA(i*200+1:i*200+200));
end
binsA2(15+1)=sum(binsA(15*200+1:end));

hfig=figure;
histogram('BinEdges',edgesA2,'BinCounts',binsA2)
hold on
histogram('BinEdges',edges2,'BinCounts',bins2)
xlabel('Displacement range (in.)','FontSize',8,'FontName','Times New Roman')
ylabel('Cycle counts','FontSize',8,'FontName','Times New Roman')
set(gca,'YScale','log')
set(gca,'FontSize',8,'FontName','Times New Roman')
xticks(0:0.2:2.4)
yticks([1 10 1e2 1e3 1e4 1e5 1e6 1e7 1e8])
% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\figures\nd1814DispComp.';
print(hfig,[fileout,'tif'],'-r200','-dtiff');

%% disp at node 1817
fs=1/0.02;
[c,hist,edges,rmm,idx] = rainflow(ndLocYsAll{4}*39.37,fs); %convert m to inch
[cA,histA,edgesA,rmmA,idxA] = rainflow(ndLocYsAllAll{4}*39.37,fs); %convert m to inch
figure
histogram('BinEdges',edges','BinCounts',51*sum(hist,2))
set(gca,'YScale','log')
figure
histogram('BinEdges',edgesA','BinCounts',51*sum(histA,2))
set(gca,'YScale','log')

edges2=0:0.1:1.8;
bins=51*sum(hist,2);
bins2=zeros(18,1);
for i=0:16
    bins2(i+1)=sum(bins(i*50+1:i*50+50));
end
bins2(17+1)=sum(bins(17*50+1:end));

edgesA2=0:0.1:1.8;
binsA=51*sum(histA,2);
binsA2=zeros(18,1);
for i=0:16
    binsA2(i+1)=sum(binsA(i*100+1:i*100+100));
end
binsA2(17+1)=sum(binsA(17*100+1:end));

hfig=figure;
histogram('BinEdges',edgesA2,'BinCounts',binsA2)
hold on
histogram('BinEdges',edges2,'BinCounts',bins2)
xlabel('Displacement range (in.)','FontSize',8,'FontName','Times New Roman')
ylabel('Cycle counts','FontSize',8,'FontName','Times New Roman')
set(gca,'YScale','log')
set(gca,'FontSize',8,'FontName','Times New Roman')
xticks(0:0.2:2.4)
yticks([1 10 1e2 1e3 1e4 1e5 1e6 1e7 1e8])
% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\figures\nd1817DispComp.';
print(hfig,[fileout,'tif'],'-r200','-dtiff');

%%
function [ndLocYs]=forceDispResp(nodeDisp)
nodeRec=[1701:1733,1801:1833,1301:1333,1401:1433,1501:1533]';

nodeDispDiv=cell(length(nodeRec),1);
for i=1:length(nodeRec)
    nodeDispDiv{i}=nodeDisp(:,6*(i-1)+2:6*i+1);
end

%% nodal displacement
nd1714=nodeDispDiv{find(nodeRec==1714)};
nd1715=nodeDispDiv{find(nodeRec==1715)};
nd1716=nodeDispDiv{find(nodeRec==1716)};
nd1717=nodeDispDiv{find(nodeRec==1717)};
nd1814=nodeDispDiv{find(nodeRec==1814)};
nd1815=nodeDispDiv{find(nodeRec==1815)};
nd1816=nodeDispDiv{find(nodeRec==1816)};
nd1817=nodeDispDiv{find(nodeRec==1817)};

nd1714LocY=nd1714(:,3)*cos(30/180*pi)-nd1714(:,1)*sin(30/180*pi);
nd1715LocY=nd1715(:,3)*cos(30/180*pi)-nd1715(:,1)*sin(30/180*pi);
nd1716LocY=nd1716(:,3)*cos(30/180*pi)-nd1716(:,1)*sin(30/180*pi);
nd1717LocY=nd1717(:,3)*cos(30/180*pi)-nd1717(:,1)*sin(30/180*pi);
nd1814LocY=nd1814(:,3)*cos(30/180*pi)-nd1814(:,1)*sin(30/180*pi);
nd1815LocY=nd1815(:,3)*cos(30/180*pi)-nd1815(:,1)*sin(30/180*pi);
nd1816LocY=nd1816(:,3)*cos(30/180*pi)-nd1816(:,1)*sin(30/180*pi);
nd1817LocY=nd1817(:,3)*cos(30/180*pi)-nd1817(:,1)*sin(30/180*pi);

ndLocYs={nd1714LocY;nd1717LocY;nd1814LocY;nd1817LocY;nd1715LocY;nd1716LocY;nd1815LocY;nd1816LocY};
end