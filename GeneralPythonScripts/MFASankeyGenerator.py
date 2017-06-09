
with open("/home/sidney/Dropbox/CML/NabeelMFA/dataInput.csv") as f:
    lis=[line.split('\t') for line in f]        # create a list of lists
    #set indices for export, import, production, consumption
    exp = 3
    imp = 4
    prod = 5
    cons = 6
    #remove header
    lis.pop(0)
    #create empty node list
    nodes=[]
    sources=[]


    key = 'id'
    value = 'name'
    key_s = 'source'
    target_s = 'target'
    value_s = 'strength'


    #nodes.append('{"'+key+'": 0')
    nodes.append('{"' + key + '": "Extraction"},\n')
    nodes.append('{"' + key + '": "Import"},\n')
    nodes.append('{"' + key + '": "Component Import"},\n')
    nodes.append('{"' + key + '": "Product Import"},\n')
    #nodes.append(',{"' + key + '": 1')
    #nodes.append(',"' + value + '": "Import"}')
    #nodes.append(',{"' + key + '": 2')
    #nodes.append(',"' + value + '": "Component Import"}')
    #nodes.append(',{"' + key + '": 3')
    #nodes.append(',"' + value + '": "Product Import"}')
    for enum,x in enumerate(lis):
        # remove weird enters
        x[-1] = x[-1].strip()

        enum = enum +4

        # if its RAW
        if x[0] == 'RAW':
            # it is either export=export, import=import, production = extraction, consumption=??
            #[
            #    {"node": 0, "name": "node0"},
            #{"source":0,"target":2,"value":2},

            #nodes.append('{"' + key + '": '+str(enum))
            nodes.append('{"' + key + '": "'+x[1]+'"},\n')
            #THESE ARE EXTRACTION
            sources.append('{"' + value_s + '": ' + x[5] + '')
            sources.append(',"' + key_s + '": ' + str(0))
            sources.append(',"' + target_s + '": ' + str(enum)+'},\n')
            #THESE ARE IMPORTS
            sources.append('{"' + value_s + '": ' + x[4] + '')
            sources.append(',"' + key_s + '": ' + str(1))
            sources.append(',"' + target_s + '": ' + str(enum) + '},\n')


        if x[0] == 'INT':
            # it is either export= component export, import=component import,
            t =0
        if x[0] == 'END':
            # it is either export= product export, import=product import,
            k = 0
    #print("{")
    #print('"nodes":[')
    print('var nodes = [')
    print(*nodes, sep='')

    #print('],')
    print('];')
    print('var edges = [')
    #print('"links":[')
    print(*sources, sep='')
    #print(']}')
    print('];')