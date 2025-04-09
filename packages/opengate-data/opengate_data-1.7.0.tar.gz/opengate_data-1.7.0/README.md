# Opengate-data

Opengate-data is a python library that helps you integrate OpenGate into your python projects.

## Installation
To install the library, run:

```python
pip install opengate-data
```

## Import
To import the OpenGateClient, use:

```python
from opengate_data import OpenGateClient
```

## Basic use with user and password

To initialize the OpenGateClient using a username and password:

```python
client = OpenGateClient(url="Url", user="User", password="Password")
```
## Basic use with api-key

To initialize the client using an api_key:

```python
client = OpenGateClient(url="Url", api_key="Api_Key")
```

## Basic use token_jwt with .env

To initialize the client using a token_jwt with a .env file.

1. Create a .env file with the following content:

    `TOKEN_JWT="token_jwt"`
    <br>

2. Load the environment variable and initialize the client:

    ```python
    client = OpenGateClient()
    ```
   
By default, if you use OpenGateClient without parameters, and you set the environment variable TOKEN_JWT, OpenGateClient will be created with this value 
Iy you want to use TOKEN_JWT from environment, you may delete API_KEY variable environment

## Basic use of token_jwt with an environment variable

To initialize the client using a token_jwt from an environment variable, you can set the token_jwt directly in your environment without relying on a .env: 

1. Create environment variable

   - On UNIX systems, use:
     ```bash
     export TOKEN_JWT="token_jwt"
     ```

   - On Windows, use:
      ```bash
      set TOKEN_JWT="token_jwt"
      ```

2. Initialize the client.

    ```python
    client = OpenGateClient()
    ```

Similar to the previous example, if you use OpenGateClient without parameters, and you set the environment variable TOKEN_JWT, OpenGateClient will be created with this value
Iy you want to use TOKEN_JWT from environment, you may delete API_KEY variable environment

## Basic use without url for services K8s

To initialize the OpenGateClient without specifying a URL, you can either `omit` the `URL` parameter or set it to `None`

```python
client = OpenGateClient(api_key="Api_Key")
# or
client = OpenGateClient(url=None, api_key="Api_Key")
```
Similar to the previous examples, you have the option to provide the `api_key` directly, set it to `None`, or `omit` it altogether. If you choose to `omit` it, the client will automatically retrieve the `api_key` from the environment variable if it is set. Additionally, you can also authenticate using a `username` and `password` by specifying those credentials instead.


## Features

The library consists of the following modules:

- **IA**
  - Models
  - Pipelines
  - Transformers
- **Collection**
  - Collection
  - Bulk Collection
- **Provision**
  - Asset
  - Bulk
  - Devices
  - Processor
- **Rules**
  - Rules
- **Searching**
  - Datapoints
  - Data sets
  - Entities
  - Operations
  - Rules
  - Timeseries

## Documentation

To generate the API documentation you can execute `./generate_doc.sh` and open the generated Markdown on:
**docs/documentation.md**

## Basic Examples of the OpenGate-Data Modules

The examples of the different modules are found in the path `docs/basic_examples.md`

## Additional Documentation

For more details and examples about each of the modules,
consult the [complete documentation](https://documentation.opengate.es/).

## Generate version

To configure uploading packages to `PyPI`, you need to create and set up the .pypirc file in your home directory. Below are the steps for different operating systems:

- **Windows**: `notepad $env:USERPROFILE\.pypirc`. 
- **Linux**: `nano ~/.pypirc`. 

Inside the .pypirc file, configure the following lines, replacing token with your actual PyPI API token:

```python
[pypi]
     username = __token__
     password = token
```

Open the setup.py file and update the version of your project as needed and install twine. `pip install twine`
After updating the version in setup.py, run the following script to build and upload your package to PyPI: `./dish.sh`

## Test

### Running All Tests

If you want to run all the tests, both unit and integration tests, you can execute the `pytest.ini` file.
Run the following command in your terminal: `pytest`

### Running Unit Tests

Inside the unit folder, you will find all the unit tests corresponding to each module.
These tests verify the functionality of each function individually.
To run a unit test, use the pytest command followed by the name of the unit test.
For example: `pytest test_iot_collection.py`

### Running Integration Tests

Inside the test/features, you will find all the integration tests.
Additionally, you need to add the `url` and `api_key` to the `test_steps_cucumber.py` file

To run the tests, use the following command: `pytest test_steps_cucumber.py`

## License

This project is licensed under the MIT License.
