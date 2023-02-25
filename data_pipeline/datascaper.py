from bs4 import BeautifulSoup
import requests

BASE_URL = "http://premchand.co.in"
SAVE_PATH = "input/"

def get_story_urls():
    """Get all story urls from the site"""
    response = requests.get(BASE_URL + "/stories")
    soup = BeautifulSoup(response.text, "html.parser")
    story_urls = []
    for link in soup.find_all("a"):
        url = link.get("href")
        if url.startswith("/story/"):
            story_urls.append(url)
    return story_urls


def save_story(url, content):
    """Save the story to a file"""
    story_id = url.split("/")[-1]
    file_name = SAVE_PATH + story_id + ".txt"
    with open(file_name, "w") as f:
        f.write(content)

def get_story_content(url):
    """Get the content of a story"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    story_content = soup.find("p").text

    try:
        save_story(url, story_content)
        print("Saved story: ", url)
    except Exception as e:
        print("Error: ", e)



if __name__ == "__main__":
    story_urls_path = get_story_urls()
    # print(story_urls)
    final_story_urls = [BASE_URL + url for url in story_urls_path]
    # print(final_story_urls)
    for url in final_story_urls:
        get_story_content(url)
