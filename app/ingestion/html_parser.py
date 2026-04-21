from bs4 import BeautifulSoup

def parse_html(html_doc):
	soup = BeautifulSoup(html_doc, "html.parser")
	return {
		"title": soup.title.string.strip() if soup.title and soup.title.string else None,
		"content": soup.get_text()
	}
