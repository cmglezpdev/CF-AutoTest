import os
import requests
import resource
import subprocess
from typing import Union

from Platforms import Platform, Codeforces, AtCoder
from veredict import print_veredict

class Problem:
    name:        str
    link:        str
    problemId:   str
    timeLimit:   int
    memoryLimit: int
    platform:    Union[Platform, None]
    testCases:   list[(str, str)]
    folder:      str
    code_file:   str

    def __init__(self, url: str):
        self.platform = self.select_platform(url)

        if self.platform:
            self.link = url
            self.problemId = self.platform.get_problem_id(self.platform, url)
            self.testCases = self.platform.get_test_cases(self.platform, url)
            time_limit, memory_limit = self.platform.get_time_memory_limits(self.platform, url)
            self.timeLimit = time_limit
            self.memoryLimit = memory_limit

            self._create_files(" ")

    def process_problem(self):
        modif_time = os.path.getmtime(self.code_file)
        
        while True:
            current_time = os.path.getatime(self.code_file)
            if modif_time < current_time:
                self._compile_test_cases()
                modif_time = current_time

    def _create_files(self, base: str):
        try:
            tests = self.testCases
            self.folder = self.problemId
            if not os.path.exists(self.folder):
                os.mkdir(self.problemId)

            for i, test in enumerate(tests):
                self._create_test_case_file(self.problemId, test, i)


            self.code_file = os.path.join(self.problemId, f"{self.problemId}.cpp")
            if not os.path.exists(self.code_file):
                with open(self.code_file, 'w'):
                    pass

            print(f"{len(tests)} were created in the directory {self.problemId}")

            # Create file for the solution

        except Exception as e:
            raise Exception(f"Fail to extract the tests cases. Error in the code: {e}")

    def _compile_test_cases(self):
        os.system('clear')
        binary: str = f"{self.folder}/{self.problemId}"
        compile_result = subprocess.run(["g++", self.code_file, "-o", binary], stderr=subprocess.PIPE)
        
        if compile_result.returncode != 0:
            error_message = compile_result.stderr.decode()
            print(error_message)
            print_veredict("CE")
        else:
            for test in self._scan_test_cases():
                (finput, fanswer) = test
                print(f"========= START DATA SET #{finput[-5]} =========")
                
                try:
                    with open(finput, "r") as input_file:
                        resource.setrlimit(resource.RLIMIT_AS, (self.memoryLimit * 1024, self.memoryLimit * 1024))
                        result = subprocess.run([binary], timeout=self.timeLimit / 1000, stdin=input_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        
                        time_used = resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime
                        memory_used = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
                        
                        result_stout = result.stdout.decode()
                        result_stderr = result.stderr.decode()

                        if result_stderr:
                            print(result_stout, result_stderr)
                            print_veredict("RE")
                        elif self.memoryLimit < memory_used:
                            print_veredict("MLE")
                        else:
                            output_filename = f"{self.folder}/output.txt"
                            with open(output_filename, "w") as output:
                                output.write(result_stout)

                            print(result_stout)
                            if self._compare_file_content(output_filename, fanswer):
                                print_veredict("AC")
                            else:
                                print_veredict("WA")

                            print("Tiempo utilizado: ", (int)(time_used * 1000), "ms")
                            print("Memoria utilizada: ", memory_used, "KB")
                            
                            os.remove(output_filename)

                except subprocess.TimeoutExpired:
                    print_veredict("TLE")

                print(f"========= END DATA SET #{finput[-5]} =========", "\n")

    def _scan_test_cases(self) -> list[(str, str)]:
        txts = [file for file in os.listdir(self.folder) if file.endswith(".txt")]
        inputs =  [file for file in txts if file.startswith("input")]
        answers = [file for file in txts if file.startswith("answer")]

        tests: list[(str, str)] = []
        for input in inputs:
            end = input[len("input"):]
            if answers.count("answer" + end) == 1:
                tests.append((f"{self.folder}/{input}", f"{self.folder}/answer{end}"))

        tests.sort(key=lambda a: a[0]);
        return tests

    def _compare_file_content(self, file1: str, file2: str) -> bool:
        f1 = open(file1, "r")
        f2 = open(file2, "r")
        f1_content = f1.read()
        f2_content = f2.read()
        f1.close()
        f2.close()

        if f1_content.rstrip() == f2_content.rstrip():
            return True
        return False

    def _create_test_case_file(self, folder: str, test: str, index: int):
        input_filename = os.path.join(folder, f"input.{index + 1}.txt")        
        answer_filename = os.path.join(folder, f"answer.{index + 1}.txt")        
        with open(input_filename, 'w') as input_file:
            input_file.write(test[0])
        with open(answer_filename, 'w') as answer_file:
            answer_file.write(test[1])

    @staticmethod
    def select_platform(url: str) -> Union[Platform, None]:
        return Codeforces
