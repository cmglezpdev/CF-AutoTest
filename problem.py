import os
import requests
from typing import Union
from Platforms import Platform, Codeforces, AtCoder

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
            self.create_files(" ")


    def create_files(self, base: str):
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

    @staticmethod
    def select_platform(url: str) -> Union[Platform, None]:
        return Codeforces

    def _create_test_case_file(self, folder: str, test: str, index: int):
        input_filename = os.path.join(folder, f"input.{index + 1}.txt")        
        answer_filename = os.path.join(folder, f"answer.{index + 1}.txt")        
        with open(input_filename, 'w') as input_file:
            input_file.write(test[0])
        with open(answer_filename, 'w') as answer_file:
            answer_file.write(test[1])
