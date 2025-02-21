import re
import requests
from html.parser import HTMLParser
from telegraph import Telegraph  # Correctly import Telegraph
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Received /start command")  # Debugging line
    await update.message.reply_text('Welcome to the Pornrips Scraper Bot! Type a search term using /search.')

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("The bot is working!")

data = requests.get(f'https://pornrips.to/?s={what}&page={page_number}').text
print(data)  # Debugging: Print the raw HTML data

telegraph = Telegraph()
telegraph.create_account(short_name='PornripsBot')

response = telegraph.create_page(
    title='Test Page',
    html_content="<p>This is a test content</p>"
)

print(f"Created page: https://telegra.ph/{response['path']}")

# Create a class for your scraper
class PornripsScraper:
    url = 'https://pornrips.to'
    name = 'Pornrips.to (PRT)'

    class MyHtmlParser(HTMLParser):
        is_in_article: bool
        is_in_content: bool
        is_in_title: bool
        is_in_size: bool
        articles_data: list
        size_pattern = re.compile('(\d+ ?\w+)')

        def __init__(self) -> None:
            HTMLParser.__init__(self)
            self.is_in_article = False
            self.is_in_content = False
            self.is_in_title = False
            self.is_in_size = False
            self.articles_data = []  # List to store all articles

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
                self.articles_data.append(self.article_data)  # Append article to the list

    def search(self, what):
        page_number = 1
        all_articles = []
        while True:
            data = requests.get(f'https://pornrips.to/?s={what}&page={page_number}').text
            prt_parser = self.MyHtmlParser()
            prt_parser.feed(data)
            prt_parser.close()

            all_articles.extend(prt_parser.articles_data)  # Add current page's results to the list

            # Check if there's a "Next" page by looking for the "Next" button
            if 'Next' in data:  # Looking for 'Next' in page source to detect pagination
                page_number += 1  # Go to the next page
            else:
                break  # No more pages, stop the loop

        return all_articles  # Return all scraped articles



# Telegraph API integration to create a page
def create_telegraph_page(title, content):
    telegraph = Telegraph()  # Ensure Telegraph is initialized
    telegraph.create_account(short_name='PornripsBot')

    # Create a page with scraped data
    response = telegraph.create_page(
        title=title,
        html_content=f"<p>{content}</p>"
    )
    return f'https://telegra.ph/{response["path"]}'

# Define the /search command handler
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Received /search command")  # Debugging line
    query = " ".join(context.args)  # Get the query from the user
    if query:
        print(f"Searching for: {query}")  # Debugging line
        scraper = PornripsScraper()
        results = scraper.search(query)  # Pass the query to the scraper
        
        # Debugging: Check if results are collected
        print(f"Found {len(results)} results")  # Debugging line
        for result in results:  # Debugging loop to inspect results
            print(f"Result - Name: {result['name']}, Size: {result.get('size')}, Link: {result.get('link')}")
        
        if results:
            formatted_results = ""
            for result in results:
                formatted_results += f"Title: {result['name']}\nSize: {result.get('size', 'Unknown')}\nLink: {result.get('link', 'No link available')}\n\n"
            
            page_url = create_telegraph_page(query, formatted_results)
            print(f"Generated page URL: {page_url}")  # Debugging line
            await update.message.reply_text(f"Here are your results: {page_url}")
        else:
            await update.message.reply_text('No results found.')
    else:
        await update.message.reply_text('Please provide a search term.')



# Main function to start the bot
def main() -> None:
    # Replace with your actual Telegram bot token
    application = Application.builder().token('7933218460:AAFbOiu04bmACRQh43eh7VfazGesw01T0-Y').build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(CommandHandler("test", test))
    
    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
