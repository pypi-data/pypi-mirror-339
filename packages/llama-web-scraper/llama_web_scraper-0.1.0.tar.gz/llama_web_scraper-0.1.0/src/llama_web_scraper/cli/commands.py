import asyncio

import typer
from ai.llm_processor import process_content_with_llm
from loguru import logger
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from scraper.crawler import Crawler
from utils.db_utils import get_all_pages, init_db, update_page_analysis

app = typer.Typer()
console = Console()


@app.command()
def scrape(
    url: str = typer.Option(..., prompt=True, help="URL to scrape"),
    depth: int = typer.Option(2, help="Depth of scraping"),
):
    """Scrape a website starting from the given URL up to a certain depth."""
    asyncio.run(scrape_site(url, depth))


async def scrape_site(url: str, depth: int):
    init_db()
    crawler = Crawler()
    await crawler.crawl(start_url=url, max_depth=depth)
    pages = get_all_pages()
    for page in pages:
        analysis = await process_content_with_llm(page["url"], page["content"])
        update_page_analysis(analysis)
    logger.info("Scraping and analysis completed.")


@app.command()
def search(
    query: str = typer.Option(..., prompt=True, help="Search query"),
    max_results: int = typer.Option(10, help="Number of search results"),
):
    """Search for URLs to scrape using DuckDuckGo."""
    from scraper.duckduckgo_search import search_urls

    urls = search_urls(query, max_results)
    print("[bold green]Search Results:[/bold green]")
    for url in urls:
        print(url)
    if typer.confirm("Do you want to scrape these URLs?"):
        for url in urls:
            asyncio.run(scrape_site(url, depth=2))


@app.command()
def summarize():
    """Summarize the given text using LLM."""
    text = Prompt.ask("Enter the text to summarize")
    summary = asyncio.run(summarize_text(text))
    print("[bold green]Summary:[/bold green]")
    print(summary)


async def summarize_text(text: str):
    from ai.llm_processor import summarize_content

    return await summarize_content(text)


@app.command()
def sentiment():
    """Analyze sentiment of the given text using LLM."""
    text = Prompt.ask("Enter the text to analyze sentiment")
    sentiment = asyncio.run(analyze_sentiment_text(text))
    print(f"[bold green]Sentiment:[/bold green] {sentiment}")


async def analyze_sentiment_text(text: str):
    from ai.llm_processor import analyze_sentiment

    return await analyze_sentiment(text)


@app.command()
def keywords():
    """Extract keywords from the given text."""
    text = Prompt.ask("Enter the text to extract keywords")
    num_keywords = typer.prompt("Enter the number of keywords", default=10)
    from utils.nlp_utils import extract_keywords

    kws = extract_keywords(text, int(num_keywords))
    print("[bold green]Keywords:[/bold green]")
    print(", ".join(kws))


@app.command()
def pdf():
    """Generate a PDF from the given URL."""
    url = Prompt.ask("Enter the URL to generate PDF from")
    filename = Prompt.ask("Enter the filename to save the PDF as")

    asyncio.run(generate_pdf_from_url(url, filename))


async def generate_pdf_from_url(url: str, filename: str):
    browser = BrowserAutomation()
    content = await browser.automate_browser(url)
    generate_pdf(content, filename)
    print(f"[bold green]PDF generated and saved as {filename}[/bold green]")


@app.command()
def analyze():
    """Analyze previously scraped data."""
    pages = get_all_pages()
    if not pages:
        print("[bold red]No data available. Please run the scrape command first.[/bold red]")
        return
    for page in pages:
        print(f"[bold blue]URL:[/bold blue] {page['url']}")
        print(f"[bold green]Content:[/bold green] {page['content'][:500]}...")


@app.command()
def run():
    """Run interactive mode."""
    while True:
        print("[bold cyan]Choose an option:[/bold cyan]")
        print("1. Scrape a website")
        print("2. Search and scrape websites")
        print("3. Summarize text")
        print("4. Analyze sentiment")
        print("5. Extract keywords")
        print("6. Generate PDF")
        print("7. Analyze data")
        print("8. Exit")
        choice = Prompt.ask("Enter your choice")
        if choice == "1":
            scrape()
        elif choice == "2":
            search()
        elif choice == "3":
            summarize()
        elif choice == "4":
            sentiment()
        elif choice == "5":
            keywords()
        elif choice == "6":
            pdf()
        elif choice == "7":
            analyze()
        elif choice == "8":
            break
        else:
            print("[bold red]Invalid choice. Please try again.[/bold red]")


if __name__ == "__main__":
    app()
