import re
import telebot
from html.parser import HTMLParser
import telegraph
import requests
from telegram import Bot
from telegram.ext import Updater, CommandHandler

# Your Telegram bot API token
API_TOKEN = '7933218460:AAFbOiu04bmACRQh43eh7VfazGesw01T0-Y'
bot = telebot.TeleBot(API_TOKEN)

# URL of the site to scrape
url = 'https://pornrips.to'

class pornrips(object):
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
                self.article_data = { 'seeds': -1, 'leech': -1, 'desk_link': -1, 'engine_url': url }
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
                self.article_data['link'] = f"{url}/torrents/{self.article_data['name']}.torrent"
            elif self.is_in_size and re.search(self.size_pattern, data):
                self.is_in_size = False
                self.article_data['size'] = data

        def handle_endtag(self, tag: str) -> None:
            if self.is_in_article and tag == 'article':
                self.is_in_article = False
                prettyPrinter(self.article_data)

    def search(self, what, cat='all'):
        search_url = f'https://pornrips.to/?s={what}'
        response = requests.get(search_url)
        return response.text

# Initialize a telegraph page
def create_telegraph_page(data):
    t = telegraph.Telegraph()
    t.create_account(short_name='PornRipsBot')
    
    title = f"<h3>{data['name']}</h3>"
    link = f"<p><a href='{data['link']}'>Download Torrent</a></p>"
    size = f"<p><b>Size:</b> {data['size']}</p>"

    # Create a simple HTML page for Telegram
    content = title + link + size
    page = t.create_page(title=data['name'], html_content=content)
    return page['url']


# Handle the search command from Telegram users
@bot.message_handler(commands=['search'])
def search_and_show(message):
    query = message.text.split(' ', 1)[1]
    p = pornrips()
    raw_data = p.search(query)
    parser = pornrips.MyHtmlParser()
    parser.feed(raw_data)
    parser.close()
    
    # Assuming parser.article_data contains the result
    if parser.article_data:
        telegraph_url = create_telegraph_page(parser.article_data)
        bot.send_message(message.chat.id, f"Here is your search result: {telegraph_url}")
    else:
        bot.send_message(message.chat.id, "No results found.")

# Start the bot
bot.polling()
