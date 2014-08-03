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
