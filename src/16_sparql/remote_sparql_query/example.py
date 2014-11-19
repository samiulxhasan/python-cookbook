#!/usr/bin/env python

from SPARQLWrapper import SPARQLWrapper2, JSON, TURTLE, DESCRIBE
import time

#PARAMETERS
query_service = "http://localhost:9892/sparql"
query_graph = "http://targetvalidation.org/cttv0009_gwas/" #This is Tony's GWAS data

sparql = SPARQLWrapper2(query_service)
if (sparql):
    print("Connect to "+query_service+" OK")

sparql.addDefaultGraph(query_graph)

def run_me(query_string):
    """Runs a SPARQL formatted query
    """
    
    start = time.time()

    sparql.setQuery(query_string)
    #sparql.setReturnFormat(TURTLE)  #this won't make a difference for this function but useful to know
    results = sparql.query()
    
    end = time.time()
    timepass = end - start
    print  "time_taken: "+str(timepass)+" seconds"

    #these are like the table "column headings" in SQL; an array of dictionaries with the full bindings
    bindings = results.variables
    print(bindings)
    
    try:
        datas = results[bindings]
        for d in datas :
            for b in bindings :
                subj = d[b].value
                print subj+"\t",
        print("\n")
    except IndexError:
        print "No hits!"
        return
        
#Pull out the first 10 triples from the dataset
query_string = "SELECT * WHERE { ?subj ?prop ?obj } LIMIT 10"
run_me(query_string)

#What unique classes are declared?
query_string = """
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

#a is a SPARQL shortcut for rdf:type
SELECT * WHERE
{
  { ?class a owl:Class }
  UNION
  { ?class a rdfs:Class }
  
  ?class a ?classType
}
"""

run_me(query_string)

#What unique properties are used in this dataset?
query = """
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX gwas: <http://rdf.ebi.ac.uk/terms/gwas/>

SELECT DISTINCT ?property
WHERE {
    ?s ?property ?o .
}
"""

run_me(query)

#What properties are declared?
query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?property WHERE {
    ?property a rdf:Property
}"""

run_me(query)
#This returned no results for GWAS catalog data

#What sub-properties are declared?
query = """
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

#The + is used like in regular expressions: subClassOf->subClassOf->subClassOf+++++
SELECT * WHERE {
    ?propClass rdf:subClassOf+ rdf:Property .
    ?property a ?propClass
}"""

run_me(query)
#Again no subproperties were found in GWAS catalog data

#What classes have instances?
query = """
SELECT DISTINCT ?class
WHERE {
    ?instance a ?class .
}
ORDER by ?class
"""
run_me(query)

#How many trait associations are there?
query = """
PREFIX gwas: <http://rdf.ebi.ac.uk/terms/gwas/>

SELECT COUNT(DISTINCT(?instance)) AS ?iTotal
WHERE {
    ?instance a gwas:TraitAssociation .
}
"""

run_me(query)

#pick a unique TraitAssociation
query = """PREFIX gwas: <http://rdf.ebi.ac.uk/terms/gwas/>

SELECT *
WHERE {
    ?instance a gwas:TraitAssociation
}
LIMIT 1"""
run_me(query)

#Which classes use the property 'http://rdf.ebi.ac.uk/terms/gwas/has_p_value'?

query = """
PREFIX gwas: <http://rdf.ebi.ac.uk/terms/gwas/>

SELECT DISTINCT ?class
WHERE {
    ?s gwas:has_p_value ?o ;
      a ?class .
}
LIMIT 1
"""
run_me(query)

#How much was the has_p_value property used?

query = """
PREFIX gwas: <http://rdf.ebi.ac.uk/terms/gwas/>

SELECT COUNT(?o)
WHERE { ?s gwas:has_p_value ?o }
"""

run_me(query)

#How much has each property been used?
query = """
SELECT ?p (COUNT(?p) AS ?pTotal)
WHERE
{ ?s ?p ?o . }
GROUP BY ?p
ORDER BY DESC(?pTotal)"""

run_me(query)

#How much has each property been used? Now make it more readable
query = """
SELECT ?p (COUNT(?p) AS ?pTotal)
WHERE
{ ?s ?p ?o . }
GROUP BY ?p
ORDER BY DESC(?pTotal)"""

run_me(query)


#How many instances of http://rdf.ebi.ac.uk/terms/gwas/TraitAssociation are there?
query = """
PREFIX gwas: <http://rdf.ebi.ac.uk/terms/gwas/>

SELECT 
(COUNT(?s) AS ?traitCount)
WHERE {
    ?s a gwas:TraitAssociation .
}
"""

run_me(query)

#What data is there about a TraitAssociation class?

query = """
PREFIX gwas: <http://rdf.ebi.ac.uk/terms/gwas/>

SELECT DISTINCT(?prop)
WHERE {
    gwas:TraitAssociation ?prop ?o .
}
"""

run_me(query)

