# Core
The CML Django-based platform includes development & showcase applications. 
The initial idea for this platform is to visualize, share IE/CML-wide data. This vision emerged some years ago and a large proportion of the current code-base dates back to 2016.
Thus bare in mind that some of the "Django apps" are outdated prototype code bases. In view of potential further development parts are currently being updated.

# Overview of apps and folders
* CMLMasterProject: the core of the platform.
* CMS (app - Unused): A Wagtail content management system for databases and project overviews. It can potentially also include a blog.
* PUMA (app): An app visualizing material resources embedded in objects in Amsterdam.
* MicroVis: (app): An application to showcase interactive visuals related to small project results.
* data:  all data used for MicroVis.
* static, templates: general Django folders.

# General info on server (Ronin)
Ronin hosts at the moment (July 2019) the core platform deployed with Apache. We use the subdomain "cml.liacs.nl" from Liacs (https://liacs.leidenuniv.nl/). Another Django application called CircuMat is running 
on port 8080 deployed with Nginx (via supervisord). CircuMat is based on Rama-scene see https://bitbucket.org/CML-IE/rama-scene/src/master/ for more info.

# Getting started
Pull the repository to your local computer.
```
$ git clone https://github.com/Polariks/polariks_proto_ndvi.git
```
Install requirement.txt in a Python3.x virtual environment:
```
$ pip install -r requirements.txt 
```
Apply database migrations:
```
$ python manage.py makemigrations
$ python manage.py migrate
```
Run the development server:
```
$ python manage.py runserver
```




# Starting MicroVis and PUMA 
With the runserver command used you can now visit MicroVis and PUMA:
* PUMA: http://127.0.0.1:8000/puma/
* MicroVis: http://127.0.0.1:8000/research/microvis/