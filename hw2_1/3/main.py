import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
    with open(filename, "a") as f:
        f.write("Hello, docker\n")
        f.close()
