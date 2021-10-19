## zbMATH Links API
![test status](https://github.com/zbmathopen/linksApi/actions/workflows/pytest.yml/badge.svg)

The purpose of the zbMATH Links API is to show the interconnections between [zbMATH](https://zbmath.org/) (the `target` of the API) and external platforms (called here `partners` and constituting the `source` of the API) which store links linking to objects in the target, i.e., documents indexed at zbMATH. 
The prototypical partner is the [Digital Library of Mathematical Functions](https://dlmf.nist.gov/) (DLMF), which contains more than 6.000 links linking to publications indexed at zbMATH. 
Other partners can be integrated as well.

   **Dummy database.**  To run the zbMATH Links API with a dummy database (only for illustrative purposes) please follow these steps:

1) Install the requirements and set the environment variables.
On a first install:

    ```
    python3 -m venv env
    source env/bin/activate
    pip install -e .
    ```

    This will install the package, `zbmath-links-api` in the [virtual environment](https://docs.python.org/3/tutorial/venv.html).


2) Create the database.
Define an environment variable `SQLALCHEMY_DATABASE_URI` to set the [database connection URI](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/?highlight=sqlalchemy_database_uri#connection-uri-format). Connect
to the database, e.g., `export SQLALCHEMY_DATABASE_URI="postgresql:///my_database"`.
With initialization a migration folder will be automatically created.
   
   ```
   flask db init
   flask schema add
   flask db migrate
   flask db upgrade
   flask extra_tables add
   flask view add
   ```


3) Populate the (dummy) database. 
The following command adds just a single illustrative entry in all tables as a starting example dataset.
   
   ```
   flask seed all
   ```

4) Run the zbMATH Links API:

   ```
   flask run
   ```

5) View the API at http://127.0.0.1:5000/links_api/

**Remark.** See settings for configuring writing access. 
One can use [dotenv](https://pypi.org/project/python-dotenv/) to store your settings.
   

**DLMF database.**  To run the zbMATH Links API with DLMF data an auxiliary package is needed, `update-zblinks-api` (available [here](https://github.com/zbMATHOpen/Update_Links)), to be installed separately. 
This will allow the user to populate the database with real data coming from DLMF and execute an update when needed. 
Please follow these steps (only the third step is different from above):

1) As above.

2) As above.
   
3) To populate the database, please install the separate package `update-zblinks-api` and follow the instructions for that package.

4) As above.

5) As above.

**Remark.** See settings for configuring writing access. 
One can use [dotenv](https://pypi.org/project/python-dotenv/) to store your settings.
 
**Remark.**   For a proper operation of the API with real DLMF data at least one table (more precisely, a subset of it) of the real database of zbMATH is needed, i.e., `math_documents`. 
Indeed, the needed table must contain at least those documents indexed at zbMATH that are referenced in the links obtained by the `update-zblinks-api` package. For the same reason, a view of the zbMATH table `math_authors_ids` is needed.

## Remarks:

a) In what follows links are objects belonging to the `source` (within a given partner) and zbMATH objects are objects belonging to the `target` [zbMATH](https://zbmath.org/).

b) The zbMATH Links API offers 12 endpoints.

1. GET /link. It retrieves links for given zbMATH objects.

2. DELETE /link/item. It deletes a link from the database.

3. POST /link/item. It creates a new link related to a zbMATH object.

4. GET /link/item. It checks relations between a given link and a given zbMATH object.

5. PATCH /link/item. It edits and existing link.

6. GET /link/item/{doc_id}. It retrieves links for a given zbMATH object.

7. GET /partner. It retrieves data of a given zbMATH partner.

8. PUT /partner. It edits data of a given zbMATH partner.

9. POST /partner. It creates a new partner related to zbMATH.

10. GET /source. It produces a list of all links of a given zbMATH partner.

11. GET /statistics/msc. It shows the occurrence of primary MSC codes (2-digit level) of zbMATH objects in the set of links of a given partner.

12. GET /statistics/year. It shows the occurrence of years of publication of zbMATH objects in the set of links of a given partner.

c) The X-Field is an optional parameter that can be used when one is running a query that can pull back a lot of metadata, but only a few fields in the output are of interest. Example: in the GET/link one is interested only in retrieving the id identifier of sources where the name of the author is Abramowitz.
Then, Author: Abramowitz, X-Field: {Source{Identifier{ID}}}.

## Docker use

run
```
docker-compose up -d
```
visit http://127.0.0.1:5001/links_api/

## Settings

To use the write feature in some endpoints it is required to set the environment variable
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

All settings are listed at in the method [zb_links.app.configure_app](src/zb_links/app.py).
## Running GitHub actions locally
Install https://github.com/nektos/act and run
```
act
```