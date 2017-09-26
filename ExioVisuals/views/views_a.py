
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


# Create your views here.
#Homepage code
def home(request):
    context = RequestContext(request)


    start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)
    nb_element = 150
    xdata = range(nb_element)
    xdata = list(map(lambda x: start_time + x * 1000000000, xdata))
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = list(map(lambda x: x * 2, ydata))

    tooltip_date = "%d %b %Y %H:%M:%S %p"
    extra_serie1 = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "date_format": tooltip_date,
    }
    extra_serie2 = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "date_format": tooltip_date,
    }
    chartdata = {'x': xdata,
        'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie1, 'kwargs1': { 'color': '#778899' },
        'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie2, 'kwargs2': { 'color': '#b22121' },
    }

    charttype = "lineChart"
    chartcontainer = 'linechart_container'  # container name
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '%d %b %Y %H',
            'tag_script_js': True,
            'jquery_on_ready': False,
        },'sample_datas' : [
    {"value": 100, "name": "alpha"      },
    {"value": 70, "name": "beta"},
            {"value": 30, "name": "Test"},
            {"value": 10, "name": "bla"},

  ]
    }
    #print(data)
    return render(request,'ExioVisuals/home.html', data)





    #return render_to_response('ExioVisuals/home.html', {'data': data})


#global tab code

def distributionView(request):

    #by default mode is :
    mode = 0
    #Retrieve skeleton of forms-------------------------------------------------------------
    formTree = ProductSelectionForm(request.POST or None)
    formTreeCountry = CountrySelectionForm(request.POST or None)
    formTreeSubstance = SubstanceSelectionForm(request.POST or None)
    formTreeYear = YearFSelectionForm(request.POST or None)
    print("wher")

    MemberFormSet = formset_factory(wraps(PostFormEFactor)(partial(PostFormEFactor)))

 #retrieve filter data!
    if request.method == 'POST':

        #First and foremost try to retrieve any mode (decomposition data)
        mode = (request.POST.get('y'))
        exportRaw = request.POST.get('raw')
        exportRaw2 = request.POST.get('raw2')

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
                #normally we want to load data here that makes sense of the selected mode
                xdata, ydata = retrieveData()

                #set title,description, size
                title = "Contribution footprint of consumption split by consumed product category"
                xdata, ydata = defaultData("PieChart", title, request)
                description = ""

                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
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
                for i in productP:
                    i['selected'] = False
                    for x in i['children']:
                        x['selected'] = False
                        for y in x['children']:
                            y['selected'] = False
                            for k in y['children']:
                                k['selected'] = True


                print(parsed_json)
                #print(countryDataReady)

                #parsed_json[0]['selected'] = True
                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                productP = json.dumps(productP)
                yearData = json.dumps(yearData)

                #countryDataReady = (countryDataReady.replace("'", '"'))
                #call pieChart function
                pieData = pieChart(xdata,ydata, title , description)
             #updata dictionary for filter options: form skeletons
                pieData.update({'modeForm':modeFormSet})

                pieData.update({'sourceData': sourceData})
                pieData.update({'countryDataReady': countryDataReady})
                pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #create select modes for fancyTree : so single select or multiple
                pieData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                pieData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                pieData.update({'mode_tree': 2, 'warning_6':"","productPurchased":productP})
                pieData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
                pieData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                pieData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
                #pieData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})

                #send signal for popup and default data
                popup = 1
                default =1
                pieData.update({'popup': popup})
                pieData.update({'default': default})

                pieData.update({'userSelectMode': "Contribution footprint of consumption split by consumed product category"})
                return render(request,"ExioVisuals/distribution.html", pieData)
            if mode=="selectB":
                #call all the necessary forms
                modeFormSet = modes(initial={'selection': 'selectB'})


                #set title,description, size
                title = "Contribution footprint of consumption split by consuming region"
                description = ""
                xdata, ydata = defaultData("PieChart", title, request)
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

                #countryDataReady = (countryDataReady.replace("'", '"'))
                #call pieChart function
                pieData = pieChart(xdata,ydata, title , description)
             #updata dictionary for filter options: form skeletons
                pieData.update({'modeForm':modeFormSet})

                pieData.update({'sourceData': sourceData})
                pieData.update({'countryDataReady': countryDataReady})
                pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #create select modes for fancyTree : so single select or multiple
                pieData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                pieData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction": sourceData})
                pieData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                pieData.update({'mode_tree2': 2, 'warning_5':"","regionConsumng":regConsuming})
                pieData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                pieData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
                #pieData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})

                popup = 1
                default =1
                pieData.update({'popup': popup})
                pieData.update({'default': default})
                pieData.update({'userSelectMode': "Contribution footprint of consumption split by consuming region"})
                return render(request,"ExioVisuals/distribution.html", pieData)
            if mode=="selectD":
                #call all the necessary forms
                modeFormSet = modes(initial={'selection': 'selectD'})
                yearsSelect = yearsSingleSelect(initial={'Year': '2011'})



                #set title,description, size
                title = "Contribution footprint of consumption split by country where impact occurs"
                description = ""
                xdata, ydata = defaultData("PieChart", title, request)
                sourceData = generateTrees(formTree)
                countryDataReady = generateTrees(formTreeCountry)
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
                        else:
                            x['selected'] = False

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


                #countryDataReady = (countryDataReady.replace("'", '"'))
                #call pieChart function
                pieData = pieChart(xdata,ydata, title , description)
             #updata dictionary for filter options: form skeletons
                pieData.update({'modeForm':modeFormSet})

                pieData.update({'sourceData': sourceData })
                pieData.update({'countryDataReady': countryDataReady})
                pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #create select modes for fancyTree : so single select or multiple
                pieData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                pieData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                pieData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                pieData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady2})
                pieData.update({'mode_tree3': 2, 'warning_7':"","regionProducing":regProducing})
                pieData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady2})
                #send signal for popup and default data
                popup = 1
                default =1
                pieData.update({'popup': popup})
                pieData.update({'default': default})
                pieData.update({'userSelectMode': "Contribution footprint of consumption split by country where impact occurs"})
                return render(request,"ExioVisuals/distribution.html", pieData)
            if mode=="selectC":
                #call all the necessary forms
                modeFormSet = modes(initial={'selection': 'selectC'})
                yearsSelect = yearsSingleSelect(initial={'Year': '2011'})


                #set title,description, size
                title = "Contribution footprint of consumption split by sector where impact occurs"
                description = ""
                #normally we want to load data here that makes sense of the selected mode
                xdata, ydata = defaultData("PieChart", title, request)

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

                #countryDataReady = (countryDataReady.replace("'", '"'))
                #call pieChart function
                pieData = pieChart(xdata,ydata, title , description)
             #updata dictionary for filter options: form skeletons
                pieData.update({'modeForm':modeFormSet})

                pieData.update({'yearsMode1':yearsSelect})
                pieData.update({'sourceData': sourceData})
                pieData.update({'countryDataReady': countryDataReady})
                pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #create select modes for fancyTree : so single select or multiple
                pieData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                pieData.update({'mode_tree4': 2, 'warning_8':"", "sectorOfProduction": secOfProduction})
                pieData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":productPurchased})
                pieData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":regOfProduction})
                pieData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":regOfProduction})
                pieData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":regOfProduction})
                #pieData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})

                #send signal for popup and default data
                popup = 1
                default =1
                pieData.update({'popup': popup})
                pieData.update({'default': default})
                pieData.update({'userSelectMode': "Contribution footprint of consumption split by sector where impact occurs"})
                return render(request,"ExioVisuals/distribution.html", pieData)
            if mode=="selectF":
                #call all the necessary forms
                modeFormSet = modes(initial={'selection': 'selectF'})
                yearsSelect = yearsSingleSelect(initial={'Year': '2011'})



                #set title,description, size
                title = "Contribution footprint of consumption split by region selling"
                description = ""
                xdata, ydata = defaultData("PieChart", title, request)
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
                pieData = pieChart(xdata,ydata, title , description)
             #updata dictionary for filter options: form skeletons
                pieData.update({'modeForm':modeFormSet})

                pieData.update({'sourceData': sourceData })
                pieData.update({'countryDataReady': countryDataReady})
                pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #create select modes for fancyTree : so single select or multiple
                pieData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

                pieData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                pieData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                pieData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady2})
                pieData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady2})
                pieData.update({'mode_tree6': 2, 'warning_10':"","regionSelling":regProducing})
                #send signal for popup and default data
                popup = 1
                default =1
                pieData.update({'popup': popup})
                pieData.update({'default': default})
                pieData.update({'userSelectMode': "Contribution footprint of consumption split by region selling"})
                return render(request,"ExioVisuals/distribution.html", pieData)

        #************START RETRIEVING USER SELECTIONS*******************
