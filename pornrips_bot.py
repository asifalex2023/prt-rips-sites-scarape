import re
import requests
from html.parser import HTMLParser
from telegraph import Telegraph
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

class PornripsScraper:
    url = 'https://pornrips.to'
    name = 'Pornrips.to (PRT)'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    class MyHtmlParser(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.articles_data = []
            self.current_article = {}
            self.in_article = False
            self.in_title = False
            self.in_size = False
            self.size_pattern = re.compile(r'Size:\s*(\d+\.?\d*\s*\w+)', re.IGNORECASE)

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            # Look for article containers
            if tag == 'article' and 'post' in attrs.get('class', ''):
                self.in_article = True
                self.current_article = {
                    'engine_url': PornripsScraper.url,
                    'link': attrs.get('data-href', '')  # Some sites use data attributes
                }
            
            # Look for title elements
            elif self.in_article and tag == 'h2':
                self.in_title = True
                if 'class' in attrs and 'entry-title' in attrs['class']:
                    self.current_article['link'] = attrs.get('href', '')
            
            # Look for size information
            elif self.in_article and tag == 'span' and 'post-size' in attrs.get('class', ''):
                self.in_size = True

        def handle_data(self, data):
            if self.in_title:
                self.current_article['name'] = data.strip()
            elif self.in_size:
                if match := self.size_pattern.search(data):
                    self.current_article['size'] = match.group(1)

        def handle_endtag(self, tag):
            if tag == 'article' and self.in_article:
                self.in_article = False
                if self.current_article.get('name'):
                    self.articles_data.append(self.current_article)
                self.current_article = {}
            elif tag == 'h2' and self.in_title:
                self.in_title = False
            elif tag == 'span' and self.in_size:
                self.in_size = False

    def search(self, query):
        all_results = []
        page = 1
        
        while True:
            try:
                # Build URL with proper encoding
                url = f"{self.url}/page/{page}/?s={requests.utils.quote(query)}" if page > 1 \
                    else f"{self.url}/?s={requests.utils.quote(query)}"
                
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code != 200 or page > 3:  # Reduced safety limit
                    break
                
                # Debug: Save HTML for inspection
                with open(f"debug_page_{page}.html", 'w') as f:
                    f.write(response.text)

                parser = self.MyHtmlParser()
                parser.feed(response.text)
                
                if not parser.articles_data:
                    break
                
                all_results.extend(parser.articles_data)
                page += 1

            except Exception as e:
                print(f"Error scraping page {page}: {str(e)}")
                break

        return all_results

# Rest of the code remains the same (Telegraph and Telegram handlers)

    def search(self, query):
        all_results = []
        page = 1
        while True:
            url = f'{self.url}/page/{page}/?s={query}' if page > 1 else f'{self.url}/?s={query}'
            response = requests.get(url)
            
            if response.status_code != 200 or page > 5:
                break
                
            parser = self.MyHtmlParser()
            parser.feed(response.text)
            parser.close()
            
            if not parser.articles_data:
                break
                
            all_results.extend(parser.articles_data)
            page += 1

        return all_results

# Rest of the code remains unchanged...

def create_telegraph_page(title, content):
    telegraph = Telegraph()
    telegraph.create_account(short_name='PornripsBot')
    response = telegraph.create_page(
        title=title,
        html_content=f"<p>{content}</p>"
    )
    return f'https://telegra.ph/{response["path"]}'

# Add the missing start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome to Pornrips Scraper Bot! Type /search <query> to find content.')

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text('Please provide a search term.')
        return

    scraper = PornripsScraper()
    results = scraper.search(query)
    
    if not results:
        await update.message.reply_text('No results found.')
        return

    formatted = "\n\n".join(
        f"Title: {res['name']}\nSize: {res.get('size', 'N/A')}\nLink: {res.get('link', 'N/A')}"
        for res in results
    )
    
    page_url = create_telegraph_page(f"Search Results for {query}", formatted)
    await update.message.reply_text(f"Results ({len(results)} found): {page_url}")

def main() -> None:
    application = Application.builder().token('7933218460:AAFbOiu04bmACRQh43eh7VfazGesw01T0-Y').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))
    application.run_polling()

if __name__ == '__main__':
    main()
