# Flask Application for Ml Dev to prod

Production Ready Flask application with docker container with uwsgi and nginx config with wait time up to 10 min.

procduction Ready Message Broker consumer and publisher using RabbitMq Pikka with docker container.

can use both as as an flask Api and Meggage Broker.

S3 bucket download and upload and check code.

## Table of Contents

1. [Dependencies](#dependencies)
2. [Getting Started](#getting-started)
3. [Commands](#commands)
4. [Development](#development)
5. [Testing](#testing)
6. [Lint](#lint)
7. [Swagger](#swagger)
8. [Python-Debugger-With-Docker](#Running Python's PDB debugger with Docker)
9. [production](#production)
10. [important](#important)
11. [production-commands](##production commands)

## Dependencies

You will need [docker](https://docs.docker.com/engine/installation/) and [docker-compose](https://docs.docker.com/compose/install/).

## Getting Started

First, clone the project:

```bash
$ git clone https://giriyouplus@bitbucket.org/youplus/flaskmlserviceapp.git <application name here>  
$ cd application name here> 
```

Then install dependencies and check that it works

```bash
$ make install      # Install the pip dependencies on the docker container
$ make start        # Run the container containing your local python server
```

If everything works, you should see the available routes [here](http://127.0.0.1:3000/application/spec).

The API runs locally on docker containers. You can easily change the python version you are willing to use in docker-compose.yml, by fetching a docker image of the python version you want.

## Commands

While developing, you will probably rely mostly on `make start`; however, there are additional scripts at your disposal:

| `make <script>` | Description                                                                  |
| --------------- | ---------------------------------------------------------------------------- |
| `install`       | Install the pip dependencies on the server's container.                      |
| `start`         | Run your local server in its own docker container.                           |
| `daemon`        | Run your local server in its own docker container as a daemon.               |
| `test`          | Run unit tests with pytest in its own container.                             |
| `coverage`      | Run test coverage using pytest-cov.                                          |
| `lint`          | Run flake8 on the `src` and `test` directories.                              |
| `safety`        | Run safety to check if your vendors have security issues.                    |


## Development

To develop locally, here are your two options:

```bash
$ make start           # Create the containers containing your python server in your terminal
$ make daemon          # Create the containers containing your python server as a daemon
```

The containers will reload by themselves as your source code is changed.
You can check the logs in the `./server.log` file.


#Application Articture
Request comes to Route - configuring the Http end points is done here

Route pass the data to Resources - route understands the required resources and first level to check is done on the data is done here

Resources passes data to service - service understands which repo to be called based on the request request level logic is  handled here

Repository - Repo does the heavly lifiting of loading the ml model and predicting

MLModel - Store all you ml model

Downalods - any http request downloads to be added here and made sure its deleted

utility - all helper methods go here

Models - Return type object should be a model and baseModel inherated should be used to convet in to a json object

#Things to be taken in to consideration
1) os.path should not be used beacuse for production in Docker the working directory is different from dev
for example to use Ml model in Ml directory from repo use the below code
```bash
    currentPath = os.path.dirname(os.path.realpath(__file__))
    parentPath = os.path.abspath(os.path.join(currentPath, os.pardir))
    MlPath = parentPath + '/MLModel/'
```

2) parent folder name app , and the calling main file should always be main.py and flask server should be give name "app" this is beacuse 
the uwsgi and nginx server finds this structure to start the server

3) wave file downloader example is availabe in Repository

4) for unit test if model config not found error occures use
```bash
import sys
sys.path.append('/mnt/app/')
from app.main import app
```


## Testing

To add a unit test, simply create a `test_*.py` file anywhere in `./test/`, prefix your test classes with `Test` and your testing methods with `test_`. Unittest will run them automaticaly.
You can add objects in your database that will only be used in your tests, see example.
You can run your tests in their own container with the command:

```bash
$ make test
```

## Lint

To lint your code using flake8, just run in your terminal:

```bash
$ make lint
```

It will run the flake8 commands on your project in your server container, and display any lint error you may have in your code.

## Swagger

Your API needs a description of it's routes and how to interact with them.

The API description will be available http://127.0.0.1:3000/spec.

The Swagger UI will be available  http://127.0.0.1:3000/apidocs.

## Running Python's PDB debugger with Docker
1. Add to docker-compose.yml
  ```bash
  stdin_open: true  
  tty: true 
  ```
  to the service configuration in docker-compose.yml . 
2. To debug add
   ```bash
   import pdb;pdb.set_trace();
   ```
3. The debugger is running inside the container, so we need to attach into the container to use it.

    Find the container id using 
    ```bash 
    docker container ps
    ``` 
    Use the command 
    ```bash
    docker attach <CONTAINER_ID> 
    ```
    to attach to the container.

4. Now just navigate to the page and the debugger will start, so you will be able to use the usual commands like n or c.
5. To exit you should use CONTROL + P, CONTROL + Q.
6. If you use Control + C the container will stop.
For reference click [here](https://blog.lucasferreira.org/howto/2017/06/03/running-pdb-with-docker-and-gunicorn.html/).

#production

Docker image is using uwsgi-nginx for production

image name : tiangolo/uwsgi-nginx

Docker hub link of image[here](https://hub.docker.com/r/tiangolo/uwsgi-nginx/).

Git hub link of image[here](https://github.com/tiangolo/uwsgi-nginx-flask-docker).

Any change needs to done to nginx and uswgi can be done in nginx.conf and uwsgi.ini

Request time out for nginx and uwsgi is 1000 sec = 15 min

### important
To use as a message boker consumner and publisher add this lines in docker file
```bash
COPY ./prestart.sh /app
CMD [ "python", "-u", "task.py" ]
```

To use as an api remove this lines in docker file
```bash
 remove this two lines
  COPY ./prestart.sh /app
  CMD [ "python", "-u", "task.py" ]
```

to use both as an api and a consumer add this lines in docker file
```bash
COPY ./prestart.sh /app
```

#production commands
To change the environment variable for production use prod.env 

To build image use 
```bash
$ make build
```


To run prod containter on port 3002 
```bash
$ make prod
```

To kill prod container  
```bash
$ make k-prod
```

To remove prod container  
```bash
$ make r-prod
```

#Stagging commands
To change the environment variable for production use stagging.env 

To build image use 
```bash
$ make build
```

To run prod containter on port 3002  
```bash
$ make stagging
```

To kill prod container  
```bash
$ make k-stag
```

To remove prod container  
```bash
$ make r-stag
```




##If more process are required for uwsgi use the below code in the Dockerfile
ENV UWSGI_CHEAPER 4

ENV UWSGI_PROCESSES 64

#For nginx config use the nginx.conf file 