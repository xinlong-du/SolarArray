close all; clear; clc;
%% load data
filename='../../../WindAnalysis/FiguresDeg30/CTspdPb30.txt';
spdDura=load(filename);
duraDiv=floor(spdDura(:,2)/10);            %10 is for 10s duration of simulation data 
duraDiv=floor(duraDiv/min(duraDiv)); %the final counts should multiply 165
duraDiv=reshape(duraDiv,[10,12]);

exForce2All=[];
nfsAll=cell(8,1);
ndLocYsAll=cell(8,1);
for i=0:30:330
    for j=0:9
        filename=strcat('./testAllcases/dir',num2str(i),'spd',num2str(j),'nodeDisp.out');
        nodeDisp=load(filename);
        filename=strcat('./testAllcases/dir',num2str(i),'spd',num2str(j),'eleForce.out');
        eleForce=load(filename);
        filename=strcat('./testAllcases/dir',num2str(i),'spd',num2str(j),'springResp.out');
        springResp=load(filename);
        [nfs,exForce,exForce2,ndLocYs]=forceDispResp(nodeDisp,eleForce,springResp);
        for k=1:8
            nfsAll{k}=[nfsAll{k};repmat(nfs{k},duraDiv(j+1,i/30+1),1)];
            ndLocYsAll{k}=[ndLocYsAll{k};repmat(ndLocYs{k},duraDiv(j+1,i/30+1),1)];
        end
        exForce2All=[exForce2All;repmat(exForce2,duraDiv(j+1,i/30+1),1)];
    end
end

