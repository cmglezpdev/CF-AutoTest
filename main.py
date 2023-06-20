import argparse
from problem import Problem

def main(url):  
    # AtCoder.getTestCases(url)
    problem = Problem(url)
    print(problem.problemId)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Problem Link')
    args = parser.parse_args()
    main(args.url)