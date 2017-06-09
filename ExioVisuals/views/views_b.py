
#****TREEMAP CODE
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect, render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import JsonResponse

from ExioVisuals.models import GhgEmissions, Product, Country, Substance, YearF

import random, re
import datetime,time


from django.forms.formsets import formset_factory
from ExioVisuals.forms import PostFormEFactor, reloadForm, modes, yearsSingleSelect, yearsMultipleSelect, modesTimeSeries
from functools import partial, wraps
import json
from django.shortcuts import render, get_object_or_404, redirect
from ExioVisuals.forms import ProductSelectionForm, CountrySelectionForm, SubstanceSelectionForm, YearFSelectionForm

import numpy as np
import h5py
from CMLMasterProject.settings import PATH_HDF5

 #retrieve mandatory context
def treemap(request):
    #by default mode is :
    mode = 0
    #intialize mode
    modeFormSet = modes()
    treemapData = ({'modeForm':modeFormSet})
    #Retrieve skeleton of forms-------------------------------------------------------------
    formTree = ProductSelectionForm(request.POST or None)
    formTreeCountry = CountrySelectionForm(request.POST or None)
    formTreeSubstance = SubstanceSelectionForm(request.POST or None)
    formTreeYear = YearFSelectionForm(request.POST or None)

    MemberFormSet = formset_factory(wraps(PostFormEFactor)(partial(PostFormEFactor)))

 #retrieve filter data!
    if request.method == 'POST':

        #First and foremost try to retrieve any mode (decomposition data)
        mode = (request.POST.get('y'))
        exportRaw = request.POST.get('raw')
        exportRaw2 = request.POST.get('raw2')
        previousMode = request.POST.get('previousMode')
        defaultMode = request.POST.get('previousType')
        session = request.POST.get('session')


        if exportRaw != None and len(exportRaw) != 0 and exportRaw2 != None and len(exportRaw2) != 0:

                import csv
                from django.utils.encoding import smart_str

                #exportRaw2 = exportRaw2.split(",")

                bt = (exportRaw)


                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename=output.csv'
                writer = csv.writer(response, csv.excel)
                response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
                writer.writerow([
                    smart_str(u"Name"),
                    smart_str(u"Data"),

                ])
                print("****")

                #convert to actual list
                import ast
                titles = ast.literal_eval(exportRaw)
                data = ast.literal_eval(exportRaw2)
                #merge the two sorted lists
                points = zip(titles,data)
                #print(list(exportRaw))
                #rint(list(exportRaw))
                for obj in points:
                        cleanedObj = obj[0].replace(",", " ")
                    #print(obj)
                        writer.writerow([
                            smart_str((cleanedObj)),
                            smart_str((obj[1])),

                        ])



                return response


        if mode != None:
            print("Entering mode:" +mode)
            if mode=="selectA":
                #call all the necessary forms
                modeFormSet = modes(initial={'selection': 'selectA'})


                #set title,description, size
                title = "Contribution footprint of consumption split by consumed product category"
                #xdata, ydata = defaultData("PieChart", title, request)
                description = ""
                xdata, ydata = defaultData("TreeMap", title, request)
                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                productP = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)

                 #make year total unselectable in this case
             #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == "2011":
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
                        x['selected'] = False
                        for y in x['children']:
                            y['selected'] = False
                            for k in y['children']:
                                k['selected'] = True


                #print(countryDataReady)

                #parsed_json[0]['selected'] = True
                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                productP = json.dumps(productP)
                yearData = json.dumps(yearData)


                #countryDataReady = (countryDataReady.replace("'", '"'))
                treemapData = treeMp(xdata,ydata,title, "")
             #updata dictionary for filter options: form skeletons
                treemapData.update({'modeForm':modeFormSet})

                treemapData.update({'sourceData': sourceData})
                treemapData.update({'countryDataReady': countryDataReady})
                treemapData.update({'substanceDataReady': generateTrees(formTreeSubstance)})

                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #create select modes for fancyTree : so single select or multiple
                #we need to check the previous mode and update accordingly or set a default mode
