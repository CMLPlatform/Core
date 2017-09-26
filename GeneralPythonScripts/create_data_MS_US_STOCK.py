import json
def getfile():
    #open the file
    #*** > give the path to the file.
    f=open('../data/US_stockflows_tonnes_MS_total.csv', 'r')

    #get the content
    F=f.read()
    #split (make an array where each element is determined by an enter)
    U = F.split('\n')






    #Create empty list !!!!!!! THIS IS THE WORKING LIST OF LIST WE NEED FOR EVERYTHING !!
    L = []

    #fill the empty list with the data (this time split even further by tabs)
    for line in U:
        L.append(line.split('#'))
    #data cleaning
    L.pop(-1)

    L.pop(0)
    return L
def create_output(input):

    data_list = []
    for line in input:
        if line[0] != None:
            years = (line[0])
            MS_hist = (line[1])
            MS_sc1 = (line[2])
            MS_sc2 = (line[3])
            MS_sc3 = (line[4])
            # if there is no data present we dont want to create the string for that data element
            # until 2005 the scenarios are not plotted offcourse.
            if MS_sc1 == '' and MS_sc2 == '':
                temp_output = '{"date" : "'+years+'-01-01"'+', "MS_total_hist" : '+MS_hist+'},'
                data_list.append(temp_output)
            #if no historical data present do not deal with those elements
            if MS_hist == '':
                temp_output = '{"date" : "'+years+'-01-01"'+',"MS_total_sc1" :'+MS_sc1+',"MS_total_sc2" : '+MS_sc2+'},'
                data_list.append(temp_output)
            # in 2005 all data elements are present
            if years == '2005':
                temp_output = '{"date" : "' + years + '-01-01"' + ', "MS_total_hist" : ' + MS_hist + ',"MS_total_sc1" :' + MS_sc1 + ',"MS_total_sc2" : ' + MS_sc2 +'},'
                data_list.append(temp_output)

    output = data_list
    return output



# Start execution here!
if __name__ == '__main__':
    print ("Starting JSON data viz creation script...")

    data = getfile()
    output = create_output(data)
    for line in output:
        print(line)