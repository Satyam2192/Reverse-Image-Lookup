# A very basic web crawler stub for demonstration.
# In a real crawler, you'd parse HTML, follow links, etc.

class WebCrawler:
    async def crawl(self, url: str):
        # For demo, pretend we found two images at this URL
        return [
            "https://example.com/image1.jpg",
            "https://example.com/image2.jpg"
        ]
