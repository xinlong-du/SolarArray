close all;clear;clc;
for i=30
filename=strcat('./testAllcases/dir',num2str(i),'spd9nodeDisp.out');
nodeDisp=load(filename);
plotDisp(nodeDisp)
end

function plotDisp(nodeDisp)
nodeRec=[1301:1333,1401:1433,1501:1533]';
nodeDispDiv=cell(length(nodeRec),1);
for i=1:length(nodeRec)
    nodeDispDiv{i}=nodeDisp(:,6*(i-1)+2:6*i+1);
end

nd1508=nodeDispDiv{find(nodeRec==1508)};
nd1511=nodeDispDiv{find(nodeRec==1511)};
nd1515=nodeDispDiv{find(nodeRec==1515)};
nd1517=nodeDispDiv{find(nodeRec==1517)};
nd1520=nodeDispDiv{find(nodeRec==1520)};
nd1523=nodeDispDiv{find(nodeRec==1523)};

nd1508LocY=(nd1508(:,3)*cos(30/180*pi)-nd1508(:,3)*sin(30/180*pi))*39.37; %m to in
nd1511LocY=(nd1511(:,3)*cos(30/180*pi)-nd1511(:,3)*sin(30/180*pi))*39.37;
nd1515LocY=(nd1515(:,3)*cos(30/180*pi)-nd1515(:,3)*sin(30/180*pi))*39.37;
nd1517LocY=(nd1517(:,3)*cos(30/180*pi)-nd1517(:,3)*sin(30/180*pi))*39.37;
nd1520LocY=(nd1520(:,3)*cos(30/180*pi)-nd1520(:,3)*sin(30/180*pi))*39.37;
nd1523LocY=(nd1523(:,3)*cos(30/180*pi)-nd1523(:,3)*sin(30/180*pi))*39.37;

hfig=figure;
time=0.02:0.02:10;
plot(time,nd1508LocY)
hold on
plot(time,nd1511LocY)
plot(time,nd1515LocY)
plot(time,nd1517LocY)
plot(time,nd1520LocY)
plot(time,nd1523LocY)
set(gca,'FontSize',8,'FontName','Times New Roman')
legend({'Panel 1','Panel 2','Panel 3','Panel 4','Panel 5','Panel 6'},'FontSize',8,'FontName','Times New Roman')
legend('location','southeast')
xlabel('Time (s)','FontSize',8,'FontName','Times New Roman')
ylabel('Displacement (in)','FontSize',8,'FontName','Times New Roman')
% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\highQtrDisp.';
print(hfig,[fileout,'tif'],'-r300','-dtiff');

hfig=figure;
time=0.02:0.02:10;
plot(time,nd1508LocY./nd1517LocY)
hold on
plot(time,nd1511LocY./nd1517LocY)
plot(time,nd1515LocY./nd1517LocY)
plot(time,nd1517LocY./nd1517LocY)
plot(time,nd1520LocY./nd1517LocY)
plot(time,nd1523LocY./nd1517LocY)
set(gca,'FontSize',8,'FontName','Times New Roman')
legend({'Panel 1/Panel 4','Panel 2/Panel 4','Panel 3/Panel 4','Panel 4/Panel 4','Panel 5/Panel 4','Panel 6/Panel 4'},'FontSize',8,'FontName','Times New Roman')
legend('location','southeast')
xlabel('Time (s)','FontSize',8,'FontName','Times New Roman')
ylabel('Displacement (in)','FontSize',8,'FontName','Times New Roman')
ylim([-1 1])
% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\highQtrRelaDisp.';
print(hfig,[fileout,'tif'],'-r300','-dtiff');
end