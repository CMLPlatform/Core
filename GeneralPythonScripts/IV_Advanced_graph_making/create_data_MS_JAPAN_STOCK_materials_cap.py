import json
def getfile():
    #open the file
    #*** > give the path to the file.
    f=open('../../data/IV_Advanced_graph_making/JAPAN_stock_materials_cap.csv', 'r')

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
        #minerals_sc3 = line[19]

        #as we know the dataset by heart we can manipulate in a simple manner

        #we only take historical data now which is all years untill 2005
        if years < '2005':
            temp_output = '{"date" : "' + years + '-01-01"' + ', "MS_timber_hist_jp" : ' + timber_hist +', "MS_iron_hist_jp" : '+\
                          iron_hist+', "MS_other_hist_jp" : '+ other_hist+', "MS_minerals_hist_jp" : '+ minerals_hist + '},'
            data_list.append(temp_output)
        elif years == '2005':
            temp_output = '{"date" : "' + years + '-01-01"' + ', "MS_timber_hist_jp" : ' + timber_hist + ', "MS_iron_hist_jp" : ' + \
                          iron_hist + ', "MS_other_hist_jp" : ' + other_hist + ', "MS_minerals_hist_jp" : ' + minerals_hist + \
                          ', "MS_timber_sc1_jp" : ' + timber_sc1 + ', "MS_iron_sc1_jp" : ' + \
                          iron_sc1 + ', "MS_other_sc1_jp" : ' + other_sc1 + ', "MS_minerals_sc1_jp" : ' + minerals_sc1 \
                          + ', "MS_timber_sc2_jp" : ' + timber_sc2 + ', "MS_iron_sc2_jp" : ' + \
                          iron_sc2 + ', "MS_other_sc2_jp" : ' + other_sc2 + ', "MS_minerals_sc2_jp" : ' + minerals_sc2 \
                          + '},'

            data_list.append(temp_output)
        #after 2005 we have two scenarios we want to use
        else:
            temp_output = '{"date" : "' + years + '-01-01"' + ', "MS_timber_sc1_jp" : ' + timber_sc1 +', "MS_iron_sc1_jp" : '+\
                          iron_sc1+', "MS_other_sc1_jp" : '+ other_sc1+', "MS_minerals_sc1_jp" : '+ minerals_sc1 \
                          + ', "MS_timber_sc2_jp" : ' + timber_sc2 + ', "MS_iron_sc2_jp" : ' + \
                          iron_sc2 + ', "MS_other_sc2_jp" : ' + other_sc2 + ', "MS_minerals_sc2_jp" : ' + minerals_sc2+ '},'
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