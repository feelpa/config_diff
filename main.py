import argparse

import utils
from pyfgtconflib import Parser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--old", required=True, help="filepath to older input file")
    parser.add_argument("-n", "--new", required=True, help="filepath to newer input file")
    args = parser.parse_args()

    with open(args.old, 'r') as old_file:
        config = Parser()
        config.parse_text(old_file)
        old_conf = config.section_dict

    with open(args.new, 'r') as new_file:
        config = Parser()
        config.parse_text(new_file)
        new_conf = config.section_dict

    old_conf_ordered = utils.recursively_order_dict(old_conf)
    new_conf_ordered = utils.recursively_order_dict(new_conf)

    utils.prettyprint(old_conf_ordered, filename="old.conf")
    utils.prettyprint(new_conf_ordered, filename="new.conf")


if __name__ == "__main__":
    main()
