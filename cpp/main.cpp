#include <iostream>

#include <Government.hpp>

int main()
{
  Government gov();

  std::cout << Government::ontoname << std::endl;

  std::cout << "superclasses():" << std::endl;
  for (auto superclass : Government::superclasses) {
    std::cout << superclass << std::endl;
  }

  return 0;
}
