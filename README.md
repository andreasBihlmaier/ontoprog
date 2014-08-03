Every *Entity* in SUMO becomes an OOP class. Each class will be assigned a unique identity string corresponding to it's SUMO node (and class name).
Some *Relations* correspond to features already hard-coded into OOP languages, these are mapped accordingly.

| SUMO relation | OOP construct | Comment |
| --- | --- | --- |
| subclass, subrelation | (Multiple-)Inheritance between classes | |
| domain, range | Classes/Types | {domain,range}Subclass is handled by inheritance/polymorphism |
| instance-of | Objects | | 
| documentation | Doxygen comment | |
| equal | equality operator | Overloaded `==` operator, `equals` otherwise |
| valence | Function/Method signature | |