#as it only allows one year we will fetch one (there is a case that multiple years are selected due to cookies)
        year = (request.POST.get('ft_6[]'))
        #check if year has been filled in properly
        if not year:
            error_status = {"error":"<Year> data has not been filled in properly."}
            return render(request, "ExioVisuals/error_page.html", error_status)

        year = YearF.objects.values_list('name', flat=True).get(pk=year)
        envP = (request.POST.getlist('ft_4[]'))
        envPtitles = []
        for x in envP:
            print("Environmental Pressure:")
            print(Substance.objects.get(pk=x))
            print(Substance.objects.values_list('name', flat=True).get(pk=x))
            name = (Substance.objects.values_list('name', flat=True).get(pk=x))
            envPtitles.append(name)


        year = (request.POST.get('ft_6[]'))
        print(year)

        print(YearF.objects.get(pk=year))

        year = YearF.objects.values_list('name', flat=True).get(pk=year)
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


        print("test8888888")
        print(regP)
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
        print(year)

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
            plotType = "PieChart"
            #QUERY THE DATABASE
            plotData,regPtitles, queryData = queryhdf5(plotType,selectMode, envP, year, regPdata, secPdata,regRSdata, regCdata,secCdata, regPtitles,request)

            table = generateDesc(selectMode,envPtitles,year,regPquery, secPparents, regRSquery, regCparents, secCparents, queryData)

            pieData = pieChart(regPtitles,plotData,selectMode, table)
            modeFormSet = modes(initial={'selection': 'selectA'})
            pieData.update({'modeForm':modeFormSet})
            pieData.update({'titles': regPtitles})
            pieData.update({'plot': plotData})
            sourceData = generateTrees(formTree)
            countryDataReady = generateTrees(formTreeCountry)
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
                    else:
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

            #print(countryDataReady)

            #parsed_json[0]['selected'] = True
            countryDataReady2 = json.dumps(parsed_json)
            sourceData = json.dumps(parsed_json2)
            regProducing = json.dumps(regProducing)
            yearData = json.dumps(yearData)


            #countryDataReady = (countryDataReady.replace("'", '"'))
            #call pieChart function

         #updata dictionary for filter options: form skeletons
            pieData.update({'modeForm':modeFormSet})
            pieData.update({'session': "session"})
            pieData.update({'sourceData': sourceData })
            pieData.update({'countryDataReady': countryDataReady})
            pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
            notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
            #create select modes for fancyTree : so single select or multiple
            pieData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})
            pieData.update({'userSelectMode': "Contribution footprint of consumption split by country where impact occurs"})

            pieData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
            pieData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
            pieData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady2})
            pieData.update({'mode_tree3': 2, 'warning_7':"","regionProducing":regProducing})
            pieData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady2})
        if selectMode == "Contribution footprint of consumption split by sector where impact occurs":
            plotType = "PieChart"
            #QUERY THE DATABASE
            plotData,secPtitles, queryData = queryhdf5(plotType,selectMode, envP, year, regPdata, secPdata,regRSdata, regCdata,secCdata, secPtitles, request)

            table = generateDesc(selectMode,envPtitles,year,regPparents, secPquery, regRSquery, regCparents, secCparents,queryData)

            pieData = pieChart(secPtitles,plotData,selectMode, table)
            modeFormSet = modes(initial={'selection': 'selectA'})
            pieData.update({'modeForm':modeFormSet})
            pieData.update({'titles': secPtitles})
            pieData.update({'plot': plotData})

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

            #countryDataReady = (countryDataReady.replace("'", '"'))
            #call pieChart function
         #updata dictionary for filter options: form skeletons
            pieData.update({'modeForm':modeFormSet})

            pieData.update({'sourceData': sourceData})
            pieData.update({'countryDataReady': countryDataReady})
            pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
            notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
            #create select modes for fancyTree : so single select or multiple
            pieData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})
            pieData.update({'session': "session"})
            pieData.update({'mode_tree4': 2, 'warning_8':"", "sectorOfProduction": secOfProduction})
            pieData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":productPurchased})
            pieData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":regOfProduction})
            pieData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":regOfProduction})
            pieData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":regOfProduction})
            #pieData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})

            #send signal for popup and default data
            popup = 1

            pieData.update({'popup': popup})
            pieData.update({'userSelectMode': "Contribution footprint of consumption split by sector where impact occurs"})

        if selectMode == "Contribution footprint of consumption split by consumed product category":
            plotType = "PieChart"
            #QUERY THE DATABASE
            plotData,secCtitles, queryData = queryhdf5(plotType,selectMode, envP, year, regPdata, secPdata,regRSdata, regCdata,secCdata, secCtitles, request)
            modeFormSet = modes(initial={'selection': 'selectA'})
            table = generateDesc(selectMode,envPtitles,year,regPquery, secPquery, regRSquery, regCquery, secCquery, queryData)
            pieData = pieChart(secCtitles,plotData,selectMode, table)
            countryDataReady = generateTrees(formTreeCountry)
            parsed_json = json.loads(countryDataReady)
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
            for i in productP:
                i['selected'] = False
                for x in i['children']:
                    x['selected'] = False
                    for y in x['children']:
                        y['selected'] = False
                        for k in y['children']:
                            k['selected'] = False


            print(parsed_json)
            #print(countryDataReady)

            #parsed_json[0]['selected'] = True
            countryDataReady = json.dumps(parsed_json)
            sourceData = json.dumps(parsed_json2)
            productP = json.dumps(productP)
            yearData = json.dumps(yearData)
            pieData.update({'modeForm':modeFormSet})
            #countryDataReady = (countryDataReady.replace("'", '"'))
            #call pieChart function
         #updata dictionary for filter options: form skeletons

            pieData.update({'countryDataReady': countryDataReady})
            pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
            notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
            #create select modes for fancyTree : so single select or multiple
            pieData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})

            pieData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
            pieData.update({'mode_tree': 2, 'warning_6':"","productPurchased":productP})
            pieData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
            pieData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
            pieData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
            #pieData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})
            pieData.update({'session': "session"})
            pieData.update({'userSelectMode': "Contribution footprint of consumption split by consumed product category"})


            pieData.update({'titles': secCtitles})
            pieData.update({'plot': plotData})
        if selectMode == "Contribution footprint of consumption split by consuming region":
            plotType = "PieChart"

            print(regCdata)
            print(regCtitles)
            #QUERY THE DATABASE
            plotData,regCtitles, queryData = queryhdf5(plotType,selectMode, envP, year, regPdata, secPdata,regRSdata, regCdata,secCdata, regCtitles, request)

            table = generateDesc(selectMode,envPtitles,year,regPquery, secPquery, regRSquery, regCquery, secCquery, queryData)

            pieData = pieChart(regCtitles,plotData,selectMode, table)
            modeFormSet = modes(initial={'selection': 'selectA'})
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
            for i in regConsuming:
                if i['title'] == "Total":
                    i['selected'] = False
                for x in i['children']:
                    x['selected'] = False
                    for y in x['children']:
                                y['selected'] = False

            #print(countryDataReady)

            #parsed_json[0]['selected'] = True
            countryDataReady = json.dumps(parsed_json)
            sourceData = json.dumps(parsed_json2)
            regConsuming = json.dumps(regConsuming)
            yearData = json.dumps(yearData)

            #countryDataReady = (countryDataReady.replace("'", '"'))
            #call pieChart function
         #updata dictionary for filter options: form skeletons
            pieData.update({'modeForm':modeFormSet})
            pieData.update({'session': "session"})
            pieData.update({'sourceData': sourceData})
            pieData.update({'countryDataReady': countryDataReady})
            pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
            notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
            #create select modes for fancyTree : so single select or multiple
            pieData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})
            pieData.update({'session': "session"})
            pieData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction": sourceData})
            pieData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
            pieData.update({'mode_tree2': 2, 'warning_5':"","regionConsumng":regConsuming})
            pieData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
            pieData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
            #pieData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})

            popup = 1
            pieData.update({'popup': popup})
            pieData.update({'userSelectMode': "Contribution footprint of consumption split by consuming region"})
            pieData.update({'modeForm':modeFormSet})
            pieData.update({'titles': regCtitles})
            pieData.update({'plot': plotData})
        if selectMode == "Contribution footprint of consumption split by region selling":
            plotType = "PieChart"
            #QUERY THE DATABASE
            plotData,regRStitles, queryData = queryhdf5(plotType,selectMode, envP, year, regPdata, secPdata,regRSdata, regCdata,secCdata, regRStitles,request)

            table = generateDesc(selectMode,envPtitles,year,regPquery, secPparents, regRSquery, regCparents, secCparents, queryData)

            pieData = pieChart(regRStitles,plotData,selectMode, table)
            modeFormSet = modes(initial={'selection': 'selectF'})
            pieData.update({'modeForm':modeFormSet})
            pieData.update({'titles': regRStitles})
            pieData.update({'plot': plotData})
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
            pieData.update({'modeForm':modeFormSet})

            pieData.update({'sourceData': sourceData })
            pieData.update({'countryDataReady': countryDataReady})
            pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
            notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
            #create select modes for fancyTree : so single select or multiple
            pieData.update({'mode_tree7': 1, 'warning_11':notification,'yearDataReady': yearData})
            pieData.update({'session': "session"})
            pieData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
            pieData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
            pieData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady2})
            pieData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady2})
            pieData.update({'mode_tree6': 2, 'warning_10':"","regionSelling":regProducing})
            #send signal for popup and default data
            popup = 1
            pieData.update({'popup': popup})
            pieData.update({'userSelectMode': "Contribution footprint of consumption split by region selling"})



        #json_data = json.dumps(dataReady)

        #pieData = json_data
        #popup = 0
        #pieData.update({'popup': popup})
        #for key in request.POST.get('ft_01[]'):
         #   print(key)
          #  value = request.POST[key]
           # print(value)

        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
        if request.is_ajax():
            #Always use get on request.POST. Correct way of querying a QueryDict.
            email = request.POST.get('email')
            password = request.POST.get('password')
            mode = request.POST.get('radio')
            print(request.POST)
            print(email)
            data = {"email":email , "password" : password, "sign": "Dsdfs"}


            #Returning same data back to browser.It is not possible with Normal submit
            return JsonResponse(data)
        #as I use formsets this is mandatory
        formset = MemberFormSet(request.POST)
        #make sure every form is validMemberFormSet = formset_factory(wraps(PostFormEFactor)(partial(PostFormEFactor)))


        return render(request,"ExioVisuals/distribution.html", pieData)






        #invoke retrieve data function (should take more filtering values of course).
    #xdata, ydata = retrieveData()

        #set title,description, size
    #title = "Global CO2 emission distribution"
    #description = "This chart shows the GHG emission distribution per country in the world. You can click on a country name to filter out the corresponding country from the piechart. Double click to select only one country."

        #call pieChart function
    #pieData = pieChart(xdata,ydata, title , description)





    #pieData.update(bla)
     #updata dictionary for filter options : FancyTree
    pieData = ({'formTree2': formTree})
    pieData.update({'desc': '<div class="alert alert-info"><h2><span class="glyphicon glyphicon-arrow-up" aria-hidden="true"></span></H2><strong><span class="glyphicon glyphicon-info-sign" aria-hidden="true"></span>  Select your mode in the navigation bar.</strong></div>' })


    #start getting some form skeletons now!
    ArticleFormSet = formset_factory(PostFormEFactor)
    formset = ArticleFormSet()
    formset = formset_factory(wraps(PostFormEFactor)(partial(PostFormEFactor)), extra=1)
     #updata dictionary for filter options: form skeletons
    pieData.update({'formset2':formset})
    selectionForm = formset_factory(wraps(reloadForm)(partial(reloadForm)), extra=1)
    pieData.update({'selectionForm': selectionForm})



    pieData.update({'sourceData': generateTrees(formTree)})
    pieData.update({'countryDataReady': generateTrees(formTreeCountry)})
    pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
    modeFormSet = modes(initial={'selection': 'selectA'})
    pieData.update({'modeForm':modeFormSet})


    return render(request,"ExioVisuals/distribution.html", pieData)

