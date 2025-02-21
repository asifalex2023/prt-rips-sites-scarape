import re
import requests
import io
from html.parser import HTMLParser
from urllib.parse import quote, urlparse
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

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == 'article' and 'post' in attrs.get('class', ''):
                self.in_article = True
                self.current_article = {'engine_url': PornripsScraper.url}
            
            if self.in_article and tag == 'h2' and 'entry-title' in attrs.get('class', ''):
                self.in_title = True

        def handle_data(self, data):
            if self.in_title:
                # Clean title and generate torrent URL
                clean_title = re.sub(r'[^\w.]+', '.', data.strip())  # Remove special chars
                clean_title = re.sub(r'\.{2,}', '.', clean_title)     # Remove multiple dots
                self.current_article['name'] = clean_title
                self.current_article['link'] = f"{PornripsScraper.url}/torrents/{clean_title}.torrent"

        def handle_endtag(self, tag):
            if tag == 'article' and self.in_article:
                self.in_article = False
                if self.current_article.get('name'):
                    self.articles_data.append(self.current_article)
                self.current_article = {}
            elif tag == 'h2' and self.in_title:
                self.in_title = False

    def search(self, query):
        all_results = []
        page = 1
        
        while True:
            try:
                search_url = f"{self.url}/page/{page}/?s={quote(query)}" if page > 1 \
                    else f"{self.url}/?s={quote(query)}"
                
                response = requests.get(search_url, headers=self.headers)
                
                if response.status_code != 200 or page > 3:
                    break
                
                parser = self.MyHtmlParser()
                parser.feed(response.text)
                
                if not parser.articles_data:
                    break
                
                all_results.extend(parser.articles_data)
                page += 1

            except Exception as e:
                print(f"Scraping Error: {str(e)}")
                break

        return all_results

def create_telegraph_page(title, content):
    telegraph = Telegraph()
    telegraph.create_account(short_name='PornripsBot')
    response = telegraph.create_page(
        title=title,
        html_content=f"<pre>{content}</pre>"  # Using pre for better formatting
    )
    return f'https://telegra.ph/{response["path"]}'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('🔍 Welcome to Pornrips Scraper Bot!\n\nSend /search <query> to find content')

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text('⚠️ Please provide a search term\nExample: /search 25.01.19')
        return

    scraper = PornripsScraper()
    results = scraper.search(query)
    
    if not results:
        await update.message.reply_text('❌ No results found')
        return

    formatted = "\n\n".join(
        f"🏷 Title: {res['name']}\n🔗 Link: {res['link']}"
        for res in results
    )
    
    page_url = create_telegraph_page(f"Results for: {query}", formatted)
    await update.message.reply_text(
        f"✅ Found {len(results)} results:\n{page_url}",
        disable_web_page_preview=True
    )
# Existing PornripsScraper class remains unchanged...

async def extract_links(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /links command to extract torrent links from Telegraph page"""
    if not context.args:
        await update.message.reply_text('⚠️ Please provide a Telegraph URL\nExample: /links https://telegra.ph/Results-for-250129-02-21')
        return

    telegraph_url = context.args[0]
    
    # Validate URL format
    if not telegraph_url.startswith('https://telegra.ph/'):
        await update.message.reply_text('❌ Invalid Telegraph URL format')
        return

    try:
        # Extract page path
        parsed = urlparse(telegraph_url)
        path = parsed.path.strip('/')
        
        # Fetch page content from Telegraph API
        api_url = f'https://api.telegra.ph/getPage/{path}?return_content=true'
        response = requests.get(api_url)
        data = response.json()
        
        if not data.get('ok'):
            await update.message.reply_text('❌ Could not fetch Telegraph page')
            return

        # Extract all .torrent links using regex
        content = data['result']['content']
        html_content = ''.join([item.get('children', [''])[0] for item in content if item.get('tag') == 'p'])
        torrent_links = re.findall(r'(https?://[^\s<>"]+\.torrent)', html_content)

        if not torrent_links:
            await update.message.reply_text('❌ No torrent links found in this page')
            return

        # Create in-memory text file
        text_file = io.BytesIO('\n'.join(torrent_links).encode('utf-8'))
        text_file.name = 'torrent_links.txt'

        # Send file with formatted message
        await update.message.reply_document(
            document=text_file,
            caption=f"🔗 Found {len(torrent_links)} torrent links:",
            filename='torrent_links.txt'
        )

    except Exception as e:
        await update.message.reply_text(f'⚠️ Error processing request: {str(e)}')


def main() -> None:
    application = Application.builder().token('7933218460:AAFbOiu04bmACRQh43eh7VfazGesw01T0-Y').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(CommandHandler("links", extract_links))  # New command handler
    application.run_polling()
    
if __name__ == '__main__':
    main()
    
