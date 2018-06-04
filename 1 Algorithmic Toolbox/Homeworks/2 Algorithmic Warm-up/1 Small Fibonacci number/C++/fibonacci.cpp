#include <iostream>
#include <vector>

using std::vector;

int fibonacci_naive(int n) {
	if (n <= 1)
		return n;

	return fibonacci_naive(n - 1) + fibonacci_naive(n - 2);
}

int fibonacci_fast(int n) {
	vector<int> fib_nums(n + 1);
	fib_nums[0] = 0;
	fib_nums[1] = 1;
	for (int i = 2; i < n + 1; i++)
		fib_nums[i] = fib_nums[i - 1] + fib_nums[i - 2];
	return fib_nums[n];
}

int main() {
	int n = 0;
	std::cin >> n;
	std::cout << fibonacci_fast(n) << '\n';
	return 0;
}
