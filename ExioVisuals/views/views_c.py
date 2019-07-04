
#*********SUPPLYCHAIN CODE
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect, render
from ExioVisuals.forms import supplychainLeftMode, supplychainRightMode
from ExioVisuals.views.views_a import  generateTrees
from ExioVisuals.forms import ProductSelectionForm, CountrySelectionForm, SubstanceSelectionForm, YearFSelectionForm
from ExioVisuals.models import GhgEmissions, Product, Country, Substance, YearF
import numpy as np
import h5py, json
from CMLMasterProject.settings import PATH_HDF5

#get the latest year (the model should be ordered in order for this to work)
latest_year = YearF.objects.values_list('name', flat=True)
latest_year_str = latest_year.reverse()[0]
latest_year_int = int(latest_year.reverse()[0])


def supplychain(request):
    #Retrieve skeleton of forms-------------------------------------------------------------
    formTree = ProductSelectionForm(request.POST or None)
    formTreeCountry = CountrySelectionForm(request.POST or None)
    formTreeSubstance = SubstanceSelectionForm(request.POST or None)
    formTreeYear = YearFSelectionForm(request.POST or None)
    leftFormSet = supplychainLeftMode()
    rightFormSet = supplychainRightMode()
    left_choice = ""
    right_choice = ""
     #retrieve filter data!
    if request.method == 'POST':
        data = request.POST

        leftInput = data.get('left')
        mode = data.get('selectMode')
        rightInput = data.get('right')
        exportRaw = request.POST.get('raw')


        if exportRaw != None and len(exportRaw)!= 0:



    #fill the empty list with the data (this time split even further by tabs)

            #print(exportRaw)
            #start making the csv file with "From" as columns and "To" as a row




            import csv
            from django.utils.encoding import smart_str




            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=output.csv'
            writer = csv.writer(response, csv.excel)
            response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
            firstColumn = []
            firstColumn.append(" ")
            TOlist = []

            import ast
            exportData = ast.literal_eval(exportRaw)

            import collections

            fromList = []
            toList = []


            #convert list of list to dictionary with FROM elements as unique keys
            dict_x = collections.defaultdict(list)
            dict_values = collections.defaultdict(list)
            for x in exportData:
                key = x[0]
                value= x[2]
                dict_x[key].append(value+"\t"+x[1])
                dict_values[key].append(value)
                fromList.append(key)
                toList.append(x[1])



            #make lists unique for CSV


            #fromList.insert(0," ")
            fromList = []
            for key in dict_x.keys():
                fromList.append(key)



            valueList = []
            newData = []
            newData1=[]
            #iterate over that dictionary to get the name data out of it (now it are list connected to keys so the order is fixed)
            for value in dict_x.values():
                newData1.append(value)
            for x in newData1:
                for y in x:
                    names = (y.split("\t"))
                    newData.append(names[1])
            #as newData is an ordered toList we can use the length of the unordered toList and uniquefy so we get enough for the CSV
            newData = newData[:len(set(toList))]
            #for each element of newData take it and on top write take that spefic element out of value list
            for value in dict_values.values():
                valueList.append(value)

            toList = []
            for z in newData:
                toList.append(z.replace(",", " "))
            # The order of the list is now aligned with the data itself
            #insert the from name to the list of data
            for x,item in enumerate(valueList):
                item.insert(0,fromList[x])

            toList.insert(0, "from/to")


            #write header
            writer.writerow(toList)
            #write row after row
            writer.writerows(valueList)




            #print(error)
            return response

        if mode == None:
            #error handling
            if not leftInput:
                error_status = {"error":"<From> input data has not been filled in properly."}
                return render(request, "ExioVisuals/error_page.html", error_status)
            if not rightInput:
                error_status = {"error":"<To> input data has not been filled in properly."}
                return render(request, "ExioVisuals/error_page.html", error_status)
            #do check if dimensions make sense and get the data
            if leftInput < rightInput:
                left_index = int(leftInput)
                left_choices = (supplychainLeftMode.CHOICES)
                left_choice = left_choices[left_index-1][1]
                right_index = int(rightInput)
                right_choices = (supplychainRightMode.CHOICES)
                right_choice = right_choices[right_index-1][1]

            else:
                error_status = {"error":"The selected dimensions cannot be visualized."}
                return render(request, "ExioVisuals/error_page.html", error_status)

        #start creating the filter according to that input
        if data != None:
            if left_choice == "Country of emission" and right_choice == "Sector of emission":
                #set title,description, size
                title = "Country and Sector of emission"
                description = ""

                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                regP = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = True
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = True
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False
                #select lowest nodes
                for i in productP:
                    i['selected'] = False
                    for x in i['children']:
                        x['selected'] = True
                        for y in x['children']:
                            y['selected'] = False
                            for k in y['children']:
                                k['selected'] = False


                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                secP = json.dumps(productP)
                regP = json.dumps(regP)
                yearData = json.dumps(yearData)


             #updata dictionary for filter options: form skeletons
                supplyChainData = ({'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title})
                nodesList, linkList, notUsed = defaultData(request,title)

                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'default': default})
                supplyChainData.update({'userSelectMode': "Country and Sector of emission"})
                supplyChainData.update({'title':"Country and Sector of emission"})


                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                supplyChainData.update({'mode_tree4': 2, 'warning_8':"","sectorOfProduction":secP})
                supplyChainData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                supplyChainData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
                supplyChainData.update({'mode_tree3': 2, 'warning_7':"","regionProducing":regP})
                supplyChainData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
                return render(request,'ExioVisuals/supplychain.html',supplyChainData)
            if left_choice == "Country of emission" and right_choice == "Country of supply":
                #set title,description, size
                title = "Country of emission and Country of supply"
                description = ""

                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                regP = json.loads(countryDataReady)
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = True

                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = True
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = True
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False

                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                productP = json.dumps(productP)
                yearData = json.dumps(yearData)
                regP = json.dumps(regP)


             #updata dictionary for filter options: form skeletons
                supplyChainData = ({'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title})
                nodesList, linkList, notUsed = defaultData(request,title)

                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'default': default})
                supplyChainData.update({'userSelectMode': "Country of emission and Country of supply"})


                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                supplyChainData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                supplyChainData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                supplyChainData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
                supplyChainData.update({'mode_tree3': 2, 'warning_7':"","regionProducing":regP})
                supplyChainData.update({'mode_tree6': 2, 'warning_10':"","regionSelling":regP})
                return render(request,'ExioVisuals/supplychain.html',supplyChainData)
            if left_choice == "Country of emission" and right_choice == "Product or service":
                #set title,description, size
                title = "Country of emission and Product or service"
                description = ""


                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                regP = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = True
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = True
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False
                #select lowest nodes
                for i in productP:
                    i['selected'] = False
                    for x in i['children']:
                        x['selected'] = True
                        for y in x['children']:
                            y['selected'] = False
                            for k in y['children']:
                                k['selected'] = False


                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                secP = json.dumps(productP)
                regP = json.dumps(regP)
                yearData = json.dumps(yearData)


             #updata dictionary for filter options: form skeletons
                supplyChainData = ({'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title})
                nodesList, linkList, notUsed = defaultData(request,title)

                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'default': default})
                supplyChainData.update({'userSelectMode': "Country of emission and Product or service"})


                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                supplyChainData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                supplyChainData.update({'mode_tree': 2, 'warning_6':"","productPurchased":secP})
                supplyChainData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
                supplyChainData.update({'mode_tree3': 2, 'warning_7':"","regionProducing":regP})
                supplyChainData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
                return render(request,'ExioVisuals/supplychain.html',supplyChainData)
            if left_choice == "Country of emission" and right_choice == "Country of consumption":
                #set title,description, size
                title = "Country of emission and Country of consumption"
                description = ""

                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                regP = json.loads(countryDataReady)

                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = True
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = True
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False


                productP = json.dumps(productP)

                regP = json.dumps(regP)
                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                productP = json.dumps(productP)
                yearData = json.dumps(yearData)

             #updata dictionary for filter options: form skeletons
                supplyChainData = ({'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title})
                nodesList, linkList, notUsed = defaultData(request,title)

                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'default': default})
                supplyChainData.update({'userSelectMode': "Country of emission and Country of consumption"})


                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                supplyChainData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                supplyChainData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                supplyChainData.update({'mode_tree2': 2, 'warning_5':"","regionConsumng":regP})
                supplyChainData.update({'mode_tree3': 2, 'warning_7':"","regionProducing":regP})
                supplyChainData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
                return render(request,'ExioVisuals/supplychain.html',supplyChainData)
            if left_choice == "Sector of emission" and right_choice == "Country of supply":
                #set title,description, size
                title = "Sector of emission and Country of supply"
                description = ""

                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                regP = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = True
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = True
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False
                #select lowest nodes
                for i in productP:
                    i['selected'] = False
                    for x in i['children']:
                        x['selected'] = True
                        for y in x['children']:
                            y['selected'] = False
                            for k in y['children']:
                                k['selected'] = False


                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                secP = json.dumps(productP)
                regP = json.dumps(regP)
                yearData = json.dumps(yearData)



             #updata dictionary for filter options: form skeletons
                supplyChainData = ({'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title})
                nodesList, linkList, notUsed = defaultData(request,title)

                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'default': default})
                supplyChainData.update({'userSelectMode': "Sector of emission and Country of supply"})


                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                supplyChainData.update({'mode_tree4': 2, 'warning_8':"","sectorOfProduction":secP})
                supplyChainData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                supplyChainData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
                supplyChainData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                supplyChainData.update({'mode_tree6': 2, 'warning_10':"","regionSelling":regP})
                return render(request,'ExioVisuals/supplychain.html',supplyChainData)
            if left_choice == "Sector of emission" and right_choice == "Product or service":
                #set title,description, size
                title = "Sector of emission and Product or service"
                description = ""

                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                regP = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = True
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False


                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False
                #select lowest nodes
                for i in productP:
                    i['selected'] = False
                    for x in i['children']:
                        x['selected'] = True
                        for y in x['children']:
                            y['selected'] = False
                            for k in y['children']:
                                k['selected'] = False


                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                secP = json.dumps(productP)

                yearData = json.dumps(yearData)

             #updata dictionary for filter options: form skeletons
                supplyChainData = ({'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title})
                nodesList, linkList, notUsed = defaultData(request,title)

                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'default': default})
                supplyChainData.update({'userSelectMode': "Sector of emission and Product or service"})


                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                supplyChainData.update({'mode_tree4': 2, 'warning_8':"","sectorOfProduction":secP})
                supplyChainData.update({'mode_tree': 2, 'warning_6':"","productPurchased":secP})
                supplyChainData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
                supplyChainData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                supplyChainData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
                return render(request,'ExioVisuals/supplychain.html',supplyChainData)
            if left_choice == "Sector of emission" and right_choice == "Country of consumption":
                #set title,description, size
                title = "Sector of emission and Country of consumption"
                description = ""

                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                regP = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = True
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = True
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False
                #select lowest nodes
                for i in productP:
                    i['selected'] = False
                    for x in i['children']:
                        x['selected'] = True
                        for y in x['children']:
                            y['selected'] = False
                            for k in y['children']:
                                k['selected'] = False


                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                secP = json.dumps(productP)
                regP = json.dumps(regP)
                yearData = json.dumps(yearData)



             #updata dictionary for filter options: form skeletons
                supplyChainData = ({'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title})
                
                nodesList, linkList, notUsed = defaultData(request,title)

                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'default': default})
                supplyChainData.update({'userSelectMode': "Sector of emission and Country of consumption"})


                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                supplyChainData.update({'mode_tree4': 2, 'warning_8':"","sectorOfProduction":secP})
                supplyChainData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                supplyChainData.update({'mode_tree2': 2, 'warning_5':"","regionConsumng":regP})
                supplyChainData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                supplyChainData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
                return render(request,'ExioVisuals/supplychain.html',supplyChainData)
            if left_choice == "Country of supply" and right_choice == "Product or service":
                #set title,description, size
                title = "Country of supply and Product or service"
                description = ""

                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                regP = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = True
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = True
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False
                #select lowest nodes
                for i in productP:
                    i['selected'] = False
                    for x in i['children']:
                        x['selected'] = True
                        for y in x['children']:
                            y['selected'] = False
                            for k in y['children']:
                                k['selected'] = False


                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                secP = json.dumps(productP)
                regP = json.dumps(regP)
                yearData = json.dumps(yearData)


             #updata dictionary for filter options: form skeletons
                supplyChainData = ({'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title})
                nodesList, linkList, notUsed = defaultData(request,title)

                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'default': default})
                supplyChainData.update({'userSelectMode': "Country of supply and Product or service"})


                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                supplyChainData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                supplyChainData.update({'mode_tree': 2, 'warning_6':"","productPurchased":secP})
                supplyChainData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
                supplyChainData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                supplyChainData.update({'mode_tree6': 2, 'warning_10':"","regionSelling":regP})
                return render(request,'ExioVisuals/supplychain.html',supplyChainData)
            if left_choice == "Country of supply" and right_choice == "Country of consumption":
                #set title,description, size
                title = "Country of supply and Country of consumption"
                description = ""

                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                regP = json.loads(countryDataReady)

                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = True
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = True
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False


                productP = json.dumps(productP)

                regP = json.dumps(regP)
                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                productP = json.dumps(productP)
                yearData = json.dumps(yearData)


             #updata dictionary for filter options: form skeletons
                supplyChainData = ({'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title})
                nodesList, linkList, notUsed = defaultData(request,title)

                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'default': default})
                supplyChainData.update({'userSelectMode': "Country of supply and Country of consumption"})


                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                supplyChainData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                supplyChainData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                supplyChainData.update({'mode_tree2': 2, 'warning_5':"","regionConsumng":regP})
                supplyChainData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                supplyChainData.update({'mode_tree6': 2, 'warning_10':"","regionSelling":regP})
                return render(request,'ExioVisuals/supplychain.html',supplyChainData)
            if left_choice == "Product or service" and right_choice == "Country of consumption":
                #set title,description, size
                title = "Product or service and Country of consumption"
                description = ""

                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                regP = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = True
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = True
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = True
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False
                #select lowest nodes
                for i in productP:
                    i['selected'] = False
                    for x in i['children']:
                        x['selected'] = True
                        for y in x['children']:
                            y['selected'] = False
                            for k in y['children']:
                                k['selected'] = False


                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                secP = json.dumps(productP)
                regP = json.dumps(regP)
                yearData = json.dumps(yearData)


             #updata dictionary for filter options: form skeletons
                supplyChainData = ({'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title})
                nodesList, linkList, notUsed = defaultData(request,title)

                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'default': default})
                supplyChainData.update({'userSelectMode': "Product or service and Country of consumption"})
                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})
                supplyChainData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                supplyChainData.update({'mode_tree': 2, 'warning_6':"","productPurchased":secP})
                supplyChainData.update({'mode_tree2': 2, 'warning_5':"","regionConsumng":regP})
                supplyChainData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                supplyChainData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
                return render(request,'ExioVisuals/supplychain.html',supplyChainData)
        #First and foremost try to retrieve any mode (decomposition data)
        #mode = (request.POST.get('y'))
 #************START RETRIEVING USER SELECTIONS*******************
        if mode != None:
            envP = (request.POST.getlist('ft_4[]'))
            envPtitles = []
            '''
            for x in envP:
                print("Environmental Pressure:")
                print(Substance.objects.get(pk=x))
                print(Substance.objects.values_list('name', flat=True).get(pk=x))
                name = (Substance.objects.values_list('name', flat=True).get(pk=x))
                envPtitles.append(name)

'''

            #as it only allows one year we will fetch one (there is a case that multiple years are selected due to cookies)
            year = (request.POST.get('ft_6[]'))
            #check if year has been filled in properly
            if not year:
                error_status = {"error":"<Year> data has not been filled in properly."}
                return render(request, "ExioVisuals/error_page.html", error_status)

            year = YearF.objects.values_list('name', flat=True).get(pk=year)
                #print(YearF.objects.values_list('name', flat=True).get(pk=x))
                #local = Product.objects.values_list('local', flat=True).get(pk=x)
                #year = YearF.objects.values_list('name', flat=True).get(pk=x)
                #lwst_level = Product.objects.values_list('lwst_level', flat=True).get(pk=x)
                # retrieve the indices for HDf5 query





            regP = (request.POST.getlist('ft_2[]'))
            regPdata = []
            regPtitles = []
            regPquery =[]
            regPparents = []
            for x in regP:

                #local = Product.objects.values_list('local', flat=True).get(pk=x)
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                #lwst_level = Product.objects.values_list('lwst_level', flat=True).get(pk=x)
                # retrieve the indices for HDf5 query
                id = Country.objects.values_list('id', flat=True).get(pk=x)
                #mitigate the offset
                id = id - 1
                regPparents.append(Country.objects.values_list('name', flat=True).get(pk=x))
                if len(name) > 25:
                    regPtitles.append(name[:40])
                else:
                    regPtitles.append(name)
                regPquery.append(name)
                regPdata.append(id)




            secP = (request.POST.getlist('ft_5[]'))
            secPdata = []
            secPtitles = []
            secPquery = []
            secPparents = []
            da = 0
            for x in secP:

                #local = Product.objects.values_list('local', flat=True).get(pk=x)
                name = Product.objects.values_list('name', flat=True).get(pk=x)
                #lwst_level = Product.objects.values_list('lwst_level', flat=True).get(pk=x)
                # retrieve the indices for HDf5 query
                id = Product.objects.values_list('id', flat=True).get(pk=x)
                #mitigate the offset
                id = id - 1
                secPparents.append(Product.objects.values_list('name', flat=True).get(pk=x))
                if len(name) > 25:
                    secPtitles.append(name[:40])
                else:
                    secPtitles.append(name)
                secPquery.append(name)
                secPdata.append(id)

            regRS = (request.POST.getlist('ft_7[]'))
            regRSdata = []
            regRStitles = []
            regRSquery = []
            regRSparents = []
            for x in regRS:

                #local = Product.objects.values_list('local', flat=True).get(pk=x)
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                #lwst_level = Product.objects.values_list('lwst_level', flat=True).get(pk=x)
                # retrieve the indices for HDf5 query
                id = Country.objects.values_list('id', flat=True).get(pk=x)
                #mitigate the offset
                id = id - 1
                regRSparents.append(Country.objects.values_list('name', flat=True).get(pk=x))
                if len(name) > 25:
                    regRStitles.append(name[:40])
                else:
                    regRStitles.append(name)
                regRSquery.append(name)
                regRSdata.append(id)

            secC = (request.POST.getlist('ft_3[]'))
            secCdata = []
            secCtitles = []
            secCquery = []
            secCparents = []
            for x in  secC:

                #local = Product.objects.values_list('local', flat=True).get(pk=x)
                name = Product.objects.values_list('name', flat=True).get(pk=x)
                #lwst_level = Product.objects.values_list('lwst_level', flat=True).get(pk=x)
                # retrieve the indices for HDf5 query
                id = Product.objects.values_list('id', flat=True).get(pk=x)
                #mitigate the offset
                id = id - 1
                secCparents.append(Product.objects.values_list('name', flat=True).get(pk=x))
                if len(name) > 25:
                    secCtitles.append(name[:40])
                else:
                    secCtitles.append(name)
                secCquery.append(name
                                 )
                secCdata.append(id)


            regC = (request.POST.getlist('ft_1[]'))
            regCdata = []
            regCtitles = []
            regCquery = []
            regCparents = []
            for x in regC:

                #local = Product.objects.values_list('local', flat=True).get(pk=x)
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                #lwst_level = Product.objects.values_list('lwst_level', flat=True).get(pk=x)
                # retrieve the indices for HDf5 query
                id = Country.objects.values_list('id', flat=True).get(pk=x)
                #mitigate the offset
                #id = id - 1
                regCparents.append(Country.objects.values_list('name', flat=True).get(pk=x))
                if len(name) > 25:
                    regCtitles.append(name[:40])
                else:
                    regCtitles.append(name)
                regCquery.append(name
                                 )
                regCdata.append(id)




            selectMode = (request.POST.get('selectMode'))




            #validate input

            if not regPdata:
                error_status = {"error":"<Country of Production> data has not been filled in properly."}
                return render(request, "ExioVisuals/error_page.html", error_status)
            if not secPdata:
                error_status = {"error":"<Sector of Production> data has not been filled in properly."}
                return render(request, "ExioVisuals/error_page.html", error_status)
            if not regRSdata:
                error_status = {"error":"<Region Selling> has not been filled in properly."}
                return render(request, "ExioVisuals/error_page.html", error_status)
            if not regCdata:
                error_status = {"error":"<Country of consumption> data has not been filled in properly."}
                return render(request, "ExioVisuals/error_page.html", error_status)
            if not secCdata:
                error_status = {"error":"<Sector of consumption> data has not been filled in properly."}
                return render(request, "ExioVisuals/error_page.html", error_status)

            #check which mode we are in
            if selectMode == "Country and Sector of emission":
                regPForm = list(zip(regPdata,regPtitles))
                secPForm = list(zip(secPdata,secPtitles))
                title = "Country and Sector of emission"
                #set cap on max plottable values
                if len(regPdata) > 40:
                    error_status = {"error":"Too many values selected in <Country of emission> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)
                if len(secPdata) > 40:
                    error_status = {"error":"Too many values selected in <Sector of emission> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)
                table = generateDesc(selectMode, envPtitles, year, regPquery, secPparents, regRSquery, regCparents,
                                     secCparents, "")

                nodesList, linkList, dataExport = queryHDF5(regPForm,secPForm,selectMode,year,regPdata,secPdata,regRSdata,regCdata,secCdata, request)
                supplyChainData = {"nodes": nodesList, "links": linkList , 'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title}

                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                regP = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = False
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False
                #select lowest nodes
                for i in productP:
                    i['selected'] = False
                    for x in i['children']:
                        x['selected'] = False
                        for y in x['children']:
                            y['selected'] = False
                            for k in y['children']:
                                k['selected'] = False


                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                secP = json.dumps(productP)
                regP = json.dumps(regP)
                yearData = json.dumps(yearData)


             #updata dictionary for filter options: form skeletons
                print(table)
                print("test")
                supplyChainData.update({'description': table})
                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})

                supplyChainData.update({'dataExport': dataExport})
                supplyChainData.update({'session': "session"})
                supplyChainData.update({'userSelectMode': "Country and Sector of emission"})
                supplyChainData.update({'title':"Country and Sector of emission"})


                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                supplyChainData.update({'mode_tree4': 2, 'warning_8':"","sectorOfProduction":secP})
                supplyChainData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                supplyChainData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
                supplyChainData.update({'mode_tree3': 2, 'warning_7':"","regionProducing":regP})
                supplyChainData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})

            if selectMode == "Country of emission and Country of supply":
                regPForm = list(zip(regPdata,regPtitles))
                regRSForm = list(zip(regRSdata,regRStitles))
                title = "Country of emission and Country of supply"
                #set cap on max plottable values
                if len(regPdata) > 40:
                    error_status = {"error":"Too many values selected in <Country of emission> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)
                if len(regRSdata) > 40:
                    error_status = {"error":"Too many values selected in <Region selling> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)
                table = generateDesc(selectMode, envPtitles, year, regPquery, secPparents, regRSquery, regCparents,
                                     secCparents, "")
                nodesList, linkList, dataExport = queryHDF5(regPForm,regRSForm,selectMode,year,regPdata,secPdata,regRSdata,regCdata,secCdata, request)
                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                regP = json.loads(countryDataReady)
                 #make year total unselectable in this case

                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = False
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False

                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                productP = json.dumps(productP)
                yearData = json.dumps(yearData)
                regP = json.dumps(regP)

                supplyChainData = {"nodes": nodesList, "links": linkList , 'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title}

                supplyChainData.update({'description': table})
                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'userSelectMode': "Country of emission and Country of supply"})
                supplyChainData.update({'session': "session"})
                supplyChainData.update({'dataExport': dataExport})
                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                supplyChainData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                supplyChainData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                supplyChainData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
                supplyChainData.update({'mode_tree3': 2, 'warning_7':"","regionProducing":regP})
                supplyChainData.update({'mode_tree6': 2, 'warning_10':"","regionSelling":regP})
            if selectMode == "Country of emission and Product or service":
                regPForm = list(zip(regPdata,regPtitles))
                secCForm = list(zip(secCdata,secCtitles))
                #set cap on max plottable values
                if len(regPdata) > 40:
                    error_status = {"error":"Too many values selected in <Country of emission> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)
                if len(secCdata) > 40:
                    error_status = {"error":"Too many values selected in <Product or service> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)
                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                regP = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)


                title="Country of emission and Product or service"
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = False
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False
                #select lowest nodes
                for i in productP:
                    i['selected'] = False
                    for x in i['children']:
                        x['selected'] = False
                        for y in x['children']:
                            y['selected'] = False
                            for k in y['children']:
                                k['selected'] = False


                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                secP = json.dumps(productP)
                yearData = json.dumps(yearData)
                regP = json.dumps(regP)
                nodesList, linkList, dataExport = queryHDF5(regPForm,secCForm,selectMode,year,regPdata,secPdata,regRSdata,regCdata,secCdata, request)
                table = generateDesc(selectMode, envPtitles, year, regPquery, secPparents, regRSquery, regCparents,
                                     secCparents, "")

                supplyChainData = {"nodes": nodesList, "links": linkList , 'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title}
                supplyChainData.update({'description': table})
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'userSelectMode': "Country of emission and Product or service"})

                supplyChainData.update({'session': "session"})
                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})
                supplyChainData.update({'dataExport': dataExport})
                supplyChainData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                supplyChainData.update({'mode_tree': 2, 'warning_6':"","productPurchased":secP})
                supplyChainData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
                supplyChainData.update({'mode_tree3': 2, 'warning_7':"","regionProducing":regP})
                supplyChainData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})

            if selectMode == "Country of emission and Country of consumption":
                regPForm = list(zip(regPdata,regPtitles))
                regCForm = list(zip(regCdata,regCtitles))

                title = "Country of emission and Country of consumption"
                #set cap on max plottable values
                if len(regCdata) > 40:
                    error_status = {"error":"Too many values selected in <Country of consumption> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)
                if len(regPdata) > 40:
                    error_status = {"error":"Too many values selected in <Country of emission> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)

                nodesList, linkList, dataExport = queryHDF5(regPForm,regCForm,selectMode,year,regPdata,secPdata,regRSdata,regCdata,secCdata, request)
                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                regP = json.loads(countryDataReady)
                table = generateDesc(selectMode, envPtitles, year, regPquery, secPparents, regRSquery, regCparents,
                                     secCparents, "")
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = False

                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = False
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False

                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                productP = json.dumps(productP)
                yearData = json.dumps(yearData)
                regP = json.dumps(regP)

                supplyChainData = {"nodes": nodesList, "links": linkList , 'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title}

                supplyChainData.update({'dataExport': dataExport})

                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'userSelectMode': "Country of emission and Country of consumption"})
                supplyChainData.update({'description': table})
                supplyChainData.update({'session': "session"})
                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                supplyChainData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                supplyChainData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                supplyChainData.update({'mode_tree2': 2, 'warning_5':"","regionConsumng":regP})
                supplyChainData.update({'mode_tree3': 2, 'warning_7':"","regionProducing":regP})
                supplyChainData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})

            if selectMode == "Sector of emission and Country of supply":
                secPForm = list(zip(secPdata,secPtitles))
                regRSForm = list(zip(regRSdata,regRStitles))
                title = "Sector of emission and Country of supply"
                #set cap on max plottable values
                if len(regRSdata) > 40:
                    error_status = {"error":"Too many values selected in <Country of supply> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)
                if len(secPdata) > 40:
                    error_status = {"error":"Too many values selected in <Sector of emission> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)
                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                regP = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                table = generateDesc(selectMode, envPtitles, year, regPquery, secPparents, regRSquery, regCparents,
                                     secCparents, "")
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = False
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False
                #select lowest nodes
                for i in productP:
                    i['selected'] = False
                    for x in i['children']:
                        x['selected'] = False
                        for y in x['children']:
                            y['selected'] = False
                            for k in y['children']:
                                k['selected'] = False


                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                secP = json.dumps(productP)
                regP = json.dumps(regP)
                yearData = json.dumps(yearData)
                nodesList, linkList, dataExport = queryHDF5(secPForm,regRSForm,selectMode,year,regPdata,secPdata,regRSdata,regCdata,secCdata, request)
                supplyChainData = {"nodes": nodesList, "links": linkList , 'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title}
                supplyChainData.update({'session': "session"})
                supplyChainData.update({'dataExport': dataExport})

                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'userSelectMode': "Sector of emission and Country of supply"})
                supplyChainData.update({'description': table})

                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                supplyChainData.update({'mode_tree4': 2, 'warning_8':"","sectorOfProduction":secP})
                supplyChainData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                supplyChainData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
                supplyChainData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                supplyChainData.update({'mode_tree6': 2, 'warning_10':"","regionSelling":regP})


            if selectMode == "Sector of emission and Product or service":
                secCForm = list(zip(secCdata,secCtitles))
                secPForm = list(zip(secPdata,secPtitles))
                #set cap on max plottable values
                if len(secPdata) > 40:
                    error_status = {"error":"Too many values selected in <Sector of emission> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)
                if len(secCdata) > 40:
                    error_status = {"error":"Too many values selected in <Product or service> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)
                table = generateDesc(selectMode, envPtitles, year, regPquery, secPparents, regRSquery, regCparents,
                                     secCparents, "")
                title = "Sector of emission and Product or service"
                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                regP = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = False
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False


                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False
                #select lowest nodes
                for i in productP:
                    i['selected'] = False
                    for x in i['children']:
                        x['selected'] = False
                        for y in x['children']:
                            y['selected'] = False
                            for k in y['children']:
                                k['selected'] = False


                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                secP = json.dumps(productP)

                yearData = json.dumps(yearData)
                nodesList, linkList, dataExport = queryHDF5(secPForm,secCForm,selectMode,year,regPdata,secPdata,regRSdata,regCdata,secCdata, request)

             #updata dictionary for filter options: form skeletons
                supplyChainData = {"nodes": nodesList, "links": linkList , 'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title}
                supplyChainData.update({'session': "session"})
                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'userSelectMode': "Sector of emission and Product or service"})
                supplyChainData.update({'dataExport': dataExport})
                supplyChainData.update({'description': table})
                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                supplyChainData.update({'mode_tree4': 2, 'warning_8':"","sectorOfProduction":secP})
                supplyChainData.update({'mode_tree': 2, 'warning_6':"","productPurchased":secP})
                supplyChainData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
                supplyChainData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                supplyChainData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
            if selectMode == "Sector of emission and Country of consumption":
                regCForm = list(zip(regCdata,regCtitles))
                secPForm = list(zip(secPdata,secPtitles))
                #set cap on max plottable values
                if len(regCdata) > 40:
                    error_status = {"error":"Too many values selected in <Country of consumption> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)
                if len(secPdata) > 40:
                    error_status = {"error":"Too many values selected in <Sector of emission> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)

                nodesList, linkList, dataExport = queryHDF5(secPForm,regCForm,selectMode,year,regPdata,secPdata,regRSdata,regCdata,secCdata, request)
                table = generateDesc(selectMode, envPtitles, year, regPquery, secPparents, regRSquery, regCparents,
                                     secCparents, "")
                title = "Sector of emission and Country of consumption"
                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                regP = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = False
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False
                #select lowest nodes
                for i in productP:
                    i['selected'] = False
                    for x in i['children']:
                        x['selected'] = False
                        for y in x['children']:
                            y['selected'] = False
                            for k in y['children']:
                                k['selected'] = False


                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                secP = json.dumps(productP)
                regP = json.dumps(regP)
                yearData = json.dumps(yearData)



             #updata dictionary for filter options: form skeletons
                supplyChainData = {"nodes": nodesList, "links": linkList , 'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title}
                supplyChainData.update({'dataExport': dataExport})
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'userSelectMode': "Sector of emission and Country of consumption"})

                supplyChainData.update({'session': "session"})
                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})
                supplyChainData.update({'description': table})
                supplyChainData.update({'mode_tree4': 2, 'warning_8':"","sectorOfProduction":secP})
                supplyChainData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                supplyChainData.update({'mode_tree2': 2, 'warning_5':"","regionConsumng":regP})
                supplyChainData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                supplyChainData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
            if selectMode == "Country of supply and Product or service":
                secCForm = list(zip(secCdata,secCtitles))
                regRSForm = list(zip(regRSdata,regRStitles))
                title = "Country of supply and Product or service"
                #set cap on max plottable values
                if len(regRSdata) > 40:
                    error_status = {"error":"Too many values selected in <Country of supply> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)
                if len(secCdata) > 40:
                    error_status = {"error":"Too many values selected in <Product or service> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)

                nodesList, linkList, dataExport = queryHDF5(regRSForm,secCForm,selectMode,year,regPdata,secPdata,regRSdata,regCdata,secCdata, request)
                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                regP = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                table = generateDesc(selectMode, envPtitles, year, regPquery, secPparents, regRSquery, regCparents,
                                     secCparents, "")
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = False
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False
                #select lowest nodes
                for i in productP:
                    i['selected'] = False
                    for x in i['children']:
                        x['selected'] = False
                        for y in x['children']:
                            y['selected'] = False
                            for k in y['children']:
                                k['selected'] = False


                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                secP = json.dumps(productP)
                regP = json.dumps(regP)
                yearData = json.dumps(yearData)


                supplyChainData = {"nodes": nodesList, "links": linkList , 'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title}

                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'description': table})
                supplyChainData.update({'userSelectMode': "Country of supply and Product or service"})
                supplyChainData.update({'dataExport': dataExport})
                supplyChainData.update({'session': "session"})
                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                supplyChainData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                supplyChainData.update({'mode_tree': 2, 'warning_6':"","productPurchased":secP})
                supplyChainData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
                supplyChainData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                supplyChainData.update({'mode_tree6': 2, 'warning_10':"","regionSelling":regP})
            if selectMode == "Country of supply and Country of consumption":
                regCForm = list(zip(regCdata,regCtitles))
                regRSForm = list(zip(regRSdata,regRStitles))
                table = generateDesc(selectMode, envPtitles, year, regPquery, secPparents, regRSquery, regCparents,
                                     secCparents, "")
                #set cap on max plottable values
                if len(regCdata) > 40:
                    error_status = {"error":"Too many values selected in <Country of consumption> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)
                if len(regRSdata) > 40:
                    error_status = {"error":"Too many values selected in <Country of supply> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)

                nodesList, linkList, dataExport = queryHDF5(regRSForm,regCForm,selectMode,year,regPdata,secPdata,regRSdata,regCdata,secCdata, request)

                title = "Country of supply and Country of consumption"
                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                regP = json.loads(countryDataReady)

                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = False
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False


                productP = json.dumps(productP)

                regP = json.dumps(regP)
                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                productP = json.dumps(productP)
                yearData = json.dumps(yearData)


                supplyChainData = {"nodes": nodesList, "links": linkList , 'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title}

                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'userSelectMode': "Country of supply and Country of consumption"})
                supplyChainData.update({'description': table})
                supplyChainData.update({'session': "session"})
                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})
                supplyChainData.update({'dataExport': dataExport})
                supplyChainData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                supplyChainData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                supplyChainData.update({'mode_tree2': 2, 'warning_5':"","regionConsumng":regP})
                supplyChainData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                supplyChainData.update({'mode_tree6': 2, 'warning_10':"","regionSelling":regP})
            if selectMode == "Product or service and Country of consumption":
                secCForm = list(zip(secCdata,secCtitles))
                regCForm = list(zip(regCdata,regCtitles))
                title = "Product or service and Country of consumption"
                table = generateDesc(selectMode, envPtitles, year, regPquery, secPparents, regRSquery, regCparents,
                                     secCparents, "")
                #set cap on max plottable values
                if len(regCdata) > 40:
                    error_status = {"error":"Too many values selected in <Country of consumption> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)
                if len(secCdata) > 40:
                    error_status = {"error":"Too many values selected in <Product or service> for plottable output."}
                    return render(request, "ExioVisuals/error_page.html", error_status)

                nodesList, linkList, dataExport = queryHDF5(secCForm,regCForm,selectMode,year,regPdata,secPdata,regRSdata,regCdata,secCdata, request)
                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                regP = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == latest_year_str:
                            x['selected'] = False
                for i in parsed_json:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False
                for i in regP:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                    y['selected'] = False

                for i in parsed_json2:
                    if i['title'] == "Total":
                        i['selected'] = False
                        for x in i['children']:
                            x['selected'] = False
                            for y in x['children']:
                                y['selected'] = False
                                for k in y['children']:
                                    k['selected'] = False
                #select lowest nodes
                for i in productP:
                    i['selected'] = False
                    for x in i['children']:
                        x['selected'] = False
                        for y in x['children']:
                            y['selected'] = False
                            for k in y['children']:
                                k['selected'] = False


                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                secP = json.dumps(productP)
                regP = json.dumps(regP)
                yearData = json.dumps(yearData)


                supplyChainData = {"nodes": nodesList, "links": linkList , 'leftMode':leftFormSet, 'rightMode':rightFormSet, 'title':title}
                supplyChainData.update({'session': "session"})
                supplyChainData.update({"nodes": nodesList, "links": linkList })
                supplyChainData.update({'sourceData': sourceData})
                supplyChainData.update({'countryDataReady': countryDataReady})
                supplyChainData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #send signal for popup and default data
                popup = 1
                supplyChainData.update({'description': table})
                default =1
                supplyChainData.update({'popup': popup})
                supplyChainData.update({'userSelectMode': "Product or service and Country of consumption"})
                #create select modes for fancyTree : so single select or multiple
                supplyChainData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})
                supplyChainData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                supplyChainData.update({'mode_tree': 2, 'warning_6':"","productPurchased":secP})
                supplyChainData.update({'mode_tree2': 2, 'warning_5':"","regionConsumng":regP})
                supplyChainData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                supplyChainData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
                supplyChainData.update({'dataExport': dataExport})


        return render(request,'ExioVisuals/supplychain.html',supplyChainData)

    if request.method != 'POST':
        print("done")
        supplyChainData = ({'session': "RESET"})
        # load tree with nothing suich that we can reset the cookies and remove any previous selections
        supplyChainData.update({'mode_tree7': 2, 'warning_11': "", 'yearDataReady': ["N/A", "N/A"]})
        supplyChainData.update({'mode_tree4': 1, 'warning_8': "", "sectorOfProduction": ["N/A", "N/A"]})
        supplyChainData.update({'mode_tree': 1, 'warning_6': "", "productPurchased": ["N/A", "N/A"]})
        supplyChainData.update({'mode_tree2': 1, 'warning_5': "", "regionConsumng": ["N/A", "N/A"]})
        supplyChainData.update({'mode_tree3': 2, 'warning_7': "", "regionProducing": ["N/A", "N/A"]})
        supplyChainData.update({'mode_tree6': 1, 'warning_10': "", "regionSelling": ["N/A", "N/A"]})
        supplyChainData.update({'mode_tree5': 1, 'warning_10': "", "substanceDataReady": ["N/A", "N/A"]})

        supplyChainData.update({'leftMode':leftFormSet, 'rightMode':rightFormSet,'desc': '<div class="alert alert-info"><h2><span class="glyphicon glyphicon-arrow-up" aria-hidden="true"></span></H2><strong><span class="glyphicon glyphicon-info-sign" aria-hidden="true"></span>  Select your dimension in the navigation bar.</strong></div>' })
    #basic first page
    return render(request,'ExioVisuals/supplychain.html', supplyChainData)

