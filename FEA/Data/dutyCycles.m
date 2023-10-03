close all; clear; clc;
%% load data
filename='../../../WindAnalysis/FiguresDeg30/CTspdPb30.txt';
spdDura=load(filename);
duraDiv10s=floor(spdDura(:,2)/10);
duraDiv10s=reshape(duraDiv10s,[10,12]);

exForceAll=[];
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
            nfsAll{k}=[nfsAll{k};repmat(nfs{k},duraDiv10s(j+1,i/30+1),1)];
            ndLocYsAll{k}=[ndLocYsAll{k};repmat(ndLocYs{k},duraDiv10s(j+1,i/30+1),1)];
        end
        exForceAll=[exForceAll;repmat(exForce,duraDiv10s(j+1,i/30+1),1)];
        exForce2All=[exForce2All;repmat(exForce2,duraDiv10s(j+1,i/30+1),1)];
    end
end

%% duty cycles
fs=1/0.02;
rainflow(exForceAll(:,2),fs)
figure
rainflow(exForceAll(:,3),fs)
figure
rainflow(exForce2All(:,2),fs)
figure
rainflow(exForce2All(:,3),fs)
%%
for i=1:8
    figure
    rainflow(ndLocYsAll{i}*39.37,fs)
end
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