from .main import news_index

def add_news_meili(news_element):
  documents = [
    {
      "id": news_element["position"],
      "title" : news_element["title"],
      "name" : news_element["name"],
      "description": news_element["description"],
      "thumbnail_link" : news_element["thumbnail_link"],
      "tags" : news_element["tags"],
    }
  ]
  news_index.add_documents(documents)
