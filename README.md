# mg-rest-tad
Microservice RESTful API for the querying of a Cassandra db that had been generated using the code from the mg-process-fastq scripts

# Requirements
- Cassandra 3.7+
- Python 2.7+ (If using Cassandra 3.7 this requires Python 2.7.10 or less)
- pyenv
- pyenv virtualenv
- pip
- Python Modules
  - Flask
  - Flask-Restful
  - json
  - pytest

# Installation
## Initialise
```
pyenve virtualenv TADrest

cd rest
```

## Require data files
The dataset files for each of the genomes:

- datasets.json
```
{
    "taxon_id": {
        "9606": {
            "accession": {
                "GCA_000001405.22": {
                    "datasets": ["rao2014"],
                    "chromosomes": [
                        ["1", 249250621],
                        ["2", 243199373],
                        ["3", 198022430],
                        ["4", 191154276],
                        ["5", 180915260],
                        ...
                    ]
                }
            }
        }
    }
}
```

## Starting the Service
```
virtualenv env
source env/bin/activate

cd rest
python app.py
```

Place this in the boot scripts to get intialised as a service.

# RESTful API
## List taxon IDs
```
wget http://<host>/rest/v0.0/getTADs/
```

## List assemblies
```
wget http://<host>/rest/v0.0/getTADs/<string:taxon_id>
```

## List options for the assembly
```
wget http://<host>/rest/v0.0/getTADs/<string:taxon_id>/<string:accession_id>
```

## List datasets
```
wget http://<host>/rest/v0.0/getTADs/<string:taxon_id>/<string:accession_id>/datasets
```

## List available resolutions
List the avaiable resolutions the are loaded for a given dataset
```
wget http://<host>/rest/v0.0/getTADs/<string:taxon_id>/<string:accession_id>/resolutions
```

## List chromosomes
List the chromosomes at the given resolution
```
wget http://<host>/rest/v0.0/getTADs/<string:taxon_id>/<string:accession_id>/chromosomes
```
## List TADs
List the TADs for a given taxon and assembly that match the defined conditions within the parameters
```
wget http://<host>/rest/v0.0/getTADs/<string:taxon_id>/<string:accession_id>/tads?chr=<string:chromosome_id>&res=<integer:resolution>&start=<integer:start_pos>&end=<integer:end_position>
```
All of the parameters are required. If one or more of `chr`, `res`, `start` or `end` are missing then an exception is raised
