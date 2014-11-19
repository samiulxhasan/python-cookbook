<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](http://doctoc.herokuapp.com/)*

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

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

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