import urllib
import re
from bs4 import BeautifulSoup

class CPCB:
	'Parameters, Nitric Oxide, Nitrogen Dioxide, NOx, Sulfur Dioxide, Ozone, PM 2.5, Benzene, Toluene, Ethyl Benzene, Temperature, Relative Humidity, Wind Speed, Wind Direction, Vertical Wind Speed, Solar Radiation'
	
	def __init__(self):
		print ("cpcb class instanciated")

	def getData(self,url):
		#cpcb_url="http://www.cpcb.gov.in/CAAQM/frmCurrentDataNew.aspx?StationName=sirifort&StateId=6&CityId=85"
		cpcb_url = url
		page = urllib.request.urlopen(cpcb_url)
		soup = BeautifulSoup(page, 'html.parser')
		tableRows=soup.find('span', attrs={'id':'lblReportCurrentData'}).find('table').find_all('tr')
		airContents={}
		for row in tableRows:
			cols = row.find_all('td')
			pattern = re.compile('<span style=\"\w+\:\w+\;\">(.*?)\</span>', re.IGNORECASE)
			if len(cols)>6:
				subjectCase = cols[3].find('span',attrs={'style':'color:Blue;'})
				concentrationValue=pattern.findall(str(subjectCase))
				if concentrationValue:
					concentrationValue= concentrationValue[0]
				else:
					concentrationValue=None
				airContents.update({(cols[0].string):{
					"Parameters":(cols[0].string),
					"Date":(cols[1].string),
					"Time":(cols[2].string),
					"Concentration":concentrationValue,
					"Unit":(cols[4].string),
					#"Standard":(cols[5].string)
					}})
		return airContents

	def getDataOf(self,airParameter):
		cpcb_url="http://www.cpcb.gov.in/CAAQM/frmCurrentDataNew.aspx?StationName=sirifort&StateId=6&CityId=85"
		page = urllib.request.urlopen(cpcb_url)
		soup = BeautifulSoup(page, 'html.parser')
		tableRows=soup.find('span', attrs={'id':'lblReportCurrentData'}).find('table').find_all('tr')
		airContents={}
		for row in tableRows:
			cols = row.find_all('td')
			pattern = re.compile('<span style=\"\w+\:\w+\;\">(.*?)\</span>', re.IGNORECASE)
			if len(cols)>6:
				subjectCase = cols[3].find('span',attrs={'style':'color:Blue;'})
				concentrationValue=pattern.findall(str(subjectCase))
				if concentrationValue:
					concentrationValue= concentrationValue[0]
				else:
					concentrationValue=None
				airContents.update({(cols[0].string):{
					"Parameters":(cols[0].string),
					"Date":(cols[1].string),
					"Time":(cols[2].string),
					"Concentration":concentrationValue,
					"Unit":(cols[4].string),
					#"Standard":(cols[5].string)
					}})
		return airContents[str(airParameter)]
if __name__ == "__main__":
	cpcb=CPCB()
	print (CPCB.__doc__)
	print ("##################")
	cpcbData=cpcb.getData("http://www.cpcb.gov.in/CAAQM/frmCurrentDataNew.aspx?StationName=ihbas&StateId=6&CityId=85")
	print (cpcbData.items())
	print ("##################")
	

