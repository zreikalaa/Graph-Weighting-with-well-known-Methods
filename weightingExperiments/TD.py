import os
import pickle
import rdflib
from rdflib.plugins.sparql import prepareQuery


def get_weights(file_name="td_weights.txt"):
    with open(file_name, "rb") as MyFile:
        concepts_weight = pickle.load(MyFile)
        return concepts_weight


class TD:
    ontology = "crm_bnf.owl"

    def extract_root_node(self):
        graph = rdflib.Graph()
        graph.parse(self.ontology)

        q = prepareQuery('''SELECT ?a WHERE { 
                            ?a rdf:type <http://www.w3.org/2002/07/owl#Class>.
                            FILTER NOT EXISTS { ?a rdfs:subClassOf ?b}
                        }''')
        root_node = ""
        for row in graph.query(q):
            root_node = row[0]
        return str(root_node)

    def get_children(self, parent):
        graph = rdflib.Graph()
        graph.parse(self.ontology)
        children = []
        q = prepareQuery('''select ?child { 
                                    ?child rdfs:subClassOf <''' + parent + '''>.
                                    }''')
        for row in graph.query(q):
            children.append(str(row[0]))
        return children

    def get_concept_id(self, concept):
        graph = rdflib.Graph()
        graph.parse(self.ontology)
        q = prepareQuery('''SELECT ?id 
                                WHERE { <''' + concept + '''> <http://www.semanticweb.org/CrmBnF#Id> ?id.
                                }''')
        concept_id = None
        for row in graph.query(q):
            concept_id = str(row[0])
        return concept_id

    def calculate_td(self):
        filesize = os.path.getsize("td_weights.txt")
        if filesize == 0:
            concepts_weights = self.calculate_weights()
            self.save_weights(concepts_weights)
        else:
            concepts_weights = get_weights()
        return concepts_weights



    def calculate_weights(self):
        root = self.extract_root_node()
        queue = [(root, 1)]
        concepts_weights = {}
        while len(queue) != 0:
            concept_url, weight = queue.pop(0)
            children = self.get_children(concept_url)
            children_number = len(children)
            if children_number == 0:
                concept = self.get_concept_id(concept_url)
                if concept != "Communication":
                    concepts_weights[concept] = weight
            else:
                for child in children:
                    queue.append((child, weight / children_number))


        return concepts_weights

    def save_weights(self, concepts_weights):
        with open("td_weights.txt", "wb") as MyFile:
            pickle.dump(concepts_weights, MyFile)
