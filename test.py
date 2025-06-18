import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_trial_links(query, max_results=10):
    base_url = "https://clinicaltrials.gov/ct2/results"
    params = {
        "cond": "acne vulgaris",
        "term": "H. pylori",
        "recrs": "a",  # All studies
        "displayxml": "true"
    }
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(base_url, params=params, headers=headers)
    print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")

    trials = soup.select(".ct-body3 a[href^='/ct2/show/']")
    links = ["https://clinicaltrials.gov" + tag['href'] for tag in trials[:max_results]]
    return links

def extract_trial_data(url):
    response = requests.get(url)
    print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").text.strip()
    enrollment_elem = soup.find("td", string="Enrollment")
    enrollment = (
        enrollment_elem.find_next_sibling("td").text.strip()
        if enrollment_elem else "Not found"
    )
    start_date_elem = soup.find("td", string="Start Date")
    start_date_str = (
        start_date_elem.find_next_sibling("td").text.strip()
        if start_date_elem else "Unknown"
    )

    try:
        start_date = datetime.strptime(start_date_str, "%B %Y")
    except:
        start_date = None

    return {
        "title": title,
        "url": url,
        "enrollment": enrollment,
        "start_date": start_date_str,
        "parsed_start": start_date
    }

def main():
    links = get_trial_links("H. pylori AND acne vulgaris", max_results=20)
    print(links)
    print(f"Found {len(links)} trials. Checking details...\n")

    for link in links:
        trial = extract_trial_data(link)
        if trial["parsed_start"] and datetime(2018, 1, 1) <= trial["parsed_start"] <= datetime(2018, 5, 31):
            print(f"Title: {trial['title']}")
            print(f"URL: {trial['url']}")
            print(f"Start Date: {trial['start_date']}")
            print(f"Enrollment: {trial['enrollment']}")
            print("-" * 80)

def gaia_benchmark_create():
    import json
    with open("gaia_benchmark/gaia_benchmark_validation.txt","r") as f:
        lines = f.readlines()

    level_1 = []
    level_2 = []
    level_3 = []  
    for line in lines:
        task = json.loads(line)
        match task["Level"]:
            case 1:
                #print(f"Level 1 question is: {task['file_name']}")
                level_1.append(json.dumps(task))
            case 2:
                #print(f"Level 2 question is: {task['file_name']}")
                level_2.append(json.dumps(task))
            case 3:
                #print(f"Level 3 question is: {task['file_name']}")
                level_3.append(json.dumps(task))
            case _:
                print(f"Unknown Level question is: {task['file_name']}")

    with open("gaia_benchmark/validation/level_1/tasks.txt","w") as f:
        for task in level_1:
            f.write(task)
            f.write("\n")

    with open("gaia_benchmark/validation/level_2/tasks.txt","w") as f:
        for task in level_2:
            f.write(task)
            f.write("\n")

    with open("gaia_benchmark/validation/level_3/tasks.txt","w") as f:
        for task in level_3:
            f.write(task)
            f.write("\n")

def question():
    pass


if __name__ == "__main__":
    gaia_benchmark_create()
    