#
                treemapData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                treemapData.update({'mode_tree': 2, 'warning_6':"","productPurchased":productP})
                treemapData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
                treemapData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                treemapData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
                treemapData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})
                #treemapData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})

                #send signal for popup and default data
                popup = 1
                default =1
                treemapData.update({'popup': popup})
                treemapData.update({'default': default})
                treemapData.update({'title':"Contribution footprint of consumption split by consumed product category"})

                treemapData.update({'userSelectMode': "Contribution footprint of consumption split by consumed product category"})
                return render(request,"ExioVisuals/treemap.html", treemapData)
            if mode=="selectB":
                #call all the necessary forms
                modeFormSet = modes(initial={'selection': 'selectB'})
                #normally we want to load data here that makes sense of the selected mode

                #set title,description, size
                title = "Contribution footprint of consumption split by consuming region"
                description = ""
                xdata, ydata = defaultData("TreeMap", title, request)


                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                regConsuming = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)

                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == "2011":
                            x['selected'] = True

                #DEFAULT SELECTION, MAY FAIL IF LEVELS OF DATA are changed (in that case remove these lines)

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
                for i in regConsuming:
                    if i['title'] == "Total":
                        i['selected'] = False
                    for x in i['children']:
                        x['selected'] = False
                        for y in x['children']:
                                    y['selected'] = True

                print(parsed_json)
                #print(countryDataReady)

                #parsed_json[0]['selected'] = True
                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                regConsuming = json.dumps(regConsuming)
                yearData = json.dumps(yearData)

                treemapData = treeMp(xdata,ydata,title, "")

             #updata dictionary for filter options: form skeletons
                treemapData.update({'modeForm':modeFormSet})

                treemapData.update({'sourceData': sourceData})
                treemapData.update({'countryDataReady': countryDataReady})
                treemapData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #create select modes for fancyTree : so single select or multiple
                treemapData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                treemapData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction": sourceData})
                treemapData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                treemapData.update({'mode_tree2': 2, 'warning_5':"","regionConsumng":regConsuming})
                treemapData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                treemapData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
                #treemapData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})
                #send signal for popup and default data
                popup = 1
                default =1
                treemapData.update({'popup': popup})
                treemapData.update({'default': default})
                treemapData.update({'title':"Contribution footprint of consumption split by consuming region"})
                treemapData.update({'userSelectMode': "Contribution footprint of consumption split by consuming region"})
                return render(request,"ExioVisuals/treemap.html", treemapData)
            if mode=="selectD":
                #call all the necessary forms
                modeFormSet = modes(initial={'selection': 'selectD'})


                #set title,description, size
                title = "Contribution footprint of consumption split by country where impact occurs"
                description = ""
                xdata, ydata = defaultData("TreeMap", title, request)
                sourceData = generateTrees(formTree)
                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                parsed_json2 = json.loads(sourceData)
                #start selecting some nodes of the tree (some countries)
                parsed_json = json.loads(countryDataReady)
                regProducing = json.loads(countryDataReady)
                parsed_json2 = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)

                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == "2011":
                            x['selected'] = True
                #start selecting some nodes of the tree (some countries)

                #DEFAULT SELECTION, MAY FAIL IF LEVELS OF DATA are changed (in that case remove these lines)
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
                for i in regProducing:
                    if i['title'] == "Total":
                        i['selected'] = False
                    for x in i['children']:
                        x['selected'] = False
                        for y in x['children']:
                                    y['selected'] = True

                print(parsed_json)
                #print(countryDataReady)

                #parsed_json[0]['selected'] = True
                countryDataReady2 = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                regProducing = json.dumps(regProducing)
                yearData = json.dumps(yearData)
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                treemapData = treeMp(xdata,ydata,title, "")
                #do check on previousModes




             #updata dictionary for filter options: form skeletons
                treemapData.update({'modeForm':modeFormSet})

                treemapData.update({'sourceData': sourceData })
                treemapData.update({'countryDataReady': countryDataReady})
                treemapData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                #create select modes for fancyTree : so single select or multiple
                treemapData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})
                treemapData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})

                treemapData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData, })
                treemapData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady2})
                treemapData.update({'mode_tree3': 2, 'warning_7':"","regionProducing":regProducing})
                treemapData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady2})
                #send signal for popup and default data
                popup = 1
                default =1
                treemapData.update({'popup': popup})
                treemapData.update({'default': default})
                treemapData.update({'title':"Contribution footprint of consumption split by country where impact occurs"})
                treemapData.update({'userSelectMode': "Contribution footprint of consumption split by country where impact occurs"})
                return render(request,"ExioVisuals/treemap.html", treemapData)
            if mode=="selectC":
                #call all the necessary forms
                modeFormSet = modes(initial={'selection': 'selectC'})
                #normally we want to load data here that makes sense of the selected mode


                #set title,description, size
                title = "Contribution footprint of consumption split by sector where impact occurs"
                description = ""
                xdata, ydata = defaultData("TreeMap", title, request)

                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                sourceData = generateTrees(formTree)
                parsed_json2 = json.loads(sourceData)
                secOfProduction = json.loads(sourceData)
                regOfProduction = json.loads(countryDataReady)
                productPurchased = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)

                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == "2011":
                            x['selected'] = True

                 #DEFAULT SELECTION, MAY FAIL IF LEVELS OF DATA are changed (in that case remove these lines)
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
                for i in secOfProduction:
                    i['selected'] = False
                    for x in i['children']:
                        x['selected'] = False
                        for y in x['children']:
                            y['selected'] = False
                            for k in y['children']:
                                k['selected'] = True
                #print(countryDataReady)

                #parsed_json[0]['selected'] = True
                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                secOfProduction = json.dumps(secOfProduction)
                regOfProduction = json.dumps(parsed_json)
                productPurchased = json.dumps(parsed_json2)
                yearData = json.dumps(yearData)

                treemapData = treeMp(xdata,ydata,title, "")

             #updata dictionary for filter options: form skeletons
                treemapData.update({'modeForm':modeFormSet})

                treemapData.update({'sourceData': sourceData})
                treemapData.update({'countryDataReady': countryDataReady})
                treemapData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #create select modes for fancyTree : so single select or multiple
                treemapData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                treemapData.update({'mode_tree4': 2, 'warning_8':"", "sectorOfProduction": secOfProduction})
                treemapData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":productPurchased})
                treemapData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":regOfProduction})
                treemapData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":regOfProduction})
                treemapData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":regOfProduction})
                #treemapData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})

                #send signal for popup
                #send signal for popup and default data
                popup = 1
                default =1
                treemapData.update({'popup': popup})
                treemapData.update({'default': default})
                treemapData.update({'title':"Contribution footprint of consumption split by sector where impact occurs"})
                treemapData.update({'userSelectMode': "Contribution footprint of consumption split by sector where impact occurs"})
                return render(request,"ExioVisuals/treemap.html", treemapData)
            if mode=="selectF":

                #call all the necessary forms
                modeFormSet = modes(initial={'selection': 'selectF'})



                #set title,description, size
                title = "Contribution footprint of consumption split by region selling"
                description = ""
                xdata, ydata = defaultData("TreeMap", title, request)

                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)

                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        if x['title'] == "2011":
                            x['selected'] = True
                #start selecting some nodes of the tree (some countries)






                treemapData = treeMp(xdata,ydata,title, "")

             #updata dictionary for filter options: form skeletons
                treemapData.update({'modeForm':modeFormSet})
                sourceData = generateTrees(formTree)
                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
                regRS = json.loads(countryDataReady)
                parsed_json2 = json.loads(sourceData)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
    
                    for x in i['children']:
                        if x['title'] == "2011":
                            x['selected'] = True
                        else:
                            x['selected'] = False
    
     #DEFAULT SELECTION, MAY FAIL IF LEVELS OF DATA are changed (in that case remove these lines)
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
                for i in regRS:
                    if i['title'] == "Total":
                        i['selected'] = False
                    for x in i['children']:
                        x['selected'] = False
                        for y in x['children']:
                                    y['selected'] = True
                #print(countryDataReady)
    
                #parsed_json[0]['selected'] = True
                countryDataReady2 = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                regProducing = json.dumps(regRS)
                yearData = json.dumps(yearData)
    
    
                #countryDataReady = (countryDataReady.replace("'", '"'))
                #call pieChart function
             #updata dictionary for filter options: form skeletons
                treemapData.update({'modeForm':modeFormSet})
    
                treemapData.update({'sourceData': sourceData })
                treemapData.update({'countryDataReady': countryDataReady})
                treemapData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #create select modes for fancyTree : so single select or multiple
                treemapData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})
    
                treemapData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                treemapData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                treemapData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady2})
                treemapData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady2})
                treemapData.update({'mode_tree6': 2, 'warning_10':"","regionSelling":regProducing})
                #send signal for popup and default data
                popup = 1
                default =1
                treemapData.update({'popup': popup})
                treemapData.update({'default': default})
                treemapData.update({'userSelectMode': "Contribution footprint of consumption split by region selling"})

                return render(request,"ExioVisuals/treemap.html", treemapData)

        #************START RETRIEVING USER SELECTIONS*******************

        envP = (request.POST.getlist('ft_4[]'))
        envPtitles = []
        for x in envP:
            print("Environmental Pressure:")
            print(Substance.objects.get(pk=x))
            print(Substance.objects.values_list('name', flat=True).get(pk=x))
            name = (Substance.objects.values_list('name', flat=True).get(pk=x))
            envPtitles.append(name)


        print(request.POST)
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


        print("Year selected:")
        print(year)


        regP = (request.POST.getlist('ft_2[]'))
        regPdata = []
        regPtitles = []
        regPquery =[]
        regPparents = []
        for x in regP:
            print("Region of production:")
            print(Country.objects.get(pk=x))
            print(Country.objects.values_list('name', flat=True).get(pk=x))
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
            regPquery.append(name+"("+str(id)+")")
            regPdata.append(id)


    
 
        secP = (request.POST.getlist('ft_5[]'))
        secPdata = []
        secPtitles = []
        secPquery = []
        secPparents = []
        da = 0
        for x in secP:
            print("Sector of production:")
            print(Product.objects.get(pk=x))
            print(Product.objects.values_list('name', flat=True).get(pk=x))
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
            secPquery.append(name+"("+str(id)+")")
            secPdata.append(id)

        regRS = (request.POST.getlist('ft_7[]'))
        regRSdata = []
        regRStitles = []
        regRSquery = []
        regRSparents = []
        for x in regRS:
            print("Region selling:")
            print(Country.objects.get(pk=x))
            print(Country.objects.values_list('name', flat=True).get(pk=x))
            #local = Product.objects.values_list('local', flat=True).get(pk=x)
            name = Country.objects.values_list('name', flat=True).get(pk=x)
            #lwst_level = Product.objects.values_list('lwst_level', flat=True).get(pk=x)
            # retrieve the indices for HDf5 query
            id = Country.objects.values_list('id', flat=True).get(pk=x)
            #mitigate the offset
            id = id - 1
            regPparents.append(Country.objects.values_list('name', flat=True).get(pk=x))
            if len(name) > 25:
                regRStitles.append(name[:40])
            else:
                regRStitles.append(name)
            regRSquery.append(name+"("+str(id)+")")
            regRSdata.append(id)
        print(regRSquery)
        secC = (request.POST.getlist('ft_3[]'))
        secCdata = []
        secCtitles = []
        secCquery = []
        secCparents = []
        for x in  secC:
            print("Sector of consumption:")
            print(Product.objects.get(pk=x))
            print(Product.objects.values_list('name', flat=True).get(pk=x))
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
            secCquery.append(name+"("+str(id)+")")
            secCdata.append(id)


        regC = (request.POST.getlist('ft_1[]'))
        regCdata = []
        regCtitles = []
        regCquery = []
        regCparents = []
        for x in regC:
            print("Region selling:")
            print(Country.objects.get(pk=x))
            print(Country.objects.values_list('name', flat=True).get(pk=x))
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
            regCquery.append(name+"("+str(id)+")")
            regCdata.append(id)
        print(regCquery)

        #remove duplicate selections and preserve order
        def f7(seq):
            seen = set()
            seen_add = seen.add
            return [x for x in seq if not (x in seen or seen_add(x))]
        regCdata = f7(regCdata)

        selectMode = (request.POST.get('selectMode'))


        print("Select mode is: ")
        print(selectMode)
        print(secPdata)
        print(")*(^%%%%%%%%")

        #validate input

        if not regPdata:
            error_status = {"error":"<Region of Production> data has not been filled in properly."}
            return render(request, "ExioVisuals/error_page.html", error_status)
        if not secPdata:
            error_status = {"error":"<Sector of Production> data has not been filled in properly."}
            return render(request, "ExioVisuals/error_page.html", error_status)
        if not regRSdata:
            error_status = {"error":"<Region Selling> has not been filled in properly."}
            return render(request, "ExioVisuals/error_page.html", error_status)
        if not regCdata:
            error_status = {"error":"<Region of Consumption> data has not been filled in properly."}
            return render(request, "ExioVisuals/error_page.html", error_status)
        if not secCdata:
            error_status = {"error":"<Sector of consumption> data has not been filled in properly."}
            return render(request, "ExioVisuals/error_page.html", error_status)


        #START MAKING PLOT DATA
        if selectMode == "Contribution footprint of consumption split by country where impact occurs":
            plotType = "TreeMap"

            if session == None:
                print("No session")
                session = None
            else:
                #there is a session so we want to do something dynamic with the data send to user
                print("we are in a session")
                session = "session"
            #QUERY THE DATABASE
            plotData,regPtitles, queryData = queryhdf5(plotType,selectMode, envP, year, regPdata, secPdata,regRSdata, regCdata,secCdata, regPtitles,request)

            table = generateDesc(selectMode,envPtitles,year,regPquery, secPparents, regRSquery, regCparents, secCparents, queryData)

            treemapData = treeMp(regPtitles,plotData,selectMode, table)
            modeFormSet = modes(initial={'selection': 'selectA'})
            treemapData.update({'modeForm':modeFormSet})
            sourceData = generateTrees(formTree)
            countryDataReady = generateTrees(formTreeCountry)
            treemapData.update({'titles': regPtitles})
            treemapData.update({'plot': plotData})
            parsed_json = json.loads(countryDataReady)
            regProducing = json.loads(countryDataReady)
            parsed_json2 = json.loads(sourceData)
            yearData = generateTrees(formTreeYear)
            yearData = json.loads(yearData)

             #make year total unselectable in this case
            for i in yearData:
                if i['title'] == "Total":
                    i['unselectable'] = True
                for x in i['children']:
                    if x['title'] == "2011":
                        x['selected'] = False
            #start selecting some nodes of the tree (some countries)

            #DEFAULT SELECTION, MAY FAIL IF LEVELS OF DATA are changed (in that case remove these lines)
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
            for i in regProducing:
                if i['title'] == "Total":
                    i['selected'] = False
                for x in i['children']:
                    x['selected'] = False
                    for y in x['children']:
                                y['selected'] = False

            print(parsed_json)
            #print(countryDataReady)

            #parsed_json[0]['selected'] = True
            countryDataReady2 = json.dumps(parsed_json)
            sourceData = json.dumps(parsed_json2)
            regProducing = json.dumps(regProducing)
            yearData = json.dumps(yearData)
            notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'



         #updata dictionary for filter options: form skeletons
            treemapData.update({'modeForm':modeFormSet, 'session': session})
            treemapData.update({'session': "session"})
            treemapData.update({'sourceData': sourceData })
            treemapData.update({'countryDataReady': countryDataReady})
            treemapData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
            #create select modes for fancyTree : so single select or multiple
            treemapData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})
            treemapData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})

            treemapData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData, })
            treemapData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady2})
            treemapData.update({'mode_tree3': 2, 'warning_7':"","regionProducing":regProducing})
            treemapData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady2})
            treemapData.update({'userSelectMode': "Contribution footprint of consumption split by country where impact occurs"})

        if selectMode == "Contribution footprint of consumption split by sector where impact occurs":
            plotType = "TreeMap"
            #QUERY THE DATABASE
            plotData,secPtitles, queryData = queryhdf5(plotType,selectMode, envP, year, regPdata, secPdata,regRSdata, regCdata,secCdata, secPtitles, request)
            if session == None:
                print("No session")
                session = None
            else:
                #there is a session so we want to do something dynamic with the data send to user
                print("we are in a session")
                session = "session"
            table = generateDesc(selectMode,envPtitles,year,regPparents, secPquery, regRSquery, regCparents, secCparents,queryData)

            treemapData = treeMp(secPtitles,plotData,selectMode, table)
            modeFormSet = modes(initial={'selection': 'selectA'})
            treemapData.update({'modeForm':modeFormSet})
            treemapData.update({'titles': secPtitles})
            treemapData.update({'plot': plotData})
            countryDataReady = generateTrees(formTreeCountry)
            parsed_json = json.loads(countryDataReady)
            sourceData = generateTrees(formTree)
            parsed_json2 = json.loads(sourceData)
            secOfProduction = json.loads(sourceData)
            regOfProduction = json.loads(countryDataReady)
            productPurchased = json.loads(sourceData)
            yearData = generateTrees(formTreeYear)
            yearData = json.loads(yearData)

             #make year total unselectable in this case
            for i in yearData:
                if i['title'] == "Total":
                    i['unselectable'] = True
                for x in i['children']:
                    if x['title'] == "2011":
                        x['selected'] = False

             #DEFAULT SELECTION, MAY FAIL IF LEVELS OF DATA are changed (in that case remove these lines)
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
            for i in secOfProduction:
                i['selected'] = False
                for x in i['children']:
                    x['selected'] = False
                    for y in x['children']:
                        y['selected'] = False
                        for k in y['children']:
                            k['selected'] = False
            #print(countryDataReady)

            #parsed_json[0]['selected'] = True
            countryDataReady = json.dumps(parsed_json)
            sourceData = json.dumps(parsed_json2)
            secOfProduction = json.dumps(secOfProduction)
            regOfProduction = json.dumps(parsed_json)
            productPurchased = json.dumps(parsed_json2)
            yearData = json.dumps(yearData)


         #updata dictionary for filter options: form skeletons
            treemapData.update({'modeForm':modeFormSet})
            treemapData.update({'session': "session"})

            treemapData.update({'sourceData': sourceData})
            treemapData.update({'countryDataReady': countryDataReady})
            treemapData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
            notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
            #create select modes for fancyTree : so single select or multiple
            treemapData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

            treemapData.update({'mode_tree4': 2, 'warning_8':"", "sectorOfProduction": secOfProduction})
            treemapData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":productPurchased})
            treemapData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":regOfProduction})
            treemapData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":regOfProduction})
            treemapData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":regOfProduction})
            #treemapData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})

            #send signal for popup
            #send signal for popup and default data
            popup = 1
            treemapData.update({'popup': popup})
            treemapData.update({'title':"Contribution footprint of consumption split by sector where impact occurs"})
            treemapData.update({'userSelectMode': "Contribution footprint of consumption split by sector where impact occurs"})
        if selectMode == "Contribution footprint of consumption split by consumed product category":
            plotType = "TreeMap"
            #QUERY THE DATABASE
            plotData,secCtitles, queryData = queryhdf5(plotType,selectMode, envP, year, regPdata, secPdata,regRSdata, regCdata,secCdata, secCtitles, request)

            table = generateDesc(selectMode,envPtitles,year,regPquery, secPquery, regRSquery, regCquery, secCquery, queryData)
            if session == None:
                print("No session")
                session = None
            else:
                #there is a session so we want to do something dynamic with the data send to user
                print("we are in a session")
                session = "session"
            treemapData = treeMp(secCtitles,plotData,selectMode, table)
            modeFormSet = modes(initial={'selection': 'selectA'})
            treemapData.update({'modeForm':modeFormSet})
            treemapData.update({'titles': secCtitles})
            treemapData.update({'plot': plotData})
            notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
            #create select modes for fancyTree : so single select or multiple
            countryDataReady = generateTrees(formTreeCountry)
            parsed_json = json.loads(countryDataReady)
            sourceData = generateTrees(formTree)
            parsed_json2 = json.loads(sourceData)
            productP = json.loads(sourceData)
            yearData = generateTrees(formTreeYear)
            yearData = json.loads(yearData)

             #make year total unselectable in this case
         #make year total unselectable in this case
            for i in yearData:
                if i['title'] == "Total":
                    i['unselectable'] = True
                for x in i['children']:
                    if x['title'] == "2011":
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


            #print(countryDataReady)

            #parsed_json[0]['selected'] = True
            countryDataReady = json.dumps(parsed_json)
            sourceData = json.dumps(parsed_json2)
            productP = json.dumps(productP)
            yearData = json.dumps(yearData)


            #countryDataReady = (countryDataReady.replace("'", '"'))
         #updata dictionary for filter options: form skeletons
            treemapData.update({'modeForm':modeFormSet})

            treemapData.update({'sourceData': sourceData})
            treemapData.update({'countryDataReady': countryDataReady})
            treemapData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
            treemapData.update({'session': "session"})

            notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
            #create select modes for fancyTree : so single select or multiple
            #we need to check the previous mode and update accordingly or set a default mode
