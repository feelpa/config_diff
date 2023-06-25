import argparse
import logging
import sys

import utils
from pyfgtconflib import Parser


class Colors:
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--old", required=True, help="filepath to older input file")
    parser.add_argument("-n", "--new", required=True, help="filepath to newer input file")
    args = parser.parse_args()

    logging.info(f"Beginning parsing {Colors.CYAN}{args.old}{Colors.RESET}...")
    with open(args.old, 'r') as old_file:
        config = Parser()
        config.parse_text(old_file)
        old_conf = config.section_dict
    logging.info(f"Parsing of {Colors.CYAN}{args.old}{Colors.RESET} {Colors.UNDERLINE}concluded{Colors.RESET}.")

    logging.info(f"Beginning parsing {Colors.CYAN}{args.new}{Colors.RESET}...")
    with open(args.new, 'r') as new_file:
        config = Parser()
        config.parse_text(new_file)
        new_conf = config.section_dict
    logging.info(f"Parsing of {Colors.CYAN}{args.new}{Colors.RESET} {Colors.UNDERLINE}concluded{Colors.RESET}.")

    logging.info(f"Ordering data in {Colors.CYAN}{args.old}{Colors.RESET}. It may take a moment...")
    old_conf_ordered = utils.recursively_order_dict(old_conf)
    logging.info(f"Ordering data in {Colors.CYAN}{args.old}{Colors.RESET} {Colors.UNDERLINE}concluded{Colors.RESET}.")

    logging.info(f"Ordering data in {Colors.CYAN}{args.new}{Colors.RESET}. It may take a moment...")
    new_conf_ordered = utils.recursively_order_dict(new_conf)
    logging.info(f"Ordering data in {Colors.CYAN}{args.new}{Colors.RESET} {Colors.UNDERLINE}concluded{Colors.RESET}.")

    logging.info("Start producing output files...")
    path = args.old.rsplit("/", maxsplit=1)[0:-1][0] + "/"
    name = ".ORDERED.".join(args.old.rsplit("/", maxsplit=1)[-1].split("."))
    old_path = path + name
    utils.prettyprint(old_conf_ordered, filename=old_path)
    logging.info(f"Writing file {Colors.GREEN}{old_path}{Colors.RESET} {Colors.UNDERLINE}concluded{Colors.RESET}.")

    path = args.new.rsplit("/", maxsplit=1)[0:-1][0] + "/"
    name = ".ORDERED.".join(args.new.rsplit("/", maxsplit=1)[-1].split("."))
    new_path = path + name
    utils.prettyprint(new_conf_ordered, filename=new_path)
    logging.info(f"Writing file {Colors.GREEN}{new_path}{Colors.RESET} {Colors.UNDERLINE}concluded{Colors.RESET}.")

    logging.info("Exiting now...")
    sys.exit(0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
