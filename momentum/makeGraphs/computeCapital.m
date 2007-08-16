clear all;
wekaOut = load ('../data/matlab/BEASOut.csv');
testCSV = load('../data/matlab/testBEAS.csv');

openPrice=testCSV(:,2);
highPrice=testCSV(:,3);
closePrice=testCSV(:,5);

capital=25000;
for day=2:size(testCSV,1)
    capital(day)=capital(day-1);
    
    if(wekaOut(day,2)==1) %then buy
        shares=capital(day)/openPrice(day);
        capital(day)=0;
        
        if(highPrice(day)>openPrice(day)*1.02)
            capital(day)=shares*openPrice(day)*1.02;
        else
            capital(day)=shares*closePrice(day);
        end
    end
end


plot(capital)

