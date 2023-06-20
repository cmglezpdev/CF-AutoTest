import re
import requests
from bs4 import BeautifulSoup
from Platforms.platform import Platform

class Dmoj (Platform):
    pattern = r'https://dmoj.uclv.edu.cu/problem/([^/]*)'

    def is_valid_problem_url(self, url):
        if re.match(self.pattern, url):
            return True
        return False

    def get_test_cases(self, url):
        if not self.is_valid_problem_url(self, url):
            raise ValueError(f"{url} is not a valid dmoj problem url")

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        content_description = soup.find('div', {'class', 'content-description'})
        testscases = [pre.getText().strip() for pre in content_description.find_all('pre')]

        tests = []
        for i in range(0, len(testscases)):
            if i % 2 == 0 and i + 1 < len(testscases):
                tests.append((testscases[i], testscases[i + 1]))
        return tests


    def get_problem_id(self, url):
        match = re.search(self.pattern, url)
        if match:
            idContest = match.group(1)
            return idContest
        return None

    def get_time_memory_limits(self, url):
        if not self.is_valid_problem_url(self, url):
            raise ValueError(f"{url} is not a valid codeforces problem url")

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        limits = []
        for problem_info in soup.find_all('div', {'class', 'problem-info-entry'}):


            if problem_info.getText().strip().count("Time limit:") > 0:
                time_limit = problem_info.find('span', {'class', 'pi-value'})
                limits.append(float(time_limit.getText().strip()[:-1]) * 1000)
            elif (problem_info.getText()).count("Memory limit:") > 0:
                memory_limit = problem_info.find('span', {'class', 'pi-value'})
                limits.append(int(memory_limit.getText().strip()[:-1]) * 1024)

        # time limit, memory limit
        return (limits[0], limits[1])