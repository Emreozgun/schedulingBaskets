from geopy.geocoders import Nominatim
import random # to generate random geocodes in range
from math import sin, cos, sqrt, atan2, radians
import time

geolocator = Nominatim(user_agent="code")

baskets = dict()
counter = 0

def checkForAddBasket(
		newLat, newLong, 
		newAddress ):
	
	global baskets,counter

	R = 6373.0
	isAddedToBasket = False
	currentCounter = 0

	for basket in baskets.values() :
		totalLat = 0.0 
		totalLong = 0.0
		for geocode in basket : 
			totalLat += geocode[0]
			totalLong += geocode[1] 	 
		
		avgLat = totalLat / len(basket)
		avgLong = totalLong / len(basket)
		
		if __debug__ : 
			print("average lattitude : " , avgLat)
			print("average longtitude : " , avgLong)

			print("new lattitude  : " , newLat)
			print("new longtitude : " , newLong)

		lat1 = radians(avgLat)
		lon1 = radians(avgLong)
		lat2 = radians(newLat)
		lon2 = radians(newLong)

		dlon = lon2 - lon1
		dlat = lat2 - lat1

		a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))

		distance = R * c

		#print(currentCounter, " - Result:", distance)
		# continue to next one
		if distance > 1.0 :  
			currentCounter += 1
			continue
		# assign to current basket
		else :   
			baskets[currentCounter].append([newLat, newLong, newAddress])
			isAddedToBasket = True	
			break
		currentCounter += 1

	if not isAddedToBasket:
		baskets[counter] = [[newLat, newLong, newAddress]]
		counter += 1


def findRandomLocation(): 
	randomLat = random.uniform( 41.105, 41.119 )
	randomLong = random.uniform( 29.01 , 29.028 )

	location = geolocator.reverse(str(randomLat) + "," + str(randomLong))

	return randomLat, randomLong, location.address

def main(
		time_sec ):

	global baskets,counter

	while time_sec : 
		mins, secs = divmod(time_sec, 60)
		timeformat = '{:02d}:{:02d}'.format(mins, secs)
		print(timeformat, end='\r')
		time.sleep(1)
		newLat, newLong , newAddress = findRandomLocation()
		
		print("New order come from this address : " , 
			newLat, newLong , newAddress )

		if len(baskets) != 0 : 
			isAvailable = checkForAddBasket(
				newLat, newLong , 
				newAddress )
		else : 
			baskets[counter] = [[newLat, newLong,newAddress]] 
			counter += 1
		time_sec -= 1
	
def displayBaskets():
	global baskets
	print(baskets)

	for basket in baskets.keys() :
		print("SEPET" + str(basket) +  "#") 
		itemNo = 0
		for item in baskets[basket] : 
			print("\t item#" + str(itemNo) + " [" + str(item[0]) + 
								"," + str(item[1]) + "] , " + str(item[2]) )
			itemNo += 1

if __name__ == '__main__':
	main(10)
	displayBaskets()



