import os
import sys
import time
import random

def clear_console():
    command = 'cls' if os.name in ('nt', 'dos') else 'clear'
    os.system(command)

def typing_print(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def random_8d_vector_generator(n=None):
    """
    Generator that yields random 8-dimensional float vectors.
    :param n: Optional number of vectors to generate. If None, generates indefinitely.
    """
    count = 0
    while n is None or count < n:
        yield [random.uniform(-1, 1) for _ in range(8)]
        count += 1

if __name__ == "__main__":
    clear_console()
    print("~$ ", end="")
    time.sleep(5)

    typing_print("raic-foundry inference start naip-geospatial-imagery")

    print()
    print("------------------------------------------------------")
    print()
    print("  Welcome to the RAIC Foundry")
    print()
    print("------------------------------------------------------")
    print()
    time.sleep(0.5)

    print("Finding objects...")
    print()
    time.sleep(0.5)

    print("Generating searchable embeddings...")
    print()
    time.sleep(0.5)

    vector_iterator = random_8d_vector_generator(50)
    for vector in vector_iterator:
        print(vector)
        time.sleep(0.05)

    print()
    print("~$ ", end="")
    time.sleep(5)
 


