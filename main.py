from pathlib import Path

from src.scraper import scrape_2016_article, write_raw_outputs


def main() -> None:
    project_root = Path(__file__).resolve().parent
    result = scrape_2016_article()
    outputs = write_raw_outputs(project_root, result)

    print(f"Saved article text to: {outputs['article']}")
    print(f"Saved references to: {outputs['references']}")
    print(f"Saved source metadata to: {outputs['metadata']}")
    print(f"Collected {len(result.references)} references")


if __name__ == "__main__":
    main()