#
            treemapData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
            treemapData.update({'mode_tree': 2, 'warning_6':"","productPurchased":productP})
            treemapData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
            treemapData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
            treemapData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
            treemapData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})
            #treemapData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})
            treemapData.update({'userSelectMode': "Contribution footprint of consumption split by consumed product category"})

        if selectMode == "Contribution footprint of consumption split by consuming region":
            plotType = "TreeMap"

            print(regCdata)
            print(regCtitles)
            #QUERY THE DATABASE
            plotData,regCtitles, queryData = queryhdf5(plotType,selectMode, envP, year, regPdata, secPdata,regRSdata, regCdata,secCdata, regCtitles, request)

            table = generateDesc(selectMode,envPtitles,year,regPquery, secPquery, regRSquery, regCquery, secCquery, queryData)
            if session == None:
                print("No session")
                session = None
            else:
                #there is a session so we want to do something dynamic with the data send to user
                print("we are in a session")
                session = "session"
            treemapData = treeMp(regCtitles,plotData,selectMode, table)
            modeFormSet = modes(initial={'selection': 'selectA'})
            treemapData.update({'modeForm':modeFormSet})
            treemapData.update({'titles': regCtitles})
            treemapData.update({'plot': plotData})
            countryDataReady = generateTrees(formTreeCountry)
            parsed_json = json.loads(countryDataReady)
            regConsuming = json.loads(countryDataReady)
            sourceData = generateTrees(formTree)
            parsed_json2 = json.loads(sourceData)
            yearData = generateTrees(formTreeYear)
            yearData = json.loads(yearData)

             #make year total unselectable in this case
            for i in yearData:
                if i['title'] == "Total":
                    i['unselectable'] = True
                for x in i['children']:
                    if x['title'] == "2011":
                        x['selected'] = False

            #DEFAULT SELECTION, MAY FAIL IF LEVELS OF DATA are changed (in that case remove these lines)

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
            for i in regConsuming:
                if i['title'] == "Total":
                    i['selected'] = False
                for x in i['children']:
                    x['selected'] = False
                    for y in x['children']:
                                y['selected'] = False

            print(parsed_json)
            #print(countryDataReady)

            #parsed_json[0]['selected'] = True
            countryDataReady = json.dumps(parsed_json)
            sourceData = json.dumps(parsed_json2)
            regConsuming = json.dumps(regConsuming)
            yearData = json.dumps(yearData)


         #updata dictionary for filter options: form skeletons
            treemapData.update({'modeForm':modeFormSet})
            treemapData.update({'session': "session"})

            treemapData.update({'sourceData': sourceData})
            treemapData.update({'countryDataReady': countryDataReady})
            treemapData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
            notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
            #create select modes for fancyTree : so single select or multiple
            treemapData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

            treemapData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction": sourceData})
            treemapData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
            treemapData.update({'mode_tree2': 2, 'warning_5':"","regionConsumng":regConsuming})
            treemapData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
            treemapData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
            #treemapData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})
            #send signal for popup and default data
            popup = 1
            treemapData.update({'popup': popup})
            treemapData.update({'title':"Contribution footprint of consumption split by consuming region"})
            treemapData.update({'userSelectMode': "Contribution footprint of consumption split by consuming region"})
        if selectMode == "Contribution footprint of consumption split by region selling":
            plotType = "TreeMap"
            #QUERY THE DATABASE
            plotData,regRStitles, queryData = queryhdf5(plotType,selectMode, envP, year, regPdata, secPdata,regRSdata, regCdata,secCdata, regRStitles,request)

            table = generateDesc(selectMode,envPtitles,year,regPquery, secPparents, regRSquery, regCparents, secCparents, queryData)
            if session == None:
                print("No session")
                session = None
            else:
                #there is a session so we want to do something dynamic with the data send to user
                print("we are in a session")
                session = "session"
            treemapData = treeMp(regRStitles,plotData,selectMode, table)
            modeFormSet = modes(initial={'selection': 'selectF'})
            treemapData.update({'modeForm':modeFormSet})
            treemapData.update({'titles': regRStitles})
            treemapData.update({'plot': plotData})
            #updata dictionary for filter options: form skeletons
            treemapData.update({'modeForm':modeFormSet})
            sourceData = generateTrees(formTree)
            countryDataReady = generateTrees(formTreeCountry)
            parsed_json = json.loads(countryDataReady)
            regRS = json.loads(countryDataReady)
            parsed_json2 = json.loads(sourceData)
            yearData = generateTrees(formTreeYear)
            yearData = json.loads(yearData)
             #make year total unselectable in this case
            for i in yearData:
                if i['title'] == "Total":
                    i['unselectable'] = True

                for x in i['children']:
                    if x['title'] == "2011":
                        x['selected'] = False
                    else:
                        x['selected'] = False

 #DEFAULT SELECTION, MAY FAIL IF LEVELS OF DATA are changed (in that case remove these lines)
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
            for i in regRS:
                if i['title'] == "Total":
                    i['selected'] = False
                for x in i['children']:
                    x['selected'] = False
                    for y in x['children']:
                                y['selected'] = False
            #print(countryDataReady)

            #parsed_json[0]['selected'] = True
            countryDataReady2 = json.dumps(parsed_json)
            sourceData = json.dumps(parsed_json2)
            regProducing = json.dumps(regRS)
            yearData = json.dumps(yearData)


            #countryDataReady = (countryDataReady.replace("'", '"'))
            #call pieChart function
         #updata dictionary for filter options: form skeletons
            treemapData.update({'modeForm':modeFormSet})
            treemapData.update({'session': "session"})

            treemapData.update({'sourceData': sourceData })
            treemapData.update({'countryDataReady': countryDataReady})
            treemapData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
            notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
            #create select modes for fancyTree : so single select or multiple
            treemapData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

            treemapData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
            treemapData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
            treemapData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady2})
            treemapData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady2})
            treemapData.update({'mode_tree6': 2, 'warning_10':"","regionSelling":regProducing})
            #send signal for popup and default data
            popup = 1

            treemapData.update({'popup': popup})

            treemapData.update({'userSelectMode': "Contribution footprint of consumption split by region selling"})





    #****DEFAULT LOADING PAGE
        #set title,description, size
    title = "TreeMap"
    description = ""

   





    #treemapData.update(bla)
     #updata dictionary for filter options : FancyTree
    treemapData.update({'formTree2': formTree})
    treemapData.update({'desc': '<div class="alert alert-info"><h2><span class="glyphicon glyphicon-arrow-up" aria-hidden="true"></span></H2><strong><span class="glyphicon glyphicon-info-sign" aria-hidden="true"></span>  Select your mode in the navigation bar.</strong></div>' })


    #start getting some form skeletons now!
    ArticleFormSet = formset_factory(PostFormEFactor)
    formset = ArticleFormSet()
    formset = formset_factory(wraps(PostFormEFactor)(partial(PostFormEFactor)), extra=1)
     #updata dictionary for filter options: form skeletons
    treemapData.update({'formset2':formset})
    selectionForm = formset_factory(wraps(reloadForm)(partial(reloadForm)), extra=1)
    treemapData.update({'selectionForm': selectionForm})



    treemapData.update({'sourceData': generateTrees(formTree)})
    treemapData.update({'countryDataReady': generateTrees(formTreeCountry)})
    treemapData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
    modeFormSet = modes(initial={'selection': 'selectA'})
    treemapData.update({'modeForm':modeFormSet})


    return render(request,"ExioVisuals/treemap.html",  treemapData)


