import csv
import os  
import datetime
import time
import sys
import xlrd
# import copy
import json
from xlutils.copy import copy
import time
from timeloop import Timeloop
from datetime import timedelta
import pandas as pd
import tensorflow as tf
import numpy as np
from keras.models import *
from keras import backend as k
from keras import optimizers, regularizers
from sklearn.preprocessing import StandardScaler,MinMaxScaler 
import fancyimpute
#from keras.models import load_model
#global graph
#graph = tf.get_default_graph()
#model = load_model('model.h5', custom_objects={})

tl = Timeloop()

# reload(sys)
# sys.setdefaultencoding('utf-8')
from time import gmtime, strftime
import cpcb as cpcbModule
from xlwt import Workbook 

unixTime= int(time.time())
gmtDate = str(strftime("%d-%m-%Y", gmtime()))
gmtTime = str(strftime("%H:%M:%S", gmtime()))
filename='cpcbData.csv'
data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/'+filename))
file_existence_flag=int(os.path.isfile(data_file))  

param = {0:{
	'Nitric Oxide':1,
	'Nitrogen dioxide':2,
	'Oxides of Nitrogen':3,
	'Carbon Monoxide':4,
	'Ammonia':5,
	'PM2.5':6,
	'Temperature':9,
	'Relative Humidity':10,
	'Wind Speed ':11,
	'Wind Direction':12,
	'Solar Radiation':13,
	'Sulfur Dioxide':14
},
1:{
	'Nitric Oxide':1,
	'Nitrogen Dioxide':2,
	'Oxides of Nitrogen':3,
	'Carbon Monoxide':4,
	'Ammonia':5,
	'PM 2.5':6,
	'Temperature':9,
	'Relative Humidity':10,
	'Wind Speed ':11,
	'Wind Direction':12,
	'Solar Radiation':13,
	'Sulfur Dioxide':14
}}
curl ={
0:"http://www.cpcb.gov.in/CAAQM/frmCurrentDataNew.aspx?StationName=sirifort&StateId=6&CityId=85",
1:"http://www.cpcb.gov.in/CAAQM/frmCurrentDataNew.aspx?StationName=ihbas&StateId=6&CityId=85"
} 
@tl.job(interval=timedelta(seconds=10))
def cpcbToCsv():
	for j in curl:
		print(j)
		cpcb=cpcbModule.CPCB()
		cpcbData=cpcb.getData(url = curl[j])
		# f = open(data_file, 'a+')
		wb = Workbook() 
		# sheet1 = wb.add_sheet('Sheet 1') 
		rb = xlrd.open_workbook('xlwt.xls',formatting_info=True)
		r_sheet = rb.sheet_by_index(j)
		r = r_sheet.nrows
		wb = copy(rb)
		sheet1 = wb.get_sheet(j) 
		try:
			# sheet1.write(r, 0, "Date") 
			# sheet1.write(r, 1, "Time") 
			# for par in param:
			#     sheet1.write(r, param[par]+1,par)
			sheet1.write(r, 0, cpcbData['Nitric Oxide']['Date']+" "+cpcbData['Nitric Oxide']['Time']) 
			sheet1.write(r, 1, cpcbData['Nitric Oxide']['Time'] ) 
			print(cpcbData)
			for par in param[j]:
				sheet1.write(r, param[j][par]+1,cpcbData[par]['Concentration'])
		finally:
			wb.save('xlwt.xls')
			dataset = pd.read_excel('xlwt.xls')
			dataset = dataset.set_index(["Date"])
			dataset.index = pd.to_datetime(dataset.index)
			dataset = dataset.iloc[-97:-1]
			print(dataset)
			dataset = dataset.drop([ 'Carbon Monoxide',  'Benzene', 'Time','Toluene'], axis=1)
			print(dataset.index[0:5])
			dataset_2 = dataset
			dataset = dataset.replace("None", np.nan)
			dataset = dataset.replace(0, np.nan)

			XY_incomplete = dataset.values[:, :]

			n_imputations = 10
			XY_completed = []
			for i in range(n_imputations):
				imputer = fancyimpute.IterativeImputer(sample_posterior=True, random_state=i)
				XY_completed.append(imputer.fit_transform(XY_incomplete))

			XY_completed_mean = np.mean(XY_completed, 0)
			XY_completed_std = np.std(XY_completed, 0)
		
			#Save the imputed values in dataset_2
			dataset = pd.DataFrame(XY_completed_mean,index=dataset_2.index,columns=dataset_2.columns)
			dataset = dataset.resample('60T').mean()
			dataset = dataset.iloc[-24:]
			sc = MinMaxScaler()
			scaled_values = sc.fit_transform(dataset.values)
			scaled_dataframe = pd.DataFrame(scaled_values, index=dataset.index, columns=dataset.columns)

			
			#scaled_values = np.array(scaled_values)[indices.astype(int)]
			print(scaled_values.shape)
			scaled_values_reshape = scaled_values.reshape((1,scaled_values.shape[0],scaled_values.shape[1]))
			# load json and create model
			json_file = open('model_final.json', 'r')
			loaded_model_json = json_file.read()
			json_file.close()	
			loaded_model = model_from_json(loaded_model_json)
			# load weights into new model
			loaded_model.load_weights("model_final.h5")
			print("Loaded model from disk")
			yhat = loaded_model.predict(scaled_values_reshape)


			inv_yhat = np.concatenate((yhat, scaled_values[0, 4:].reshape((1,-1))), axis = 1)
			inv_yhat = sc.inverse_transform(inv_yhat)
			inv_yhat = inv_yhat[:,0:4]
			data = {}
			data["NO2"]= inv_yhat[0][0]
			data["NO"]= inv_yhat[0][1]
			data["PM2.5"]= inv_yhat[0][2]
			data["SO2"]= inv_yhat[0][3]
			with open(str(j)+'d.json', 'w') as outfile:
				json.dump(data, outfile)

# def makeStringForCSV(x):
# 	# print '%s <= data' % str(cpcbData[x]['Parameters'])
# 	return (
# 		  cpcbData[x]['Parameters'],cpcbData[x]['Concentration'],cpcbData[x]['Unit'],cpcbData[x]['Date'],cpcbData[x]['Time']
# 		)

if __name__ == "__main__":
    #  cpcbToCsv()
    tl.start(block=True)
    #  print '%s <= Time' % str(cpcbData['Ozone']['Time'])
    #  print "done"
