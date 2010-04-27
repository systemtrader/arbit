import sys	# for maxint
import data
import constants

class classifier:
	def __init__(self, symbol, currentDate, quotes):
		self.symbol=symbol
		self.currentDate=currentDate
		self.quotes=quotes
	
	def run(self):
		'''
		[trainingSet, testPoint]=self.createDataSet()
		p=self.naiveBayes(trainingSet, testPoint)
		'''
		
		p={}
		p['Good']=self.e()
		p['Bad']=1.0
		
		return p
	
	def e(self):
		# this is E(Symbol)
		
		window=100
		
		e=1.0
		currentIndex=data.getIndex(self.currentDate, self.quotes[self.symbol])
		if currentIndex and currentIndex-window>0:
			for day in range(currentIndex-window, currentIndex):
				Open=self.quotes[self.symbol]['Open'][day]
				Low=self.quotes[self.symbol]['Low'][day]
				High=self.quotes[self.symbol]['High'][day]
				Close=self.quotes[self.symbol]['Close'][day]
				
				# go long
				if(High>Open*(1.0+constants.take)):
					e*=1.0+constants.take
				else:
					e*=1.0+((Close-Open)/Open)
		
		return e
	
	def naiveBayes(self, trainingSet, testPoint):
		if not trainingSet or not len(trainingSet)>0:
			return False
		
		classes=['Good', 'Bad']
		
		# compute p(C)
		p_C={}
		for C in classes:
			p_C[C]=0.0
			for i in range(0, len(trainingSet)):
				if trainingSet[i]['Outcome']==C:
					p_C[C]+=1
			p_C[C]/=len(trainingSet)
			
		# compute p(F_i|C)
		p_F_C={}
		c_F_C={}
		for predictor in testPoint:
			if predictor!='Outcome':
				p_F_C[predictor]={}
				c_F_C[predictor]={}
				for C in classes:
					p_F_C[predictor][C]=0.0
					c_F_C[predictor][C]=0
		
		for i in range(0, len(trainingSet)):
			for predictor in trainingSet[i]:
				if predictor!='Outcome':
					C=trainingSet[i]['Outcome']
					if trainingSet[i][predictor]==testPoint[predictor]:
						p_F_C[predictor][C]+=1
					c_F_C[predictor][C]+=1
		
		for predictor in p_F_C:
			for C in p_F_C[predictor]:
				if c_F_C[predictor][C]==0:
					p_F_C[predictor][C]=0
				else:
					p_F_C[predictor][C]/=c_F_C[predictor][C]
		
		# compute p(F_i)
		p_F={}
		c_F={}
		for predictor in testPoint:
			if predictor!='Outcome':
				p_F[predictor]=0.0
				c_F[predictor]=0
		
		for i in range(0, len(trainingSet)):
			for predictor in trainingSet[i]:
				if predictor!='Outcome':
					if trainingSet[i][predictor]==testPoint[predictor]:
						p_F[predictor]+=1
					c_F[predictor]+=1
		for predictor in p_F:
			p_F[predictor]/=c_F[predictor]
		
		#compute p(C) * pi[p(F_i|C)/p(F_i)]
		p={}
		for C in classes:
			p[C]=p_C[C]
			for predictor in p_F:
				if p_F[predictor]!=0:
					p[C]*=p_F_C[predictor][C]/p_F[predictor]
		
		return p
	
	def createDataSet(self):
		# the key value is the window to use the predictor for
		# this is an odd mix of time series and priors
		predictors = {'Symbol':5, 'xDayHigh':100, 'xDayLow':100, 'shortWin':50, 'longWin':50, 'win':50}
		
		# create the training set
		trainingSet=[]
		for symbol in self.quotes:
			currentIndex=data.getIndex(self.currentDate, self.quotes[symbol])
			if currentIndex and currentIndex-105>0:
				
				# add a data point for each predictor and day
				for predictor in predictors:
					window=predictors[predictor]
					for day in range(currentIndex-window, currentIndex):
						trainingSet.append(self.createDataPoint(day, symbol, predictor))
		
		# create a test point
		testPoint={}
		day=data.getIndex(self.currentDate, self.quotes[self.symbol])
		
		for predictor in predictors:
			point=self.createDataPoint(day, self.symbol, predictor)
			testPoint[predictor]=point[predictor]
		
		return [trainingSet, testPoint]
	
	def createDataPoint(self, day, symbol, predictor):
		dataPoint={}
		
		if predictor=='Symbol':
			dataPoint['Symbol']=symbol
		elif predictor=='xDayHigh':
			# last closing price was x% of the y day high
			High=0
			for i in range(day-4, day+1):
				if self.quotes[symbol]['High'][i]>High:
					High=self.quotes[symbol]['High'][i]
			Last=self.quotes[symbol]['Close'][day]
			dataPoint['xDayHigh']=self.bin(Last/High)
		elif predictor=='xDayLow':
			# last closing price was x% of the y day low
			Low=sys.maxsize
			for i in range(day-4, day+1):
				if self.quotes[symbol]['Low'][i]<Low:
					Low=self.quotes[symbol]['Low'][i]
			Last=self.quotes[symbol]['Close'][day]
			dataPoint['xDayLow']=self.bin(Last/Low)
		elif predictor=='longWin':
			e=1.0
			window=100
			for day in range(day-window, day):
				Open=self.quotes[self.symbol]['Open'][day]
				Low=self.quotes[self.symbol]['Low'][day]
				High=self.quotes[self.symbol]['High'][day]
				Close=self.quotes[self.symbol]['Close'][day]
				
				if(High>Open*(1.0+constants.take)):
					e*=1.0+constants.take
				else:
					e*=1.0+((Close-Open)/Open)
					
			dataPoint['longWin']=self.bin(e)
		
		elif predictor=='shortWin':
			e=1.0
			window=100
			for day in range(day-window, day):
				Open=self.quotes[self.symbol]['Open'][day]
				Low=self.quotes[self.symbol]['Low'][day]
				High=self.quotes[self.symbol]['High'][day]
				Close=self.quotes[self.symbol]['Close'][day]
				
				if(Low<Open*(1.0-constants.take)):
					e*=1.0+constants.take
				else:
					e*=1.0+((Open-Close)/Open)
					
			dataPoint['shortWin']=self.bin(e)
		
		elif predictor=='win':
			e=1.0
			window=100
			for day in range(day-window, day):
				print(self.symbol)
				print(day)
				Open=self.quotes[self.symbol]['Open'][day]
				Low=self.quotes[self.symbol]['Low'][day]
				High=self.quotes[self.symbol]['High'][day]
				Close=self.quotes[self.symbol]['Close'][day]
				
				if(High>Open*(1.0+constants.take)):
					e*=1.0+constants.take
				else:
					e*=1.0+((Close-Open)/Open)
					
				if(Low<Open*(1.0-constants.take)):
					e*=1.0+constants.take
				else:
					e*=1.0+((Open-Close)/Open)
			
			dataPoint['win']=self.bin(e)
		else:
			print('I found an unrecognized predictor: ' + predictor + '. This means there is an error in your code.')
		
		# populate the outcome for today if we have data
		if len(self.quotes[symbol]['Open'])>day+1:
			if self.quotes[symbol]['High'][day+1]>self.quotes[symbol]['Open'][day+1]*(1+constants.take):
				dataPoint['Outcome']='Good'
			else:
				dataPoint['Outcome']='Bad'
		
		return dataPoint
	
	def bin(self, x):
		return round(x*20)/20
