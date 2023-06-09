import os
import argparse
from problem import Problem



def main(url):  
    problem = Problem(url)
    if problem.platform:
        problem.process_problem()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Problem Link')
    args = parser.parse_args()
    main(args.url)