#function that trims the old tree data from mySQL to only get the source data which is what is used for rendering
def generateTrees(treeData):
    tree = str(treeData)
    trimTree = (tree.partition('[{')[-1].rpartition('}]')[0])
    rebuildTree = "[{"+trimTree+"}]"
    return rebuildTree

def timeseries(request):
    #intialize mode
    modeFormSet = modesTimeSeries()
    pieData = ({'modeForm':modeFormSet})
    #Retrieve skeleton of forms-------------------------------------------------------------
    #by default mode is :
    mode = 0
    #Retrieve skeleton of forms-------------------------------------------------------------
    formTree = ProductSelectionForm(request.POST or None)
    formTreeCountry = CountrySelectionForm(request.POST or None)
    formTreeSubstance = SubstanceSelectionForm(request.POST or None)
    formTreeYear = YearFSelectionForm(request.POST or None)
    print("wher")

    MemberFormSet = formset_factory(wraps(PostFormEFactor)(partial(PostFormEFactor)))
 #retrieve filter data!
    if request.method == 'POST':

        #First and foremost try to retrieve any mode (decomposition data)
        mode = (request.POST.get('y'))
        exportRaw = request.POST.get('raw')
        exportRaw2 = request.POST.get('raw2')


        if exportRaw != None and len(exportRaw) != 0 and exportRaw2 != None and len(exportRaw2) != 0:

                import csv
                from django.utils.encoding import smart_str

                #exportRaw2 = exportRaw2.split(",")

                bt = (exportRaw)
               #convert to actual list
                import ast
                titles = ast.literal_eval(exportRaw)
                data = ast.literal_eval(exportRaw2)

                from collections import defaultdict

                c = defaultdict(int)
                for d in data:
                    c[d['name']] += d['value']


                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename=output.csv'
                writer = csv.writer(response, csv.excel)
                response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
                writer.writerow([
                    smart_str(u"Title"),
                    smart_str(u"Data"),smart_str(u"year"),

                ])
                print("****")


                #merge the two sorted lists
                points = zip(titles,data)
                #print(list(exportRaw))
                #rint(list(exportRaw))
                for key, value in c.items():
                    #print(value)
                    seperate = (key.split("_"))
                    year = (seperate[0])
                    name = (seperate[1])
                    cleanedObj = name.replace(",", " ")
                    #print(obj)
                    writer.writerow([
                        smart_str((cleanedObj)),
                        smart_str((value)),
                        smart_str((year)),


                    ])



                return response
        if mode != None:
            if mode=="selectA":
                #call all the necessary forms
                modeFormSet = modesTimeSeries()

                #normally we want to load data here that makes sense of the selected mode
                #xdata, ydata = retrieveData()

                #set title,description, size
                title = "Contribution footprint of consumption split by consumed product category"
                description = ""

                csvData, ydata = defaultData("TimeSeries", title, request)
                from collections import defaultdict
                            #sum the value if years and name are the same (timeseries query gives multiple values)
                c = defaultdict(int)
                for d in csvData:
                    c[d['name']] += d['value']
                queryData = []
                shorten = []
                    #generate list for table
                for key, value in c.items():
                        #print(value)
                        seperate = (key.split("_"))
                        year = (seperate[0])

                        name = (seperate[1])
                        queryData.append(year+"_"+name+"_"+str(value))

                pieData.update({'graph':ydata})
                pieData.update({'modeForm':modeFormSet})
                #pieData.update({'titles': secCtitles})
                pieData.update({'plot': csvData})
                 #send signal for popup and default data
                popup = 1
                default =1
                pieData.update({'popup': popup})
                pieData.update({'default': default})


                countryDataReady = generateTrees(formTreeCountry)
                parsed_json = json.loads(countryDataReady)
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
                for i in productP:
                    i['selected'] = False
                    for x in i['children']:
                        x['selected'] = True
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
                #call pieChart function
             #updata dictionary for filter options: form skeletons
                pieData.update({'modeForm':modeFormSet})

                pieData.update({'sourceData': sourceData})
                pieData.update({'countryDataReady': countryDataReady})
                pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #create select modes for fancyTree : so single select or multiple
                pieData.update({'mode_tree7': 2, 'warning_11':"",'yearDataReady': yearData})

                pieData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                pieData.update({'mode_tree': 2, 'warning_6':"","productPurchased":productP})
                pieData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
                pieData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                pieData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
                #pieData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})

                #send signal for popup and default data
                popup = 1
                default =1
                pieData.update({'popup': popup})
                pieData.update({'default': default})

                pieData.update({'userSelectMode': "Contribution footprint of consumption split by consumed product category"})

                #countryDataReady = (countryDataReady.replace("'", '"'))
                #call pieChart function
                #pieData = pieChart(xdata,ydata, title , description)
             #updata dictionary for filter options: form skeletons
                pieData.update({'modeForm':modeFormSet})



                pieData.update({'title':"Contribution footprint of consumption split by consumed product category"})

                pieData.update({'userSelectMode': "Contribution footprint of consumption split by consumed product category"})
                return render(request,"ExioVisuals/timeseries.html", pieData)
            if mode=="selectB":
                #call all the necessary forms
                modeFormSet = modesTimeSeries()

                #normally we want to load data here that makes sense of the selected mode
                #xdata, ydata = retrieveData()

                #set title,description, size
                title = "Contribution footprint of consumption split by consuming region"
                description = ""
                csvData, ydata = defaultData("TimeSeries", title, request)


                pieData.update({'graph':ydata})
                pieData.update({'modeForm':modeFormSet})
                #pieData.update({'titles': secCtitles})
                pieData.update({'plot': csvData})
                 #send signal for popup and default data
                popup = 1
                default =1
                pieData.update({'popup': popup})
                pieData.update({'default': default})

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
                        x['selected'] = True
                        for y in x['children']:
                                    y['selected'] = False

                print(parsed_json)
                #print(countryDataReady)

                #parsed_json[0]['selected'] = True
                countryDataReady = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                regConsuming = json.dumps(regConsuming)
                yearData = json.dumps(yearData)

                #countryDataReady = (countryDataReady.replace("'", '"'))
                #call pieChart function
             #updata dictionary for filter options: form skeletons
                pieData.update({'modeForm':modeFormSet})

                pieData.update({'sourceData': sourceData})
                pieData.update({'countryDataReady': countryDataReady})
                pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #create select modes for fancyTree : so single select or multiple
                pieData.update({'mode_tree7': 2, 'warning_11':"",'yearDataReady': yearData})

                pieData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction": sourceData})
                pieData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                pieData.update({'mode_tree2': 2, 'warning_5':"","regionConsumng":regConsuming})
                pieData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
                pieData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
                #pieData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})

                popup = 1
                default =1
                pieData.update({'popup': popup})
                pieData.update({'default': default})
                pieData.update({'title':"Contribution footprint of consumption split by consuming region"})
                pieData.update({'userSelectMode': "Contribution footprint of consumption split by consuming region"})
                return render(request,"ExioVisuals/timeseries.html", pieData)
            if mode=="selectC":
                #call all the necessary forms
                modeFormSet = modesTimeSeries()

                #normally we want to load data here that makes sense of the selected mode
                #xdata, ydata = retrieveData()

                #set title,description, size
                title = "Contribution footprint of consumption split by sector where impact occurs"
                description = ""
                csvData, ydata = defaultData("TimeSeries", title, request)
                from collections import defaultdict
                            #sum the value if years and name are the same (timeseries query gives multiple values)
                c = defaultdict(int)
                for d in csvData:
                    c[d['name']] += d['value']
                queryData = []
                shorten = []
                    #generate list for table
                for key, value in c.items():
                        #print(value)
                        seperate = (key.split("_"))
                        year = (seperate[0])

                        name = (seperate[1])
                        queryData.append(year+"_"+name+"_"+str(value))
                pieData.update({'graph':ydata})
                pieData.update({'modeForm':modeFormSet})
                #pieData.update({'titles': secCtitles})
                pieData.update({'plot': csvData})
                 #send signal for popup and default data
                popup = 1
                default =1
                pieData.update({'popup': popup})
                pieData.update({'default': default})

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
                        x['selected'] = True
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

                #countryDataReady = (countryDataReady.replace("'", '"'))
                #call pieChart function
             #updata dictionary for filter options: form skeletons
                pieData.update({'modeForm':modeFormSet})

                pieData.update({'sourceData': sourceData})
                pieData.update({'countryDataReady': countryDataReady})
                pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #create select modes for fancyTree : so single select or multiple
                pieData.update({'mode_tree7': 2, 'warning_11':"",'yearDataReady': yearData})

                pieData.update({'mode_tree4': 2, 'warning_8':"", "sectorOfProduction": secOfProduction})
                pieData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":productPurchased})
                pieData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":regOfProduction})
                pieData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":regOfProduction})
                pieData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":regOfProduction})
                #pieData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})

                #send signal for popup and default data
                popup = 1
                default =1
                pieData.update({'popup': popup, 'title': title})
                pieData.update({'default': default})
                pieData.update({'userSelectMode': "Contribution footprint of consumption split by sector where impact occurs"})

                pieData.update({'title':"Contribution footprint of consumption split by sector where impact occurs"})
                pieData.update({'userSelectMode': "Contribution footprint of consumption split by sector where impact occurs"})
                return render(request,"ExioVisuals/timeseries.html", pieData)
            if mode=="selectD":
                #call all the necessary forms
                modeFormSet = modesTimeSeries()

                #xdata, ydata = retrieveData()

                #set title,description, size
                title = "Contribution footprint of consumption split by country where impact occurs"
                description = ""
                sourceData = generateTrees(formTree)
                csvData, ydata = defaultData("TimeSeries", title, request)
                from collections import defaultdict
                            #sum the value if years and name are the same (timeseries query gives multiple values)
                c = defaultdict(int)
                for d in csvData:
                    c[d['name']] += d['value']
                queryData = []
                shorten = []
                    #generate list for table
                for key, value in c.items():
                        #print(value)
                        seperate = (key.split("_"))
                        year = (seperate[0])

                        name = (seperate[1])
                        queryData.append(year+"_"+name+"_"+str(value))
                pieData.update({'graph':ydata})
                pieData.update({'modeForm':modeFormSet})
                #pieData.update({'titles': secCtitles})
                pieData.update({'plot': csvData})
                 #send signal for popup and default data
                popup = 1
                default =1
                pieData.update({'popup': popup})
                pieData.update({'default': default})

                sourceData = generateTrees(formTree)
                countryDataReady = generateTrees(formTreeCountry)
                yearData = generateTrees(formTreeYear)
                yearData = json.loads(yearData)
                 #make year total unselectable in this case
                for i in yearData:
                    if i['title'] == "Total":
                        i['unselectable'] = True
                    for x in i['children']:
                        x['selected'] = True
                yearData = json.dumps(yearData)

                sourceData = generateTrees(formTree)
                countryDataReady = generateTrees(formTreeCountry)
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
                        x['selected'] = True
                        for y in x['children']:
                                    y['selected'] = False

                print(parsed_json)
                #print(countryDataReady)

                #parsed_json[0]['selected'] = True
                countryDataReady2 = json.dumps(parsed_json)
                sourceData = json.dumps(parsed_json2)
                regProducing = json.dumps(regProducing)
                yearData = json.dumps(yearData)


                #countryDataReady = (countryDataReady.replace("'", '"'))
                #call pieChart function
             #updata dictionary for filter options: form skeletons
                pieData.update({'modeForm':modeFormSet})

                pieData.update({'sourceData': sourceData })
                pieData.update({'countryDataReady': countryDataReady})
                pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #create select modes for fancyTree : so single select or multiple
                pieData.update({'mode_tree7':2, 'warning_11':"",'yearDataReady': yearData})

                pieData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                pieData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                pieData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady2})
                pieData.update({'mode_tree3': 2, 'warning_7':"","regionProducing":regProducing})
                pieData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady2})
                #send signal for popup and default data
                popup = 1
                default =1
                pieData.update({'popup': popup, 'title': title})

                pieData.update({'default': default})
                pieData.update({'userSelectMode': "Contribution footprint of consumption split by country where impact occurs"})
                return render(request,"ExioVisuals/timeseries.html", pieData)
            if mode=="selectF":
                #call all the necessary forms
                modeFormSet = modesTimeSeries()

                #xdata, ydata = retrieveData()

                #set title,description, size
                title = "Contribution footprint of consumption split by region selling"
                description = ""
                sourceData = generateTrees(formTree)
                csvData, ydata = defaultData("TimeSeries", title, request)
                from collections import defaultdict
                            #sum the value if years and name are the same (timeseries query gives multiple values)
                c = defaultdict(int)
                for d in csvData:
                    c[d['name']] += d['value']
                queryData = []
                shorten = []
                    #generate list for table
                for key, value in c.items():
                        #print(value)
                        seperate = (key.split("_"))
                        year = (seperate[0])

                        name = (seperate[1])
                        queryData.append(year+"_"+name+"_"+str(value))
                pieData.update({'graph':ydata})
                pieData.update({'modeForm':modeFormSet})
                #pieData.update({'titles': secCtitles})
                pieData.update({'plot': csvData})
                 #send signal for popup and default data

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
                for i in regRS:
                    if i['title'] == "Total":
                        i['selected'] = False
                    for x in i['children']:
                        x['selected'] = True
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
                pieData.update({'modeForm':modeFormSet})

                pieData.update({'sourceData': sourceData })
                pieData.update({'countryDataReady': countryDataReady})
                pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
                notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
                #create select modes for fancyTree : so single select or multiple
                pieData.update({'mode_tree7': 2, 'warning_11':"",'yearDataReady': yearData})

                pieData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
                pieData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
                pieData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady2})
                pieData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady2})
                pieData.update({'mode_tree6': 2, 'warning_10':"","regionSelling":regProducing})
                #send signal for popup and default data
                popup = 1
                default =1
                pieData.update({'popup': popup, 'title': title})
                pieData.update({'default': default})

                pieData.update({'userSelectMode': "Contribution footprint of consumption split by region selling"})
                return render(request,"ExioVisuals/timeseries.html", pieData)
        #************START RETRIEVING USER SELECTIONS*******************
        envP = (request.POST.getlist('ft_4[]'))
        envPtitles = []
        envP = (request.POST.getlist('ft_4[]'))
        envPtitles = []
        for x in envP:
            print("Environmental Pressure:")
            print(Substance.objects.get(pk=x))
            print(Substance.objects.values_list('name', flat=True).get(pk=x))
            name = (Substance.objects.values_list('name', flat=True).get(pk=x))
            envPtitles.append(name)


        #print(request.POST)
        year = []
        years = (request.POST.getlist('ft_6[]'))
        #check if year has been filled in properly
        if not years:
            error_status = {"error":"<Year> data has not been filled in properly."}
            return render(request, "ExioVisuals/error_page.html", error_status)
        if YearF.objects.values_list('name', flat=True).get(pk=years[0]) == "Total":
            # if it is total get all objects
            year = YearF.objects.values_list('name', flat=True)
            year = list(year)
            year.pop(0)
        else:
            for x in years:

                name = YearF.objects.values_list('name', flat=True).get(pk=x)
                year.append(name)
        print("Years selected:")

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


        print("test8888888")
        print(regP)
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
        print("gdsf")

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


        if selectMode == "Contribution footprint of consumption split by consumed product category":
            plotType = "TimeSeries"

            #QUERY THE DATABASE
            plotData,csvData, queryData = queryhdf5(plotType,selectMode, envP, year, regPdata, secPdata,regRSdata, regCdata,secCdata, secCtitles, request)

            from collections import defaultdict
            #sum the value if years and name are the same (timeseries query gives multiple values)
            c = defaultdict(int)
            for d in csvData:
                c[d['name']] += d['value']
            queryData = []
            shorten = []
                #generate list for table
            for key, value in c.items():
                    #print(value)
                    seperate = (key.split("_"))
                    ayear = (seperate[0])

                    name = (seperate[1])
                    queryData.append(ayear+"_"+name+"_"+str(value))

            table = generateDesc(selectMode,envPtitles,year,regPquery, secPquery, regRSquery, regCquery, secCquery, queryData)
            pieData = {'graph':plotData}

            countryDataReady = generateTrees(formTreeCountry)
            parsed_json = json.loads(countryDataReady)
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
            for i in productP:
                i['selected'] = False
                for x in i['children']:
                    x['selected'] = False
                    for y in x['children']:
                        y['selected'] = False
                        for k in y['children']:
                            k['selected'] = False


            print(parsed_json)
            #print(countryDataReady)

            #parsed_json[0]['selected'] = True
            countryDataReady = json.dumps(parsed_json)
            sourceData = json.dumps(parsed_json2)
            productP = json.dumps(productP)
            yearData = json.dumps(yearData)

            #countryDataReady = (countryDataReady.replace("'", '"'))
            #call pieChart function
         #updata dictionary for filter options: form skeletons
            pieData.update({'modeForm':modeFormSet})
            pieData.update({'session': "session"})
            pieData.update({'sourceData': sourceData})
            pieData.update({'countryDataReady': countryDataReady})
            pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
            notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
            #create select modes for fancyTree : so single select or multiple
            pieData.update({'mode_tree7': 2, 'warning_11': "",'yearDataReady': yearData})

            pieData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
            pieData.update({'mode_tree': 2, 'warning_6':"","productPurchased":productP})
            pieData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady})
            pieData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
            pieData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
            #pieData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})

            #send signal for popup and default data
            popup = 1
            pieData.update({'popup': popup})

            pieData.update({'userSelectMode': "Contribution footprint of consumption split by consumed product category"})

            #countryDataReady = (countryDataReady.replace("'", '"'))
            #call pieChart function
            #pieData = pieChart(xdata,ydata, title , description)
         #updata dictionary for filter options: form skeletons
            pieData.update({'modeForm':modeFormSet})



            pieData.update({'title':"Contribution footprint of consumption split by consumed product category"})

            pieData.update({'userSelectMode': "Contribution footprint of consumption split by consumed product category"})

            pieData.update({'description':table})
            pieData.update({'modeForm':modeFormSet})
            pieData.update({'title':selectMode})
            pieData.update({'titles': secCtitles})
            pieData.update({'plot': csvData})


        if selectMode == "Contribution footprint of consumption split by sector where impact occurs":
            plotType = "TimeSeries"
            #QUERY THE DATABASE

            plotData,csvData, queryData = queryhdf5(plotType,selectMode, envP, year, regPdata, secPdata,regRSdata, regCdata,secCdata, secPtitles,request)
            from collections import defaultdict

            #sum the value if years and name are the same (timeseries query gives multiple values)
            c = defaultdict(int)
            for d in csvData:
                c[d['name']] += d['value']
            queryData = []
            shorten = []
                #generate list for table
            for key, value in c.items():
                    #print(value)
                    seperate = (key.split("_"))
                    ayear = (seperate[0])

                    name = (seperate[1])
                    queryData.append(ayear+"_"+name+"_"+str(value))



            table = generateDesc(selectMode,envPtitles,year,regPquery, secPquery, regRSquery, regCquery, secCquery,queryData)
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

            #countryDataReady = (countryDataReady.replace("'", '"'))
            #call pieChart function
         #updata dictionary for filter options: form skeletons
            pieData.update({'modeForm':modeFormSet})

            pieData.update({'sourceData': sourceData})
            pieData.update({'countryDataReady': countryDataReady})
            pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
            notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
            #create select modes for fancyTree : so single select or multiple
            pieData.update({'mode_tree7': 2, 'warning_11':"",'yearDataReady': yearData})
            pieData.update({'session': "session"})
            pieData.update({'mode_tree4': 2, 'warning_8':"", "sectorOfProduction": secOfProduction})
            pieData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":productPurchased})
            pieData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":regOfProduction})
            pieData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":regOfProduction})
            pieData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":regOfProduction})
            #pieData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})

            #send signal for popup and default data
            popup = 1
            pieData.update({'popup': popup})
            pieData.update({'userSelectMode': "Contribution footprint of consumption split by sector where impact occurs"})

            pieData.update({'title':"Contribution footprint of consumption split by sector where impact occurs"})
            pieData.update({'userSelectMode': "Contribution footprint of consumption split by sector where impact occurs"})
            pieData.update({'graph':plotData})
            pieData.update({'description':table})
            pieData.update({'modeForm':modeFormSet})
            pieData.update({'title':selectMode})
            pieData.update({'titles': secPtitles})
            pieData.update({'plot': csvData})



        if selectMode == "Contribution footprint of consumption split by consuming region":
            plotType = "TimeSeries"

            #QUERY THE DATABASE
            plotData,csvData, queryData = queryhdf5(plotType,selectMode, envP, year, regPdata, secPdata,regRSdata, regCdata,secCdata, regCtitles, request)

            table = generateDesc(selectMode,envPtitles,year,regPquery, secPquery, regRSquery, regCquery, secCquery, queryData)
            pieData = {'graph':plotData}
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

            #countryDataReady = (countryDataReady.replace("'", '"'))
            #call pieChart function
         #updata dictionary for filter options: form skeletons
            pieData.update({'modeForm':modeFormSet})

            pieData.update({'sourceData': sourceData})
            pieData.update({'countryDataReady': countryDataReady})
            pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
            notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
            #create select modes for fancyTree : so single select or multiple
            pieData.update({'mode_tree7': 2, 'warning_11':"",'yearDataReady': yearData})

            pieData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction": sourceData})
            pieData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
            pieData.update({'mode_tree2': 2, 'warning_5':"","regionConsumng":regConsuming})
            pieData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady})
            pieData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady})
            #pieData.update({'warning': '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'})
            pieData.update({'session': "session"})
            popup = 1
            pieData.update({'popup': popup})
            pieData.update({'userSelectMode': "Contribution footprint of consumption split by consuming region"})
            pieData.update({'description':table})
            pieData.update({'modeForm':modeFormSet})
            pieData.update({'title':selectMode})

            pieData.update({'titles': regCtitles})
            pieData.update({'plot': csvData})


        #START MAKING PLOT DATA
        if selectMode == "Contribution footprint of consumption split by country where impact occurs":
            plotType = "TimeSeries"
            from collections import defaultdict
                 #QUERY THE DATABASE

            plotData,csvData, queryData = queryhdf5(plotType,selectMode, envP, year, regPdata, secPdata,regRSdata, regCdata,secCdata, regPtitles, request)
            from collections import defaultdict
            #sum the value if years and name are the same (timeseries query gives multiple values)
            c = defaultdict(int)
            for d in csvData:
                c[d['name']] += d['value']
            queryData = []

                #generate list for table
            for key, value in c.items():
                    #print(value)
                    seperate = (key.split("_"))
                    ayear = (seperate[0])

                    name = (seperate[1])
                    queryData.append(ayear+"_"+name+"_"+str(value))

            table = generateDesc(selectMode,envPtitles,year,regPquery, secPquery, regRSquery, regCquery, secCquery, queryData)

            sourceData = generateTrees(formTree)
            countryDataReady = generateTrees(formTreeCountry)
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


            #countryDataReady = (countryDataReady.replace("'", '"'))
            #call pieChart function
         #updata dictionary for filter options: form skeletons
            pieData.update({'modeForm':modeFormSet})
            pieData.update({'session': "session"})
            pieData.update({'sourceData': sourceData })
            pieData.update({'countryDataReady': countryDataReady})
            pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
            notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
            #create select modes for fancyTree : so single select or multiple
            pieData.update({'mode_tree7': 2, 'warning_11':"",'yearDataReady': yearData})

            pieData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
            pieData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
            pieData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady2})
            pieData.update({'mode_tree3': 2, 'warning_7':"","regionProducing":regProducing})
            pieData.update({'mode_tree6': 1, 'warning_10':notification,"regionSelling":countryDataReady2})
            #send signal for popup and default data

            pieData.update({'graph':plotData})
            pieData.update({'description':table})
            #modeFormSet = modes(initial={'selection': 'selectA'})
            pieData.update({'modeForm':modeFormSet})
            pieData.update({'title':selectMode})
            pieData.update({'userSelectMode': "Contribution footprint of consumption split by country where impact occurs"})

            pieData.update({'titles': regPtitles})
            pieData.update({'plot': csvData})
        if selectMode == "Contribution footprint of consumption split by region selling":
            plotType = "TimeSeries"
            from collections import defaultdict
                 #QUERY THE DATABASE

            plotData,csvData, queryData = queryhdf5(plotType,selectMode, envP, year, regPdata, secPdata,regRSdata, regCdata,secCdata, regRStitles, request)
            from collections import defaultdict
            #sum the value if years and name are the same (timeseries query gives multiple values)
            c = defaultdict(int)
            for d in csvData:
                c[d['name']] += d['value']
            queryData = []

                #generate list for table
            for key, value in c.items():
                    #print(value)
                    seperate = (key.split("_"))
                    ayear = (seperate[0])

                    name = (seperate[1])
                    queryData.append(ayear+"_"+name+"_"+str(value))

            table = generateDesc(selectMode,envPtitles,year,regPquery, secPquery, regRSquery, regCquery, secCquery, queryData)
            pieData = {'graph':plotData}
            pieData.update({'description':table})
            #modeFormSet = modes(initial={'selection': 'selectA'})
            pieData.update({'modeForm':modeFormSet})
            pieData.update({'title':selectMode})

            pieData.update({'titles': regRStitles})
            pieData.update({'plot': csvData})
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
            pieData.update({'modeForm':modeFormSet})
            pieData.update({'session': "session"})
            pieData.update({'sourceData': sourceData })
            pieData.update({'countryDataReady': countryDataReady})
            pieData.update({'substanceDataReady': generateTrees(formTreeSubstance)})
            notification = '<div class="alert alert-warning"><strong><span class="glyphicon glyphicon-alert" aria-hidden="true"></span></strong> Only single selection is possible, because of selected mode.</div>'
            #create select modes for fancyTree : so single select or multiple
            pieData.update({'mode_tree7': 2, 'warning_11':"",'yearDataReady': yearData})

            pieData.update({'mode_tree4': 1, 'warning_8':notification,"sectorOfProduction":sourceData})
            pieData.update({'mode_tree': 1, 'warning_6':notification,"productPurchased":sourceData})
            pieData.update({'mode_tree2': 1, 'warning_5':notification,"regionConsumng":countryDataReady2})
            pieData.update({'mode_tree3': 1, 'warning_7':notification,"regionProducing":countryDataReady2})
            pieData.update({'mode_tree6': 2, 'warning_10':"","regionSelling":regProducing})
            #send signal for popup and default data
            popup = 1
            pieData.update({'popup': popup})

            pieData.update({'userSelectMode': "Contribution footprint of consumption split by region selling"})
    else:
        pieData.update({'desc': '<div class="alert alert-info"><h2><span class="glyphicon glyphicon-arrow-up" aria-hidden="true"></span></H2><strong><span class="glyphicon glyphicon-info-sign" aria-hidden="true"></span>  Select your mode in the navigation bar.</strong></div>' })



    """
    lineChart page

    start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)
    nb_element = 150
    xdata = range(nb_element)
    xdata = list(map(lambda x: start_time + x * 1000000000, xdata))
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = list(map(lambda x: x * 2, ydata))

    tooltip_date = "%d %b %Y %H:%M:%S %p"
    extra_serie1 = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "date_format": tooltip_date,
    }
    extra_serie2 = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "date_format": tooltip_date,
    }
    chartdata = {'x': xdata,
        'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie1, 'kwargs1': { 'color': '#778899' },
        'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie2, 'kwargs2': { 'color': '#b22121' },
    }

    charttype = "lineChart"
    chartcontainer = 'linechart_container'  # container name
    data = {
        'charttype2': charttype,
        'chartdata2': chartdata,
        'chartcontainer2': chartcontainer,
        'extra2': {
            'x_is_date': True,
            'x_axis_format': '%d %b %Y %H',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }}
        """
    return render(request,"ExioVisuals/timeseries.html", pieData)







