import requests
from bs4 import BeautifulSoup
from Sepidar import Sepidar

class search:
    def __init__(self, text, page=1,*args, **kwargs) -> dict:
        """
        Run library
        ```python
        from Music_search import search
        result = search("name music and artist")
        print(result)

        ```
        """
        self.text = text
        self.page = page
        self.result = Sepidar(text, page=page)

    @staticmethod
    def get_mp3_links_and_title(url):
        """
        Fetches the title and .mp3 links from the given URL.
        
        Args:
            url (str): The website URL to scrape.

        Returns:
            dict: A dictionary containing the title and .mp3 links, or None if no links are found.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            title = soup.title.string if soup.title else "No title found"
            mp3_links = [
                link["href"] for link in soup.find_all("a", href=True)
                if link["href"].endswith(".mp3")
            ]
            
            return {"name": title, "url": mp3_links} if mp3_links else None
        
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return None

    def search(self):
        """
        Searches for .mp3 files based on the initialized search text.

        Returns:
            list: A list of dictionaries containing the titles and .mp3 links from search results.
        """
        music_list = []
        search_results = self.result.search().get('results', [])
        
        for item in search_results:
            site_url = item.get('link')
            if site_url:
                music_data = self.get_mp3_links_and_title(site_url)
                if music_data:
                    music_list.append(music_data)
        
        return music_list

    def __str__(self):
        return str(self.search())