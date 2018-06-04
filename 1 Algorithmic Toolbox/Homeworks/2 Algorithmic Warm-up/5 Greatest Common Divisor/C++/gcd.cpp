#include <iostream>

int gcd(int a, int b) {
	if (b == 0) return a;
	int a_remainder = a % b;
	return gcd(b, a_remainder);
}

int main() {
	int a(0), b(0);
	std::cin >> a >> b;
	std::cout << gcd(a, b) << std::endl;
	return 0;
}
