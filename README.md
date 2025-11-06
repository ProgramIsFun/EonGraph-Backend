
# dev logs

This branch is coming from https://github.com/ProgramIsFun/graphPythonBackend11/tree/master.  

I basically take one folder of that branch and then make it azure compatible in this branch

# how to develop 

you modify ipynb files and then convert them to python files using nbconvert.

pip install nbconvert
jupyter nbconvert example.ipynb --to python

# how to run this code

Install a virtual environment possibly using the VS code

pip install -r requirements.txt

set FLASK_APP=app.py
set FLASK_ENV=development

flask run

https://learn.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-cli%2Cazure-cli-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli

# how to deploy this code

I suggest using vs code extension

# below is the original readme from the original repo

# Deploy a Python (Flask) web app to Azure App Service - Sample Application

This is the sample Flask application for the Azure Quickstart [Deploy a Python (Django or Flask) web app to Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python). For instructions on how to create the Azure resources and deploy the application to Azure, refer to the Quickstart article.

Sample applications are available for the other frameworks here:

* Django [https://github.com/Azure-Samples/msdocs-python-django-webapp-quickstart](https://github.com/Azure-Samples/msdocs-python-django-webapp-quickstart)
* FastAPI [https://github.com/Azure-Samples/msdocs-python-fastapi-webapp-quickstart](https://github.com/Azure-Samples/msdocs-python-fastapi-webapp-quickstart)

If you need an Azure account, you can [create one for free](https://azure.microsoft.com/en-us/free/).