#this function is adjusted to create the plotdata simultaniously, as it saves extra loops and parsing efforts
def queryHDF5(fromParam, toParam, plotMode, year, regP, secP, regRS, regC,secC,request):
    if plotMode == "Country and Sector of emission":
        #order lists for query
        fromParamAdjusted = (sorted(fromParam))
        toParamAdjusted = sorted(toParam)
        nodesList = []

        linksList = []
        dataExport1 = []
        with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(year) ,'r') as hf:
            db = (hf.get('region{0}'.format(int(regC[0]))))
            #set offset to create matching target indices for toParameters
            offsetTarget = len(fromParamAdjusted)
            #add node names for the FromParameters
            for index,values in enumerate(fromParamAdjusted):
                nodesList.append({"name":values[1]})
            #add node names for the toParameters
            for index,values in enumerate(toParamAdjusted):
                nodesList.append({"name":values[1]})
            #start creating links beteween nodes
            for source,values in enumerate(fromParamAdjusted):
                #print(index)
                regPindex = values[0]
                for idx, inputs in enumerate(toParamAdjusted):

                    toNames = inputs[1]
                    indices = inputs[0]
                    target = idx+offsetTarget
                    value =  db[regPindex,indices,int(regRS[0]),int(secC[0])]

                    linksList.append({"source": source, "target":target, "value":value})
                    sourceData = str(source)+"_"+values[1]
                    targetData = str(target)+"_"+toNames
                    valueData = str(value)
                    dataExport1.append(sourceData + "\t"+targetData+"\t"+valueData)
        dataExport = []
        for line in dataExport1:
            dataExport.append(line.split("\t"))

        #regPadjusted = [point[0] for point in pack]
        #plotDatatitles = [point[1] for point in pack]
        return nodesList, linksList, dataExport
    if plotMode == "Country of emission and Country of supply":
        #order lists for query
        fromParamAdjusted = (sorted(fromParam))
        toParamAdjusted = sorted(toParam)
        nodesList = []

        linksList = []
        dataExport1 = []
        with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(year) ,'r') as hf:
            db = (hf.get('region{0}'.format(int(regC[0]))))
            #set offset to create matching target indices for toParameters
            offsetTarget = len(fromParamAdjusted)
            #add node names for the FromParameters
            for index,values in enumerate(fromParamAdjusted):
                nodesList.append({"name":values[1]})
            #add node names for the toParameters
            for index,values in enumerate(toParamAdjusted):
                nodesList.append({"name":values[1]})
            #start creating links beteween nodes
            for source,values in enumerate(fromParamAdjusted):
                #print(index)
                regPindex = values[0]
                for idx, inputs in enumerate(toParamAdjusted):

                    toNames = inputs[1]
                    indices = inputs[0]
                    target = idx+offsetTarget
                    value =  db[regPindex,int(secP[0]),indices,int(secC[0])]

                    linksList.append({"source": source, "target":target, "value":value})
                    sourceData = str(source)+"_"+values[1]
                    targetData = str(target)+"_"+toNames
                    valueData = str(value)
                    dataExport1.append(sourceData + "\t"+targetData+"\t"+valueData)
        dataExport = []
        for line in dataExport1:
            dataExport.append(line.split("\t"))

        #regPadjusted = [point[0] for point in pack]
        #plotDatatitles = [point[1] for point in pack]
        return nodesList, linksList, dataExport

    if plotMode == "Country of emission and Product or service":
        #order lists for query
        fromParamAdjusted = (sorted(fromParam))
        toParamAdjusted = sorted(toParam)
        nodesList = []

        linksList = []
        dataExport1 = []
        with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(year) ,'r') as hf:
            db = (hf.get('region{0}'.format(int(regC[0]))))
            #set offset to create matching target indices for toParameters
            offsetTarget = len(fromParamAdjusted)
            #add node names for the FromParameters
            for index,values in enumerate(fromParamAdjusted):
                nodesList.append({"name":values[1]})
            #add node names for the toParameters
            for index,values in enumerate(toParamAdjusted):
                nodesList.append({"name":values[1]})
            #start creating links beteween nodes
            for source,values in enumerate(fromParamAdjusted):
                #print(index)
                regPindex = values[0]
                for idx, inputs in enumerate(toParamAdjusted):

                    toNames = inputs[1]
                    indices = inputs[0]
                    target = idx+offsetTarget
                    value =  db[regPindex,int(secP[0]),int(regRS[0]),indices]

                    linksList.append({"source": source, "target":target, "value":value})
                    sourceData = str(source)+"_"+values[1]
                    targetData = str(target)+"_"+toNames
                    valueData = str(value)
                    dataExport1.append(sourceData + "\t"+targetData+"\t"+valueData)
        dataExport = []
        for line in dataExport1:
            dataExport.append(line.split("\t"))

        #regPadjusted = [point[0] for point in pack]
        #plotDatatitles = [point[1] for point in pack]
        return nodesList, linksList, dataExport

    if plotMode == "Country of emission and Country of consumption":
        #order lists for query
        fromParamAdjusted = (sorted(fromParam))
        toParamAdjusted = sorted(toParam)
        nodesList = []
        linksList = []
                #add node names for the FromParameters
        for index,values in enumerate(fromParamAdjusted):
            nodesList.append({"name":values[1]})
        #add node names for the toParameters
        for index,values in enumerate(toParamAdjusted):
            nodesList.append({"name":values[1]})
         #set offset to create matching target indices for toParameters
        offsetTarget = len(fromParamAdjusted)
        dataExport1 = []
        with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(year) ,'r') as hf:
            for index, id_secC in enumerate(fromParamAdjusted):

                source = index
                id_inquery = id_secC[0]

                for index, id_regC in enumerate(toParamAdjusted):
                    id = id_regC[0]
                    toNames = id_regC[1]
                    target = index + offsetTarget
                    db = (hf.get('region{0}'.format(id)))
                    value = db[id_inquery,int(secP[0]),int(regRS[0]),int(secC[0])]
                    linksList.append({"source": source, "target":target, "value":value})
                    sourceData = str(source)+"_"+id_secC[1]
                    targetData = str(target)+"_"+toNames
                    valueData = str(value)

                    dataExport1.append(sourceData + "\t"+targetData+"\t"+valueData)
        dataExport = []
        for line in dataExport1:
            dataExport.append(line.split("\t"))


        #regPadjusted = [point[0] for point in pack]
        #plotDatatitles = [point[1] for point in pack]
        return nodesList, linksList, dataExport
    if plotMode == "Sector of emission and Country of supply":
                #order lists for query
        fromParamAdjusted = (sorted(fromParam))
        toParamAdjusted = sorted(toParam)
        nodesList = []

        linksList = []
        dataExport1  = []
        with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(year) ,'r') as hf:
            db = (hf.get('region{0}'.format(int(regC[0]))))
            #set offset to create matching target indices for toParameters
            offsetTarget = len(fromParamAdjusted)
            #add node names for the FromParameters
            for index,values in enumerate(fromParamAdjusted):
                nodesList.append({"name":values[1]})
            #add node names for the toParameters
            for index,values in enumerate(toParamAdjusted):
                nodesList.append({"name":values[1]})
            #start creating links beteween nodes
            for source,values in enumerate(fromParamAdjusted):
                #print(index)
                secPindex = values[0]
                #print(secPindex)
                for idx, inputs in enumerate(toParamAdjusted):
                    toNames = inputs[1]
                    indices = inputs[0]
                    target = idx+offsetTarget

                    value =  db[int(regP[0]),secPindex,indices,int(secC[0])]
                    linksList.append({"source": source, "target":target, "value":value})
                    sourceData = str(source)+"_"+values[1]
                    targetData = str(target)+"_"+toNames
                    valueData = str(value)
                    dataExport1.append(sourceData + "\t"+targetData+"\t"+valueData)
        dataExport = []
        for line in dataExport1:
            dataExport.append(line.split("\t"))

        #regPadjusted = [point[0] for point in pack]
        #plotDatatitles = [point[1] for point in pack]
        return nodesList, linksList, dataExport
    if plotMode == "Sector of emission and Product or service":
                #order lists for query
        fromParamAdjusted = (sorted(fromParam))
        toParamAdjusted = sorted(toParam)
        nodesList = []

        linksList = []
        dataExport1 = []
        with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(year) ,'r') as hf:
            db = (hf.get('region{0}'.format(int(regC[0]))))
            #set offset to create matching target indices for toParameters
            offsetTarget = len(fromParamAdjusted)
            #add node names for the FromParameters
            for index,values in enumerate(fromParamAdjusted):
                nodesList.append({"name":values[1]})
            #add node names for the toParameters
            for index,values in enumerate(toParamAdjusted):
                nodesList.append({"name":values[1]})
            #start creating links beteween nodes
            for source,values in enumerate(fromParamAdjusted):
                #print(index)
                secPindex = values[0]
                #print(secPindex)
                for idx, inputs in enumerate(toParamAdjusted):
                    toNames = inputs[1]
                    indices = inputs[0]
                    target = idx+offsetTarget

                    value =  db[int(regP[0]),secPindex,int(regRS[0]),indices]
                    linksList.append({"source": source, "target":target, "value":value})
                    sourceData = str(source)+"_"+values[1]
                    targetData = str(target)+"_"+toNames
                    valueData = str(value)
                    dataExport1.append(sourceData + "\t"+targetData+"\t"+valueData)
        dataExport = []
        for line in dataExport1:
            dataExport.append(line.split("\t"))

        #regPadjusted = [point[0] for point in pack]
        #plotDatatitles = [point[1] for point in pack]
        return nodesList, linksList, dataExport

    if plotMode == "Sector of emission and Country of consumption":
        #order lists for query
        fromParamAdjusted = (sorted(fromParam))
        toParamAdjusted = sorted(toParam)
        nodesList = []
        linksList = []
        dataExport1 = []
                #add node names for the FromParameters
        for index,values in enumerate(fromParamAdjusted):
            nodesList.append({"name":values[1]})
        #add node names for the toParameters
        for index,values in enumerate(toParamAdjusted):
            nodesList.append({"name":values[1]})
         #set offset to create matching target indices for toParameters
        offsetTarget = len(fromParamAdjusted)

        with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(year) ,'r') as hf:
            for index, id_secP in enumerate(fromParamAdjusted):

                source = index
                id_inquery = id_secP[0]

                for index, id_regC in enumerate(toParamAdjusted):
                    id = id_regC[0]
                    toNames = id_regC[1]
                    target = index + offsetTarget
                    db = (hf.get('region{0}'.format(id)))
                    value = db[int(regP[0]),id_inquery,int(regRS[0]),int(secC[0])]
                    linksList.append({"source": source, "target":target, "value":value})
                    sourceData = str(source)+"_"+id_secP[1]
                    targetData = str(target)+"_"+toNames
                    valueData = str(value)
                    dataExport1.append(sourceData + "\t"+targetData+"\t"+valueData)
        dataExport = []
        for line in dataExport1:
            dataExport.append(line.split("\t"))

        #regPadjusted = [point[0] for point in pack]
        #plotDatatitles = [point[1] for point in pack]
        return nodesList, linksList, dataExport

    if plotMode == "Country of supply and Product or service":
                #order lists for query
        fromParamAdjusted = (sorted(fromParam))
        toParamAdjusted = sorted(toParam)
        nodesList = []

        linksList = []
        dataExport1 = []
        with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(year) ,'r') as hf:
            db = (hf.get('region{0}'.format(int(regC[0]))))
            #set offset to create matching target indices for toParameters
            offsetTarget = len(fromParamAdjusted)
            #add node names for the FromParameters
            for index,values in enumerate(fromParamAdjusted):
                nodesList.append({"name":values[1]})
            #add node names for the toParameters
            for index,values in enumerate(toParamAdjusted):
                nodesList.append({"name":values[1]})
            #start creating links beteween nod#(fromParam, toParam, plotMode, year, regP, secP, regRS, regC,secC,request):es
            for source,values in enumerate(fromParamAdjusted):
                #print(index)
                regRSindex = values[0]
                #print(secPindex)
                for idx, inputs in enumerate(toParamAdjusted):
                    toNames = inputs[1]
                    indices = inputs[0]
                    target = idx+offsetTarget

                    value =  db[int(regP[0]),int(secP[0]),regRSindex,indices]
                    linksList.append({"source": source, "target":target, "value":value})
                    sourceData = str(source)+"_"+values[1]
                    targetData = str(target)+"_"+toNames
                    valueData = str(value)
                    dataExport1.append(sourceData + "\t"+targetData+"\t"+valueData)
        dataExport = []
        for line in dataExport1:
            dataExport.append(line.split("\t"))

        #regPadjusted = [point[0] for point in pack]
        #plotDatatitles = [point[1] for point in pack]
        return nodesList, linksList, dataExport

    if plotMode == "Country of supply and Country of consumption":
        #order lists for query
        fromParamAdjusted = (sorted(fromParam))
        toParamAdjusted = sorted(toParam)
        nodesList = []
        linksList = []
                #add node names for the FromParameters
        for index,values in enumerate(fromParamAdjusted):
            nodesList.append({"name":values[1]})
        #add node names for the toParameters
        for index,values in enumerate(toParamAdjusted):
            nodesList.append({"name":values[1]})
         #set offset to create matching target indices for toParameters
        offsetTarget = len(fromParamAdjusted)

        dataExport1 = []
        with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(year) ,'r') as hf:
            for index, id_regRS in enumerate(fromParamAdjusted):

                source = index
                id_inquery = id_regRS[0]

                for index, id_regC in enumerate(toParamAdjusted):
                    id = id_regC[0]
                    toNames = id_regC[1]
                    target = index + offsetTarget
                    db = (hf.get('region{0}'.format(id)))
                    value = db[int(regP[0]),int(secP[0]),id_inquery,int(secC[0])]
                    linksList.append({"source": source, "target":target, "value":value})
                    sourceData = str(source)+"_"+id_regRS[1]
                    targetData = str(target)+"_"+toNames
                    valueData = str(value)
                    dataExport1.append(sourceData + "\t"+targetData+"\t"+valueData)
        dataExport = []
        for line in dataExport1:
            dataExport.append(line.split("\t"))

        #regPadjusted = [point[0] for point in pack]
        #plotDatatitles = [point[1] for point in pack]
        return nodesList, linksList, dataExport
    if plotMode == "Product or service and Country of consumption":
        #order lists for query
        fromParamAdjusted = (sorted(fromParam))
        toParamAdjusted = sorted(toParam)
        nodesList = []
        linksList = []
        dataExport1 = []
                #add node names for the FromParameters
        for index,values in enumerate(fromParamAdjusted):
            nodesList.append({"name":values[1]})
        #add node names for the toParameters
        for index,values in enumerate(toParamAdjusted):
            nodesList.append({"name":values[1]})
         #set offset to create matching target indices for toParameters
        offsetTarget = len(fromParamAdjusted)

        with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(year) ,'r') as hf:
            for index, id_PP in enumerate(fromParamAdjusted):

                source = index
                id_inquery = id_PP[0]

                for index, id_regC in enumerate(toParamAdjusted):
                    id = id_regC[0]
                    toNames = id_regC[1]
                    target = index + offsetTarget
                    db = (hf.get('region{0}'.format(id)))
                    value = db[int(regP[0]),int(secP[0]),int(regRS[0]),id_inquery]
                    linksList.append({"source": source, "target":target, "value":value})
                    sourceData = str(source)+"_"+id_PP[1]
                    targetData = str(target)+"_"+toNames
                    valueData = str(value)
                    dataExport1.append(sourceData + "\t"+targetData+"\t"+valueData)
        dataExport = []
        for line in dataExport1:
            dataExport.append(line.split("\t"))

        #regPadjusted = [point[0] for point in pack]
        #plotDatatitles = [point[1] for point in pack]
        return nodesList, linksList, dataExport


