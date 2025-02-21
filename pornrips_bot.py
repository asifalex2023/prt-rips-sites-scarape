import re
import requests
from html.parser import HTMLParser
from telegraph import Telegraph
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

class PornripsScraper:
    url = 'https://pornrips.to'
    name = 'Pornrips.to (PRT)'

    class MyHtmlParser(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.articles_data = []
            # Changed from self.url to PornripsScraper.url
            self.current_article = {'engine_url': PornripsScraper.url}
            self.in_article = False
            self.in_content = False
            self.in_title = False
            self.in_size = False
            self.size_pattern = re.compile(r'(\d+ ?\w+)')

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == 'article' and 'post' in attrs.get('class', ''):
                self.in_article = True
                # FIX: Access parent class's URL using outer class name
                self.current_article = {'engine_url': PornripsScraper.url}
            elif self.in_article and tag == 'div' and 'wrapper-excerpt-content' in attrs.get('class', ''):
                self.in_content = True
            elif self.in_content and tag == 'h2' and 'entry-title' in attrs.get('class', ''):
                self.in_title = True
                self.current_article['link'] = attrs.get('href', '')
            elif self.in_content and tag == 'p':
                self.in_size = True

        # Rest of the parser methods remain the same...

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
