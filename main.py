import os
import argparse
from veredict import print_veredict
from problem import Problem

import subprocess
import resource

def scan_test_cases(folder: str) -> list[(str, str)]:
    txts = [file for file in os.listdir(folder) if file.endswith(".txt")]
    inputs =  [file for file in txts if file.startswith("input")]
    answers = [file for file in txts if file.startswith("answer")]

    tests: list[(str, str)] = []
    for input in inputs:
        end = input[len("input"):]
        if answers.count("answer" + end) == 1:
            tests.append((f"{folder}/{input}", f"{folder}/answer{end}"))

    tests.sort(key=lambda a: a[0]);
    return tests

def compare_file_content(file1: str, file2: str) -> bool:
    f1 = open(file1, "r")
    f2 = open(file2, "r")
    f1_content = f1.read()
    f2_content = f2.read()
    f1.close()
    f2.close()

    if f1_content.rstrip() == f2_content.rstrip():
        return True
    return False


def compile_test_cases(problem: Problem):
    os.system('clear')
    binary: str = f"{problem.folder}/{problem.problemId}"
    compile_result = subprocess.run(["g++", problem.code_file, "-o", binary], stderr=subprocess.PIPE)
    
    if compile_result.returncode != 0:
        error_message = compile_result.stderr.decode()
        print(error_message)
        print_veredict("CE")
    else:
        for test in scan_test_cases(problem.folder):
            (finput, fanswer) = test
            print(f"========= START DATA SET #{finput[-5]} =========")
            
            try:
                with open(finput, "r") as input_file:
                    # Establecer límite de memoria en 1 GB (1000000000 bytes)
                    memory_limit = 1000000000
                    resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
                    result = subprocess.run([binary], timeout=1, stdin=input_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    
                    time_used = resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime
                    memory_used = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
                    
                    result_stout = result.stdout.decode()
                    result_stderr = result.stderr.decode()

                    if result_stderr:
                        print(result_stout, result_stderr)
                        print_veredict("RE")
                    elif memory_limit < memory_used:
                        print_veredict("MLE")
                    else:
                        output_filename = f"{problem.folder}/output.txt"
                        with open(output_filename, "w") as output:
                            output.write(result_stout)

                        print(result_stout)
                        if compare_file_content(output_filename, fanswer):
                            print_veredict("AC")
                        else:
                            print_veredict("WA")

                        print("Tiempo utilizado: ", (int)(time_used * 1000), "ms")
                        print("Memoria utilizada: ", memory_used, "KB")
                        
                        os.remove(output_filename)

            except subprocess.TimeoutExpired:
                print_veredict("TLE")

            print(f"========= END DATA SET #{finput[-5]} =========", "\n")



def process_problem(problem: Problem):
    modif_time = os.path.getmtime(problem.code_file)
    
    while True:
        current_time = os.path.getatime(problem.code_file)
        if modif_time < current_time:
            compile_test_cases(problem)
            modif_time = current_time

def main(url):  
    problem = Problem(url)
    if problem.platform:
        process_problem(problem)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Problem Link')
    args = parser.parse_args()
    main(args.url)