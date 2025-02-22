from src.classes.Scraper import Scraper
from fastapi import FastAPI
from src.classes.SQLInjectionTester import SQLInjectionTester

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI App"}

@app.get("/scan")
async def scan(domain: str = "https://mahaveer.dev"):

    try:
        scraper = Scraper(domain)
        result = await scraper.start()
        return result
    except Exception as e:
        print(e)
        
        
@app.get("/test_sql")
async def test_sql(domain: str):
    scraper = Scraper(domain)
    result = await scraper.start()
    sql_tester = SQLInjectionTester(result["forms"])
    vulnerable_forms = sql_tester.test_sql_injection()
    return {"vulnerable_forms": vulnerable_forms}