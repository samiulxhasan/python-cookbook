<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](http://doctoc.herokuapp.com/)*

- [Investigate RDF queries](#investigate-rdf-queries)
      - [total number of triples](#total-number-of-triples)
      - [total number of entities](#total-number-of-entities)
      - [total number of distinct resource URIs (deprecated??)](#total-number-of-distinct-resource-uris-deprecated)
      - [total number of distinct classes](#total-number-of-distinct-classes)
      - [total number of distinct predicates](#total-number-of-distinct-predicates)
      - [total number of distinct subject nodes](#total-number-of-distinct-subject-nodes)
      - [total number of distinct object nodes](#total-number-of-distinct-object-nodes)
      - [exhaustive list of classes used in the dataset](#exhaustive-list-of-classes-used-in-the-dataset)
      - [exhaustive list of properties used in the dataset](#exhaustive-list-of-properties-used-in-the-dataset)
      - [table: class vs. total number of instances of the class](#table-class-vs-total-number-of-instances-of-the-class)
      - [table: property vs. total number of triples using the property](#table-property-vs-total-number-of-triples-using-the-property)
      - [table: property vs. total number of distinct subjects in triples using the property](#table-property-vs-total-number-of-distinct-subjects-in-triples-using-the-property)
      - [table: property vs. total number of distinct objects in triples using the property](#table-property-vs-total-number-of-distinct-objects-in-triples-using-the-property)
- [Querying ontologies](#querying-ontologies)
      - [Finding super classes](#finding-super-classes)
      - [Finding sub classes](#finding-sub-classes)
      - [If you need the transitive closure of sub/super classes then you have two options:](#if-you-need-the-transitive-closure-of-subsuper-classes-then-you-have-two-options)
      - [Tutorials - counting classes, subclasses etc.](#tutorials---counting-classes-subclasses-etc)
- [Virtuoso](#virtuoso)
      - [Enable federated querying from Virtuoso](#enable-federated-querying-from-virtuoso)
      - [Start/stop Virtuoso](#startstop-virtuoso)
        - [shut it down method-1](#shut-it-down-method-1)
        - [shut it down method-2](#shut-it-down-method-2)
      - [bash script - load RDF data](#bash-script---load-rdf-data)
      - [Federated query bug](#federated-query-bug)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

#Investigate RDF queries

#### total number of triples
SELECT (COUNT(*) AS ?no) { ?s ?p ?o  }
#### total number of entities
SELECT COUNT(distinct ?s) AS ?no { ?s a []  }
#### total number of distinct resource URIs (deprecated??)
SELECT (COUNT(DISTINCT ?s ) AS ?no) { { ?s ?p ?o  } UNION { ?o ?p ?s } FILTER(!isBlank(?s) && !isLiteral(?s)) }         
#### total number of distinct classes
SELECT COUNT(distinct ?o) AS ?no { ?s rdf:type ?o }
#### total number of distinct predicates
SELECT count(distinct ?p) { ?s ?p ?o }
#### total number of distinct subject nodes
SELECT (COUNT(DISTINCT ?s ) AS ?no) {  ?s ?p ?o   } 
#### total number of distinct object nodes
SELECT (COUNT(DISTINCT ?o ) AS ?no) {  ?s ?p ?o  filter(!isLiteral(?o)) }                               
#### exhaustive list of classes used in the dataset
SELECT DISTINCT ?type { ?s a ?type }
#### exhaustive list of properties used in the dataset
SELECT DISTINCT ?p { ?s ?p ?o }
#### table: class vs. total number of instances of the class
SELECT  ?class (COUNT(?s) AS ?count ) { ?s a ?class } GROUP BY ?class ORDER BY ?count
#### table: property vs. total number of triples using the property
SELECT  ?p (COUNT(?s) AS ?count ) { ?s ?p ?o } GROUP BY ?p ORDER BY ?count
#### table: property vs. total number of distinct subjects in triples using the property
SELECT  ?p (COUNT(DISTINCT ?s ) AS ?count ) { ?s ?p ?o } GROUP BY ?p ORDER BY ?count
#### table: property vs. total number of distinct objects in triples using the property
SELECT  ?p (COUNT(DISTINCT ?o ) AS ?count ) { ?s ?p ?o } GROUP BY ?p ORDER BY ?count

#Querying ontologies

#### Finding super classes

```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://www.domain.com/your/namespace/>

SELECT ?superClass WHERE { ns:AcousticWave rdfs:subClassOf ?superClass . }
```

#### Finding sub classes

```
SELECT ?subClass WHERE { ?subClass rdfs:subClassOf ns:Wave . }
If you want to retrieve the labels for every subclass of ns:Wave you would do something like ...

SELECT ?subClass ?label WHERE { 
        ?subClass rdfs:subClassOf ns:Wave . 
        ?subClass rdfs:label ?label . 
}
```

#### If you need the transitive closure of sub/super classes then you have two options:

- Iterate recursively over these queries until you have collected the closure.
- Pass your RDF data through a RDF/RDFS reasoner to forward chain all entailments and assert these in your RDF database.

#### Tutorials - counting classes, subclasses etc.

[Ontobee tutorial](http://www.ontobee.org/tutorial/tutorial_sparql.php)

[Virtuoso tutorial](http://virtuoso.openlinksw.com/dataspace/doc/dav/wiki/Main/VirtsubClassOfOrientedSubsumptionTransitiveOptions)

#Virtuoso

#### Enable federated querying from Virtuoso

1. [Enable CORS](http://www.openlinksw.com/dataspace/doc/dav/wiki/Main/VirtTipsAndTricksGuideCORSSetup#Server-level CORS Setup)
2. At http://localhost:9892/sparql, click "Details" and follow the instructions to allow secure querying

#### Start/stop Virtuoso

>virtuoso-t +configfile virtuoso.ini
dba/dba

##### shut it down method-1
>isql 2224 dba <password> -K

##### shut it down method-2
>isql 2224 dba <password>
SQL>shutdown();

#### bash script - load RDF data
```bash
#!/bin/bash
/usr/local/virtuoso-opensource/bin/isql 1111 dba dba <<'EOF'
SPARQL CREATE GRAPH <free>;
ld_dir('/home/najib', 'term.rdf', 'free');
rdf_loader_run();
SPARQL SELECT * FROM <free> WHERE {?s ?o ?p};
EOF
```

#### Federated query bug
```
SELECT * where
{ 
   SERVICE <http://bio2rdf.org/sparql>
   {?x <http://bio2rdf.org/ns/bio2rdf#inchi> ?o}
} 
limit 10
```
>Virtuoso 42000 Error SQ200: Must have select privileges on view DB.DBA.SPARQL_SINV_2

```
grant select on "DB.DBA.SPARQL_SINV_2" to "SPARQL";

grant execute on "DB.DBA.SPARQL_SINV_IMP" to "SPARQL";
```