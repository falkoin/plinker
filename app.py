import typer
from datetime import date
from jinja2 import Template


class HugoWriter:
    def __init__(self, path: str):
        f = open("./template.md")
        self.template = Template(f.read())
        f.close()
        self.f = open(path, "w")

    def write_template(self, link: str, description: str):
        self.f.write(
            self.template.render(
                title=date.today().strftime("%d-%m-%Y"),
                link=link,
                description=description,
            )
        )

    def close_file(self):
        self.f.close()


app = typer.Typer()


@app.command()
def add(url: str, description: str):
    hugo_writer = HugoWriter(f"./{date.today().strftime('%Y-%m-%d')}.md")
    hugo_writer.write_template(link=url, description=description)
    hugo_writer.close_file()


@app.command()
def test():
    pass


if __name__ == "__main__":
    app()
