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

nd1408=nodeDispDiv{find(nodeRec==1408)};
nd1411=nodeDispDiv{find(nodeRec==1411)};
nd1414=nodeDispDiv{find(nodeRec==1414)};
nd1417=nodeDispDiv{find(nodeRec==1417)};
nd1420=nodeDispDiv{find(nodeRec==1420)};
nd1423=nodeDispDiv{find(nodeRec==1423)};

nd1408LocY=(nd1408(:,3)*cos(30/180*pi)-nd1408(:,3)*sin(30/180*pi))*39.37; %m to in
nd1411LocY=(nd1411(:,3)*cos(30/180*pi)-nd1411(:,3)*sin(30/180*pi))*39.37;
nd1414LocY=(nd1414(:,3)*cos(30/180*pi)-nd1414(:,3)*sin(30/180*pi))*39.37;
nd1417LocY=(nd1417(:,3)*cos(30/180*pi)-nd1417(:,3)*sin(30/180*pi))*39.37;
nd1420LocY=(nd1420(:,3)*cos(30/180*pi)-nd1420(:,3)*sin(30/180*pi))*39.37;
nd1423LocY=(nd1423(:,3)*cos(30/180*pi)-nd1423(:,3)*sin(30/180*pi))*39.37;

hfig=figure;
time=0.02:0.02:10;
plot(time,nd1408LocY)
hold on
plot(time,nd1411LocY)
plot(time,nd1414LocY)
plot(time,nd1417LocY)
plot(time,nd1420LocY)
plot(time,nd1423LocY)
set(gca,'FontSize',8,'FontName','Times New Roman')
legend({'Module 1','Module 2','Module 3','Module 4','Module 5','Module 6'},'FontSize',8,'FontName','Times New Roman')
legend('location','southeast')
xlabel('Time (s)','FontSize',8,'FontName','Times New Roman')
ylabel('Displacement (in)','FontSize',8,'FontName','Times New Roman')
% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\centerDisp2.';
print(hfig,[fileout,'tif'],'-r300','-dtiff');

hfig=figure;
time=0.02:0.02:10;
plot(time,nd1408LocY./nd1417LocY)
hold on
plot(time,nd1411LocY./nd1417LocY)
plot(time,nd1414LocY./nd1417LocY)
plot(time,nd1417LocY./nd1417LocY)
plot(time,nd1420LocY./nd1417LocY)
plot(time,nd1423LocY./nd1417LocY)
set(gca,'FontSize',8,'FontName','Times New Roman')
legend({'Module 1/Module 4','Module 2/Module 4','Module 3/Module 4','Module 4/Module 4','Module 5/Module 4','Module 6/Module 4'},'FontSize',8,'FontName','Times New Roman')
legend('location','southeast')
xlabel('Time (s)','FontSize',8,'FontName','Times New Roman')
ylabel('Displacement (in)','FontSize',8,'FontName','Times New Roman')
ylim([-1 1])
% save figure
figWidth=6;
figHeight=3;
set(hfig,'PaperUnits','inches');
set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
fileout='.\centerRelaDisp.';
print(hfig,[fileout,'tif'],'-r300','-dtiff');
end