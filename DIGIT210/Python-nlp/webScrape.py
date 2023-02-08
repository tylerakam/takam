# 2021-03-03 ebb: I'm adapting a script for downloading videos
# from GeeksforGeeks.org: https://www.geeksforgeeks.org/downloading-files-web-using-python/
# ebb: Before beginning, go out to your shell (Git Bash or Terminal) and enter:
# pip install BeautifulSoup4
import bs4
import requests
import os

# ebb: This variable stores the website address that you want to scrape.
archive_url = "http://www.textfiles.com/music/PINKFLOYD/"
# archive_url = "https://www.cs.cmu.edu/~spok/grimmtmp/"

def get_scripts():
    # create response object
    r = requests.get(archive_url)

    # create beautiful-soup object
    soup = bs4.BeautifulSoup(r.content, 'html.parser')

    # find all links on web-page
    # for ultag in soup.find_all('ul', {'class': 'a2z'}):
    # ultag = soup.find('ul', class_ = "a2z")
    # print(ultag)
    # for item in ultag.findAll('li'):
    #     link = item.find('a')
    #     href = archive_url + link['href']
    #     print(href)
    #     download_links(href)
    links = soup.findAll('a')
    hrefs = [archive_url + link['href'] for link in links]
    print(hrefs)
    for href in hrefs:
        download_links(href)
    print("Lyrics Downloaded")
    # ebb: After class I realized the print line indicating
    # all files downloaded needed to go after THIS loop finished.
    # Do you see why it makes sense and works here?
    # Hint: it has to do with when we call the function download_links(href)
def download_links(href):
    # obtain filename by splitting url and getting last string
    print(href)

    file_name = href.split('/')[-1]
    print("Downloading file: " + file_name)

    # create response object
    r = requests.get(href, stream = True)

    workingDir = os.getcwd()
    print("current working directory: " + workingDir)
    fileDeposit = os.path.join(workingDir, 'TWDep', file_name)
    print(fileDeposit)


    # download started
    with open(fileDeposit, 'wb') as f:
        for chunk in r.iter_content(chunk_size = 1024*1024):
            if chunk:
                f.write(chunk)
                print("Downloaded " + file_name)

    return

# ebb: Basically the line below initiates the whole program, sets it in motion.
# On the line if __name__ == "__main__": ,
# see: https://medium.com/@j.yanming/debugging-from-main-to-main-in-python-fe2a9784b36
if __name__ == "__main__":

    # getting all links to files
    get_scripts = get_scripts()






