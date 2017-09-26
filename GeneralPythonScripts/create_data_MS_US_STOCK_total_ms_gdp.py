import json
def getfile():
    #open the file
    #*** > give the path to the file.
    f=open('/home/chai/Dropbox/CML/1software_dev/Django/CMLMasterProject/data/IV_Advanced_graph_making/US_total_materials_gdp.csv', 'r')

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


            # if there is no data present we dont want to create the string for that data element
            # until 2005 the scenarios are not plotted offcourse.

            # in 2005 all data elements are present
            if years <= '2005':
                temp_output = '{"date" : "' + years + '-01-01"' + ', "MS_total_hist" : ' + MS_hist +'},'
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