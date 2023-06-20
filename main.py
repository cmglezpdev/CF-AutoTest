import os
import argparse
from problem import Problem



def main(url):  
    if Problem.select_platform(url):
        problem = Problem(url)
        problem.process_problem()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Problem Link')
    args = parser.parse_args()
    main(args.url)