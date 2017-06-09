import xlrd
from geopy.geocoders import GoogleV3

#open the excel file with the xlrd library
# Open the workbook
xl_workbook = xlrd.open_workbook('/vol/home/niccolsonsi/Dropbox/CML/TailingDam/TAILINGS DAM FAILURES 1915-2016-3.xlsx')
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
long= open("/vol/home/niccolsonsi/Dropbox/CML/TailingDam/longitude.txt","w+")
lat= open("/vol/home/niccolsonsi/Dropbox/CML/TailingDam/latitude.txt","w+")


#go through it per row
for row in locations:


        # get the location object
        location = geolocator.geocode(row)
        if location is not None:
            long.write(str(location.longitude) + "\n")
            lat.write(str(location.latitude) + "\n")
            print(location)
        else:
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