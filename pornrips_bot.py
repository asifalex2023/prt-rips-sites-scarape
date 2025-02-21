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
            self.current_article = {}
            self.in_article = False
            self.in_content = False
            self.in_title = False
            self.in_size = False
            self.size_pattern = re.compile(r'(\d+ ?\w+)')

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == 'article' and 'post' in attrs.get('class', ''):
                self.in_article = True
                self.current_article = {'engine_url': self.url}
            elif self.in_article and tag == 'div' and 'wrapper-excerpt-content' in attrs.get('class', ''):
                self.in_content = True
            elif self.in_content and tag == 'h2' and 'entry-title' in attrs.get('class', ''):
                self.in_title = True
                self.current_article['link'] = attrs.get('href', '')
            elif self.in_content and tag == 'p':
                self.in_size = True

        def handle_data(self, data):
            if self.in_title:
                self.current_article['name'] = data.strip()
            elif self.in_size and self.size_pattern.search(data):
                self.current_article['size'] = data.strip()

        def handle_endtag(self, tag):
            if tag == 'article' and self.in_article:
                self.in_article = False
                if self.current_article.get('name'):
                    self.articles_data.append(self.current_article)
                self.current_article = {}
            elif tag == 'div' and self.in_content:
                self.in_content = False
            elif tag == 'h2' and self.in_title:
                self.in_title = False
            elif tag == 'p' and self.in_size:
                self.in_size = False

    def search(self, query):
        all_results = []
        page = 1
        while True:
            if page == 1:
                url = f'{self.url}/?s={query}'
            else:
                url = f'{self.url}/page/{page}/?s={query}'
            
            response = requests.get(url)
            if response.status_code != 200:
                break
            
            parser = self.MyHtmlParser()
            parser.feed(response.text)
            parser.close()
            
            if not parser.articles_data:
                break
            
            all_results.extend(parser.articles_data)
            page += 1

            # Safety break to prevent infinite loops
            if page > 5:
                break
        
        return all_results

def create_telegraph_page(title, content):
    telegraph = Telegraph()
    telegraph.create_account(short_name='PornripsBot')
    response = telegraph.create_page(
        title=title,
        html_content=f"<p>{content}</p>"
    )
    return f'https://telegra.ph/{response["path"]}'

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

# Rest of the code remains the same
def main() -> None:
    application = Application.builder().token('7933218460:AAFbOiu04bmACRQh43eh7VfazGesw01T0-Y').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))
    application.run_polling()

if __name__ == '__main__':
    main()
