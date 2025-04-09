import argparse
from .core import Sort

def main() -> None:
    parser = argparse.ArgumentParser(description="Sorting Visualizer CLI")
    parser.add_argument("-a", "--array", type=int, nargs="+", required=True, help="Array (z.B. 7 2 5)")
    parser.add_argument("-alg", "--algorithm", choices=["bubble", "quick", "merge", "heap", "shell", "radix"], default="bubble", help="Sorting algorithm")
    
    args: argparse.Namespace = parser.parse_args()
    sv = Sort(args.array)
    
    if args.algorithm == "bubble":
        sorted_arr, steps = sv.bubble_sort()
    elif args.algorithm == "quick":
        sorted_arr, steps = sv.quick_sort()
    elif args.algorithm == "merge":
        sorted_arr, steps = sv.merge_sort()
    elif args.algorithm == "heap":
        sorted_arr, steps = sv.heap_sort()
    elif args.algorithm == "shell":
        sorted_arr, steps = sv.shell_sort()
    elif args.algorithm == "radix":
        sorted_arr, steps = sv.radix_sort()
    else:
        sorted_arr, steps = sv.bubble_sort()
        

    print(f"\nResult ({args.algorithm}): {sorted_arr}")
    print(f"Steps: {len(steps)}")

if __name__ == "__main__":
    main()
