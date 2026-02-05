from fastapi import FastAPI, Query
from gnews import GNews

app = FastAPI()

google_news = GNews(max_results=10)


DEFAULT_QUERIES = [
    "Female and child assault cases",
    "Child trafficking and exploitation",
    "Legal cases about women's rights violations",
    "Child labour and child protection news",
    "Domestic abuse affecting women and children"
]
Category_map={
    "trafficking":"Child trafficking and exploitation",
    "assault":"Female and child assault cases",
    "abuse":"Domestic abuse affecting women and children",
    "labour":"Child labour and child protection news",
    "rightviolations":"Legal cases about women's rights violations"
}

@app.get("/")
def home():
    return {"message": " api running idiot"}

@app.get("/news")
def get_news(search: str | None = Query(None),category: str | None = Query(None)) :
    if category and category in Category_map:
        queries=[Category_map[category]]
    elif search : queries = [search] 
    else:
        queries = [DEFAULT_QUERIES]
    all_results = []
    for q in queries:
        news = google_news.get_news(q)
        for article in news:
            data = {
                "query": q,
                "title": article.get("title"),
                "description": article.get("description"),
                "url": article.get("url"),
                "publisher": article.get("publisher"),
                "published_date": article.get("published date"),
            }
            all_results.append(data)
    return {
        "total_articles": len(all_results),
        "articles": all_results
    }
