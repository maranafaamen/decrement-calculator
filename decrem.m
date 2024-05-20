clc
clear all
close all
path = input('Введите путь до файла . . . ');
%% Импорт данных
opts = delimitedTextImportOptions("NumVariables", 2);
% Specify range and delimiter
opts.DataLines = [2, Inf];
opts.Delimiter = ",";
% Specify column names and types
opts.VariableNames = ["Var1", "VarName2"];
opts.SelectedVariableNames = "VarName2";
opts.VariableTypes = ["string", "double"];
% Specify file level properties
opts.ImportErrorRule = "omitrow";
opts.MissingRule = "omitrow";
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";
% Specify variable properties
opts = setvaropts(opts, "Var1", "WhitespaceRule", "preserve");
opts = setvaropts(opts, "Var1", "EmptyFieldRule", "auto");
% Import the data
imp = readtable(path, opts); % !!! Указать путь до файла
% Convert to output type
imp = table2array(imp);
% Clear temporary variables
clear opts
plot(imp)
y = -brushedData(:,2); % !!! Указать импортированный массив точек и обрезать их
%% Полиномальная апроксимация
% Smooth input data
p = smoothdata((y),"loess","SmoothingFactor",0.25);
%% Расчёт декремента
% Нахождение максимумов
x = transpose(1:length(y));
max = islocalmax(p);
xmax = x(max);
pmax = p(max);
min = islocalmin(p);
xmin = x(min);
pmin = p(min);
% Нахождение Yi и декремента
Y1 = abs(pmax(1)-pmin(1));
Y2 = abs(pmax(2)-pmin(1));
Y3 = abs(pmax(2)-pmin(2));
Y4 = abs(pmax(3)-pmin(2));
dec = log((Y1/Y3+Y2/Y4)/2)
%% Построение графиков
plot(p,'b')
hold on
plot(xmax,pmax,'r*',xmin,pmin,'r*')
legend('Polynome','Maximums','Minimums');