#-------------------------------------Retrieving data
def retrieveData():
    #below:get specific values (for filtering)
        #countryNames = GhgEmissions.objects.get(code='WM')
        #below: retrieve all absolute emissions
        absData = GhgEmissions.objects.all().values_list('absolute', flat=True)
        #below: retrieve all countrynames
        countryNames = GhgEmissions.objects.all().values_list('label', flat=True)

        #query all objects
        t = GhgEmissions.objects.all().values_list()
        #remove region data
        pre = list(t)
        #print(pre)
        #print("bla")
        '''
        pre.pop(-1)
        pre.pop(-1)
        pre.pop(-1)
        pre.pop(-1)
        pre.pop(-1)
        '''
        countryNames =[]
        absData = []
        for x in pre:
            countryNames.append(x[1])
            absData.append(x[3])


        #now map the data

        xdata = countryNames
        ydata = absData
        return xdata,ydata
def defaultData(plotType,selectMode, request):
    if plotType == "PieChart" and selectMode == "Contribution footprint of consumption split by consumed product category":
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
    if plotType == "PieChart" and selectMode == "Contribution footprint of consumption split by sector where impact occurs":
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
    if plotType == "PieChart" and selectMode == "Contribution footprint of consumption split by consuming region":
        #call queryHDF5 function with standard input


        #as regC is the exception for querying we need to pass all ids
        id = Country.objects.values_list('id', flat=True)
        locals = []
        names = []
        for x in id:
            #gather the lws_level only
            lvlCondition = Country.objects.values_list('lwst_level', flat=True).get(pk=x)
            if lvlCondition == True:
                local = Country.objects.values_list('id', flat=True).get(pk=x)
                local = int(local)
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                names.append(name)
                locals.append(local)

        plotData,secPtitles, queryData = queryhdf5(plotType,selectMode, "", 2011, [0], [0] ,[0], locals,[0], names, request)

        return secPtitles, plotData
    if plotType == "PieChart" and selectMode == "Contribution footprint of consumption split by country where impact occurs":
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
    if plotType == "PieChart" and selectMode == "Contribution footprint of consumption split by region selling":
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
    if plotType == "TimeSeries" and selectMode == "Contribution footprint of consumption split by consumed product category":
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


        plotData,csvData, queryData = queryhdf5(plotType,selectMode, "",  ["2000","2001","2002","2003","2004","2005", "2006","2007", "2008", "2009", "2010",  "2011"], [0], [0] ,[0], [1],secCdata2, secCtitlesReady, request)

        return csvData, plotData
    #plotType,selectMode, envP, year, regP, secP,regRS, regC,secC, plotDatatitles, request
    if plotType == "TimeSeries" and selectMode == "Contribution footprint of consumption split by sector where impact occurs":
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
                #secCtitlesReady.append(secC)
                #secCdata.append(str(x-1)+secC)




        plotData,secPtitles, queryData = queryhdf5(plotType,selectMode, "",  ["2000","2001","2002","2003","2004","2005", "2006","2007", "2008", "2009", "2010",  "2011"], [0], secPdata2 ,[0], [1],[0], secPtitlesReady, request)

        return secPtitles, plotData
    #plotType,selectMode, envP, year, regP, secP,regRS, regC,secC, plotDatatitles, request
    if plotType == "TimeSeries" and selectMode == "Contribution footprint of consumption split by consuming region":
        #call queryHDF5 function with standard input

        id = Country.objects.values_list('id', flat=True)


        lvls = Country.objects.values_list('lvl', flat=True)
        lwst_level = 2
        regCdata = []
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
                #secCtitlesReady.append(secC)
                #secCdata.append(str(x-1)+secC)




        plotData,regPtitles, queryData = queryhdf5(plotType,selectMode, "", ["2000","2001","2002","2003","2004","2005", "2006","2007", "2008", "2009", "2010",  "2011"], [0], [0],[0], regCdata2,[0], regCtitlesReady, request)

        return regPtitles, plotData
    if plotType == "TimeSeries" and selectMode == "Contribution footprint of consumption split by country where impact occurs":
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
                #secCtitlesReady.append(secC)
                #secCdata.append(str(x-1)+secC)




        plotData,regPtitles, queryData = queryhdf5(plotType,selectMode, "", ["2000","2001","2002","2003","2004","2005", "2006","2007", "2008", "2009", "2010",  "2011"], regPdata2, [0],[0], [1],[0], regPtitlesReady, request)

        return regPtitles, plotData
    if plotType == "TimeSeries" and selectMode == "Contribution footprint of consumption split by region selling":
        #call queryHDF5 function with standard input
        id = Country.objects.values_list('id', flat=True)


        lvls = Country.objects.values_list('lvl', flat=True)
        #lwst_level = max(lvls)
        lwst_level = 2
        regRSdata = []
        regRSdata2 = []
        regRStitlesReady = []
        for x in id:
            lvl = Country.objects.values_list('lvl', flat=True).get(pk=x)

            #print(lwst_level)
        # if lowest level get the name and id
            if lwst_level == int(lvl):
                print("FDsg")
                name = Country.objects.values_list('name', flat=True).get(pk=x)
                print(name)
                if len(name) > 25:
                    regRStitlesReady.append(name[:40])
                else:
                    regRStitlesReady.append(name)

                regRSdata2.append(x-1)
                #secCtitlesReady.append(secC)
                #secCdata.append(str(x-1)+secC)



        plotData,regPtitles, queryData = queryhdf5(plotType,selectMode, "", ["2000","2001","2002","2003","2004","2005", "2006","2007", "2008", "2009", "2010",  "2011"], [0], [0],regRSdata2, [1],[0], regRStitlesReady, request)

        return regPtitles, plotData
