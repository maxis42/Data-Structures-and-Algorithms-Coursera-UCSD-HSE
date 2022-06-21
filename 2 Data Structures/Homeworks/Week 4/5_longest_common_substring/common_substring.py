# python3

import sys
from collections import namedtuple
import random

Test = namedtuple("Test", "s t output")
Answer = namedtuple("answer_type", "i j len")


class Solver:
	# _multiplier = random.randint(1, 10**9)
	_multiplier = 1234
	_prime1 = 87178291199
	_prime2 = 3314192745739

	def __init__(self, s1, s2):
		self.s1 = s1
		self.s2 = s2

		self.max_len = min(len(self.s1), len(self.s2))

		self.hashes_s1_1 = self._precompute_hashes(self.s1, self._prime1)
		self.hashes_s1_2 = self._precompute_hashes(self.s1, self._prime2)

		self.hashes_s2_1 = self._precompute_hashes(self.s2, self._prime1)
		self.hashes_s2_2 = self._precompute_hashes(self.s2, self._prime2)

	def _precompute_hashes(self, string, prime):
		hashes = [0 for _ in range(len(string) + 1)]
		for i in range(1, len(string) + 1):
			hashes[i] = (
				self._multiplier * hashes[i - 1]
				+ ord(string[i - 1])
			) % prime
		return hashes

	def _precompute_substring_hashes(self, hashes, len_, prime):
		hashes_ss = dict()
		for i in range(len(hashes) - len_):
			hashes_ss[self._calc_substring_hash(hashes, prime, i, len_)] = i
		return hashes_ss

	@staticmethod
	def _modular_exponentitation(a, b, n):
		"""
		a**b mod n
		"""
		d = 1
		b = str(bin(b))[2:]
		for i in range(len(b)):
			d = (d * d) % n
			if int(b[i]) == 1:
				d = (d * a) % n
		return d

	def _calc_substring_hash(self, hashes, prime, start, length):
		y = self._modular_exponentitation(self._multiplier, length, prime)
		substring_hash = (hashes[start + length] - y * hashes[start]) % prime
		return substring_hash

	def longest_common_substring(self):
		answer = Answer(0, 0, 0)

		a = 1
		b = self.max_len

		while a <= b:
			len_ = (a + b) // 2
			# if not len_:
			# 	break

			found = False

			hashes_ss1_1 = self._precompute_substring_hashes(self.hashes_s1_1, len_, self._prime1)
			hashes_ss2_1 = self._precompute_substring_hashes(self.hashes_s2_1, len_, self._prime1)

			same_hash1 = set(hashes_ss1_1).intersection(hashes_ss2_1)

			if same_hash1:
				ind = same_hash1.pop()
				i = hashes_ss1_1[ind]
				j = hashes_ss2_1[ind]

				hashes_ss1_2 = self._calc_substring_hash(self.hashes_s1_2, self._prime2, i, len_)
				hashes_ss2_2 = self._calc_substring_hash(self.hashes_s2_2, self._prime2, j, len_)

				same_hash2 = (hashes_ss1_2 == hashes_ss2_2)

				if same_hash2 and (len_ > answer.len):
					answer = Answer(i, j, len_)
					found = True

			# print(a, b, len_, found)
			if found:
				a = len_ + 1
			else:
				b = len_ - 1

		return answer


def solve_naive(s1, s2):
	ans = Answer(0, 0, 0)
	for i in range(len(s1)):
		for j in range(len(s2)):
			for l in range(min(len(s1) - i, len(s2) - j) + 1):
				if (l > ans.len) and (s1[i:i+l] == s2[j:j+l]):
					ans = Answer(i, j, l)
	return ans


def run_tests():
	tests = [
		("cool", "toolbox", (1, 1, 3)),
		("aaa", "bb", (0, 0, 0)),
		# ("aabaa", "babbaab", (0, 4, 3)),
		("aabaa", "babbaab", (2, 3, 3)),
		("zsaizkvr", "ugxnv", (6, 4, 1)),
	]

	for s1, s2, output in tests:
		# answer = solve_naive(s1, s2)
		answer = Solver(s1, s2).longest_common_substring()
		answer = (answer.i, answer.j, answer.len)
		assert answer == output, f"""
		Input: s1={s1} | s2={s2}
		Expected: {output}
		Got:      {answer}
		"""
		print("Test passed!\n")


def run_stress_test():
	# alphabet = "abcdefghigklmnopqrstuvwxyz"
	alphabet = "abcde"
	while True:
		s1 = "".join([random.choice(alphabet) for _ in range(random.randint(0, 5))])
		s2 = "".join([random.choice(alphabet) for _ in range(random.randint(0, 5))])
		answer = Solver(s1, s2).longest_common_substring()
		assert answer.len == solve_naive(s1, s2).len
		assert s1[answer.i:answer.i+answer.len] == s2[answer.j:answer.j+answer.len], f"""
				Input: s1={s1} | s2={s2}
				Got:      {answer}
				"""
		print(f"Input: s1={s1} | s2={s2}\nEqual: {s1[answer.i:answer.i+answer.len]}")
		print("Test passed!\n")


def run_algo():
	for line in sys.stdin.readlines():
		s1, s2 = line.split()
		answer = Solver(s1, s2).longest_common_substring()
		print(answer.i, answer.j, answer.len)


if __name__ == "__main__":
	run_algo()
	# run_tests()
	# run_stress_test()
