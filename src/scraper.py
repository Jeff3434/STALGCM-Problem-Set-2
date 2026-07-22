"""Wikipedia scraping helpers for Problem Set 2.

This module currently focuses on the 2016 Philippine presidential election
article and its references. The functions are intentionally small so they can
be reused when the 2022 article is added later.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


WIKIPEDIA_2016_URL = "https://en.wikipedia.org/wiki/2016_Philippine_presidential_election"


@dataclass(frozen=True)
class ScrapeResult:
    article_title: str
    article_text: str
    references: list[str]
    reference_entries: list[tuple[str, list[str]]]
    source_url: str


@dataclass(frozen=True)
class ReferencePageResult:
    index: int
    citation: str
    source_url: str
    output_path: Path


def fetch_html(url: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            )
        },
    )
    with urlopen(request) as response:
        return response.read().decode("utf-8", errors="replace")


def extract_article_text(soup: BeautifulSoup) -> tuple[str, str]:
    body = soup.body
    if body is None:
        raise ValueError("Could not locate page body")

    title = soup.select_one("h1#firstHeading")
    article_title = title.get_text(
        strip=True) if title else "2016 Philippine presidential election"

    return article_title, body.get_text("\n", strip=True)


def extract_references(soup: BeautifulSoup) -> list[str]:
    references_heading = soup.find(lambda tag: tag.name == "h2" and tag.get_text(
        " ", strip=True).lower().startswith("references"))
    if references_heading is None:
        return []

    references_list = references_heading.find_next("ol")
    if references_list is None:
        return []

    references: list[str] = []
    for item in references_list.find_all("li", recursive=False):
        text = item.get_text("\n", strip=True)
        if text:
            references.append(text)

    return references


def extract_reference_entries(soup: BeautifulSoup, source_url: str) -> list[tuple[str, list[str]]]:
    references_heading = soup.find(lambda tag: tag.name == "h2" and tag.get_text(
        " ", strip=True).lower().startswith("references"))
    if references_heading is None:
        return []

    references_list = references_heading.find_next("ol")
    if references_list is None:
        return []

    entries: list[tuple[str, list[str]]] = []
    for item in references_list.find_all("li", recursive=False):
        citation_text = item.get_text("\n", strip=True)
        candidate_urls = extract_reference_urls(item, source_url)
        if citation_text:
            entries.append((citation_text, candidate_urls))

    return entries


def extract_reference_urls(citation_node: BeautifulSoup, source_url: str) -> list[str]:
    urls: list[str] = []
    archive_urls: list[str] = []

    for anchor in citation_node.find_all("a", href=True):
        href = urljoin(source_url, anchor["href"])
        parsed = urlparse(href)
        if parsed.scheme not in {"http", "https"}:
            continue
        if "wikipedia.org" in parsed.netloc:
            continue

        if "web.archive.org" in parsed.netloc or "ghostarchive.org" in parsed.netloc:
            if href not in archive_urls:
                archive_urls.append(href)
            continue

        if href not in urls:
            urls.append(href)

    return urls + archive_urls


def _extract_body_text(soup: BeautifulSoup) -> str:
    body = soup.body
    if body is None:
        return ""

    return body.get_text("\n", strip=True)


def fetch_reference_page_text(reference_url: str) -> str:
    html = fetch_html(reference_url)
    soup = BeautifulSoup(html, "html.parser")
    return _extract_body_text(soup)


def scrape_reference_pages(reference_entries: list[tuple[str, list[str]]], source_url: str) -> list[ReferencePageResult]:
    results: list[ReferencePageResult] = []
    base_path = Path(__file__).resolve().parent.parent
    reference_dir = base_path / "data" / "raw" / "2016" / "references"
    reference_dir.mkdir(parents=True, exist_ok=True)

    def fetch_entry(index: int, citation: str, candidate_urls: list[str]) -> ReferencePageResult | None:
        for candidate_url in candidate_urls:
            try:
                page_text = fetch_reference_page_text(candidate_url)
            except Exception:
                continue

            if page_text.strip():
                output_path = reference_dir / f"reference_{index:03d}.txt"
                output_path.write_text(page_text.strip() + "\n", encoding="utf-8")
                return ReferencePageResult(
                    index=index,
                    citation=citation,
                    source_url=candidate_url,
                    output_path=output_path,
                )

        return None

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(fetch_entry, index, citation, candidate_urls)
            for index, (citation, candidate_urls) in enumerate(reference_entries, start=1)
        ]
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                results.append(result)

    results.sort(key=lambda page: page.index)

    return results


def scrape_2016_article() -> ScrapeResult:
    html = fetch_html(WIKIPEDIA_2016_URL)
    soup = BeautifulSoup(html, "html.parser")
    article_title, article_text = extract_article_text(soup)
    references = extract_references(soup)
    reference_entries = extract_reference_entries(soup, WIKIPEDIA_2016_URL)
    return ScrapeResult(
        article_title=article_title,
        article_text=article_text,
        references=references,
        reference_entries=reference_entries,
        source_url=WIKIPEDIA_2016_URL,
    )


def write_raw_outputs(base_dir: str | Path, result: ScrapeResult) -> dict[str, Path]:
    base_path = Path(base_dir)
    article_dir = base_path / "data" / "raw" / "2016"
    article_dir.mkdir(parents=True, exist_ok=True)

    article_path = article_dir / "2016_philippine_presidential_election_article.txt"
    references_path = article_dir / \
        "2016_philippine_presidential_election_references.txt"
    metadata_path = article_dir / "2016_philippine_presidential_election_source.txt"

    article_path.write_text(result.article_text + "\n", encoding="utf-8")
    references_text = "\n\n".join(
        f"{index}. {reference}" for index, reference in enumerate(result.references, start=1))
    references_path.write_text(
        references_text + ("\n" if references_text else ""), encoding="utf-8")
    metadata_path.write_text(
        "Source URL: " + result.source_url + "\n" +
        "Title: " + result.article_title + "\n",
        encoding="utf-8",
    )
    reference_pages = scrape_reference_pages(
        result.reference_entries, result.source_url)
    manifest_path = article_dir / \
        "2016_philippine_presidential_election_reference_manifest.txt"
    manifest_lines = [
        f"{page.index}. {page.source_url} -> {page.output_path.name}"
        for page in reference_pages
    ]
    manifest_path.write_text(
        "\n".join(manifest_lines) + ("\n" if manifest_lines else ""), encoding="utf-8")

    return {
        "article": article_path,
        "references": references_path,
        "metadata": metadata_path,
        "reference_manifest": manifest_path,
    }
