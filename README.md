# Blue moon cooking
-------------------

![build status](https://github.com/andreiboyanov/blue-moon-cooking/actions/workflows/python-app.yml/badge.svg)
![test results](https://gist.githubusercontent.com/andreiboyanov/e4998217decaff96c097bf27b31417bf/raw/0a5a820dc7d9b011209de625ab34d16af934ec56/badge.svg)


This repository contains an application for cooking recipes management. The only interface provided is a REST API. It can be explored through the OpenAPI UI (see below).


```
Note
----
No authentication nor authorization mechanisms in this version version!
```

## Project organisation

- The repository: https://github.com/andreiboyanov/blue-moon-cooking
- Open issues: https://github.com/andreiboyanov/blue-moon-cooking/issues
- Project board: https://github.com/users/andreiboyanov/projects/1

## Global view of the system

![comoponent diagram](https://raw.githubusercontent.com/andreiboyanov/blue-moon-cooking/main/design/diagrams/bmcook_components.drawio.png)


## Build

The app is running within Docker containers. To build the containers do the following:
- copy the provided `.env-sample` file renaming it to `.env`
- adjust the variables in the `.env` file to suite the desired configuration; pay attention to change the usernames and passwords
- run `docker-compose build`

## Running

Start with the following command:
```shell
docker-compose up -d
```

## Creating a database

In this version of the product you have to create the application database. 
To do so, execute the following commands in the root directoryof the project:

```shell
 source .env && export $(cut -d= -f1 < .env)
 docker-compose exec bmcook cat bmcook/db/tools/init_db.sql | psql -U $POSTGRES_USER -h $POSTGRES_HOST -p $POSTGRES_PORT $POSTGRES_DATABASE
 docker-compose exec bmcook cat bmcook/tests/data/demo_data.sql | psql -U $POSTGRES_USER -h $POSTGRES_HOST -p $POSTGRES_PORT $POSTGRES_DATABASE
 ```
 This will also install some demo data.

To test the installation, open /docs on the server where you`ve installed the application in your browser. Keep in mind adding the selected port. You must see the OpenAPI UI.
For instance, if you installed it locally on the default port 8000, open the folowing url:

http://localhost:8000/docs

## Deployment

Deploy the application as any other Docker based application. 
If you are deploying with the provided docker-compose.yml file, then you must include a configuration step where you generate the .env file (see above). Otherwhise you need to configure this variables depending on the deployment method you are using. 

## User guide
