#! /usr/bin/env python3

import sys

if __name__ == "__main__":
    if sys.version_info < (3, 6):
        print(f"Netora requires Python 3.6+\nYou are using Python {sys.version.split()[0]}, which is not supported.")
        sys.exit(1)

    from netora import netora
    netora.main()