import argparse
from .core import SortingVisualizer

def main():
    parser = argparse.ArgumentParser(description="Sorting Visualizer CLI")
    parser.add_argument("-a", "--array", type=int, nargs="+", required=True, help="Array (z.B. 7 2 5)")
    parser.add_argument("-alg", "--algorithm", choices=["bubble"], default="bubble", help="Algorithmus")
    
    args = parser.parse_args()
    sv = SortingVisualizer(args.array)
    
    if args.algorithm == "bubble":
        sorted_arr, steps = sv.bubble_sort()
    
    print(f"\nErgebnis ({args.algorithm}): {sorted_arr}")
    print(f"Schritte: {len(steps)}")

if __name__ == "__main__":
    main()
