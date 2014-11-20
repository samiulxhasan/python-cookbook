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
      - [Use Virtuoso for transitive queries](#use-virtuoso-for-transitive-queries)
      - [Same as above but with standard SPARQL 1.1](#same-as-above-but-with-standard-sparql-11)
      - ["Find all the people known by Kingsley Idehen to a depth between 1 and 4 applications of the subquery"](#find-all-the-people-known-by-kingsley-idehen-to-a-depth-between-1-and-4-applications-of-the-subquery)
      - [Find all entities associated with the entity denoted by  <http://id.myopenlink.net/dataspace/person/KingsleyUyiIdehen#this> via the foaf:knows relation.](#find-all-entities-associated-with-the-entity-denoted-by--httpidmyopenlinknetdataspacepersonkingsleyuyiidehen#this-via-the-foafknows-relation)
      - [Determine how two entities (type: Person) are connected using the foaf:knows relation:](#determine-how-two-entities-type-person-are-connected-using-the-foafknows-relation)
      - [Transitivity & Equivalence Relation (owl:sameAs)](#transitivity-&-equivalence-relation-owlsameas)
      - [Transitivity, Equivalence Relation, and Named Graphs](#transitivity-equivalence-relation-and-named-graphs)
      - [Transitive Closure, Named Graphs, via RDF Schema Subsumption Reasoning 1](#transitive-closure-named-graphs-via-rdf-schema-subsumption-reasoning-1)
      - [Transitive Closure, Named Graphs, via RDF Schema Subsumption Reasoning 2](#transitive-closure-named-graphs-via-rdf-schema-subsumption-reasoning-2)
      - [Transitivity enhanced Relatedness between two entities](#transitivity-enhanced-relatedness-between-two-entities)

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

#### Use Virtuoso for transitive queries

```python
SELECT ?x
FROM <http://dbpedia.org/resource/classes/yago#>
WHERE
  {
    {
      SELECT *
      WHERE
        {
          ?x rdfs:subClassOf ?y .
        }
    } OPTION (transitive, t_distinct, t_in (?x), t_out (?y) ) .
  FILTER (?y = <http://dbpedia.org/class/yago/Receptor105608868>)
}
```

#### Same as above but with standard SPARQL 1.1
```python
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?type
WHERE
{
  {
   SELECT *
   WHERE
    {
       ?x rdfs:subClassOf+ ?type .
    }
  }
  FILTER (?x = <http://dbpedia.org/ontology/Hospital>)
}
```

#### "Find all the people known by Kingsley Idehen to a depth between 1 and 4 applications of the subquery"

```python
SELECT ?o ?dist
       (
         (
           SELECT COUNT (*)
           WHERE
             {
               ?o foaf:knows ?xx
             }
         )
       )
WHERE
  {
    {
      SELECT ?s ?o
      WHERE
        {
          ?s foaf:knows ?o
        }
    }
    OPTION ( TRANSITIVE,
             t_distinct,
             t_in(?s),
             t_out(?o),
             t_min (1),
             t_max (4),
             t_step ('step_no') as ?dist ) .
    FILTER ( ?s = <http://id.myopenlink.net/dataspace/person/KingsleyUyiIdehen#this> )
  }
ORDER BY ?dist DESC 3
LIMIT 50
```

#### Find all entities associated with the entity denoted by  <http://id.myopenlink.net/dataspace/person/KingsleyUyiIdehen#this> via the foaf:knows relation.

```python
## Do so in a manner that uses a Transitive Closure
## to include aggregates and distances between
## the entities in the foaf:knows relation

SELECT ?o ?dist
       (
         (
           SELECT COUNT (*)
           WHERE
             {
               ?o foaf:knows ?xx
             }
         )
       )
WHERE
  {
    {
      SELECT ?s ?o
      WHERE
        {
          ?s foaf:knows ?o
        }
    }
    OPTION ( TRANSITIVE,
             t_distinct,
             t_in(?s),
             t_out(?o),
             t_min (2),
             t_max (4) ,
             t_step ('step_no') as ?dist ) .
    FILTER ( ?s = <http://id.myopenlink.net/dataspace/person/KingsleyUyiIdehen#this> )
    FILTER ( !(isblank(?o))) .
  }
ORDER BY ?dist DESC 3
LIMIT 50
```

#### Determine how two entities (type: Person) are connected using the foaf:knows relation:

```python
SELECT ?link ?g ?step ?path
WHERE
  {
    {
      SELECT ?s ?o ?g
      WHERE
        {
          graph ?g {?s foaf:knows ?o }
        }
    }
    OPTION ( TRANSITIVE,
             t_distinct,
             t_in(?s),
             t_out(?o),
             t_no_cycles,
             t_shortest_only,
             t_step (?s) as ?link,
             t_step ('path_id') as ?path,
             t_step ('step_no') as ?step,
             t_direction 3 ) .
    FILTER ( ?s = <http://www.w3.org/People/Berners-Lee/card#i>
          && ?o = <http://myopenlink.net/dataspace/person/kidehen#this> )
  }
LIMIT 20
```

#### Transitivity & Equivalence Relation (owl:sameAs)
```python
## Find all co-referents of the
## IRI <http://dbpedia.org/resource/New_York>
## i.e., other IRIs that denote the same
## thing as <http://dbpedia.org/resource/New_York> .

SELECT ?syn
WHERE
  {
    {
      SELECT ?x ?syn
      WHERE
        {
          {
            ?x owl:sameAs ?syn
          }
          UNION
          {
            ?syn owl:sameAs ?x
          }
        }
    }
    OPTION ( transitive, t_in (?x), t_out (?syn), t_distinct, t_min (0) )
    FILTER ( ?x = <http://dbpedia.org/resource/New_York> ) .
  }
```

#### Transitivity, Equivalence Relation, and Named Graphs
```python
## "Find all graphs that contain
## owl:sameAs for "New York":

SELECT ?g ?x count (*) as ?count
WHERE
  {
    {
      SELECT ?x ?alias ?g
      WHERE
        {
          {
            GRAPH ?g
              {
                ?x owl:sameAs ?alias
              }
          }
          UNION
          {
            GRAPH ?g
              {
                ?alias owl:sameAs ?x
            }
          }
        }
      }
    OPTION ( TRANSITIVE,
              t_in (?x),
              t_out (?alias),
              t_distinct,
              t_min (1)
           ) .
    FILTER ( ?x = <http://dbpedia.org/resource/New_York> ) .
  }

```

#### Transitive Closure, Named Graphs, via RDF Schema Subsumption Reasoning 1
```python
## Transitivity enhanced Subsumption Reasoning

## Meaning: subClasses of subClasses are incorporated
## into the query solution by way of Transitive Closure

SELECT ?y
FROM <http://dbpedia.org/resource/classes/yago#>
WHERE
  {
    {
      SELECT *
      WHERE
        {
          ?x rdfs:subClassOf ?y .
        }
    }
    OPTION ( TRANSITIVE, t_distinct, t_in (?x), t_out (?y) ) .
    FILTER ( ?x = <http://dbpedia.org/class/yago/AlphaReceptor105609111> )
  }
```

#### Transitive Closure, Named Graphs, via RDF Schema Subsumption Reasoning 2

```python
## Transitivity enhanced Subsumption Reasoning

## Meaning: subClasses of subClasses of
## <http://dbpedia.org/class/yago/Receptor105608868>
## are incorporated into the query solution
## by way of Transitive Closure

SELECT ?y
FROM <http://dbpedia.org/resource/classes/yago#>
WHERE
  {
    {
      SELECT *
      WHERE
        {
          ?x rdfs:subClassOf ?y .
        }
    }
    OPTION ( TRANSITIVE, t_distinct, t_in (?y), t_out (?x) ) .
    FILTER ( ?y = <http://dbpedia.org/class/yago/Receptor105608868> )
  }
```

#### Transitivity enhanced Relatedness between two entities
```python
## Incorporate Transitive Closures into determining 10
## relations that associate the entity denoted by
## <http://dbpedia.org/resource/New_York>
## with other entities

SELECT DISTINCT ?s ?p ?o
       bif:either(isIri(?o),'URI',datatype(?o)) AS ?type
WHERE
  {
    ?anchor ?pp ?s
    OPTION ( TRANSITIVE,
               t_min (0),
               t_max (2),
               t_in (?anchor),
               t_out (?s),
               t_no_cycles,
               t_distinct ) .
    FILTER ( ?anchor = <http://dbpedia.org/resource/New_York>)
    ?s ?p ?o .
  }
ORDER BY ?s
LIMIT 100
```




