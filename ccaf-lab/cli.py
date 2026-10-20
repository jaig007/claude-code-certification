"""Command-line interface for the calculator library."""

import argparse
import sys

from calc import add, subtract, multiply, divide, power, average


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="cli.py",
        description="Simple calculator — run operations from the command line.",
    )
    sub = parser.add_subparsers(dest="operation", metavar="OPERATION")
    sub.required = True

    for name in ("add", "subtract", "multiply", "divide", "power"):
        p = sub.add_parser(name, help=f"Perform {name} on two numbers.")
        p.add_argument("a", type=float)
        p.add_argument("b", type=float)

    avg = sub.add_parser("average", help="Compute the mean of one or more numbers.")
    avg.add_argument("numbers", type=float, nargs="+")

    return parser


def main() -> None:
    """Parse arguments, call the matching function, and print the result."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.operation == "add":
            result = add(args.a, args.b)
        elif args.operation == "subtract":
            result = subtract(args.a, args.b)
        elif args.operation == "multiply":
            result = multiply(args.a, args.b)
        elif args.operation == "divide":
            result = divide(args.a, args.b)
        elif args.operation == "power":
            result = power(args.a, args.b)
        elif args.operation == "average":
            result = average(args.numbers)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(result)


if __name__ == "__main__":
    main()
