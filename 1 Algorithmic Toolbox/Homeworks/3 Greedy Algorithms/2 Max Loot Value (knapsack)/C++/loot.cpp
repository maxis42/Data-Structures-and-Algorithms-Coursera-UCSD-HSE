#include <iostream>
#include <vector>
#include <algorithm>

using std::vector;
using std::max_element;

double get_optimal_value(unsigned long capacity, vector<unsigned long> weights, vector<unsigned long> values) {
	double value = 0.0;
	int n = weights.size();
	std::cout << n;
	vector<double> cost(n);
	for (int i = 0; i < n; ++i) cost[i] = (double)values[i] / weights[i];

	for (int i = 0; i < n; ++i) std::cout << cost[i];
	for (int j = 0; j < n; ++j) {
		if (capacity == 0) return value;
		int indMaxCost = *max_element(cost.begin(), cost.end());
		double capacityReduction = 0;
		if (weights[indMaxCost] >= capacity) capacityReduction = capacity;
		else capacityReduction = weights[indMaxCost];
		std::cout << capacityReduction << std::endl;
		capacity -= capacityReduction;
		value += capacityReduction * cost[indMaxCost];
		cost.erase(cost.begin() + indMaxCost);
		for (int i = 0; i < n; ++i) std::cout << cost[i];
	}

	return value;
}

int main() {
	int n;
	unsigned long capacity;
	std::cin >> n >> capacity;
	vector<unsigned long> values(n);
	vector<unsigned long> weights(n);
	for (int i = 0; i < n; i++) {
		std::cin >> values[i] >> weights[i];
	}

	double optimal_value = get_optimal_value(capacity, weights, values);

	std::cout.precision(10);
	std::cout << optimal_value << std::endl;
	return 0;
}