%% duty cycles
fs=1/0.02;
[c,hist,edges,rmm,idx] = rainflow(exForce2All(:,2),fs);
figure
histogram('BinEdges',edges','BinCounts',sum(hist,2))
xlabel('Force Range')
ylabel('Cycle Counts')
set(gca,'YScale','log')

figure
rainflow(exForce2All(:,3),fs)
%% disp at node 1516
hfig=figure;
[c,hist,edges,rmm,idx] = rainflow(ndLocYsAll{5}*39.37,fs); %convert m to inch
histogram('BinEdges',edges','BinCounts',165*sum(hist,2))
xlabel('Displacement range (in.)','FontSize',8,'FontName','Times New Roman')
ylabel('Cycle counts','FontSize',8,'FontName','Times New Roman')
set(gca,'YScale','log')
set(gca,'FontSize',8,'FontName','Times New Roman')
% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\nd1516Disp.';
print(hfig,[fileout,'tif'],'-r200','-dtiff');

%% relative rotation for bending
nd1316m1318=ndLocYsAll{1}*39.37-ndLocYsAll{2}*39.37;
nd1319m1321=ndLocYsAll{3}*39.37-ndLocYsAll{4}*39.37;
rot13xx=nd1316m1318/41.26-nd1319m1321/41.26;
figure
rainflow(rot13xx,fs)

nd1516m1518=ndLocYsAll{5}*39.37-ndLocYsAll{6}*39.37;
nd1519m1521=ndLocYsAll{7}*39.37-ndLocYsAll{8}*39.37;
rot15xx=nd1516m1518/41.26-nd1519m1521/41.26;
hfig=figure;
[c,hist,edges,rmm,idx] = rainflow(rot15xx,fs);
histogram('BinEdges',edges','BinCounts',165*sum(hist,2))
xlabel('Rotation range (rad)','FontSize',8,'FontName','Times New Roman')
ylabel('Cycle counts','FontSize',8,'FontName','Times New Roman')
set(gca,'YScale','log')
set(gca,'FontSize',8,'FontName','Times New Roman')
% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\rot15xx.';
print(hfig,[fileout,'tif'],'-r200','-dtiff');

figure
rainflow(nd1519m1521,fs)

%% relative rotation for twist
nd1316m1516=ndLocYsAll{1}*39.37-ndLocYsAll{5}*39.37;
nd1321m1521=ndLocYsAll{4}*39.37-ndLocYsAll{8}*39.37;
rot1621=nd1316m1516/42.0-nd1321m1521/42.0;
hfig=figure;
[c,hist,edges,rmm,idx] = rainflow(rot1621,fs);
histogram('BinEdges',edges','BinCounts',165*sum(hist,2))
xlabel('Rotation range (rad)','FontSize',8,'FontName','Times New Roman')
ylabel('Cycle counts','FontSize',8,'FontName','Times New Roman')
set(gca,'YScale','log')
set(gca,'FontSize',8,'FontName','Times New Roman')
% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\rot1621.';
print(hfig,[fileout,'tif'],'-r200','-dtiff');

nd1318m1518=ndLocYsAll{2}*39.37-ndLocYsAll{6}*39.37;
nd1319m1519=ndLocYsAll{3}*39.37-ndLocYsAll{7}*39.37;
rot1819=nd1318m1518/42.0-nd1319m1519/42.0;
figure
rainflow(rot1819,fs)
figure
rainflow(nd1316m1516,fs)
figure
rainflow(nd1321m1521,fs)

%%
figure
rainflow(nfsAll{8}(:,2),fs)
%%
function [nfs,exForce,exForce2,ndLocYs]=forceDispResp(nodeDisp,eleForce,springResp)
nodeRec=[1301:1333,1401:1433,1501:1533]';
eleRec=[701:723,801:823]';
springRec=[21001:21022,22001:22022,23001:23022,24001:24022,45001:45022,46001:46022,47001:47022,48001:48022]';

nodeDispDiv=cell(length(nodeRec),1);
for i=1:length(nodeRec)
    nodeDispDiv{i}=nodeDisp(:,6*(i-1)+2:6*i+1);
end

eleForceDiv=cell(length(eleRec),1);
for i=1:length(eleRec)
    eleForceDiv{i}=eleForce(:,12*(i-1)+2:12*i+1);
end

springRespDiv=cell(length(springRec),1);
for i=1:length(springRec)
    springRespDiv{i}=springResp(:,12*(i-1)+2:12*i+1);
end

%% nodal forces (can be simplified using a list of nodes and a for loop)
nf1711=eleForceDiv{find(eleRec==711)}(:,7:12)+eleForceDiv{find(eleRec==712)}(:,1:6);
nf1712=eleForceDiv{find(eleRec==712)}(:,7:12)+eleForceDiv{find(eleRec==713)}(:,1:6);
nf1713=eleForceDiv{find(eleRec==713)}(:,7:12)+eleForceDiv{find(eleRec==714)}(:,1:6);
nf1714=eleForceDiv{find(eleRec==714)}(:,7:12)+eleForceDiv{find(eleRec==715)}(:,1:6);

nf1811=eleForceDiv{find(eleRec==811)}(:,7:12)+eleForceDiv{find(eleRec==812)}(:,1:6);
nf1812=eleForceDiv{find(eleRec==812)}(:,7:12)+eleForceDiv{find(eleRec==813)}(:,1:6);
nf1813=eleForceDiv{find(eleRec==813)}(:,7:12)+eleForceDiv{find(eleRec==814)}(:,1:6);
nf1814=eleForceDiv{find(eleRec==814)}(:,7:12)+eleForceDiv{find(eleRec==815)}(:,1:6);

nfs={nf1711;nf1712;nf1713;nf1714;nf1811;nf1812;nf1813;nf1814};
exForce=nf1711+nf1714+nf1811+nf1814;
exForce2=eleForceDiv{find(eleRec==711)}(:,7:12)+eleForceDiv{find(eleRec==715)}(:,1:6)+...
    eleForceDiv{find(eleRec==811)}(:,7:12)+eleForceDiv{find(eleRec==815)}(:,1:6);

%% nodal displacement
nd1316=nodeDispDiv{find(nodeRec==1316)};
nd1318=nodeDispDiv{find(nodeRec==1318)};
nd1319=nodeDispDiv{find(nodeRec==1319)};
nd1321=nodeDispDiv{find(nodeRec==1321)};

nd1516=nodeDispDiv{find(nodeRec==1516)};
nd1518=nodeDispDiv{find(nodeRec==1518)};
nd1519=nodeDispDiv{find(nodeRec==1519)};
nd1521=nodeDispDiv{find(nodeRec==1521)};

nd1316LocY=nd1316(:,3)*cos(30/180*pi)-nd1316(:,3)*sin(30/180*pi);
nd1318LocY=nd1318(:,3)*cos(30/180*pi)-nd1318(:,3)*sin(30/180*pi);
nd1319LocY=nd1319(:,3)*cos(30/180*pi)-nd1319(:,3)*sin(30/180*pi);
nd1321LocY=nd1321(:,3)*cos(30/180*pi)-nd1321(:,3)*sin(30/180*pi);

nd1516LocY=nd1316(:,3)*cos(30/180*pi)-nd1516(:,3)*sin(30/180*pi);
nd1518LocY=nd1318(:,3)*cos(30/180*pi)-nd1518(:,3)*sin(30/180*pi);
nd1519LocY=nd1319(:,3)*cos(30/180*pi)-nd1519(:,3)*sin(30/180*pi);
nd1521LocY=nd1321(:,3)*cos(30/180*pi)-nd1521(:,3)*sin(30/180*pi);

ndLocYs={nd1316LocY;nd1318LocY;nd1319LocY;nd1321LocY;nd1516LocY;nd1518LocY;nd1519LocY;nd1521LocY};
end