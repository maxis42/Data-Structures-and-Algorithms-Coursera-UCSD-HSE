#include <iostream>

unsigned long long int gcd(unsigned long long int a, unsigned long long int b) {
	if (b == 0) return a;
	unsigned long long int a_remainder = a % b;
	return gcd(b, a_remainder);
}

unsigned long long int lcm(unsigned long long int a, unsigned long long int b) {
	return a == b && b == 0 ? a : a * b / gcd(a, b);
}

int main() {
	unsigned long long int a(0), b(0);
	std::cin >> a >> b;
	std::cout << lcm(a, b) << std::endl;
	return 0;
}
