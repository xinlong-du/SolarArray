close all; clear; clc;
nodeDisp=load('./testAllcases/dir0spd0nodeDisp.out');
eleForce=load('./testAllcases/dir0spd0eleForce.out');
springResp=load('./testAllcases/dir0spd0springResp.out');

[nfs,exForce,ndLocYs]=forceDispResp(nodeDisp,eleForce,springResp);
%%
function [nfs,exForce,ndLocYs]=forceDispResp(nodeDisp,eleForce,springResp)
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

%% nodal displacement
nd1316=nodeDispDiv{find(nodeRec==1316)};
nd1318=nodeDispDiv{find(nodeRec==1318)};
nd1319=nodeDispDiv{find(nodeRec==1319)};
nd1321=nodeDispDiv{find(nodeRec==1321)};

nd1416=nodeDispDiv{find(nodeRec==1416)};
nd1418=nodeDispDiv{find(nodeRec==1418)};
nd1419=nodeDispDiv{find(nodeRec==1419)};
nd1421=nodeDispDiv{find(nodeRec==1421)};

nd1316LocY=nd1316(:,3)*cos(30/180*pi)-nd1316(:,3)*sin(30/180*pi);
nd1318LocY=nd1318(:,3)*cos(30/180*pi)-nd1318(:,3)*sin(30/180*pi);
nd1319LocY=nd1319(:,3)*cos(30/180*pi)-nd1319(:,3)*sin(30/180*pi);
nd1321LocY=nd1321(:,3)*cos(30/180*pi)-nd1321(:,3)*sin(30/180*pi);

nd1416LocY=nd1316(:,3)*cos(30/180*pi)-nd1416(:,3)*sin(30/180*pi);
nd1418LocY=nd1318(:,3)*cos(30/180*pi)-nd1418(:,3)*sin(30/180*pi);
nd1419LocY=nd1319(:,3)*cos(30/180*pi)-nd1419(:,3)*sin(30/180*pi);
nd1421LocY=nd1321(:,3)*cos(30/180*pi)-nd1421(:,3)*sin(30/180*pi);

ndLocYs={nd1316LocY;nd1318LocY;nd1319LocY;nd1321LocY;nd1416LocY;nd1418LocY;nd1419LocY;nd1421LocY};
end