import json
def getfile():
    #open the file
    #*** > give the path to the file.
    f=open('../../data/IV_Advanced_graph_making/JP_GAS_RS_materials_gdp.csv', 'r')

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
    L.pop(0)

    return L
def create_output(input):


    data_list = []
    #parse over the lines
    for line in input:
        years = line[0]
        timber_hist_jp = line[1]

        #timber_sc3 = line[4]
        iron_hist_jp = line[6]

        #iron_sc3 = line[9]
        other_hist_jp = line[11]

        #other_sc3 = line[14]
        minerals_hist_jp = line[16]

        RS_timber_hist_jp = line[21]

        # timber_sc3 = line[4]
        RS_iron_hist_jp = line[26]

        # iron_sc3 = line[9]
        RS_other_hist_jp = line[31]

        # other_sc3 = line[14]
        RS_minerals_hist_jp = line[36]

        #minerals_sc3 = line[19]

        #as we know the dataset by heart we can manipulate in a simple manner

        #we only take historical data now which is all years untill 2005
        if years <= '2005':
            temp_output = '{"date" : "' + years + '-01-01"' + ', "GS_timber_hist_jp" : ' + timber_hist_jp +', "GS_iron_hist_jp" : '+\
                          iron_hist_jp+', "GS_other_hist_jp" : '+ other_hist_jp+', "GS_minerals_hist_jp" : '+ minerals_hist_jp + ', "RS_timber_hist_jp" : ' + RS_timber_hist_jp +', "RS_iron_hist_jp" : '+\
                          RS_iron_hist_jp+', "RS_other_hist_jp" : '+ RS_other_hist_jp+', "RS_minerals_hist_jp" : '+ RS_minerals_hist_jp + '},'
            data_list.append(temp_output)



    #remove last character of string
    output = data_list
    return output



# Start execution here!
if __name__ == '__main__':
    print ("Starting JSON data viz creation script...")

    data = getfile()
    output = create_output(data)
    for line in output:
        print(line)