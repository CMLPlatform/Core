from django.shortcuts import render
#this is the first page of the Web-app
def homePage(request):


    #return render_to_response('/IEMasterProject/HomePage.html', context_dict, context)
    return render(request,'CMLMasterProject/HomePage.html')

def visuals(request):
    return render(request, 'CMLMasterProject/visuals.html')