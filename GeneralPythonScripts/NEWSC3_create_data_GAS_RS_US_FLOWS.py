import json
def getfile():
    #open the file
    #*** > give the path to the file.
    f=open('../data/NEWSC3_US_stockflows_tonnes_GAS_RS_growth.csv', 'r')

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
    #parse through the list
    for line in input:
        if line[0] != None:
            #assign the columns to variables
            years = (line[0])
            GAS_hist = (line[1])
            GAS_sc1 = (line[2])
            GAS_sc2 = (line[3])
            GAS_sc3 = (line[4])
            RS_hist = (line[4])
            RS_sc1 = (line[5])
            RS_sc2 = (line[6])
            #RS_sc3 = (line[7])
            #if there is no data present we dont want to create the string for that data element
            #until 2005 the scenarios are not plotted offcourse.
            if years < '2005':
                temp_output = '{"date" : "'+years+'-01-01"'+', "GS_total_hist" : '+GAS_hist+', "RS_total_hist" : '+RS_hist+'},'
                data_list.append(temp_output)
            #if no historical data present do not deal with those elements
            if years > '2005':
                temp_output = '{"date" : "'+years+'-01-01"'+',"GS_total_sc1" :'+GAS_sc1+',"GS_total_sc2" : '+GAS_sc2+',"RS_total_sc1" :'+RS_sc1+',"RS_total_sc2" : '+RS_sc2+'},'
                data_list.append(temp_output)
            # in 2005 all data elements are present
            if years == '2005':
                temp_output = '{"date" : "'+years+'-01-01"'+', "GS_total_Series" : '+GAS_hist+',"GS_total_sc1" :'+GAS_sc1+',"GS_total_sc2" : '+GAS_sc2+', "RS_total_hist" : '+RS_hist+',"RS_total_sc1" :'+RS_sc1+',"RS_total_sc2" : '+RS_sc2+'},'
                data_list.append(temp_output)


    output = data_list
    return output


# Start execution here!
if __name__ == '__main__':
    print ("Starting JSON data viz creation script...")
    #open file
    data = getfile()
    #get the c3.js format as string
    output = create_output(data)
    #print them out
    for line in output:
        print(line)