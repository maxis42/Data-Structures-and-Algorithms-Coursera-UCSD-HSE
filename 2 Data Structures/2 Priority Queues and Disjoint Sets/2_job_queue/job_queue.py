# python3

from collections import namedtuple, deque

AssignedJob = namedtuple("AssignedJob", ["worker", "started_at"])


class Worker:
    def __init__(self, worker_id):
        self.worker_id = worker_id
        self.time = 0

    def __str__(self):
        return f"ID #{self.worker_id}, time: {self.time}"

    def __repr__(self):
        return f"ID #{self.worker_id} / time: {self.time}"


def assign_jobs_naive(n_workers, jobs):
    # TODO: replace this code with a faster algorithm.
    result = []
    next_free_time = [0] * n_workers
    for job in jobs:
        next_worker = min(range(n_workers), key=lambda w: next_free_time[w])
        result.append(AssignedJob(next_worker, next_free_time[next_worker]))
        next_free_time[next_worker] += job

    # print(result)
    return result


def left_child(i, n_workers):
    # i - left
    # 0 - 1
    # 1 - 3
    # 2 - 5
    left = i*2 + 1
    if left >= n_workers:
        return None
    return left


def right_child(i, n_workers):
    # i - right
    # 0 - 2
    # 1 - 4
    # 2 - 6
    right = i*2 + 2
    if right >= n_workers:
        return None
    return right


def update_worker_position(workers, n_workers):
    # sift down worker as its time could only increase or stay the same
    i = 0
    while True:
        left_i = left_child(i, n_workers)
        right_i = right_child(i, n_workers)
        # print(left_i, right_i)

        parent = workers[i]
        left = None
        if left_i is not None:
            left = workers[left_i]
        right = None
        if right_i is not None:
            right = workers[right_i]

        # left and right children
        if (left is not None) and (right is not None):
            # print("Both children!")
            if left.time < right.time:
                if parent.time < left.time:
                    break
                elif parent.time == left.time:
                    if parent.worker_id < left.worker_id:
                        break
                    else:
                        workers[i], workers[left_i] = workers[left_i], workers[i]
                        i = left_i
                else:
                    workers[i], workers[left_i] = workers[left_i], workers[i]
                    i = left_i
            elif left.time == right.time:
                if parent.time < left.time:
                    break
                elif parent.time == left.time:
                    if (parent.worker_id < left.worker_id) \
                            and (parent.worker_id < right.worker_id):
                        break
                    elif (left.worker_id < parent.worker_id) and (left.worker_id < right.worker_id):
                        workers[i], workers[left_i] = workers[left_i], workers[i]
                        i = left_i
                    else:
                        workers[i], workers[right_i] = workers[right_i], workers[i]
                        i = right_i
                else:
                    if left.worker_id < right.worker_id:
                        workers[i], workers[left_i] = workers[left_i], workers[i]
                        i = left_i
                    else:
                        workers[i], workers[right_i] = workers[right_i], workers[i]
                        i = right_i
            else:
                if parent.time < right.time:
                    break
                elif parent.time == right.time:
                    if parent.worker_id < right.worker_id:
                        break
                    else:
                        workers[i], workers[right_i] = workers[right_i], workers[i]
                        i = right_i
                else:
                    workers[i], workers[right_i] = workers[right_i], workers[i]
                    i = right_i

        # only left child
        elif left is not None:
            # print("Only left!")
            if parent.time < left.time:
                break
            elif parent.time == left.time:
                if parent.worker_id < left.worker_id:
                    break
                else:
                    workers[i], workers[left_i] = workers[left_i], workers[i]
                    i = left_i
            else:
                workers[i], workers[left_i] = workers[left_i], workers[i]
                i = left_i

        # no children
        else:
            # print("No children!")
            break


def assign_jobs_pq(n_workers, jobs):
    """
    Use priority queue.
    """
    result = []

    # data structure: priority queue
    # Priority corresponds to the min end time, thus first available
    # worker will be the root of the tree.
    # If there are several workers with the same end time, the one with
    # the lowest ID has the higher priority.
    workers = [Worker(i) for i in range(n_workers)]

    for job in jobs:
        # print(job, workers)
        worker = workers[0]

        start_time = worker.time
        worker.time += job

        update_worker_position(workers, n_workers)  # log(m)

        result.append(AssignedJob(worker.worker_id, start_time))

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
        # output = assign_jobs_naive(test.input[0][0], test.input[1])
        output = assign_jobs_pq(test.input[0][0], test.input[1])
        print()
        res = all([
            o[0] == t[0] and o[1] == t[1]
            for o, t in zip(output, test.output)
        ])
        assert res, f"{test}\noutput: {output}"

    print("Success!")


def main():
    n_workers, n_jobs = map(int, input().split())
    jobs = list(map(int, input().split()))
    assert len(jobs) == n_jobs

    assigned_jobs = assign_jobs_pq(n_workers, jobs)

    for job in assigned_jobs:
        print(job.worker, job.started_at)


if __name__ == "__main__":
    main()
    # run_tests()
