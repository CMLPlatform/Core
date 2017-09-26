import json
def getfile():
    #open the file
    #*** > give the path to the file.
    f=open('../data/US_stock_materials.csv', 'r')

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
    id = 0
    id2 = 121
    id3 = 167
    json_string = "{"
    data_list = []
    #parse over the lines
    for line in input:
        years = line[0]
        timber_hist = line[1]
        timber_sc1 = line[2]
        timber_sc2 = line[3]
        timber_sc3 = line[4]
        iron_hist = line[6]
        iron_sc1 = line[7]
        iron_sc2 = line[8]
        iron_sc3 = line[9]
        other_hist = line[11]
        other_sc1 = line[12]
        other_sc2 = line[13]
        other_sc3 = line[14]
        minerals_hist = line[16]
        minerals_sc1 = line[17]
        minerals_sc2 = line[18]
        minerals_sc3 = line[19]

        #as we know the dataset by heart we can manipulate in a simple manner

        #we only take historical data now which is all years untill 2005
        if years <= '2005':

            #use id to identify the highest hierachy of the json files
            id = id + 1

            json_string += '"'+str(id)+'":{"scenarios":"MS_Historical_Series","year":'+years+\
                           ',"materials":[["timber",'+timber_hist+'],["iron",'+iron_hist+'],["other metals",'\
                           +other_hist+'],["minerals",'+minerals_hist+']]},'
        #after 2005 we have two scenarios we want to use
        else:
            id = id + 1

            #be careful with parsing here
            json_string += '"' + str(id) + '":{"scenarios":"MS_sc1","year":' + years + \
                       ',"materials":[["timber",' + timber_sc1 + '],["iron",' + iron_sc1 + '],["other metals",' \
                       + other_sc1 + '],["minerals",' + minerals_sc1 + ']]},'
            id2 = id2 + 1
            json_string += '"' + str(id2) + '":{"scenarios":"MS_sc2","year":' + years + \
                       ',"materials":[["timber",' + timber_sc2 + '],["iron",' + iron_sc2 + '],["other metals",' \
                       + other_sc2 + '],["minerals",' + minerals_sc2 + ']]},'
            id3 = id3 + 1
            json_string += '"' + str(id3) + '":{"scenarios":"MS_sc3","year":' + years + \
                       ',"materials":[["timber",' + timber_sc3 + '],["iron",' + iron_sc3 + '],["other metals",' \
                       + other_sc3 + '],["minerals",' + minerals_sc3 + ']]},'


    #remove last character of string
    json_string = json_string[:-1]
    json_string += '}'
    print(json_string)
    output = data_list
    return output



# Start execution here!
if __name__ == '__main__':
    print ("Starting JSON data viz creation script...")

    data = getfile()
    output = create_output(data)
    #for line in output:
    #    print(line)