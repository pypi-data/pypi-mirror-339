import json
import locale
import shutil

import mistune
from jinja2 import Environment as Env
from jinja2 import FileSystemLoader
from slugify import slugify

from . import VERSION
from .utils import neighborhood

locale.setlocale(locale.LC_ALL, "")
md = mistune.create_markdown(plugins=["footnotes", "superscript"])


def slugify_(value):
    return slugify(value)


def markdown(value):
    return md(value) if value else ""


def generate_html(
    title, base_url, numeros, keywords, authors, extra_vars, target_path, templates_path
):
    environment = Env(loader=FileSystemLoader(str(templates_path)))
    environment.filters["slugify"] = slugify_
    environment.filters["markdown"] = markdown

    extra_vars = json.loads(extra_vars) if extra_vars else {}

    common_params = {
        "title": title,
        "base_url": base_url,
        "numeros": numeros,
        "keywords": keywords,
        "authors": authors,
        "crieur_version": VERSION,
        **extra_vars,
    }

    template_homepage = environment.get_template("homepage.html")
    content = template_homepage.render(**common_params)
    target_path.mkdir(parents=True, exist_ok=True)
    (target_path / "index.html").write_text(content)

    for numero in numeros:
        template_numero = environment.get_template("numero.html")
        content = template_numero.render(numero=numero, **common_params)
        numero_folder = target_path / "numero" / numero.slug
        numero_folder.mkdir(parents=True, exist_ok=True)
        (numero_folder / "index.html").write_text(content)

        template_article = environment.get_template("article.html")
        for index, previous, article, next_ in neighborhood(numero.articles):
            content = template_article.render(
                article=article,
                numero=numero,
                previous_situation=previous,
                next_situation=next_,
                **common_params,
            )
            article_folder = numero_folder / "article" / article.id
            article_folder.mkdir(parents=True, exist_ok=True)
            (article_folder / "index.html").write_text(content)
            if article.images_path:
                shutil.copytree(
                    article.images_path, article_folder / "images", dirs_exist_ok=True
                )

    for slug, keyword in keywords.items():
        template_keyword = environment.get_template("keyword.html")
        content = template_keyword.render(keyword=keyword, **common_params)
        keyword_folder = target_path / "mot-clef" / keyword.slug
        keyword_folder.mkdir(parents=True, exist_ok=True)
        (keyword_folder / "index.html").write_text(content)

    for slug, author in authors.items():
        template_author = environment.get_template("author.html")
        content = template_author.render(author=author, **common_params)
        author_folder = target_path / "auteur" / author.slug
        author_folder.mkdir(parents=True, exist_ok=True)
        (author_folder / "index.html").write_text(content)
