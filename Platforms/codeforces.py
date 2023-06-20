import re
import requests
from bs4 import BeautifulSoup
from Platforms.platform import Platform

class Codeforces (Platform):
    name = "CODEFORCES"
    url_patterns = [
        r'https://codeforces.com/problemset/problem/(\d+)/([A-Z0-9]+)',
        r'https://codeforces.com/contest/(\d+)/problem/([A-Z0-9]+)',
        r'https://codeforces.com/gym/(\d+)/problem/([A-Z0-9]+)'
    ]

    # def __init__(self, url: str) -> None:

    def is_valid_problem_url(self, url):
        for p in self.url_patterns:
            if re.match(p, url):
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
        for p in self.url_patterns:
            match = re.search(p, url)
            if match:
                idContest = match.group(1)
                idProblem = match.group(2)
                return idContest + idProblem
        return None

    def get_time_memory_limits(self, url):
        if not self.is_valid_problem_url(self, url):
            raise ValueError(f"{url} is not a valid codeforces problem url")

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        time_limit_div = soup.find('div', {'class', 'time-limit'}) 
        memory_limit_div = soup.find('div', {'class', 'memory-limit'})

        time_limit   = int(time_limit_div.contents[1].split(" ")[0]) * 1000
        memory_limit = int(memory_limit_div.contents[1].split(" ")[0]) * 1024
        
        return (time_limit, memory_limit)