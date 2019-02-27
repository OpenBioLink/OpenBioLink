import os
import sys
import argparse

basic_path= 'C:\\Users\\anna\\PycharmProjects\\knowledge-graph-embeddings\\src'

sys.path.insert(0, os.path.join(basic_path, 'models'))

import base_model


def do_print(args):
    print(args.a)
    print(args.b)
    print(args)

def get_args_parser ():
    p = argparse.ArgumentParser('Link prediction models')
    p.add_argument('--a', default='foo', type=str, help='training mode ["pairwise", "single"]')
    p.add_argument('--b')
    p.add_argument('--c', default='bar')
    return p

def man_arg_parse(args_list= None):
    p = get_args_parser()
    if args_list:
        args= p.parse_args(args_list)
    else:
        args = p.parse_args()
    do_print(args)



def do_stuff(args):
    print(args.u)
    print(args.p)


def main(args_list=None):
    parser = argparse.ArgumentParser(description='get data', add_help=False,
                                     usage='this_script.py -u username -p password [options]')
    parser.add_argument('-u', type=bool, help='username')
    parser.add_argument('-p', type=str, help='password')
    parser.add_argument('-i', nargs='+', type=str, help='List of IDs')
    ...

    if args_list:
        args = parser.parse_args(args_list)
    else:
        args = parser.parse_args()

    do_stuff(args)


if __name__ == "__main__":
    main()






