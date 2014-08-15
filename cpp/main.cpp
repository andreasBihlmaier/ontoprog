#include <iostream>

#include <Government.hpp>

int main()
{
  Government gov();

  std::cout << Government::ontoname << std::endl;

  std::cout << "superclasses():" << std::endl;
  auto superclasses = Government::superclasses();
  for (auto superclass : superclasses) {
    std::cout << superclass << std::endl;
  }

  return 0;
}
