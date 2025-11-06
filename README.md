
# dev logs

- This branch is coming from https://github.com/ProgramIsFun/graphPythonBackend11/tree/master.  I basically take one folder of that branch and then make it azure compatible in this branch
- 14/8/25  https://github.com/ProgramIsFun/EonGraph-Backend/commit/37f857deae2675eb9153f7b508015466da0b752a  Changed the old library to normal flask

# how to develop

you modify ipynb files and then convert them to python files using nbconvert.

1. 

pip install nbconvert

2.

jupyter nbconvert example.ipynb --to python

# how to run this code

1. 

Install a virtual environment possibly using the VS code

2. 

pip install -r requirements.txt

3. 

set FLASK_APP=app.py
set FLASK_ENV=development

4.

flask run


ref : 

https://learn.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-cli%2Cazure-cli-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli



# how to deploy this code
1. azure app service

use website to create a free service 

2. deploy 

using vs code extension right click on the created service, deploy to web app...

3. to add env to service

az config set core.enable_broker_on_windows=false

az login 

az webapp config appsettings set --name <AppServiceName> --resource-group <ResourceGroupName> --settings MY_VARIABLE=MyValue


# principles in neo4j

It is recommended to use a user-generated ID in Neo4j for robust and portable node identification.

should it named id?

Short Answer:
It’s better not to name your user-generated ID simply id. Instead, use a more descriptive property name (like userId, uuid, productId, etc.).

Why Not Just id?
Neo4j already has an internal node identifier that can be accessed using the id() function.
Naming your property id can cause confusion, especially for new users or when reading Cypher queries.
Explicit and descriptive naming helps maintain readability and prevents accidental mix-ups between your property and Neo4j’s built-in identifier.

So when writing the code, I assume some user-generated ID will be used. These are useful when editing the graph.

MATCH (p:Person {user_id: 123}), (m:Movie {movie_id: 567})
CREATE (p)-[:LIKES]->(m)

# below is the original readme from the original repo

# Deploy a Python (Flask) web app to Azure App Service - Sample Application

This is the sample Flask application for the Azure Quickstart [Deploy a Python (Django or Flask) web app to Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python). For instructions on how to create the Azure resources and deploy the application to Azure, refer to the Quickstart article.

Sample applications are available for the other frameworks here:

* Django [https://github.com/Azure-Samples/msdocs-python-django-webapp-quickstart](https://github.com/Azure-Samples/msdocs-python-django-webapp-quickstart)
* FastAPI [https://github.com/Azure-Samples/msdocs-python-fastapi-webapp-quickstart](https://github.com/Azure-Samples/msdocs-python-fastapi-webapp-quickstart)

If you need an Azure account, you can [create one for free](https://azure.microsoft.com/en-us/free/).
