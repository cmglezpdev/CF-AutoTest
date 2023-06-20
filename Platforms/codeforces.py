import os
import re
import requests
from bs4 import BeautifulSoup
from Platforms.platform import Platform

class Codeforces (Platform):
    pProblemset = r'https://codeforces.com/problemset/problem/(\d+)/([A-Z0-9]+)'
    pContest = r'https://codeforces.com/contest/(\d+)/problem/([A-Z0-9]+)'
    pGym = r'https://codeforces.com/gym/(\d+)/problem/([A-Z0-9]+)'

    def is_valid_problem_url(self, url):
        if re.match(self.pProblemset, url) or re.match(self.pContest, url) or re.match(self.pGym, url):
            return True
        return False

    def get_test_cases(self, url):
        if not self.is_valid_problem_url(self, url):
            raise ValueError(f"{url} is not a valid codeforces problem url")

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Extract the test cases
        test_section = soup.find('div', {'class', 'sample-test'})
        inputTests = []
        outputTests = []

        # Extract inputs test case 
        for inputTest in test_section.find_all('div', {'class' : 'input'}):
            textCase = ""
            if len(inputTest.find('pre').find_all('div')) > 0:
                for line in inputTest.find('pre').find_all('div'):
                    textCase += line.text.strip() + '\n'
            else:
                for line in inputTest.find('pre').contents:
                    if line.getText().strip() != "":
                        textCase += line.getText().strip() + '\n'
            inputTests.append(textCase)


        # Extract inputs test case 
        for outputTest in test_section.find_all('div', {'class' : 'output'}):
            textCase = ""
            if len(outputTest.find('pre').find_all('div')) > 0:
                for line in outputTest.find('pre').find_all('div'):
                    textCase += line.text.strip() + '\n'
            else:
                for line in outputTest.find('pre').contents:
                    if line.getText().strip() != "":
                        textCase += line.getText().strip() + '\n'
            outputTests.append(textCase)

        tests = []
        for i in range(0, len(inputTests)):
            tests.append((inputTests[i], outputTests[i]))
        return tests

    def get_problem_id(self, url):
        match1 = re.search(self.pProblemset, url)
        if match1:
            idContest = match1.group(1)
            idProblem = match1.group(2)
            return idContest + idProblem

        match2 = re.search(self.pContest, url)
        if match2:
            idContest = match2.group(1)
            idProblem = match2.group(2)
            return idContest + idProblem

        match3 = re.search(self.pGym, url)
        if match3:
            idContest = match3.group(1)
            idProblem = match3.group(2)
            return idContest + idProblem

        return None