#function that trims the old tree data from mySQL to only get the source data which is what is used for rendering
def generateTrees(treeData):
    tree = str(treeData)
    trimTree = (tree.partition('[{')[-1].rpartition('}]')[0])
    rebuildTree = "[{"+trimTree+"}]"

    return rebuildTree
#function that generates a description of outputData
def generateDesc(selectMode,envPtitles,year,plotDataTitles, secPtitles, regRStitles, regCtitles, secCtitles, queryData):
    head = '<div class="container" ><table class="table table-hover" ><thead><tr><th class="col-sm-0.5">Type </th><th class="col-sm-0.5">Query</th></tr></thead>'
    body = '<tbody><tr><td>Select mode</td><td>{0}</td></tr><tr><td>Environmental pressure</td><td> {1}</td> </tr><tr><td>Year</td><td>{2} </td> </tr><tr><td>Region of production </td><td>{3} </td> </tr><tr><td> Sector of production</td><td>{4} </td> </tr><tr><td>Region selling</td><td>{5} </td> </tr><tr><td>Region of consumption </td><td>{6} </td> </tr><tr><td>Sector of consumption </td><td>{7} </td> </tr><tr><td>Result data </td><td>{8} </td> </tr></tbody></table></div>'.format(selectMode,envPtitles,year,plotDataTitles, secPtitles, regRStitles, regCtitles, secCtitles, list(queryData))
    table = head + body
    return table


