# Core
The CML Django-based platform includes development & showcase applications. 
The initial idea for this platform is to visualize, share IE/CML-wide data. This vision emerged some years ago and a large proportion of the current code-base dates back to 2016.
Thus bare in mind that many of the "Django apps" are outdated prototype code bases. In view of potential further development parts are currently being updated.

# Overview of apps and folders
* CMLMasterProject: the core of the platform.
* CMS (app - Unused): A Wagtail content management system for databases and project overviews. It can potentially also include a blog.
* PUMA (app): An app visualizing material resources embedded in objects in Amsterdam.
* ExioVisuals (app - Deprecated): Visualises ExioBase data. This tool has been surpassed by the developments of the Rama-Scene project see: https://www.ramascene.eu/. 
If you still wish to launch ExioVisuals, see description below.
* MicroVis: (app): An application to showcase interactive visuals related to small project results.
* data:  all data used for MicroVis.
* static, templates: general Django folders.

# General info on server (Ronin)
Ronin hosts at the moment (July 2019) the core platform deployed with Apache. We use the subdomain "cml.liacs.nl" from Liacs (https://liacs.leidenuniv.nl/). Another Django application called CircuMat is running 
on port 8080 deployed with Nginx (via supervisord). CircuMat is based on Rama-scene see https://bitbucket.org/CML-IE/rama-scene/src/master/ for more info.

# Getting started
As mentioned the platform still uses outdated code, at this point in time we don't recommend starting the platform until the platform is updated. If you wish to start the platform locally follow descriptions below.

# Starting Exiovisuals (first step)
As mentioned ExioVisuals is deprecated and we do not necessarily recommend starting this application. 
The data (2011) used for Exiovisuals can be found here: https://sidneyniccolson.stackstorage.com/s/GC5lbo4KlSsSYM7. It is an HDF5 database constructed with the Python script "final_built_26-08-16.py".
In the platform settings.py you can see an entry called PATH_HDF5, fill the correct path to your local location of the exiovis HDF5 database.
For Django migrations in case you cannot use the shipped sqlite db, ExioVisuals could cause failures related to tables being unavailable. As a workaround follow the steps below:
* Temporarily delete the contents of forms.py, views_a, views_b, views_c, views_d. Store them somewhere safe. 
* In ExioVisuals/urls.py outcomment the urls and incomment the <# url(r'^$', views.ExioVisuals, name='ExioVisuals')>
* Run: python manage.py makemigrations
* Run: python manage.py migrate
* Restore all outcommented and removed file contents.
* Run: python final_countryTree_exiovisuals_populate.py
* Run: python final_productTree_exiovisuals_populate.py 
* Run: python yearsPopulate.py 
* Run: python manage.py collectstatic
Finally python manage.py runserver and go to http://127.0.0.1:8000/exiovisuals/

# Starting MicroVis and PUMA 
With the runserver command used for exiovisuals you can now visit MicroVis and PUMA:
* PUMA: http://127.0.0.1:8000/puma/
* MicroVis: http://127.0.0.1:8000/research/microvis/