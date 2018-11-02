# Sms Service Sample

The Project is a sample application for sass application, that implament user registration, login and sms sending (until corrency balance is exhausted).

## Getting Started

please enter your Nexmo api_key and secret into docker-compose.yml
and run docker-compose up

please enter http://localhost:5000
for Swagger ui page.

## Api Documentation.
The Api Documitation is auto generated please run
```
make up # to run test enviorment
curl http://localhost:5000/swagger.json # to get the current swagger.json
```
To get swagger.json and also you can browse to http://localhost:5000/ for intactive web app.

## Running the tests

run
```
make test
```
will build and run integration tests



## Deployment

The service deployment is out of project scope.



## Some Arcitacture design.

There isn't much something new from architcture stand point.

the jwt token signature is used to Identify the user without keeping session information on the server, so the service could remain as stateless as possible.

The same private key is use to generated phone verification token also for the same reason.


## Some Restriction
* please pay attantion that to private key is generated inside the container and the public key is not shared between container.
So Horizontal scale is still not supported.

* Also this is a sample application and multiplie connection handling (gevent implamantation) is not supported yet.

* please pay attantion that that the internal microservices serve HTTP and not HTTPS so deployment should consider adding HTTPS layer of protection so middle man attack will be considerable harder.
