from src import ADT
import time
import matplotlib.pyplot as plt

def test_performance(type):
    running_times = []

    # Increase size of n in increments.
    for n in range (0, 10000, 10):
        stack = type

        start = time.time()
        for i in range(n):
            stack.push(i)
            stack.pop()
        end = time.time()

        run_time = end - start
        print(n, run_time)
        running_times.append(run_time)

    # Plot the running times
    plt.plot(running_times, 'bx')
    plt.xlabel('Size of N (x 1000)')
    plt.ylabel('Time')
    plt.show()

# test_performance(ADT.ArrayStack())
test_performance(ADT.LinkedStack())
