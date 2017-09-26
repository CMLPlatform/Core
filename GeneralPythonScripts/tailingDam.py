import xlrd
from geopy.geocoders import GoogleV3
from time import sleep
from geopy.exc import GeocoderTimedOut

def do_geocode(address):
    try:
        location = geolocator.geocode(address, timeout=None)
        return location
    except GeocoderTimedOut:
        sleep(10)
        return do_geocode(address)

#open the excel file with the xlrd library
# Open the workbook
xl_workbook = xlrd.open_workbook('../data/TAILINGS DAM FAILURES 1915-2016-3.xlsx')
#get sheet names
sheet_names = xl_workbook.sheet_names()
#get the first sheet
xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])

#get the needed column
arrayofvalues = xl_sheet.col_values(2)
#we only need to have locations so lets use slicing to capture them
locations = (arrayofvalues[2:291])

#use Google engine
geolocator = GoogleV3(api_key='AIzaSyA-n1usRnp6oUlLpE9Tnb2inES1Eqwqy7Y')

#initialize a file to write to
long= open("../data/longitude.txt","w+")
lat= open("../data/latitude.txt","w+")


#go through it per row
for row in locations:
    # get the location object
    #location = geolocator.geocode(row, timeout=None)
    location = do_geocode(row)
    if location is not None:
        long.write(str(location.longitude) + "\n")
        lat.write(str(location.latitude) + "\n")
        print(location)
    #if location is not found by default, we need to dive deeper...
    else:
        #strip on the comma's
        rowList = [x.strip() for x in row.split(',')]
        # if the first entry is unidentified remove it and search again using Google's engine
        if rowList[0] == 'Unidentified':
            rowList.pop(0)
            # search again
            newStr = ','.join(rowList)
            location = do_geocode(newStr)

            #write the object
            if location is not None:
                long.write(str(location.longitude) + "\n")
                lat.write(str(location.latitude) + "\n")
                print(location)
            # we would have to dive even deeper according to 2nd method
            else:
                try:
                    # remove the first entry (high resolution data)
                    rowList.pop(0)
                    # search again for state or country
                    newStr = ','.join(rowList)
                    location = do_geocode(newStr)

                    # try to write, alternatively -> give up :(
                    if location is not None:
                        long.write(str(location.longitude) + "\n")
                        lat.write(str(location.latitude) + "\n")
                        print(location)
                    else:
                        long.write("None" + "\n")
                        lat.write("None" + "\n")
                except:
                    long.write("None" + "\n")
                    lat.write("None" + "\n")
        #if it is not unidentified try 2nd method (that is remove the high resolution data and preserve State/Country
        else:
            try:
                #remove the first entry (high resolution data)
                rowList.pop(0)
                # search again for state or country
                newStr = ','.join(rowList)
                location = do_geocode(newStr)

                # try to write, alternatively -> give up :(
                if location is not None:
                    long.write(str(location.longitude) + "\n")
                    lat.write(str(location.latitude) + "\n")
                    print(location)
                else:
                    long.write("None" + "\n")
                    lat.write("None" + "\n")
            except:
                long.write("None" + "\n")
                lat.write("None" + "\n")

    '''
    long.write(location.longitude + "\n")
    lat.write(location.latitude + "\n")
except:
    long.write("None" +"\n")
    lat.write("None"+"\n")
'''



#location = geolocator.geocode(locations[0])
#print(location.longitude)