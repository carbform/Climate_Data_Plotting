clear all
close all

rf = readmatrix('home/sarat/deom_data.csv'); %% Reading the .csv file as a matrix

t = linspace(1901,2020,120);
%%
rf(:,1) = t; %% Assigning x-axis values to first column of the matrix

% Setting default axes properties
set(0,'DefaultAxesFontName', 'Helvetica')
set(0,'DefaultAxesFontSize', 20)
set(0,'DefaultAxesFontweight', 'bold')

set(0,'DefaultAxesLineWidth', 2);
set(0,'DefaultAxesTickDir','out');
set(0,'DefaultAxesTickLength',[0.015 0.015]);
set(0,'DefaultAxesXGrid','on');
set(0,'DefaultAxesYGrid','on');


% Setting default text fonts.
set(0,'DefaultTextFontname', 'Helvetica')
set(0,'DefaultTextFontSize', 20)
set(0,'DefaultTextFontweight', 'bold')

% Setting line properties
set(0,'DefaultLineLineWidth',2)
set(0,'DefaultLineMarkersize',10)

f=figure('Visible','off');
figure(1)

plot(rf(:,1), rf(:,2),'color','black','DisplayName','B') % Plotting 2nd column of the matrix
hold on
plot(rf(:,1), rf(:,3),'color','blue','DisplayName','S')  % Plotting 3rd column of the matrix
plot(rf(:,1), rf(:,4),'color','red','DisplayName','N')   % Plotting 4th column of the matrix
hold off
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
xlabel('Year') 
ylabel('Rainfall Deviation (mm)')
legend('Orientation','horizontal')
set(gcf, 'Units', 'Inches', 'Position', [0, 0, 12, 5])
%%
exportgraphics(f,'/home/sarat/bar_chart.eps','Resolution',600);%% saving the figure
