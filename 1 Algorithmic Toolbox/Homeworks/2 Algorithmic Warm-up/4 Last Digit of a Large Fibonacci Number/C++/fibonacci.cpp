#include <iostream>
#include <vector>

using std::vector;

int fibonacci_last_digit(int n) {
	vector<int> fib_nums_last_dig(n + 1);
	fib_nums_last_dig[0] = 0;
	fib_nums_last_dig[1] = 1;
	for (int i = 2; i < n + 1; i++)
		fib_nums_last_dig[i] = (fib_nums_last_dig[i - 1] + fib_nums_last_dig[i - 2]) % 10;
	return fib_nums_last_dig[n];
}

int main() {
	int n = 0;
	std::cin >> n;
	std::cout << fibonacci_last_digit(n) << '\n';
	return 0;
}
