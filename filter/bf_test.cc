
#include <iostream>
#include <bf.h>

int main(int argc, char **argv) {
  bf::basic_bloom_filter b(0.8, 100);

  // Add two elements.
  b.add("foo");
  b.add(42);

  // Test set membership
  std::cout << b.lookup("foo") << std::endl;  // 1
  std::cout << b.lookup("bar") << std::endl;  // 0
  std::cout << b.lookup(42) << std::endl;     // 1

  b.add("foo");

  // Remove all elements.
  b.clear();
  std::cout << b.lookup("foo") << std::endl;  // 0
  std::cout << b.lookup(42) << std::endl;     // 0
  return 0;
}