def defaultData(request,selectMode):
    #check selectmode and invoke the mySQL database to create the right "default" query to HDF5
    if selectMode == "Country and Sector of emission":
        #call queryHDF5 function with standard input
        id = Country.objects.values_list('id', flat=True)


        lvls = Country.objects.values_list('lvl', flat=True)
        lwst_level = 2
        regPdata = []
        regPdata2 = []
        regPtitlesReady = []
        for x in id:
            lvl = Country.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    regPtitlesReady.append(name[:40])
                else:
                    regPtitlesReady.append(name)

                regPdata2.append(x-1)
        #call queryHDF5 function with standard input
        id = Product.objects.values_list('id', flat=True)


        lvls = Product.objects.values_list('lvl', flat=True)
        lwst_level = 2
        secPdata = []
        secPdata2 = []
        secPtitlesReady = []

        for x in id:
            lvl = Product.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Product.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    secPtitlesReady.append(name[:40])
                else:
                    secPtitlesReady.append(name)

                secPdata2.append(x-1)
        secPForm = list(zip(secPdata2,secPtitlesReady))
        regPForm = list(zip(regPdata2,regPtitlesReady))
        nodesList, linkList, notUsed = queryHDF5(regPForm,secPForm,selectMode,latest_year_int,regPdata2,secPdata2,[0],[1],[0], request)

    if selectMode == "Country of emission and Country of supply":
        #call queryHDF5 function with standard input
        id = Country.objects.values_list('id', flat=True)


        lvls = Country.objects.values_list('lvl', flat=True)
        lwst_level = 2
        regPdata = []
        regPdata2 = []
        regPtitlesReady = []
        for x in id:
            lvl = Country.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    regPtitlesReady.append(name[:40])
                else:
                    regPtitlesReady.append(name)

                regPdata2.append(x-1)
        regPForm = list(zip(regPdata2,regPtitlesReady))
        regRSForm = list(zip(regPdata2,regPtitlesReady))
        #(fromParam, toParam, plotMode, year, regP, secP, regRS, regC,secC,request):
        nodesList, linkList, notUsed = queryHDF5(regPForm,regRSForm,selectMode,latest_year_int,regPdata2,[0],regPdata2,[1],[0], request)

    if selectMode == "Country of emission and Product or service":
        #call queryHDF5 function with standard input
        id = Country.objects.values_list('id', flat=True)


        lvls = Country.objects.values_list('lvl', flat=True)
        lwst_level = 2
        regPdata = []
        regPdata2 = []
        regPtitlesReady = []
        for x in id:
            lvl = Country.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    regPtitlesReady.append(name[:40])
                else:
                    regPtitlesReady.append(name)

                regPdata2.append(x-1)

         #call queryHDF5 function with standard input
        id = Product.objects.values_list('id', flat=True)


        lvls = Product.objects.values_list('lvl', flat=True)
        lwst_level = 2
        secPdata = []
        secPdata2 = []
        secPtitlesReady = []
        for x in id:
            lvl = Product.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Product.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    secPtitlesReady.append(name[:40])
                else:
                    secPtitlesReady.append(name)

                secPdata2.append(x-1)
        regPForm = list(zip(regPdata2,regPtitlesReady))
        secCForm = list(zip(secPdata2,secPtitlesReady))
        #(fromParam, toParam, plotMode, year, regP, secP, regRS, regC,secC,request):
        nodesList, linkList, notUsed = queryHDF5(regPForm,secCForm,selectMode,latest_year_int,regPdata2,[0],[0],[1],secPdata2, request)
    if selectMode == "Country of emission and Country of consumption":

