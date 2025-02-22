from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import asyncio
import aiohttp
from playwright.async_api import async_playwright
from urllib.parse import urljoin, urlparse

class Scraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_urls = set()
        self.forms = []
        self.links = set()
        
    async def fetch_dynamic_content(self, url):
        if url is None:
            print("URL is None, skipping navigation")
            return
        """Fetch page content dynamically using Playwright"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)  # Use headless=True for performance
            page = await browser.new_page()
            try:
                await page.goto(url, wait_until="domcontentloaded")  # Wait for all requests to finish
                content = await page.content()
            except Exception as e:
                print(f"Error navigating to the page: {e}")
                content = None
            finally:
                await browser.close()
            return content

    async def scrape_links(self, url):
        if url in self.visited_urls:
            return
        
        self.visited_urls.add(url)
        html = await self.fetch_dynamic_content(url)  # Use Playwright for dynamic content
        if not html:
            return
        
        soup = BeautifulSoup(html, "html.parser")
        
        # Extract links
        for a_tag in soup.find_all("a", href=True):
            link = urljoin(url, a_tag["href"])
            if urlparse(link).netloc == urlparse(self.base_url).netloc:
                self.links.add(link)
                await self.scrape_links(link)  # Await here to ensure completion

        # Extract forms
        self.forms.extend(self.extract_forms(soup, url))

    def extract_forms(self, soup, url):
        forms = []
        for form in soup.find_all("form"):
            form_data = {
                "action": urljoin(url, form.get("action", "")),
                "method": form.get("method", "get").lower(),
                "inputs": [
                    {
                        "name": input_tag.get("name"),
                        "type": input_tag.get("type", "text"),
                    }
                    for input_tag in form.find_all("input")
                ],
            }
            forms.append(form_data)
        return forms
    
    async def start(self):
        await self.scrape_links(self.base_url)
        return {"links": list(self.links), "forms": self.forms}
    
    # async def fetch(self, session, url):
    #     try:
    #         async with session.get(url) as response:
    #             print(await response.text())
    #             return await response.text()
    #     except Exception as e:
    #         print(f"Failed to fetch {url}: {e}")
    #         return None

    # async def scrape_links(self, url, session):
    #     if url in self.visited_urls:
    #         return
        
    #     self.visited_urls.add(url)
    #     html = await self.fetch(session, url)
    #     if not html:
    #         return
        
    #     soup = BeautifulSoup(html, "html.parser")
        
    #     # Extract links
    #     for a_tag in soup.find_all("a", href=True):
    #         link = urljoin(url, a_tag["href"])
    #         if urlparse(link).netloc == urlparse(self.base_url).netloc:
    #             self.links.add(link)
    #             asyncio.create_task(self.scrape_links(link, session))
        
    #     # Extract forms
    #     self.forms.extend(self.extract_forms(soup, url))

    # def extract_forms(self, soup, url):
    #     forms = []
    #     for form in soup.find_all("form"):
    #         form_data = {
    #             "action": urljoin(url, form.get("action", "")),
    #             "method": form.get("method", "get").lower(),
    #             "inputs": [
    #                 {
    #                     "name": input_tag.get("name"),
    #                     "type": input_tag.get("type", "text"),
    #                 }
    #                 for input_tag in form.find_all("input")
    #             ],
    #         }
    #         forms.append(form_data)
    #     return forms

    # async def start(self):
    #     async with aiohttp.ClientSession() as session:
    #         await self.scrape_links(self.base_url)
    #     return {"links": list(self.links), "forms": self.forms}

