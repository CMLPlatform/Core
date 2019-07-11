import os
import sys
import django
#stuff for newer django !





#interface
yearsList = [
        "2011"
            ];



def populate():
    add_parent(1, "Total", str(yearsList))
	#below an example to fill in 1 entry
	#add_data("America", "US", 80.5)

    for i,x in enumerate(yearsList):
        id = i + 2
        year = x
        add_child(YearF.objects.get(id=1),id,year, year)
        print(year)


#function that adds the data (offcourse)
#function that adds the data (offcourse)
def add_child(parent, id, name, slug):
    e, created = YearF.objects.get_or_create(parent=parent, id=id, name=name, slug=slug)

    return e

def add_parent(id,name, url):
    e, created = YearF.objects.get_or_create(id=id,name=name, url=url)

    return e

# Start execution here!
if __name__ == '__main__':
    print ("Starting CMLMasterProject population script...")
	
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CMLMasterProject.settings')
    django.setup()
    from ExioVisuals.models import YearF
    populate()