#--------------------------------------Visual Analytics library
def pieChart(vLabel,vData, vTitle, vDescr):

    piechartdata = []
    for x, y in zip(vLabel,vData):
        piechartdata.append({"value": y, "name": x})

    chartdata = {'x': vLabel, 'y': vData}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'
    pieData = {'pieChartData':piechartdata, 'title' : vTitle,'description': vDescr}






    return pieData

def timeSeries(vLabel,vData):
    print("is this working?")
    vData = [ int(x) for x in vData ]
    data = []

    for x, y in zip(vData, vLabel):
        data.append({"year": y, "name":"selected products and sectors", "value": x},)


    return data




def test(request):
	form = ProductSelectionForm(request.POST or None)
	print("you are here ")
	if request.method == "POST":
		if form.is_valid():
			print("you are here 3")

			subject = form.cleaned_data['categories']
			test = subject.values_list('url', flat=True)
			print(test)



	return render(request, "ExioVisuals/test.html", {'form': form})

def redirectView(request):
    MemberFormSet = formset_factory(wraps(reloadForm)(partial(reloadForm)))
    formTree = ProductSelectionForm(request.POST or None)
    if request.method == 'POST':
         #as I use formsets this is mandatory
        formset = MemberFormSet(request.POST)
        #make sure every form is validMemberFormSet = formset_factory(wraps(PostFormEFactor)(partial(PostFormEFactor)))
        if formset.is_valid():
            #start retrieving formset data, which is all filter data except FancyTree
            for f in formset:
                cd = f.cleaned_data

                print("selection:")
                selection = cd.get('selection')
                print(selection)
                #

                #start getting some form skeletons now!
                ArticleFormSet = formset_factory(PostFormEFactor)
                formset = ArticleFormSet()
                formset = formset_factory(wraps(PostFormEFactor)(partial(PostFormEFactor)), extra=1)
                #updata dictionary for filter options: form skeletons

                selectionForm = formset_factory(wraps(reloadForm)(partial(reloadForm)), extra=1)
                dict = ({'selectionForm': selectionForm})
                #now send some other forms to the filter interface
                dict.update({'formset':formset})
                dict.update({'formTree': formTree})
                #send signal for popup
                popup = 1
                dict.update({'popup': popup})
                return render(request,"ExioVisuals/distribution.html", dict)


