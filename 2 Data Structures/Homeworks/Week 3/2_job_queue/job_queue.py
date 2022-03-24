# python3

from collections import namedtuple
import heapq

AssignedJob = namedtuple("AssignedJob", ["worker", "started_at"])


def assign_jobs_naive(n_workers, jobs):
    # TODO: replace this code with a faster algorithm.
    result = []
    next_free_time = [0] * n_workers
    for job in jobs:
        next_worker = min(range(n_workers), key=lambda w: next_free_time[w])
        result.append(AssignedJob(next_worker, next_free_time[next_worker]))
        next_free_time[next_worker] += job

    return result


def run_tests():
    test = namedtuple("Test", ("input", "output"))

    tests = [
        test(
            ((2, 5), [1, 2, 3, 4, 5]),
            (
                AssignedJob(0, 0),
                AssignedJob(1, 0),
                AssignedJob(0, 1),
                AssignedJob(1, 2),
                AssignedJob(0, 4),
            )
        ),
        test(
            ((4, 20), [1]*20),
            (
                AssignedJob(0, 0),
                AssignedJob(1, 0),
                AssignedJob(2, 0),
                AssignedJob(3, 0),
                AssignedJob(0, 1),
                AssignedJob(1, 1),
                AssignedJob(2, 1),
                AssignedJob(3, 1),
                AssignedJob(0, 2),
                AssignedJob(1, 2),
                AssignedJob(2, 2),
                AssignedJob(3, 2),
                AssignedJob(0, 3),
                AssignedJob(1, 3),
                AssignedJob(2, 3),
                AssignedJob(3, 3),
                AssignedJob(0, 4),
                AssignedJob(1, 4),
                AssignedJob(2, 4),
                AssignedJob(3, 4),
            )
        ),
    ]

    for test in tests:
        output = assign_jobs_naive(test.input[0][0], test.input[1])
        print()
        res = all([
            o[0] == t[0] and o[1] == t[1]
            for o, t in zip(output, test.output)
        ])
        assert res, f"{test}, output: {output}"

    print("Success!")


def main():
    n_workers, n_jobs = map(int, input().split())
    jobs = list(map(int, input().split()))
    assert len(jobs) == n_jobs

    assigned_jobs = assign_jobs(n_workers, jobs)

    for job in assigned_jobs:
        print(job.worker, job.started_at)


if __name__ == "__main__":
    # main()
    run_tests()
