# Core
The CML Django-based platform includes development & showcase applications. 
The initial idea for this platform is to visualize, share IE/CML-wide data. This vision emerged some years ago and a large proportion of the current code-base dates back to 2016.
Thus bare in mind that some of the "Django apps" are outdated prototype code bases. In view of potential further development parts are currently being updated.

# Overview of apps and folders
* CMLMasterProject: the core of the platform.
* CMS (app - Unused): A Wagtail content management system for databases and project overviews. It can potentially also include a blog.
* PUMA (app): An app visualizing material resources embedded in objects in Amsterdam.
* ExioVisuals (app - Deprecated): Visualises ExioBase data. This tool has been surpassed by the development of Rama-Scene see: https://www.ramascene.eu/. If you still wish to launch ExioVisuals, see the branch "last-exiovisuals-support".
* MicroVis (app): An application to showcase interactive visuals related to small project results.
* CircuMat (app): CircuMat is a modified (forked) version of Rama-Scene EIT Raw Materials project related to analyzing Environmentally Extended Input-Output (EEIO) tables. CircuMat focuses on NUTS2 level classification as opposed to Rama-Scene country level analysis tool.
* data:  all data used for MicroVis.
* static, templates: general Django folders.

# General info on server (Ronin)
Ronin hosts at the moment (August 2019) the core platform which is deployed with Nginx and supervisord. We use the subdomain "cml.liacs.nl" from Liacs (https://liacs.leidenuniv.nl/).
Bare in mind that due to the integration of CircuMat the platform runs on Asgi instead of Wsgi. If you wish to run the platform without circumat use the branch "core-without-circumat".

# Getting started
Pull the repository to your local computer.
```
$ git clone https://github.com/CMLPlatform/Core.git
```
Install requirement.txt in a Python3.x virtual environment:
```
$ pip install -r requirements.txt 
```
Apply database migrations:
```
$ python manage.py makemigrations {CMLMasterProject,PUMA,panorama,CMS,MicroVis,circumat}
$ python manage.py migrate
```
Run the development server:
```
$ python manage.py runserver -settings=CMLMasterProject.config.dev
```


# Starting MicroVis and PUMA 
With the runserver command used you can now visit MicroVis and PUMA:
* PUMA: http://127.0.0.1:8000/puma/
* MicroVis: http://127.0.0.1:8000/research/microvis/

# Starting CircuMat
Follow the link below:

[starting circumat](README_circumat.md)