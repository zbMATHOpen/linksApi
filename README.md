## zbMATH links API

1) Install requirements and set the env variables. 
   
    On a first install:
    ```
    python3 -m venv env
    source env/bin/activate
    pip install .
    ```
	
    This will install the API as a package (dlmfapi) in the virtual environment. 
    The following env variables need to be set everytime the API is activated:
    ```
    export APP_SETTINGS="config.DevelopmentConfig"
    export DATABASE_URL="postgresql:///zb_links_db"
    export FLASK_APP=zb_links.app.py 
    ```
    Note: to install the API as a package outside the virtual environment, 
    deactivate your virtual environment,
    ```
    source env/bin/deactivate
    ```
    Navigate to root folder, and
    ```
    pip install .
    ```
    Then follow the last three steps in 1) above to export the env settings.
    This will have been done in the virtual environment when the 
    "pip install -r requirements.txt" is run, and can be done outside the
    virtual environment to install the package globally.  
 


2) Create the database (postgres connection, db name: zb_links_db). 
   
   With initialization a migration folder will automatically be created by 
   Flask.
   ```
   flask manage_db reset
   flask db init
   flask db migrate
   flask db upgrade
   ```


3) Populate the database.  
   
   The following command adds just a single entry in all tables as a starting 
   example dataset.
   ```
   flask seed all
   ```


4) Run the API.
   ```
   flask run
   ```
	
   
5) View the API at http://127.0.0.1:5000/links_api/


## Remarks:

a) In what follows links are objects belonging to the "source" (of a given 
partner) and zbMATH objects are objects belonging to the "target".

b) The API offers 8 endpoints.

1. GET/partner shows the partners of zbMATH.

2. PUT/partner allows one to edit a selected partner of zbMATH. 
This route requires authentication.

3. GET/link allows one to retrieve links for given zbMATH objects.
The parameters are: Authors, MSC codes, X-Field (see below).
Note: in case of no results an empty list [] will be the output.

4. GET/link/item allows one to check relations between a given link, 
and a given zbMATH object. 
The parameters are: Zbl code, Source identifier, Partner name,
X-Field (see below).
Note: in case of no results an empty list [] will be the output.

5. POST/link allows one to create a new link (in a given partner) related 
to a zbMATH object.
The parameters are: Zbl code, Source identifier, Partner name, Link relation.
This route requires authentication.

6. GET/source provides a list of all links in the source.

7. GET/statistics/msc shows the occurrence of primary MSC codes 
(2-digit level) in the source.

8. GET/statistics/year shows the occurrence of years of publication of
references in the source.

c) The X-Field is an optional parameter that can be used when one
is running a query that can pull back a lot of metadata, but only a few
fields in the output are of interest. Example: in the GET/link one is interested 
only in retrieving the id identifier of sources where the name of the 
author is Abramowitz.
Then, Author: Abramowitz, X-Field: {Source{Identifier{ID}}}.

## Docker use

run
```
docker-compose up -d
```
visit http://127.0.0.1:5001/links_api/

## Settings

To use the write feature it is required to set the environment variable
`ZBMATH_API_KEY`.
This is unfortunately a bit complicated.
See
https://docs.docker.com/compose/environment-variables/
for details.

One alternative is use a docker-compose override file.
The following example file `docker-compose.override.yml`
```
version: '3.4'
services:
  db:
    ports:
      - 5432:5432
  rest:
    environment:
      ZBMATH_API_KEY: secretKey
```
Sets the key to `secretKey` and maps the internal database to port 5432 on your host system.
This can be practical for development. 
