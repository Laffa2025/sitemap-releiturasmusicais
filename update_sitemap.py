import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import datetime

SITE_URL = "https://www.releiturasmusicais.com.br/"
SITEMAP_FILE = "sitemap.xml"

def get_internal_links(url, domain):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Ignorar links externos e âncoras
        if href.startswith('http') and domain not in href:
            continue
        if href.startswith('#'):
            continue
        # Montar URL absoluta
        full_url = urljoin(url, href)
        # Garantir que é do domínio
        if domain in full_url:
            links.add(full_url)
    return links

def crawl_site(start_url):
    domain = urlparse(start_url).netloc
    visited = set()
    to_visit = set([start_url])

    while to_visit:
        current_url = to_visit.pop()
        if current_url in visited:
            continue
        visited.add(current_url)
        links = get_internal_links(current_url, domain)
        for link in links:
            if link not in visited:
                to_visit.add(link)
    return visited

def write_sitemap(urls, filename):
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(filename, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url in sorted(urls):
            f.write('  <url>\n')
            f.write(f'    <loc>{url}</loc>\n')
            f.write(f'    <lastmod>{now}</lastmod>\n')
            f.write('    <changefreq>weekly</changefreq>\n')
            f.write('    <priority>0.5</priority>\n')
            f.write('  </url>\n')
        f.write('</urlset>\n')

if __name__ == "__main__":
    urls = crawl_site(SITE_URL)
    write_sitemap(urls, SITEMAP_FILE)
    print(f"Sitemap gerado com {len(urls)} páginas: {SITEMAP_FILE}")