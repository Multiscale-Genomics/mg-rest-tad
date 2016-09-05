"""
Copyright 2016 EMBL-European Bioinformatics Institute

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

import json
from cassandra.cluster import Cluster

class cassandra_reader:
    """
    Class related to handling the functions for interacting directly with the
    Cassandra db. All required information should be passed to this class.
    """
    
    def __init__(self):
        """
        Intialisation function for the datasets class
        """
        
        # Open database connection
        cluster = Cluster()
        self.session = cluster.connect('tad_regions')
    
    def get_range(self, accession_id, resolution, chr_id, start, end, value_url = '/rest/v0.0/getValue/9606'):
        """
        Get the interactions that happen within a defined region on a specific
        chromosome. Returns inter and intra interactions with the defined region.
        """
        
        sql = "SELECT chromosome, start, end, dataset, experiment FROM tads WHERE assembly=%s AND resolution=%s AND chromosome=%s AND start>=%s AND start<=%s";
        
        """
        For the moment I have put in a manual fudge factor allowing for the out
        of range TADS
        """
        param = (accession_id, resolution, chr_id, start-10, end)
        
        rows = self.session.execute(sql, param)
        
        results = []
        count = 0
        for row in rows:
            results.append({"chr": str(row.chromosome), "start": str(row.start), "end": str(row.end), "dataset": str(row.dataset), "experiment": str(row.experiment), '_links': {}})
            count += 1
        return {"results": results, "count": count}