def queryhdf5(plotType,selectMode, envP, year, regP, secP,regRS, regC,secC, plotDatatitles, request):
    print("query function reached")
    #determine plottype as it affects the query and determine the mode that we are in
    if plotType == "TreeMap" and selectMode == "Contribution footprint of consumption split by country where impact occurs":
        #as it is piechart we only select one year
        print("Query is: ")
        #print("regP"+str(regP[0])+"secP"+str(secP[0])+"regRS"+str(regRS[0])+"regC"+str(regC[0])+"secC"+str(secC[0]))
        #we have the title list and the actual data points , both needs to be sorted for the query to hdf5 according to the data points
        regPadjusted = [ int(x) for x in regP ]
        points = zip(regPadjusted,plotDatatitles)
        pack = (sorted(points))
        regPadjusted = [point[0] for point in pack]
        plotDatatitles = [point[1] for point in pack]
        print(year)
        outputData = []
        with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(year) ,'r') as hf:
            for x in regC:
                db = (hf.get('region{0}'.format(x)))
                tmp = db[regPadjusted,int(secP[0]),int(regRS[0]),int(secC[0])]
                outputData.append(tmp.tolist())

        test = np.asarray(outputData)


        outputData = (test.sum(axis=0).tolist())

#sort from high to low
        points = zip(outputData,plotDatatitles)
        package = (sorted(points, reverse=True))
        outputData = [point[0] for point in package]
        plotDatatitles = [point[1] for point in package]




        t = (zip(package,outputData))

        return outputData, plotDatatitles, t
    #determine plottype as it affects the query and determine the mode that we are in
    if plotType == "TreeMap" and selectMode == "Contribution footprint of consumption split by sector where impact occurs":
        #as it is piechart we only select one year
        print("Query is: ")
        #print("regP"+str(regP[0])+"secP"+str(secP[0])+"regRS"+str(regRS[0])+"regC"+str(regC[0])+"secC"+str(secC[0]))
        #we have the title list and the actual data points , both needs to be sorted for the query to hdf5 according to the data points
        secPadjusted = [ int(x) for x in secP ]
        points = zip(secPadjusted,plotDatatitles)
        pack = (sorted(points))
        secPadjusted = [point[0] for point in pack]
        plotDatatitles = [point[1] for point in pack]

        #regPadjusted = sorted(regPadjusted, key=int)
        regC = [int(x) for x in regC]
        regP = [int(x) for x in regP]
        regRS = [int(x) for x in regRS]
        secC = [int(x) for x in secC]
        outputData = []
        with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(year) ,'r')as hf:

            for x in regC:
                db = (hf.get('region{0}'.format(x)))
                tmp = db[int(regP[0]),secPadjusted,int(regRS[0]),int(secC[0])]
            #tmp = np.around(tmp, decimals=0)
            #tmp = test[0:49,43,44,2]
                outputData.append(tmp.tolist())

        test = np.asarray(outputData)


        outputData = (test.sum(axis=0).tolist())
        #sort from high to low
        points = zip(outputData,plotDatatitles)
        package = (sorted(points, reverse=True))
        outputData = [point[0] for point in package]
        plotDatatitles = [point[1] for point in package]




        t = (zip(package,outputData))


        return outputData, plotDatatitles, t

    #determine plottype as it affects the query and determine the mode that we are in
    if plotType == "TreeMap" and selectMode == "Contribution footprint of consumption split by consumed product category":
        #as it is piechart we only select one year
        print("Query is: ")
        #print("regP"+str(regP[0])+"secP"+str(secP[0])+"regRS"+str(regRS[0])+"regC"+str(regC[0])+"secC"+str(secC[0]))
        #we have the title list and the actual data points , both needs to be sorted for the query to hdf5 according to the data points

        secCadjusted = [ int(x) for x in secC ]
        points = zip(secCadjusted,plotDatatitles)
        pack = (sorted(points))
        secCadjusted = [point[0] for point in pack]
        plotDatatitles = [point[1] for point in pack]

        #regPadjusted = sorted(regPadjusted, key=int)

        #regParray = np.array( regPadjusted )
        #print(regPadjusted)
        #with h5py.File('/home/sidney/datahdf5/experiments/{0}_combined.hdf5'.format(year) ,'r')as hf:
        outputData = []
        with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(year) ,'r')as hf:
            #retrieve the data for each region of consumption and append to data variable
            for x in regC:
                test = (hf.get('region{0}'.format(int(x))))
                tmp = test[int(regP[0]),int(secP[0]),int(regRS[0]),secCadjusted]
                tmp = tmp.tolist()
                outputData.append(tmp)
            #sort from high to low


            test = np.asarray(outputData)


            outputData = (test.sum(axis=0).tolist())
            #sort from high to low
            points = zip(outputData,plotDatatitles)
            package = (sorted(points, reverse=True))
            outputData = [point[0] for point in package]
            plotDatatitles = [point[1] for point in package]





            t = (zip(package,outputData))

            return outputData, plotDatatitles, t
    #determine plottype as it affects the query and determine the mode that we are in
    if plotType == "TreeMap" and selectMode == "Contribution footprint of consumption split by consuming region":
        with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(year) ,'r')as hf:
        #with h5py.File('/home/sidney/datahdf5/experiments/{0}_combined.hdf5'.format(year) ,'r')as hf:
            outputData = []
            print("***")

            #retrieve the data for each region of consumption and append to data variable
            for x in regC:

                test = (hf.get('region{0}'.format(int(x))))
                tmp = test[int(regP[0]),int(secP[0]),int(regRS[0]),int(secC[0])]
                tmp = tmp.tolist()
                outputData.append(tmp)
            #sort from high to low
            points = zip(outputData,plotDatatitles)
            package = (sorted(points, reverse=True))
            outputData = [point[0] for point in package]
            plotDatatitles = [point[1] for point in package]


            t = (zip(package,outputData))


            return outputData, plotDatatitles, t
    if plotType == "TreeMap" and selectMode == "Contribution footprint of consumption split by region selling":
        #as it is piechart we only select one year
        print("Query is: ")
        #print("regP"+str(regP[0])+"secP"+str(secP[0])+"regRS"+str(regRS[0])+"regC"+str(regC[0])+"secC"+str(secC[0]))
        #we have the title list and the actual data points , both needs to be sorted for the query to hdf5 according to the data points
        regRSadjusted = [ int(x) for x in regRS ]
        points = zip(regRSadjusted,plotDatatitles)
        pack = (sorted(points))
        regRSadjusted = [point[0] for point in pack]
        plotDatatitles = [point[1] for point in pack]


        outputData = []
        with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(year) ,'r') as hf:
            for x in regC:
                db = (hf.get('region{0}'.format(x)))
                tmp = db[int(regP[0]),int(secP[0]),regRSadjusted,int(secC[0])]
                outputData.append(tmp.tolist())

        test = np.asarray(outputData)


        outputData = (test.sum(axis=0).tolist())

