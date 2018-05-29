#include <iostream>
#include <vector>

using std::vector;

unsigned long long int get_fib_mod(unsigned long n, unsigned int m) {
	vector<unsigned int> remainders(6 * m);
	remainders[0] = 0;
	remainders[1] = 1;

	unsigned int period = 0;

	for (unsigned int i = 2; i < 6 * m; i++) {
		remainders[i] = (remainders[i - 2] + remainders[i - 1]) % m;
		period++;
		if (remainders[i - 1] == 0 && remainders[i] == 1) break;
	}

	return remainders[n % period];
}

int main() {
	unsigned long n(0);
	unsigned int m(0);
	std::cin >> n >> m;
	std::cout << get_fib_mod(n, m) << std::endl;
	return 0;
}
