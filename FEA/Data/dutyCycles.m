close all; clear; clc;
nodeDisp=load('./testAllcases/dir0spd0nodeDisp.out');
eleForce=load('./testAllcases/dir0spd0eleForce.out');
springResp=load('./testAllcases/dir0spd0springResp.out');

%%
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