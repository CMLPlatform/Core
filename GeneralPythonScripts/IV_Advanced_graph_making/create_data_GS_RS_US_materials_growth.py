import json
def getfile():
    #open the file
    #*** > give the path to the file.
    f=open('../../data/IV_Advanced_graph_making/US_GAS_RS_materials_growth.csv', 'r')

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
        timber_hist = line[1]
        timber_sc1 = line[2]
        timber_sc2 = line[3]
        #timber_sc3 = line[4]
        iron_hist = line[6]
        iron_sc1 = line[7]
        iron_sc2 = line[8]
        #iron_sc3 = line[9]
        other_hist = line[11]
        other_sc1 = line[12]
        other_sc2 = line[13]
        #other_sc3 = line[14]
        minerals_hist = line[16]
        minerals_sc1 = line[17]
        minerals_sc2 = line[18]
        RS_timber_hist = line[21]
        RS_timber_sc1 = line[22]
        RS_timber_sc2 = line[23]
        # timber_sc3 = line[4]
        RS_iron_hist = line[26]
        RS_iron_sc1 = line[27]
        RS_iron_sc2 = line[28]
        # iron_sc3 = line[9]
        RS_other_hist = line[31]
        RS_other_sc1 = line[32]
        RS_other_sc2 = line[33]
        # other_sc3 = line[14]
        RS_minerals_hist = line[36]
        RS_minerals_sc1 = line[37]
        RS_minerals_sc2 = line[38]
        #minerals_sc3 = line[19]

        #as we know the dataset by heart we can manipulate in a simple manner

        #we only take historical data now which is all years untill 2005
        if years < '2005':
            temp_output = '{"date" : "' + years + '-01-01"' + ', "GS_timber_hist" : ' + timber_hist +', "GS_iron_hist" : '+\
                          iron_hist+', "GS_other_hist" : '+ other_hist+', "GS_minerals_hist" : '+ minerals_hist + ', "RS_timber_hist" : ' + RS_timber_hist +', "RS_iron_hist" : '+\
                          RS_iron_hist+', "RS_other_hist" : '+ RS_other_hist+', "RS_minerals_hist" : '+ RS_minerals_hist + '},'
            data_list.append(temp_output)
        elif years == '2005':
            temp_output = '{"date" : "' + years + '-01-01"' + ', "GS_timber_hist" : ' + timber_hist + ', "GS_iron_hist" : ' + \
                          iron_hist + ', "GS_other_hist" : ' + other_hist + ', "GS_minerals_hist" : ' + minerals_hist + \
                          ', "GS_timber_sc1" : ' + timber_sc1 + ', "GS_iron_sc1" : ' + \
                          iron_sc1 + ', "GS_other_sc1" : ' + other_sc1 + ', "GS_minerals_sc1" : ' + minerals_sc1 \
                          + ', "GS_timber_sc2" : ' + timber_sc2 + ', "GS_iron_sc2" : ' + \
                          iron_sc2 + ', "GS_other_sc2" : ' + other_sc2 + ', "GS_minerals_sc2" : ' + minerals_sc2 \
                          + ', "RS_timber_hist" : ' + RS_timber_hist + ', "RS_iron_hist" : ' + \
                          RS_iron_hist + ', "RS_other_hist" : ' + RS_other_hist + ', "RS_minerals_hist" : ' + RS_minerals_hist + \
                          ', "RS_timber_sc1" : ' + RS_timber_sc1 + ', "RS_iron_sc1" : ' + \
                          RS_iron_sc1 + ', "RS_other_sc1" : ' + RS_other_sc1 + ', "RS_minerals_sc1" : ' + RS_minerals_sc1 \
                          + ', "RS_timber_sc2" : ' + RS_timber_sc2 + ', "RS_iron_sc2" : ' + \
                          RS_iron_sc2 + ', "RS_other_sc2" : ' + RS_other_sc2 + ', "RS_minerals_sc2" : ' + RS_minerals_sc2 \
                          + '},'
            data_list.append(temp_output)
        #after 2005 we have two scenarios we want to use
        else:
            temp_output = '{"date" : "' + years + '-01-01"' + ', "GS_timber_sc1" : ' + timber_sc1 +', "GS_iron_sc1" : '+\
                          iron_sc1+', "GS_other_sc1" : '+ other_sc1+', "GS_minerals_sc1" : '+ minerals_sc1 \
                          + ', "GS_timber_sc2" : ' + timber_sc2 + ', "GS_iron_sc2" : ' + \
                          iron_sc2 + ', "GS_other_sc2" : ' + other_sc2 + ', "GS_minerals_sc2" : ' + minerals_sc2+ ', "RS_timber_sc1" : ' + RS_timber_sc1 +', "RS_iron_sc1" : '+\
                          RS_iron_sc1+', "RS_other_sc1" : '+ RS_other_sc1+', "RS_minerals_sc1" : '+ RS_minerals_sc1 \
                          + ', "RS_timber_sc2" : ' + RS_timber_sc2 + ', "RS_iron_sc2" : ' + \
                          RS_iron_sc2 + ', "RS_other_sc2" : ' + RS_other_sc2 + ', "RS_minerals_sc2" : ' + RS_minerals_sc2+ '},'
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