#call queryHDF5 function with standard input
        id = Country.objects.values_list('id', flat=True)


        lvls = Country.objects.values_list('lvl', flat=True)
        lwst_level = 2
        regPdata = []
        regPdata2 = []
        regPtitlesReady = []
        for x in id:
            lvl = Country.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    regPtitlesReady.append(name[:40])
                else:
                    regPtitlesReady.append(name)

                regPdata2.append(x-1)
#call queryHDF5 function with standard input
        id = Country.objects.values_list('id', flat=True)


        lvls = Country.objects.values_list('lvl', flat=True)
        lwst_level = 2

        regCdata2 = []
        regCtitlesReady = []
        for x in id:
            lvl = Country.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    regCtitlesReady.append(name[:40])
                else:
                    regCtitlesReady.append(name)

                regCdata2.append(x)

        regPForm = list(zip(regPdata2,regPtitlesReady))
        regCForm = list(zip(regCdata2,regCtitlesReady))
        #(fromParam, toParam, plotMode, year, regP, secP, regRS, regC,secC,request):
        nodesList, linkList, notUsed = queryHDF5(regPForm,regCForm,selectMode,latest_year_int,regPdata2,[0],[0],regCdata2,[0], request)
 #check selectmode and invoke the mySQL database to create the right "default" query to HDF5
    if selectMode == "Sector of emission and Country of supply":
        #call queryHDF5 function with standard input
        id = Country.objects.values_list('id', flat=True)


        lvls = Country.objects.values_list('lvl', flat=True)
        lwst_level = 2
        regPdata = []
        regRSdata2 = []
        regRStitlesReady = []
        for x in id:
            lvl = Country.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    regRStitlesReady.append(name[:40])
                else:
                    regRStitlesReady.append(name)

                regRSdata2.append(x-1)
        #call queryHDF5 function with standard input
        id = Product.objects.values_list('id', flat=True)


        lvls = Product.objects.values_list('lvl', flat=True)
        lwst_level = 2
        secPdata = []
        secPdata2 = []
        secPtitlesReady = []
        for x in id:
            lvl = Product.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Product.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    secPtitlesReady.append(name[:40])
                else:
                    secPtitlesReady.append(name)

                secPdata2.append(x-1)
        secPForm = list(zip(secPdata2,secPtitlesReady))
        regRSForm = list(zip(regRSdata2,regRStitlesReady))
        nodesList, linkList, notUsed = queryHDF5(secPForm,regRSForm,selectMode,latest_year_int,[0],secPdata2,regRSdata2,[1],[0], request)
