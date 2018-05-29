#include <iostream>

int get_change(int m) {
	int typesOfCoins[3] = {10, 5, 1};
	int counterOfCoins(0), curType(0);

	while (m != 0) {
		if (m / typesOfCoins[curType] != 0) {
			counterOfCoins++;
			m -= typesOfCoins[curType];
		}
		else curType++;
	}

	return counterOfCoins;
}

int main() {
	int m;
	std::cin >> m;
	std::cout << get_change(m) << '\n';
}