# Kati - Web Crawler

A Python web crawler that extracts links and content from websites.

## Installation

1. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

2. Activate the virtual environment:
   ```bash
   poetry shell
   ```

## Configuration

### Starting URL

To change the starting URL for the crawler, modify line 110 in `main.py`:

```python
crawl_url("https://your-starting-url.com")
```

### Base URL

The crawler converts relative URLs (starting with `/`) to absolute URLs using a base URL. To change the base URL, modify line 57 in `main.py`:

```python
href = 'https://your-base-url.com' + href
```

**Note:** Make sure the base URL matches the domain you're crawling.

### Request Timeout

The crawler waits up to 10 seconds for each HTTP request. To change the timeout, modify line 17 in `main.py`:

```python
response = requests.get(url, headers=user_agent, timeout=30)  # 30 seconds
```

### User-Agent

The crawler uses a User-Agent header to identify itself as a browser. To change it, modify line 15 in `main.py`:

```python
user_agent = {"User-Agent": "Your-Custom-User-Agent-String"}
```

### Data Files

The crawler saves and loads state from three text files:

- `links_to_crawl.txt` - Queue of URLs waiting to be crawled
- `links_crawled.txt` - List of URLs that have been successfully crawled
- `broken_links.txt` - List of URLs that failed to load

These files are automatically created when you quit the crawler (press 'q'). They are automatically loaded when you start the program. If the files don't exist, the crawler will start with empty lists.

## Usage

Run the crawler:

```bash
python main.py
```

The crawler will:
1. Load any previously saved state from the data files
2. Start crawling from the configured starting URL
3. Extract links and add them to the crawl queue
4. Extract text content from `<main>` tags
5. Prompt you to continue or quit after each page

Press Enter to continue crawling the next link, or 'q' to quit and save progress.

## Features

- **Resumable crawling**: Progress is saved to files, so you can stop and resume later
- **Link extraction**: Automatically finds and queues all links on each page
- **Content extraction**: Extracts text from `<main>` HTML tags
- **Error handling**: Tracks broken links separately
- **Relative URL handling**: Automatically converts relative URLs to absolute URLs

