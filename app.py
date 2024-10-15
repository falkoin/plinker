from typing import Dict, List, Optional, Tuple
import typer
from datetime import date, datetime
from jinja2 import Template
import re
import yaml
from contextlib import suppress


class HugoWriter:
    def __init__(self) -> None:
        self.path_to_posts = self._process_settings()
        self.template = self._load_template()

    @staticmethod
    def _process_settings() -> Dict:
        with open("./settings.yml") as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def _load_template() -> Template:
        with open("./template.md") as f:
            return Template(f.read())

    def get_file_with_path(self) -> str:
        return f"{self.path_to_posts['posts']}{date.today().strftime('%Y-%m-%d')}.md"


    def read_existing_template(self, links: List[Tuple]) -> List[Tuple]:
        pattern = r"^(.*?)(\[\[\d+\]\])\((.*?)\)"
        file_with_path = self.get_file_with_path()
        old_links = []
        with suppress(FileNotFoundError):
            with open(file_with_path, "r") as f:
                for line in f:
                    matched_line = re.search(pattern, line)
                    if matched_line:
                        link = matched_line.group(3)
                        description = matched_line.group(1).strip()
                        old_links.append((description, link))

        return old_links + links

    def write_template(self, links: List[Tuple]):
        time_now = datetime.now()
        date_now = date.today()
        date_format = f"{date_now.strftime('%Y-%m-%d')}T{time_now.strftime('%H:%M:%S')}+02:00"
        file_with_path = self.get_file_with_path()
        with open(file_with_path, "w") as f:
            f.write(
                self.template.render(
                    title=date_now.strftime("%d-%m-%Y"),
                    date_today=date_format,
                    links=links
                )
            )

app = typer.Typer()


@app.command()
def add(url: str, description: str):
    hugo_writer = HugoWriter()
    links = hugo_writer.read_existing_template(links=[(description, url)])
    print(links)
    hugo_writer.write_template(links=links)


@app.command()
def test():
    pass


if __name__ == "__main__":
    app()
