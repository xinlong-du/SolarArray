clear;clc;
MB40=load('MB40Mid.out');
DB40=load('DB40Mid.out');
DB40Rinchen=load('DB40MidRInchen.out');
DB40NoImperf=load('DB40MidNoImperf.out');
%% plot lateral disp
hfig=figure;
plot(MB40(11:end,5),MB40(11:end,1),'k-','LineWidth',1.0)
hold on
plot(DB40(2:end,5),DB40(2:end,1),'r-','LineWidth',1.0)
plot(DB40Rinchen(11:end,5),DB40Rinchen(11:end,1),'r--','LineWidth',1.0)
plot(DB40NoImperf(11:end,5),DB40NoImperf(11:end,1),'b-','LineWidth',1.0)
legend({'MB40','DB40','DB40RoundCorner','DB40NoImperf'},'FontSize',8)
ylim([0 10])
ylabel('Load (kN)','FontSize',10) 
xlabel('twist (rad)','FontSize',10)
%%
hfig=figure;
plot(MB40(11:end,5),MB40(11:end,1),'k-','LineWidth',1.0)
hold on
plot(DB40(2:end,5),DB40(2:end,1),'r-','LineWidth',1.0)
plot(DB40Rinchen(11:end,5),DB40Rinchen(11:end,1),'r--','LineWidth',1.0)
legend({'MB40','DB40','DB40RoundCorner'},'FontSize',10)
ylim([0 10])
ylabel('Load (kN)','FontSize',10) 
xlabel('twist (rad)','FontSize',10)
% xlim([0 60])
% ylim([1 2.8])
% set(gca,'XTick',(0:10:60))
% set(gca,'YTick',(1:0.2:2.8))
% set(gca,'FontSize',10)
% xlabel('z-displacement of point O','FontSize',10) 
% ylabel('Load P/1000','FontSize',10)
% legend({'Battini','DB2','DB4','DB8','DB40','MB2','MB4','MB8','MB40'},'FontSize',8)
% legend('Location','southeast')
% % save figure
% figWidth=3.5;
% figHeight=3;
% set(hfig,'PaperUnits','inches');
% set(hfig,'PaperPosition',[0 0 figWidth figHeight]);
% fileout=('test2.');
% print(hfig,[fileout,'tif'],'-r800','-dtiff');