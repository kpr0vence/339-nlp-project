import requests
from bs4 import BeautifulSoup
import time
import os
import re

links_to_crawl = []
links_crawled = []
broken_links = []
numbers_found = []


def crawl_url(url):
    global links_to_crawl, links_crawled, broken_links
    print("Crawling:", url)
    # user_agent makes it seem like the request is coming from a web browser (versus a bot)
    user_agent = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=user_agent, timeout=10)
        html = response.content
        extract_links_and_add_to_crawl_list(html)
        extract_text_from_html(html)
    except:
        broken_links.append(url)
        print("Broken link:", url)

    # output the links:
    print("Num links to crawl:", len(links_to_crawl))
    print("Num links crawled:", len(links_crawled))
    print("Num broken links:", len(broken_links))
    
    choice = input("Press Enter to crawl the next link or 'q' to quit...")
    if choice.lower() == 'q':
        print("Quitting...")
        save_lists()
        save_findings()
        return
    
    if len(links_to_crawl) > 0:
        url = links_to_crawl.pop(0)
        links_crawled.append(url)
        crawl_url(url)

def extract_links_and_add_to_crawl_list(html):
    
    soup = BeautifulSoup(html, "html.parser")

    # Find all <li> tags
    a_tags = soup.select("a")

    # Extract hrefs from their inner <a> tags
    hrefs = [a.get("href") for a in a_tags]
    for href in hrefs:
        # don't crawl internal links
        if href.startswith("#"):
            continue

        # add base URL if it's a relative link:
        if href.startswith("/"):
            href = 'https://www.stilltasty.com/' + href

        # if the link hasn't been crawled yet, add it to the list of links to crawl:
        if href not in links_crawled:
            links_to_crawl.append(href)

def extract_text_from_html(html):
    # do something smart with the html here:
    soup = BeautifulSoup(html, "html.parser")
    header2 = soup.find("h2").get_text().strip()
    main = soup.find("body")
    if main:
        print("Body Found")
        print(header2)
        get_words_around_numbers(main.get_text(), header2)
    else:
        print("No container body found")

def get_words_around_numbers(text, title):
    global numbers_found
    # We have the whole text
    # Try to get the h2 tag to use as a label

    # Anywhere we spot a number, get the surrounding 2 words on each side
    targets = re.findall(r"\s*\S+\s*\S+\s*\d\s*\S+\s*\S+s*\S+\s*\S+", text)
    print(f"Targets: {targets}")
    numbers_found.insert(title, targets)
    

def load_lists():
    global links_to_crawl, links_crawled, broken_links
    if os.path.exists("links_to_crawl.txt"):
        with open("links_to_crawl.txt", "r") as f:
            links_to_crawl = [line.strip() for line in f.readlines()]
    else:
        links_to_crawl = []
    
    if os.path.exists("links_crawled.txt"):
        with open("links_crawled.txt", "r") as f:
            links_crawled = [line.strip() for line in f.readlines()]
    else:
        links_crawled = []
    
    if os.path.exists("broken_links.txt"):
        with open("broken_links.txt", "r") as f:
            broken_links = [line.strip() for line in f.readlines()]
    else:
        broken_links = []

    print("Number of links to crawl:", len(links_to_crawl))
    print("Number of links crawled:", len(links_crawled))
    print("Number of broken links:", len(broken_links))

def save_lists():
    with open("links_to_crawl.txt", "w") as f:
        for link in links_to_crawl:
            f.write(link + "\n")
    with open("links_crawled.txt", "w") as f:
        for link in links_crawled:
            f.write(link + "\n")
    with open("broken_links.txt", "w") as f:
        for link in broken_links:
            f.write(link + "\n")

# RN it just overwrites.
def save_lists():
    with open("findings.txt", "w") as f:
        for finding in numbers_found:
            f.write(finding + "\n")

if __name__ == "__main__":
    load_lists()
    crawl_url("https://www.stilltasty.com/")
