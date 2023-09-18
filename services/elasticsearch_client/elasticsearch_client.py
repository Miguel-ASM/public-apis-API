import elasticsearch

class Elastic():
  def __init__(self,hosts,mappings, index):
    self.index = index
    self.mappings = mappings
    self.es = elasticsearch.Elasticsearch(hosts=hosts)
  
  def resetindex(self):
    self.es.indices.delete(index=self.index,ignore_unavailable=True)
    self.es.indices.create(
      index= self.index,
      mappings=self.mappings
    )
