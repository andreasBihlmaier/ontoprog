# Ontology-based Programming
Extended Semantics for OOP languages

## General Idea
In addition to the rather flat semantics provided by the core of OOP languages (classes and objects, inheritance and polymorphism, member variables and methods), ontoprog aims to add more elaborate semantical constructs to everyday programming.

So far every library is based on an ad hoc ontology that is supposed to give semantics to its syntactic constructs.
Most of the time there is no formal semantics at all, but rather the programmer has to come up with a - hopefully consistent - semantic interpretation by himself based on textual descriptions.
Instead all libraries should be based on a common ontology with well defined (i.e. formally defined) semantics.
First library classes should map to entities in the ontology.
Second composition/aggregation should not be flat (everything is a member), but well defined in terms of relations in the ontology.
For example the relation between a car and its tires is mereological (the tire is [*part*](http://sigma-01.cim3.net:8080/sigma/Browse.jsp?kb=SUMO&lang=EnglishLanguage&flang=SUO-KIF&term=part) of the car), yet the cars color is one of its [*attribute*](http://sigma-01.cim3.net:8080/sigma/Browse.jsp?kb=SUMO&lang=EnglishLanguage&flang=SUO-KIF&term=attribute)s.
Furthermore, instead of color being a tuple of numbers (int or float? rgb or bgr?) it should be a [*ColorAttribute*](http://sigma-01.cim3.net:8080/sigma/Browse.jsp?lang=EnglishLanguage&flang=SUO-KIF&kb=SUMO&term=ColorAttribute) with a clear semantic meaning and that is convertible into different low-level representations.

Now instead of postulating yet another ad hoc ontology ontoprog relies on the broadly discussed (and accepted) [Suggested Upper Merged Ontology (SUMO)](http://ontologyportal.org/).

* Is ontoprog a new programming language? **No**. It merely extends existing OOP languages by a fixed set of base classes and methods that have a *well defined semantic meaning*.
* What about performance and memory footprint (think embedded systems)? My assessment: Feasible, i.e. low for most cases.
* Advantages?
    * Less ad hoc library ontologies to understand (within a specific language and between languages)
    * Future: Automatic mappings between libraries. Automatic software and hardware integration (semantic driver interfaces + semantically annotated microcontroller ports).



## Details

Every *Entity* in SUMO becomes an OOP class. Each class will be assigned a unique identity string corresponding to it's SUMO node (and class name).

Some *Relations* correspond to features already hard-coded into OOP languages, these are mapped accordingly:

| SUMO relation | OOP construct | Comment |
| --- | --- | --- |
| subclass, subrelation | (Multiple-)Inheritance between classes | |
| domain, range | Classes/Types | {domain,range}Subclass is handled by inheritance/polymorphism |
| instance | Objects | | 
| documentation | Doxygen comment | |
| equal | equality operator | Overloaded `==` operator, `equals` otherwise |
| valence | Function/Method signature | |
| exhaustiveAttribute | enum | |
| subAttribute | | |
| contraryAttribute | | |
| successorAttribute | increment operator | Overloaded `++` operator | |
| greaterThan, greaterThanOrEqualTo, greaterThanByQuality, less* | comparison operator | Overloaded `>` or `>=` operator |
| entails | | |

*instance* vs *subclass*:
*(instance sokrates Human)*: Normal case; object *sokrates* of class *Human*
*(instance equal BinaryPredicate)*: Problematic case; there is no single object *equal*, instead many instances of *equal* relation each pertaining to a certain class


Functions/Members and Classes:
Use [Function objects](http://en.wikipedia.org/wiki/Function_object) where possible because they allow for *subrelation* and to assign identifiers.
