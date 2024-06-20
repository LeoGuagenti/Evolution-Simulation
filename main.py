import sys
from simulator import Simulator

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) >= 1: SEED = args[0]
    sim = Simulator()
    