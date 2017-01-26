"""
Copyright 2017 EMBL-European Bioinformatics Institute

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from flask import Flask, make_response, request
from flask_restful import Api, Resource

from datasets import datasets
#from cassandra_reader import cassandra_reader
from mysql_reader import mysql_reader

app = Flask(__name__)
api = Api(app)

@api.representation('application/tsv')
def output_tsv(data, code, headers=None):
    """
    TSV representation for interactions
    """
    if request.endpoint == "values":
        outstr = ''
        for v in data["values"]:
            outstr += str(v["chrA"]) + "\t" + str(v["startA"]) + "\t" + str(v["chrB"]) + "\t" + str(v["startB"]) + "\t" + str(v["value"]) + "\n"
        resp = make_response(outstr, code)
        resp.headers.extend(headers or {})
        return resp


class GetChrParam(Resource):
    """
    Class to handle the http requests for retrieving all chr_params
    """
    
    def get(self):
        ds = datasets()
        return ds.getChr_param()


class GetTaxons(Resource):
    """
    Class to handle the http requests for retrieving a list of taxon IDs
    """
    
    def get(self):
        ds = datasets()
        taxons = ds.getTaxon()
        request_path = request.path
        rp = request_path.split("/")
        return {
            '_links': {
                'self': request.base_url,
                'child': [request.base_url + "/" + str(d) for d in taxons]
            },
            'taxons': taxons
        }


class GetAccessions(Resource):
    """
    Class to handle the http requests for retrieving a list of accessions for a 
    given taxonic ID
    """
    
    def get(self, taxon_id):
        ds = datasets()
        accessions = ds.getAccessions(taxon_id)
        request_path = request.path
        rp = request_path.split("/")
        return {
            '_links': {
                'self': request.base_url,
                'child': [request.base_url + "/" + str(d) for d in accessions],
                'parent': request.url_root + 'rest/' + str(rp[2]) + '/' + str(rp[3]) + '/' + str(taxon_id)
            },
            'accessions': accessions
        }

class GetAccession(Resource):
    """
    Class to handle the http requests for retrieving a list of accessions for a 
    given taxonic ID
    """
    
    def get(self, taxon_id, accession_id):
        request_path = request.path
        rp = request_path.split("/")
        return {
            '_links': {
                'self': request.base_url,
                'child': [
                    request.base_url + "/dataset",
                    request.base_url + "/experiments",
                    request.base_url + "/resolutions",
                    request.base_url + "/chromosomes",
                    request.base_url + "/tads"
                ],
                'parent': request.url_root + 'rest/' + str(rp[2]) + '/' + str(rp[3]) + '/' + str(taxon_id)
            },
            'accession': accession_id
        }

class GetDatasets(Resource):
    """
    Class to handle the http requests for retrieving a list of datasets for a
    given accession
    """
    
    def get(self, taxon_id, accession_id):
        ds = datasets()
        dataset = ds.getDatasets(taxon_id, accession_id)
        request_path = request.path
        rp = request_path.split("/")
        return {
            '_links': {
                'self': request.base_url,
                'child': [request.base_url + "/" + str(d) for d in dataset],
                'parent': request.url_root + 'rest/' + str(rp[2]) + '/' + str(rp[3]) + '/' + str(taxon_id) + '/' + str(accession_id)
            },
            'datasets': dataset
        }

class GetExperiments(Resource):
    """
    Class to handle the http requests for retrieving a list of datasets for a
    given accession
    """
    
    def get(self, taxon_id, accession_id):
        ds = datasets()
        dataset = ds.getDatasets(taxon_id, accession_id)
        request_path = request.path
        rp = request_path.split("/")
        return {
            '_links': {
                'self': request.base_url,
                'child': [request.base_url + "/" + str(d) for d in dataset],
                'parent': request.url_root + 'rest/' + str(rp[2]) + '/' + str(rp[3]) + '/' + str(taxon_id) + '/' + str(accession_id)
            },
            'datasets': dataset
        }

class GetResolutions(Resource):
    """
    Class to handle the http requests for retrieving the available resolutions
    that have been loaded in a dataset
    """
    
    def get(self, taxon_id, accession_id):
        ds = datasets()
        resolutions = ds.getResolutions()
        request_path = request.path
        rp = request_path.split("/")
        return {
            '_links': {
                'self': request.base_url,
                'child': [request.base_url + "/" + str(r) for r in resolutions],
                'parent': request.url_root + 'rest/' + str(rp[2]) + '/' + str(rp[3]) + '/' + str(taxon_id) + '/' + str(accession_id)
            },
            'resolutionss': resolutions
        }


class GetChromosomes(Resource):
    """
    Class to handle the http requests for retrieving the list of chromosomes for
    a given accession
    """
    
    def get(self, taxon_id, accession_id):
        ds = datasets()
        resolutions = ds.getResolutions()
        chr_param = ds.getChromosomes(taxon_id, accession_id, resolutions[-1])
        request_path = request.path
        rp = request_path.split("/")
        children = []
        chromosomes = []
        for c in chr_param:
          children.append(request.base_url + "/" + c[0])
          chromosomes.append(c[0])
        return {
            '_links': {
                'self': request.base_url,
                'child': children,
                'parent': request.url_root + 'rest/' + str(rp[2]) + '/' + str(rp[3]) + '/' + str(taxon_id) + '/' + str(accession_id)
            },
            'chromosomes': chromosomes
        }

class GetTADs(Resource):
    """
    Class to handle the http requests for retrieving ranges of TADs from
    a given dataset
    """
    
    def get(self, taxon_id, accession_id):
        ds = datasets()
        resolutions = ds.getResolutions()
        chromos = ds.getChromosomes(taxon_id, str(accession_id), resolutions[-1])
        chromosomes = [i[0] for i in chromos]
        
        error = False
        
        chr_id = request.args.get('chr')
        start = int(request.args.get('start'))
        end = int(request.args.get('end'))
        resolution = int(request.args.get('res'))
        
        if chr_id not in chromosomes:
            return {
                "error" : "No chr parameter provided"
            }
        
        if resolution == None:
            return {
                "error" : "No res parameter provided"
            }
        
        if start == None or end == None:
            return {
                "error" : "No start and/or end parameter provided"
            }
        
        request_path = request.path
        rp = request_path.split("/")
        value_url = request.url_root + 'rest/' + str(rp[2]) + '/getValue/' + str(taxon_id)
        
        # Get the TADs
        #cr = cassandra_reader()
        #x = cr.get_range(accession_id, resolution, chr_id, start, end)
        
        mr = mysql_reader()
        x = mr.get_range(accession_id, resolution, chr_id, start, end)
        
        return {
            '_links': {
                'self': request.url,
                'parent': request.url_root + '/rest/' + str(rp[2]) + '/' + str(rp[3]) + '/' + str(taxon_id) + '/' + str(accession_id)
            },
            'resolution': resolution,
            'genome': accession_id,
            'tad_count': x["count"],
            'values': x["results"],
        }


"""
Define the URIs and their matching methods
"""
#   List the available species for which there are datasets available
api.add_resource(GetTaxons, "/rest/v0.0/getTADs", endpoint='taxons')

#   List the available assemblies for a given species with links
api.add_resource(GetAccessions, "/rest/v0.0/getTADs/<string:taxon_id>", endpoint='accessions')

#   List the available available options for an accession
api.add_resource(GetAccession, "/rest/v0.0/getTADs/<string:taxon_id>/<string:accession_id>", endpoint='accession')

#   List the available datasets for a given genome with links
api.add_resource(GetDatasets, "/rest/v0.0/getTADs/<string:taxon_id>/<string:accession_id>/datasets", endpoint='datasets')

#   List the available experiments for a given dataset with links
api.add_resource(GetExperiments, "/rest/v0.0/getTADs/<string:taxon_id>/<string:accession_id>/experiments", endpoint='experiments')

#   List the resolutions available with links
api.add_resource(GetResolutions, "/rest/v0.0/getTADs/<string:taxon_id>/<string:accession_id>/resolutions", endpoint='resolutions')

#   List the Chromosomes and their sizes and number of bins for the given resolution with links
api.add_resource(GetChromosomes, "/rest/v0.0/getTADs/<string:taxon_id>/<string:accession_id>/chromosomes", endpoint='chromosomes')

#   List the TADs for a given region
#   Options:
#    - chr   - chromosome (string)
#    - res   - resolution (int)
#    - start - (int)
#    - end   - (int)
api.add_resource(GetTADs, "/rest/v0.0/getTADs/<string:taxon_id>/<string:accession_id>/tads", endpoint='values')


"""
Initialise the server
"""
if __name__ == "__main__":
    app.run()