#check selectmode and invoke the mySQL database to create the right "default" query to HDF5
    if selectMode == "Sector of emission and Product or service":
        #call queryHDF5 function with standard input





        #call queryHDF5 function with standard input
        id = Product.objects.values_list('id', flat=True)


        lvls = Product.objects.values_list('lvl', flat=True)
        lwst_level = 2
        secPdata = []
        secPdata2 = []
        secPtitlesReady = []
        for x in id:
            lvl = Product.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Product.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    secPtitlesReady.append(name[:40])
                else:
                    secPtitlesReady.append(name)

                secPdata2.append(x-1)
        secPForm = list(zip(secPdata2,secPtitlesReady))
        secCForm = list(zip(secPdata2,secPtitlesReady))
        nodesList, linkList, notUsed = queryHDF5(secPForm,secCForm,selectMode,latest_year_int,[0],secPdata2,[0],[1],secPdata2, request)
    if selectMode == "Sector of emission and Country of consumption":
        #call queryHDF5 function with standard input
        id = Country.objects.values_list('id', flat=True)


        lvls = Country.objects.values_list('lvl', flat=True)
        lwst_level = 2
        regPdata = []
        regRSdata2 = []
        regRStitlesReady = []
        for x in id:
            lvl = Country.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    regRStitlesReady.append(name[:40])
                else:
                    regRStitlesReady.append(name)

                regRSdata2.append(x)
        #call queryHDF5 function with standard input
        id = Product.objects.values_list('id', flat=True)


        lvls = Product.objects.values_list('lvl', flat=True)
        lwst_level = 2
        secPdata = []
        secPdata2 = []
        secPtitlesReady = []
        for x in id:
            lvl = Product.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Product.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    secPtitlesReady.append(name[:40])
                else:
                    secPtitlesReady.append(name)

                secPdata2.append(x-1)
        secPForm = list(zip(secPdata2,secPtitlesReady))
        regCForm = list(zip(regRSdata2,regRStitlesReady))
        nodesList, linkList, notUsed = queryHDF5(secPForm,regCForm,selectMode,latest_year_int,[0],secPdata2,[0],regRSdata2,[0], request)


