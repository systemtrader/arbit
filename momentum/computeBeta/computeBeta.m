function b=computeBeta()

fprintf('Computing beta for stocks...\n')

symbols = textread('C:\momentum\data\symbols\successfullyReformattedSymbols.txt', '%s');

for i=1:size(symbols,1) %the last line is a newline
    symbol=symbols{i};
    b(i)=computeBetaForFile(symbol);
end

fid = fopen('C:\momentum\data\symbols\beta.csv','w');
for i=1:size(symbols,1) %the last line is a newline
    fprintf(fid,'%s,%f\n',char(symbols(i)), b(i));
end
fclose(fid);