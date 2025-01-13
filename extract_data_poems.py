import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def crawl_and_extract(base_url, url, target_element, element_class=None):
  """
  Crawls the given URL and extracts data based on the specified target element and class.

  :param base_url: The starting URL to crawl.
  :param url: The URL to crawl.
  :param target_element: The HTML tag (e.g., 'div', 'p', 'h1') to extract.
  :param element_class: (Optional) The class name of the target element to filter results.
  :return: A list of extracted text content.
  """

  visited = set()  # To keep track of visited URLs
  data = {}  # To store extracted data

  try:
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract elements based on tag and class
    elements = soup.find_all(target_element, class_=element_class)

    for element in elements:
      poem_response = requests.get(urljoin(base_url, element['href']))
      poem_response.raise_for_status()
      poem_soup = BeautifulSoup(poem_response.content, 'html.parser')

      poem_elements = poem_soup.find('div', class_='absatz').find_all('p')

      with open(element.get_text() + '.txt', 'w') as file:
        for poem_element in poem_elements:
          file.write(poem_element.get_text() + '\n')

  except requests.exceptions.RequestException as e:
    print(f"Error fetching the URL: {e}")
    return []


# Example usage
if __name__ == "__main__":
  base_url = "https://www.sachsen-lese.de"
  website_url = "https://www.sachsen-lese.de/streifzuege/mundartliches"  # Replace with the target website URL
  html_tag = "a"  # Replace with the desired HTML tag
  css_class = "linkTitle"  # Replace with the desired class name, or None for all tags

  crawl_and_extract(base_url, website_url, html_tag, css_class)