#check selectmode and invoke the mySQL database to create the right "default" query to HDF5
    if selectMode == "Country of supply and Product or service":
        #call queryHDF5 function with standard input
        id = Country.objects.values_list('id', flat=True)


        lvls = Country.objects.values_list('lvl', flat=True)
        lwst_level = 2
        secPdata = []
        regRSdata2 = []
        regRStitlesReady = []
        for x in id:
            lvl = Country.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    regRStitlesReady.append(name[:40])
                else:
                    regRStitlesReady.append(name)

                regRSdata2.append(x-1)
        #call queryHDF5 function with standard input
        id = Product.objects.values_list('id', flat=True)


        lvls = Product.objects.values_list('lvl', flat=True)
        lwst_level = 2
        secCdata = []
        secCdata2 = []
        secCtitlesReady = []
        for x in id:
            lvl = Product.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Product.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    secCtitlesReady.append(name[:40])
                else:
                    secCtitlesReady.append(name)

                secCdata2.append(x-1)
        secCForm = list(zip(secCdata2,secCtitlesReady))
        regRSForm = list(zip(regRSdata2,regRStitlesReady))
        nodesList, linkList, notUsed = queryHDF5(regRSForm,secCForm,selectMode,latest_year_int,[0],[0],regRSdata2,[1],secCdata2, request)
        #(fromParam, toParam, plotMode, year, regP, secP, regRS, regC,secC,request):

    if selectMode == "Country of supply and Country of consumption":

