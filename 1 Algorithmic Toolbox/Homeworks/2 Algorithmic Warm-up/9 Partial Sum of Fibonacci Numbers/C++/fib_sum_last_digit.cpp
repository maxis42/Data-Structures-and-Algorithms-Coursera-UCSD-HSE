#include <iostream>
#include <vector>

using std::vector;

unsigned long long get_fib_sum_last_digit(unsigned long long n) {
	if (n <= 1) return n;

	vector<unsigned int> remainders(6 * 10);
	remainders[0] = 0;
	remainders[1] = 1;

	int remainder_period_sum = 1;
	int remainder_sum = 0;

	for (unsigned int i = 2; i < 6 * 10; i++) {
		remainders[i] = (remainders[i - 2] + remainders[i - 1]) % 10;
		remainder_period_sum += remainders[i];
	}

	for (unsigned int i = 0; i < n % 60 + 1; i++) {
		remainder_sum += remainders[i];
	}

	return ((remainder_period_sum * (n / 60) + (unsigned long long)remainder_sum) % 10);
}

unsigned long long get_fib_part_sum_last_digit(unsigned long long m, unsigned long long n) {
	unsigned long long a = get_fib_sum_last_digit(n);
	unsigned long long b = get_fib_sum_last_digit(m - 1);
	if (a >= b) return (a - b);
	else return (10 - (b - a));
}


int main() {
	unsigned long long n(0), m(0);
	std::cin >> m >> n;
	std::cout << get_fib_part_sum_last_digit(m, n) << std::endl;
	return 0;
}