def ajax(request):
    if request.method == 'POST':
        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
        if request.is_ajax():
            #Always use get on request.POST. Correct way of querying a QueryDict.
            email = request.POST.get('email')
            password = request.POST.get('password')
            data = {"email":email , "password" : password}
            #Returning same data back to browser.It is not possible with Normal submit
            return JsonResponse(data)
    return render(request, "ExioVisuals/ajax.html")


def queryhdf5(plotType,selectMode, envP, year, regP, secP,regRS, regC,secC, plotDatatitles, request):
    print("query function reached")
    #determine plottype as it affects the query and determine the mode that we are in
    if plotType == "PieChart" and selectMode == "Contribution footprint of consumption split by country where impact occurs":
        #as it is piechart we only select one year
        print("Query is: ")
        #print("regP"+str(regP[0])+"secP"+str(secP[0])+"regRS"+str(regRS[0])+"regC"+str(regC[0])+"secC"+str(secC[0]))
        #we have the title list and the actual data points , both needs to be sorted for the query to hdf5 according to the data points
        regPadjusted = [ int(x) for x in regP ]
        points = zip(regPadjusted,plotDatatitles)
        pack = (sorted(points))
        regPadjusted = [point[0] for point in pack]
        plotDatatitles = [point[1] for point in pack]

        #regPadjusted = sorted(regPadjusted, key=int)
        regC = [int(x) for x in regC]
        secP = [int(x) for x in secP]
        regRS = [int(x) for x in regRS]
        secC = [int(x) for x in secC]

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

        outputDataReady = []
        #check the number of values to plot for the piechart LIMIT IS 20
        if len(outputData) > 19:
            # gather all values above 20 > this is going to be merged
            others = outputData[19:]
            #sum those
            others= sum(others)
            #get first twenty values and titles
            outputDataReady = outputData[:19]
            outputDataReady.append(others)
            plotDatatitles = plotDatatitles[:19]
            plotDatatitles.append("Other")
        else:#not needed but for transparancy
            outputDataReady = outputData
            plotDatatitles = plotDatatitles


        t = (zip(package,outputData))

        #print(others)
        print(outputDataReady)
        return outputDataReady, plotDatatitles, t
    #determine plottype as it affects the query and determine the mode that we are in
    if plotType == "PieChart" and selectMode == "Contribution footprint of consumption split by sector where impact occurs":
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

        outputDataReady = []
        #check the number of values to plot for the piechart LIMIT IS 20
        if len(outputData) > 19:
            # gather all values above 20 > this is going to be merged
            others = outputData[19:]
            #sum those
            others= sum(others)
            #get first twenty values and titles
            outputDataReady = outputData[:19]
            outputDataReady.append(others)
            plotDatatitles = plotDatatitles[:19]
            plotDatatitles.append("Other")
        else:#not needed but for transparancy
            outputDataReady = outputData
            plotDatatitles = plotDatatitles


        t = (zip(package,outputData))

        #print(others)
        print(outputDataReady)
        return outputDataReady, plotDatatitles, t

    #determine plottype as it affects the query and determine the mode that we are in
    if plotType == "PieChart" and selectMode == "Contribution footprint of consumption split by consumed product category":
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
            outputDataReady = []
            #check the number of values to plot for the piechart LIMIT IS 20
            if len(outputData) > 19:
                # gather all values above 20 > this is going to be merged
                others = outputData[19:]
                #sum those
                others= sum(others)
                #get first twenty values and titles
                outputDataReady = outputData[:19]
                outputDataReady.append(others)
                plotDatatitles = plotDatatitles[:19]
                plotDatatitles.append("Other")
            else:#not needed but for transparancy
                outputDataReady = outputData
                plotDatatitles = plotDatatitles



            t = (zip(package,outputData))

            #print(others)
            print(outputDataReady)
            return outputDataReady, plotDatatitles, t
    #determine plottype as it affects the query and determine the mode that we are in
    if plotType == "PieChart" and selectMode == "Contribution footprint of consumption split by consuming region":
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

            outputDataReady = []
            #check the number of values to plot for the piechart LIMIT IS 20
            if len(outputData) > 19:
                # gather all values above 20 > this is going to be merged
                others = outputData[19:]
                #sum those
                others= sum(others)
                #get first twenty values and titles
                outputDataReady = outputData[:19]
                outputDataReady.append(others)
                plotDatatitles = plotDatatitles[:19]
                plotDatatitles.append("Other")
            else:#not needed but for transparancy
                outputDataReady = outputData
                plotDatatitles = plotDatatitles


            t = (zip(package,outputData))

            #print(others)
            print(outputDataReady)
            return outputDataReady, plotDatatitles, t
    if plotType == "PieChart" and selectMode == "Contribution footprint of consumption split by region selling":
        #as it is piechart we only select one year
        print("Query is: ")
        #print("regP"+str(regP[0])+"secP"+str(secP[0])+"regRS"+str(regRS[0])+"regC"+str(regC[0])+"secC"+str(secC[0]))
        #we have the title list and the actual data points , both needs to be sorted for the query to hdf5 according to the data points
        regRSadjusted = [ int(x) for x in regRS ]
        points = zip(regRSadjusted,plotDatatitles)
        pack = (sorted(points))
        regRSadjusted = [point[0] for point in pack]
        plotDatatitles = [point[1] for point in pack]

        #regPadjusted = sorted(regPadjusted, key=int)
        regC = [int(x) for x in regC]
        secP = [int(x) for x in secP]

        secC = [int(x) for x in secC]

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

        outputDataReady = []
        #check the number of values to plot for the piechart LIMIT IS 20
        if len(outputData) > 19:
            # gather all values above 20 > this is going to be merged
            others = outputData[19:]
            #sum those
            others= sum(others)
            #get first twenty values and titles
            outputDataReady = outputData[:19]
            outputDataReady.append(others)
            plotDatatitles = plotDatatitles[:19]
            plotDatatitles.append("Other")
        else:#not needed but for transparancy
            outputDataReady = outputData
            plotDatatitles = plotDatatitles


        t = (zip(package,outputData))

        #print(others)
        print(outputDataReady)
        return outputDataReady, plotDatatitles, t
    #determine plottype as it affects the query and determine the mode that we are in
    if plotType == "TimeSeries" and selectMode == "Contribution footprint of consumption split by sector where impact occurs":


        data = []
        secPadjusted = [ int(x) for x in secP ]
        points = zip(secPadjusted,plotDatatitles)
        pack = (sorted(points))
        secPadjusted = [point[0] for point in pack]
        plotDatatitles = [point[1] for point in pack]

        data = []
        testa = []
        plottableData =[]
        print("ok?")
        #print(secPadjusted)
        csvData = []
        for i,x in enumerate(year):

            #with h5py.File('/home/sidney/datahdf5/experiments/{0}_combined.hdf5'.format(x) ,'r')as hf:
            with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(x) ,'r')as hf:
                for y in regC:
                    test = (hf.get('region{0}'.format(y)))
                    tmp = test[int(regP[0]),secPadjusted,int(regRS[0]),int(secC[0])]
                #for each year we have tmp now

                    data.append(str(tmp)+str(y))
                    tmp = tmp.tolist()
                    t = (zip(pack,tmp))

                    print("year")
                    years = x

                    #testa.append(x)
                #since the order of de x data en y data are the same (and aligned) we can use the length to retrieve specific data
                    testa.append(x)
                    testa.append(tmp)
                    testa.append(list(t))


                    for z,y in enumerate(plotDatatitles):

                        entries = {"year": years, "name":y, "value": tmp[z]}
                        plottableData.append(entries)
                        csvData.append({"name": years+"_"+y, "value": int(tmp[z])})
                #testa.append(plotDatatitles[i])

        #print(testa[1])
        #print("ok")

        return plottableData, csvData, testa

            #determine plottype as it affects the query and determine the mode that we are in
    if plotType == "TimeSeries" and selectMode == "Contribution footprint of consumption split by consumed product category":
        print(" we are here")
        #we have the title list and the actual data points , both needs to be sorted for the query to hdf5 according to the data points
        secCadjusted = [ int(x) for x in secC ]
        points = zip(secCadjusted,plotDatatitles)
        pack = (sorted(points))
        secCadjusted = [point[0] for point in pack]
        plotDatatitles = [point[1] for point in pack]

        data = []
        testa = []
        plottableData =[]
        csvData = []
        for i,x in enumerate(year):

            #with h5py.File('/home/sidney/datahdf5/experiments/{0}_combined.hdf5'.format(x) ,'r')as hf:
            with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(x) ,'r')as hf:
                for y in regC:
                    test = (hf.get('region{0}'.format(y)))
                    tmp = test[int(regP[0]),int(secP[0]),int(regRS[0]),secCadjusted]
                #for each year we have tmp now

                    data.append(str(tmp)+x)
                    tmp = tmp.tolist()
                    t = (zip(pack,tmp))
                    #print(list(t))
                    #print(pack[i])
                    #testa.append(t)
                    #print(list(t))
                    #print(tmp)
                    #print(secPadjusted[i])
                    #year
                    print("year")
                    years = x

                    #testa.append(x)
                #since the order of de x data en y data are the same (and aligned) we can use the length to retrieve specific data
                    testa.append(x)
                    testa.append(tmp)
                    testa.append(list(t))

                    for z,y in enumerate(plotDatatitles):
                        entries = {"year": years, "name":y, "value": tmp[z]}
                        plottableData.append(entries)
                        csvData.append({"name": years+"_"+y, "value": int(tmp[z])})
        return plottableData, csvData, testa
    if plotType == "TimeSeries" and selectMode == "Contribution footprint of consumption split by consuming region":
        print(" we are here*")

        testa = []
        plottableData =[]
        csvData = []
        for i,x in enumerate(year):

            #with h5py.File('/home/sidney/datahdf5/experiments/{0}_combined.hdf5'.format(x) ,'r')as hf:
            with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(x) ,'r')as hf:
            #with h5py.File('/home/chai/data/experiments/{0}_combined.hdf5'.format(year) ,'r')as hf:

            #retrieve the data for each region of consumption and append to data variable
                for z, regions in enumerate(regC):
                    test = (hf.get('region{0}'.format(int(regions))))
                    tmp = test[int(regP[0]),int(secP[0]),int(regRS[0]),int(secC[0])]
                    tmp = tmp.tolist()
                    print(x)
                    #testa.append(years)
                    testa.append(regions)
                    #print(regions)

                    #print(tmp)
                    #print("we are in year:")
                    #print(x)

                    #print(plotDatatitles)
                    #print(plotDatatitles)
                    testa.append(x)
                    testa.append(tmp)
                    testa.append(plotDatatitles[z])

                    entries = {"year": x, "name":plotDatatitles[z], "value": tmp}
                    plottableData.append(entries)
                    csvData.append({"name": x+"_"+plotDatatitles[z], "value": int(tmp)})



        return plottableData, None, testa
    if plotType == "TimeSeries" and selectMode == "Contribution footprint of consumption split by country where impact occurs":
        print(" we are here")
        #we have the title list and the actual data points , both needs to be sorted for the query to hdf5 according to the data points
        #we have the title list and the actual data points , both needs to be sorted for the query to hdf5 according to the data points
        regPadjusted = [ int(x) for x in regP ]
        points = zip(regPadjusted,plotDatatitles)
        pack = (sorted(points))
        regPadjusted = [point[0] for point in pack]
        plotDatatitles = [point[1] for point in pack]


        data = []
        testa = []
        plottableData =[]
        csvData = []
        for i,x in enumerate(year):

            #with h5py.File('/home/sidney/datahdf5/experiments/{0}_combined.hdf5'.format(x) ,'r')as hf:
            with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(x) ,'r')as hf:
                for y in regC:
                    test = (hf.get('region{0}'.format(y)))
                    tmp = test[regPadjusted,int(secP[0]),int(regRS[0]),int(secC[0])]
                #for each year we have tmp now

                    data.append(str(tmp)+x)
                    tmp = tmp.tolist()
                    t = (zip(pack,tmp))


                    years = x
                    print("year: "+years)
                    #testa.append(x)
                #since the order of de x data en y data are the same (and aligned) we can use the length to retrieve specific data
                    testa.append(x)
                    testa.append(tmp)
                    testa.append(list(t))

                    for z,y in enumerate(plotDatatitles):
                        entries = {"year": years, "name":y, "value": tmp[z]}
                        plottableData.append(entries)
                        csvData.append({"name": years+"_"+y, "value": int(tmp[z])})

        return plottableData, csvData, testa
    if plotType == "TimeSeries" and selectMode == "Contribution footprint of consumption split by region selling":
        print(" we are here")
        #we have the title list and the actual data points , both needs to be sorted for the query to hdf5 according to the data points
        #we have the title list and the actual data points , both needs to be sorted for the query to hdf5 according to the data points
        regRSadjusted = [ int(x) for x in regRS ]
        points = zip(regRSadjusted,plotDatatitles)
        pack = (sorted(points))
        regRSadjusted = [point[0] for point in pack]
        plotDatatitles = [point[1] for point in pack]


        data = []
        testa = []
        plottableData =[]
        csvData = []
        for i,x in enumerate(year):

            #with h5py.File('/home/sidney/datahdf5/experiments/{0}_combined.hdf5'.format(x) ,'r')as hf:
            with h5py.File(PATH_HDF5+'{0}_combined.hdf5'.format(x) ,'r')as hf:
                for y in regC:
                    test = (hf.get('region{0}'.format(y)))
                    tmp = test[int(regP[0]),int(secP[0]),regRSadjusted,int(secC[0])]
                #for each year we have tmp now

                    data.append(str(tmp)+x)
                    tmp = tmp.tolist()
                    t = (zip(pack,tmp))


                    years = x
                    print("year: "+years)
                    #testa.append(x)
                #since the order of de x data en y data are the same (and aligned) we can use the length to retrieve specific data
                    testa.append(x)
                    testa.append(tmp)
                    testa.append(list(t))

                    for z,y in enumerate(plotDatatitles):
                        entries = {"year": years, "name":y, "value": tmp[z]}
                        plottableData.append(entries)
                        csvData.append({"name": years+"_"+y, "value": int(tmp[z])})

        return plottableData, csvData, testa


def generateDesc(selectMode,envPtitles,year,plotDataTitles, secPtitles, regRStitles, regCtitles, secCtitles, queryData):
    head = '<div class="container" ><table class="table table-hover" ><thead><tr><th class="col-sm-0.5">Type </th><th class="col-sm-0.5">Query</th></tr></thead>'

    body = '<tbody><tr><td>Select mode</td><td>{0}</td></tr><tr><td>Environmental pressure</td><td> {1}</td> </tr><tr><td>Year</td><td>{2} </td> </tr><tr><td>Region of production </td><td>{3} </td> </tr><tr><td> Sector of production</td><td>{4} </td> </tr><tr><td>Region selling</td><td>{5} </td> </tr><tr><td>Region of consumption </td><td>{6} </td> </tr><tr><td>Sector of consumption </td><td>{7} </td> </tr><tr><td>Result data </td><td>{8} </td> </tr></tbody></table></div>'.format(selectMode,envPtitles,year,plotDataTitles, secPtitles, regRStitles, regCtitles, secCtitles, list(queryData))
    table = head + body
    return table


def info(request):

    return render(request,'ExioVisuals/infobutton.html')


