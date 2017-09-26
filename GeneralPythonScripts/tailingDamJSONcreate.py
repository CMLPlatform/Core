import xlrd, datetime
import string
import calendar
from dateutil import parser
#function to remove letters from characters
class Del:
  def __init__(self, keep=string.digits):
    self.comp = dict((ord(c),c) for c in keep)
  def __getitem__(self, k):
    return self.comp.get(k)

DD = Del()
# Open the workbook
xl_workbook = xlrd.open_workbook('../data/NEWLoc_TAILINGS_DAM_FAILURES_1915-2016-3.xlsx')
#get sheet names
sheet_names = xl_workbook.sheet_names()
#get the first sheet
xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])


id = 0
tempList = []
#use row variable as the index and parse through all rows
for row in range(1, xl_sheet.nrows):
    #only get the rows we need
    if row >= 2 and row <=290:
        id += 1
        #start allocating variables (for the greater good..)
        location = xl_sheet.cell_value(row,2)
        oretype = xl_sheet.cell_value(row,3)
        #cleaning up...
        year = str(xl_sheet.cell_value(row,11))
        year = year.rstrip('0').rstrip('.')
        #get the date
        date = xl_sheet.cell_value(row,12)
        release = xl_sheet.cell_value(row, 13)

        #the date is really messy so do a try
        try:
            date = datetime.datetime(*xlrd.xldate_as_tuple(date, xl_workbook.datemode))
        except:
            print("Something went wrong")
        dataStr = str(date)
        #if the conversion to datetime went well and make sense
        if (dataStr[:4]) == year:
            #use datatime
            realDate = dataStr
            realDate = parser.parse(realDate)
        else:
            #just use the year
            realDate = str(year)
            realDate = parser.parse(realDate)
        unixtime = calendar.timegm(realDate.timetuple()) * 1000
        #end of date function



        #release is going to be converted to magnitude scale of 0 - 10
        #try to convert to float if not possible set magnitude to 1 or do additional operations
        try:

            mag = float(release)
        except:
            release = release.split('-')
            if (release[0] ==""):
                mag = 1.0
            else:
                #if there are more numbers in the list get the highest magnitude
                try:
                    mag = release[1]
                except:
                    # remove characters that are letters
                    mag = release[0].translate(DD)
                    if mag == "":
                        mag = 1.0
            if type(mag) != float:
                mag = mag.replace(",", "")

        mag = float(mag)
        OldRange = (32243000 - 0)
        NewRange = (10 - 0)
        NewValue = (((mag - 0) * NewRange) / OldRange) + 0
        #end of magnitude stuff


        #final values here before making JSON format
        mag = NewValue
        if mag <2:
            mag = 2
        place = location
        time = unixtime
        url = "none"
        title = location
        deaths =  xl_sheet.cell_value(row, 15)
        if deaths=="":
            deaths = '"Unspecified"'
        else:
            deaths = '"'+str(deaths)+'"'
        source =  xl_sheet.cell_value(row, 16)
        oretype = oretype
        release = xl_sheet.cell_value(row, 13)
        if release =="":
            release =  '"Unspecified"'
        else:
            release = '"'+str(release)+'"'
        runout = xl_sheet.cell_value(row, 14)
        if runout=="":
            runout = '"Unspecified"'
        else:
            runout = '"'+str(runout)+'"'
        lat = xl_sheet.cell_value(row, 27)
        long = xl_sheet.cell_value(row, 28)
        if lat != "None":

            jsonString = '{"type":"Feature","properties":{"mag":'+str(5)+',"place":"'+location+'","time":'+str(time)+',"url":"https://cml.liacs.nl/core","title":"'+location+'","deaths" : '+str(deaths)+',"source" :"'+source+'","oretype": "'+oretype+'","release" : '+str(release)+',"runout" : '+str(runout)+',},"geometry":{"type":"Point","coordinates":['+str(long)+','+str(lat)+',4.57]},"id":"'+str(id)+'"},'
        print((jsonString))
        #print(date)
        #print(year)
        #print(row)
        #print(location)





