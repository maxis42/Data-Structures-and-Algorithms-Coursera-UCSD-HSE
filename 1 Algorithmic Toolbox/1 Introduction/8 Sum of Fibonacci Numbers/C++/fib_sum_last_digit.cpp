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

int main() {
	unsigned long long n(0);
	std::cin >> n;
	std::cout << get_fib_sum_last_digit(n) << std::endl;
	return 0;
}
