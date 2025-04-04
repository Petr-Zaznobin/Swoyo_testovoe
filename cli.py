import argparse
from argparse import Namespace
from pprint import pprint

def main() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_send", help="Number of sender (str)", type=str)
    parser.add_argument("--num_receive", help="Number of receiver (str)", type=str)
    parser.add_argument("--text", help="Text, you need to send (str)", type=str)

    parsed_args = parser.parse_args()

    return parsed_args

if __name__ == "__main__":
    args: Namespace = main()
    pprint(args, sort_dicts=False)