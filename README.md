# Blue moon cooking

This repository contains an application for cooking recipes management


```
Note
----
No authentication nor authorization mechanisms in this version version!
```

## Build

The app is running within Docker containers. To build the containers do the following:
- copy the provided `.env-sample` file renaming it to `.env`
- adjust the variable in this file to suite the desired configuration; make attention to change the usernames and passwords
- run `docker-compose build`

## Running

Start with the following command:
```shell
docker-compose up -d
```

To test the installation, open the url of the server where you`ve installed the application in your browser. Keep in mind adding the selected port. You must see the OpenAPI UI. 

## Deployment

Deploy the application as any other Docker based application. 
In your deployment procedure you must include a configuration step where you generate the .env file (see above)

## User guide