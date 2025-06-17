import tiktoken, requests, regex
from markdownify import markdownify

from tools.file_ops.read_file import read_file

def visit_website(url:str)->str:
    try:
        import pylibmagic, magic
        mime = magic.Magic(mime=True)  # Get MIME type
        headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-GB,en;q=0.6',
        'referer': 'https://duckduckgo.com/'
        }
        response = requests.get(url, timeout=5,headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        file_type = mime.from_buffer(response.content)
        if file_type == "text/html" or file_type == "application/XML":
            # Convert the HTML content to Markdown
            markdown_content = markdownify(response.text).strip()
            # Remove multiple line breaks
            markdown_content = regex.sub(r"\n{3,}", "\n\n", markdown_content,timeout=10)
            markdown_cleaned = regex.sub(r".*?\(# \"Expand/collapse hidden content\"\)\s*\n", " ", markdown_content, flags=regex.DOTALL,timeout=10)
            #print(markdown_cleaned)
            if markdown_cleaned:
                encoding = tiktoken.encoding_for_model("gpt-4o")
                tokens = encoding.encode(markdown_cleaned)
                if len(tokens)<25000:
                    return markdown_cleaned
                else:
                    return "?????????????????????????????CONTENT TOO LARGE?????????????????????????????????"
            else:
                return "????????????????????NO CONTENT?????????????????????????"
        else:
            return read_file(url)
    except Exception as e:
        #print(f"Exception for {url} is {e}")
        return f"Exception for {url} is {e}"