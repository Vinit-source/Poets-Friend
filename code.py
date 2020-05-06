import requests
from bs4 import BeautifulSoup
import re
from nltk.corpus import wordnet

#Step 1 : Query google to find relevant site
# get the API KEY here: https://developers.google.com/custom-search/v1/overview
API_KEY = "YOUR-API-KEY"
# get your Search Engine ID on your CSE control panel
SEARCH_ENGINE_ID = "YOUR-EARCH-ENGINE-ID"

# First Word
rhymeWord = input("Please input the rhyming word:")
# Second Word
synWord = input("Please input the synonymous word:")

#Google Search query
query = 'rhyming words for'+rhymeWord
# constructing the URL
# doc: https://developers.google.com/custom-search/v1/using_rest
url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"

# make the API request
data = requests.get(url).json()

# get the result items
search_items = data.get("items")
# iterate over 10 results found
# for i, search_item in enumerate(search_items, start=1):
# get the page title
# title = search_items[0].get("title")
# # page snippet
# snippet = search_items[0].get("snippet")
# # alternatively, you can get the HTML snippet (bolded keywords)
# html_snippet = search_items[0].get("htmlSnippet")
# extract the page url
link = search_items[0].get("link")
# print the results
# print("="*10, f"Result #{0}", "="*10)
# print("Title:", title)
# print("Description:", snippet)
# print("URL:", link, "\n")

#Step 2 : Collect words that rhyme with first input word

#get DOM from the link using requests
response = requests.get(link)
#parse the downloaded data using BeautifulSoup
soupObject = BeautifulSoup(response.content, 'html.parser')

#function to search for regular expression in href attributes
def d_searcher(href):
    return href if href and re.compile('^d=[a-z]*').search(href) else False
#find matching tags
anchorTags = soupObject.find_all(href=d_searcher)

#set for rhyming words
rhymingWords = set()
#store words in the set
for tag in anchorTags:
    rhymingWords.add(tag.text)

#Step 3: Find words synonymous to second input word
#set for rhyming words
synonyms = set()

#search for synonyms for first Word using Wordnet
for syn in wordnet.synsets(synWord):
    for l in syn.lemmas():
        synonyms.add(l.name())

result = synonyms.intersection(rhymingWords)
if result:
    print(result)
else:
    print("No common words found.")
