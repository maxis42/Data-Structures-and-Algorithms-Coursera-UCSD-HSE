#include <iostream>
#include <vector>

using std::vector;
using std::cin;
using std::cout;

long long MaxPairwiseProduct(const vector<int> &numbers) {
	int n = numbers.size();

	int max_ind1 = -1;
	for (int i = 0; i < n; i++)
		if ( (max_ind1 == -1) || (numbers[i] > numbers[max_ind1]) )
			max_ind1 = i;

	int max_ind2 = -1;
	for (int i = 0; i < n; i++)
		if ( (i != max_ind1) && ((max_ind2 == -1) || (numbers[i] > numbers[max_ind2])) )
			max_ind2 = i;

	return (long long)numbers[max_ind1] * numbers[max_ind2];
}

int main() {
	int n;
	cin >> n;
	vector<int> numbers(n);
	for (int i = 0; i < n; ++i) {
		cin >> numbers[i];
	}

	long long result = MaxPairwiseProduct(numbers);
	cout << result << "\n";
	return 0;
}
