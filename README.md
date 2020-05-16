# Star Base Weather Station File Server

This project contains the details of the AWS infrastructure used to store and retrieve weather station data from the Arduino Weather Station built using [this repo](https://github.com/crestlinesoaring/).

## Deployment Steps

1. Install AWS [Cloud Development Kit (CDK)](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)
1. Clone this repo
1. Use [pipenv](https://pipenv-fork.readthedocs.io/en/latest/install.html) to create the Python environment specified in `Pipfile`
1. Setup your AWS account and save your credentials in `~/.aws/credentials` as described [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
1. Run the commands below

```bash
cdk bootstrap
cdk deploy
```

Commands above will output `HttpEndpointDomain` value. Use this to make API calls.

## API Endpoints

#### Store Data

```bash
curl -i -X PUT -d '04:08,5/16/2020,00.0,00,1' <HttpEndpointDomain> 
```


#### Retrieve Data

```bash
curl -i -X GET  <HttpEndpointDomain>/?date=20200516
```
