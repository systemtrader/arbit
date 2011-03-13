import arbit.sql
import constants
import datetime
import nasdaq.symbols.sql
import arbit.kmeans

class classifier:
	
	def __init__(self):
		arbitSql = arbit.sql.sql()
		
		nasdaqSql = nasdaq.symbols.sql.sql()
		symbols = nasdaqSql.fetchSymbols()

		arbitSql.dropClassificationTable()
		arbitSql.createClassificationTable()
		
		currentTestDate = constants.startDate
		while currentTestDate < constants.endDate:
			currentTrainingDate = currentTestDate - datetime.timedelta(days=1)
			trainingPoints = arbitSql.fetchTrainingPoints(currentTrainingDate)
		
			for symbol in symbols:
				testPoint = arbitSql.fetchTestPoint(symbol, currentTestDate)
				if trainingPoints and testPoint:
					print('Processing ' + symbol + ' at date ' + currentTestDate.isoformat())
							
					classification={}
					classification['Classification']=self.classify(testPoint, trainingPoints)
					classification['Symbol']=symbol
					classification['CurrentTestDate']=currentTestDate
					classification['Outcome']=testPoint['Outcome'][0]
					classification['High']=testPoint['High'][0]
					classification['Close']=testPoint['Close'][0]
					
					arbitSql.insertClassification(classification)
				
			currentTestDate = currentTestDate + datetime.timedelta(days=1)

	def classify(self, testPoint, trainingPoints):
		return arbit.kmeans.classify(testPoint, trainingPoints)