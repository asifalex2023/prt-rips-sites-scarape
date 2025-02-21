import re
import requests
from html.parser import HTMLParser
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext import CommandHandler
from telegram.ext import Application

# Create a class for your scraper
class PornripsScraper:
    url = 'https://pornrips.to'
    name = 'Pornrips.to (PRT)'

    class MyHtmlParser(HTMLParser):
        is_in_article: bool
        is_in_content: bool
        is_in_title: bool
        is_in_size: bool
        article_data: dict

        size_pattern = re.compile('(\d+ ?\w+)')

        def __init__(self) -> None:
            HTMLParser.__init__(self)
            self.is_in_article = False
            self.is_in_content = False
            self.is_in_title = False
            self.is_in_size = False

        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            tag_attrs = dict(attrs)
            if not self.is_in_article and tag == 'article' and 'post' in tag_attrs.get('class'):
                self.is_in_article = True
                self.article_data = { 'seeds': -1, 'leech': -1, 'desk_link': -1, 'engine_url': PornripsScraper.url }
                return
            elif not self.is_in_article:
                return

            if tag == 'div' and tag_attrs.get('class') == 'wrapper-excerpt-content':
                self.is_in_content = True
                return
            elif self.is_in_content and tag == 'h2' and tag_attrs.get('class') == 'entry-title':
                self.is_in_title = True
                return
            elif self.is_in_content and tag == 'p':
                self.is_in_size = True
                return

        def handle_data(self, data: str) -> None:
            if self.is_in_title:
                self.is_in_title = False
                self.article_data['name'] = data
                self.article_data['link'] = f"{PornripsScraper.url}/torrents/{self.article_data['name']}.torrent"
            elif self.is_in_size and re.search(self.size_pattern, data):
                self.is_in_size = False
                self.article_data['size'] = data

        def handle_endtag(self, tag: str) -> None:
            if self.is_in_article and tag == 'article':
                self.is_in_article = False
                return self.article_data

    def search(self, what):
        data = requests.get(f'https://pornrips.to/?s={what}').text

        prt_parser = self.MyHtmlParser()
        prt_parser.feed(data)
        prt_parser.close()
        return prt_parser.article_data

# Telegraph API integration to create a page
def create_telegraph_page(title, content):
    telegraph = Telegraph()
    telegraph.create_account(short_name='PornripsBot')

    # Create a page with scraped data
    response = telegraph.create_page(
        title=title,
        html_content=f"<p>{content}</p>"
    )
    return f'https://telegra.ph/{response["path"]}'

# Telegram Bot Command Handler


# Start command handler
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome to Pornrips Scraper Bot! Type a search term.')

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = " ".join(context.args)
    if query:
        scraper = PornripsScraper()
        result = scraper.search(query)

        if result:
            title = result['name']
            content = f"Size: {result.get('size', 'Unknown')}\nLink: {result.get('link', 'No link available')}"
            page_url = create_telegraph_page(title, content)
            await update.message.reply_text(f"Here is your result: {page_url}")
        else:
            await update.message.reply_text('No results found.')
    else:
        await update.message.reply_text('Please provide a search term.')

def main() -> None:
    application = Application.builder().token('YOUR_TELEGRAM_BOT_TOKEN').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))

    application.run_polling()

if __name__ == '__main__':
    main()
