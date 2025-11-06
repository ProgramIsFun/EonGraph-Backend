# Table of Contents

- [🏃‍♂️ How to Run](#how-to-run)
- [🚀 Development cycle](#development-cycle)
- [🌍 How to Deploy](#how-to-deploy)
  - [1. Create App Service](#1-create-app-service)
  - [2. Deploy from VS Code](#2-deploy-from-vs-code)
  - [3. Add Environment Variables (e.g., for secrets)](#3-add-environment-variables-eg-for-secrets)
- [dev logs](#dev-logs)
- [references](#references)


## How to Run

Set up your local environment to run the application.

| Step | Command                                                         | Description                            |
|------|-----------------------------------------------------------------|----------------------------------------|
| 1    | _Create and activate a virtual environment (e.g., via VS Code)_ | Isolate project dependencies          |
| 2    | `pip install -r requirements.txt`                               | Install dependencies                   |
| 3    | `set FLASK_APP=app.py`      `set FLASK_ENV=development`    | Set Flask environment variables        |
| 4    | `flask run --port=5007`                                         | Start the Flask development server     |

## Development cycle

For easier development

| Step | Command                                               | Description                       |
|------|------------------------------------------------------|-----------------------------------|
| 1    | `pip install nbconvert`                              | Install nbconvert utility         |
| 2    | You Edit `.ipynb` (Jupyter notebook) files, if any   |                                   |
| 3    | `jupyter nbconvert example.ipynb --to python`        | Convert notebook to Python script |

## How to Deploy

Deploy on **Azure App Service** for production.  

### 1. Create App Service
- Use the [Azure Portal](https://portal.azure.com) to create a free App Service for your web app.

### 2. Deploy from VS Code

| Step                   | Description                                              |
|------------------------|---------------------------------------------------------|
| VS Code Deployment     | Right-click on your resource, select `Deploy to Web App…`|

### 3. Add Environment Variables (e.g., for secrets)

| Step | Command                                                                                                                                      | Description                                 |
|------|---------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
| 1    | `az config set core.enable_broker_on_windows=false`                                                                                         | Configure Azure CLI for Windows             |
| 2    | `az login`                                                                                                                                  | Authenticate with Azure                     |
| 3    | `az webapp config appsettings set --name <AppServiceName> --resource-group <ResourceGroupName> --settings MY_VARIABLE=MyValue` | Set env vars for your App Service           |

_Reference: [Azure Flask Quickstart](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-cli%2Cazure-cli-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli)_

## dev logs

- This branch is coming from https://github.com/ProgramIsFun/graphPythonBackend11/tree/master.  I basically take one folder of that branch and then make it azure compatible in this branch
- 14/8/25  https://github.com/ProgramIsFun/EonGraph-Backend/commit/37f857deae2675eb9153f7b508015466da0b752a  Changed the old library to normal flask

## references

- https://github.com/Azure-Samples/msdocs-python-flask-webapp-quickstart