#call queryHDF5 function with standard input
        id = Country.objects.values_list('id', flat=True)


        lvls = Country.objects.values_list('lvl', flat=True)
        lwst_level = 2
        regPdata = []
        regPdata2 = []
        regPtitlesReady = []
        for x in id:
            lvl = Country.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    regPtitlesReady.append(name[:40])
                else:
                    regPtitlesReady.append(name)

                regPdata2.append(x-1)
#call queryHDF5 function with standard input
        id = Country.objects.values_list('id', flat=True)


        lvls = Country.objects.values_list('lvl', flat=True)
        lwst_level = 2

        regCdata2 = []
        regCtitlesReady = []
        for x in id:
            lvl = Country.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    regCtitlesReady.append(name[:40])
                else:
                    regCtitlesReady.append(name)

                regCdata2.append(x)

        regRSForm = list(zip(regPdata2,regPtitlesReady))
        regCForm = list(zip(regCdata2,regCtitlesReady))
        #(fromParam, toParam, plotMode, year, regP, secP, regRS, regC,secC,request):
        nodesList, linkList, notUsed = queryHDF5(regRSForm,regCForm,selectMode,latest_year_int,[0],[0],regPdata2,regCdata2,[0], request)
 #check selectmode and invoke the mySQL database to create the right "default" query to HDF5
    #check selectmode and invoke the mySQL database to create the right "default" query to HDF5
    if selectMode == "Product or service and Country of consumption":
        #call queryHDF5 function with standard input
        id = Country.objects.values_list('id', flat=True)


        lvls = Country.objects.values_list('lvl', flat=True)
        lwst_level = 2

        regCdata2 = []
        regCtitlesReady = []
        for x in id:
            lvl = Country.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    regCtitlesReady.append(name[:40])
                else:
                    regCtitlesReady.append(name)

                regCdata2.append(x)
        #call queryHDF5 function with standard input
        id = Product.objects.values_list('id', flat=True)


        lvls = Product.objects.values_list('lvl', flat=True)
        lwst_level = 2

        secCdata2 = []
        secCtitlesReady = []
        for x in id:
            lvl = Product.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                name = Product.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    secCtitlesReady.append(name[:40])
                else:
                    secCtitlesReady.append(name)

                secCdata2.append(x-1)
        secCForm = list(zip(secCdata2,secCtitlesReady))
        regCForm = list(zip(regCdata2,regCtitlesReady))
        nodesList, linkList, notUsed = queryHDF5(secCForm,regCForm,selectMode,latest_year_int,[0],[0],[0],secCdata2,secCdata2, request)
        #(fromParam, toParam, plotMode, year, regP, secP, regRS, regC,secC,request):
    return nodesList, linkList, notUsed

#function that generates a description of outputData
def generateDesc(selectMode,envPtitles,year,plotDataTitles, secPtitles, regRStitles, regCtitles, secCtitles, queryData):
    head = '<div class="container" ><table class="table table-hover" ><thead><tr><th class="col-sm-0.5">Type </th><th class="col-sm-0.5">Query</th></tr></thead>'
    body = '<tbody><tr><td>Select mode</td><td>{0}</td></tr><tr hidden><td>Environmental pressure</td><td> {1}</td> </tr><tr><td>Year</td><td>{2} </td> </tr><tr><td>Region of production </td><td>{3} </td> </tr><tr><td> Sector of production</td><td>{4} </td> </tr><tr><td>country selling</td><td>{5} </td> </tr><tr><td>Region of consumption </td><td>{6} </td> </tr><tr><td>Sector of consumption </td><td>{7} </td> </tr></tbody></table></div>'.format(selectMode,envPtitles,year,plotDataTitles, secPtitles, regRStitles, regCtitles, secCtitles)
    table = head + body
    return table