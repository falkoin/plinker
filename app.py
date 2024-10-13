from typing import Dict, List, Tuple
import typer
from datetime import date, datetime
from jinja2 import Template
import re
import yaml


class HugoWriter:
    def __init__(self) -> None:
        with open("./settings.yml") as f:
            self.path_to_posts = yaml.safe_load(f)
        with open("./template.md") as f:
            self.template = Template(f.read())
        self.path = f"{self.path_to_posts['posts']}{date.today().strftime('%Y-%m-%d')}.md"

    def write_template(self, links: List[Tuple]):
        time_now = datetime.now()
        date_now = date.today()
        date_format = f"{date_now.strftime('%Y-%m-%d')}T{time_now.strftime('%H:%M:%S')}+02:00"
        with open(self.path, "w") as f:
            f.write(
                self.template.render(
                    title=date_now.strftime("%d-%m-%Y"),
                    date_today=date_format,
                    links=links
                )
            )

    def read_existing_template(self, links: List[Tuple]) -> List[Tuple]:
        pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        with open(self.path, "r") as f:
            for line in f:
                matched_line = re.search(pattern, line)
                if matched_line:
                    link = matched_line.group(2)
                    description = matched_line.group(1)
                    links.append((description, link))
        return links


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