#sort from high to low
        points = zip(outputData,plotDatatitles)
        package = (sorted(points, reverse=True))
        outputData = [point[0] for point in package]
        plotDatatitles = [point[1] for point in package]




        t = (zip(package,outputData))

        return outputData, plotDatatitles, t

def treeMp(vLabel,vData, vTitle, vDescr):
    data = []

    for x, y in zip(vData, vLabel):
        data.append({"value": x, "name":y })

    print(data)
    print("did we reach?")
    data = {
            'sample_datas' : data,
        'title' : vTitle,
        'description': vDescr,

        }
    return data


def defaultData(plotType,selectMode, request):
    if plotType == "TreeMap" and selectMode == "Contribution footprint of consumption split by consumed product category":
        #call queryHDF5 function with standard input
        id = Product.objects.values_list('id', flat=True)


        lvls = Product.objects.values_list('lvl', flat=True)
        lwst_level = max(lvls)
        secCdata = []
        secCdata2 = []
        secCtitlesReady = []
        for x in id:
            lvl = Product.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == lvl:
                name = Product.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    secCtitlesReady.append(name[:40])
                else:
                    secCtitlesReady.append(name)

                secCdata2.append(x-1)
                #secCtitlesReady.append(secC)
                #secCdata.append(str(x-1)+secC)

        #as regC is the exception for querying we need to pass all ids
        id = Country.objects.values_list('id', flat=True)
        locals = []
        for x in id:
            #gather the lws_level only
            lvlCondition = Country.objects.values_list('lwst_level', flat=True).get(pk=x)
            if lvlCondition == True:
                local = Country.objects.values_list('local', flat=True).get(pk=x)
                local = int(local)
                locals.append(local)

        plotData,secCtitles, queryData = queryhdf5(plotType,selectMode, "", 2011, [0], [0] ,[0], [1],secCdata2, secCtitlesReady, request)

        return secCtitles, plotData
    #plotType,selectMode, envP, year, regP, secP,regRS, regC,secC, plotDatatitles, request
    if plotType == "TreeMap" and selectMode == "Contribution footprint of consumption split by sector where impact occurs":
        #call queryHDF5 function with standard input
        id = Product.objects.values_list('id', flat=True)


        lvls = Product.objects.values_list('lvl', flat=True)
        lwst_level = max(lvls)
        secPdata = []
        secPdata2 = []
        secPtitlesReady = []
        for x in id:
            lvl = Product.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == lvl:
                name = Product.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    secPtitlesReady.append(name[:40])
                else:
                    secPtitlesReady.append(name)

                secPdata2.append(x-1)
                #secCtitlesReady.append(secC)
                #secCdata.append(str(x-1)+secC)

        #as regC is the exception for querying we need to pass all ids
        id = Country.objects.values_list('id', flat=True)
        locals = []
        for x in id:
            #gather the lws_level only
            lvlCondition = Country.objects.values_list('lwst_level', flat=True).get(pk=x)
            if lvlCondition == True:
                local = Country.objects.values_list('local', flat=True).get(pk=x)
                local = int(local)
                locals.append(local)

        plotData,secPtitles, queryData = queryhdf5(plotType,selectMode, "", 2011, [0], secPdata2 ,[0], [1],[0], secPtitlesReady, request)

        return secPtitles, plotData
    #plotType,selectMode, envP, year, regP, secP,regRS, regC,secC, plotDatatitles, request
    if plotType == "TreeMap" and selectMode == "Contribution footprint of consumption split by consuming region":
        #call queryHDF5 function with standard input


        #as regC is the exception for querying we need to pass all ids
        id = Country.objects.values_list('id', flat=True)
        locals = []
        names = []
        lvls = Country.objects.values_list('lvl', flat=True)
        lwst_level = max(lvls)

        regCdata2 = []
        regCtitlesReady = []
        for x in id:
            lvl = Country.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == lvl:
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    regCtitlesReady.append(name[:40])
                else:
                    regCtitlesReady.append(name)

                regCdata2.append(x-1)
        for x in id:
            #gather the lws_level only
            lvlCondition = Country.objects.values_list('lwst_level', flat=True).get(pk=x)
            if lvlCondition == True:
                local = Country.objects.values_list('id', flat=True).get(pk=x)
                local = int(local)
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                names.append(name)
                locals.append(local)

        plotData,secPtitles, queryData = queryhdf5(plotType,selectMode, "", 2011, [0], [0] ,[0], locals,[0], regCtitlesReady, request)

        return secPtitles, plotData
    if plotType == "TreeMap" and selectMode == "Contribution footprint of consumption split by country where impact occurs":
        #call queryHDF5 function with standard input
        id = Country.objects.values_list('id', flat=True)


        lvls = Country.objects.values_list('lvl', flat=True)
        lwst_level = max(lvls)
        regPdata = []
        regPdata2 = []
        regPtitlesReady = []
        for x in id:
            lvl = Country.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == lvl:
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    regPtitlesReady.append(name[:40])
                else:
                    regPtitlesReady.append(name)

                regPdata2.append(x-1)
                #secCtitlesReady.append(secC)
                #secCdata.append(str(x-1)+secC)

        #as regC is the exception for querying we need to pass all ids
        id = Country.objects.values_list('id', flat=True)
        locals = []
        for x in id:
            #gather the lws_level only
            lvlCondition = Country.objects.values_list('lwst_level', flat=True).get(pk=x)
            if lvlCondition == True:
                local = Country.objects.values_list('local', flat=True).get(pk=x)
                local = int(local)
                locals.append(local)

        plotData,regPtitles, queryData = queryhdf5(plotType,selectMode, "", 2011, regPdata2, [0],[0], [1],[0], regPtitlesReady, request)

        return regPtitles, plotData
    if plotType == "TreeMap" and selectMode == "Contribution footprint of consumption split by region selling":
        #call queryHDF5 function with standard input
        id = Country.objects.values_list('id', flat=True)


        lvls = Country.objects.values_list('lvl', flat=True)
        lwst_level = max(lvls)
        regRSdata = []
        regRSdata2 = []
        regRStitlesReady = []
        for x in id:
            lvl = Country.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == lvl:
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                if len(name) > 25:
                    regRStitlesReady.append(name[:40])
                else:
                    regRStitlesReady.append(name)

                regRSdata2.append(x-1)
                #secCtitlesReady.append(secC)
                #secCdata.append(str(x-1)+secC)

        #as regC is the exception for querying we need to pass all ids
        id = Country.objects.values_list('id', flat=True)
        locals = []
        for x in id:
            #gather the lws_level only
            lvlCondition = Country.objects.values_list('lwst_level', flat=True).get(pk=x)
            if lvlCondition == True:
                local = Country.objects.values_list('local', flat=True).get(pk=x)
                local = int(local)
                locals.append(local)

        plotData,regRStitles, queryData = queryhdf5(plotType,selectMode, "", 2011, [0], [0],regRSdata2, [1],[0], regRStitlesReady, request)

        return regRStitles, plotData

