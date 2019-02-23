#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Documentation"""

import os
from datetime import datetime
import sys
from flask import render_template
from jinja2 import Environment, FileSystemLoader
from markdown import Markdown

class md2html:

    def __init__(self):
        # self.env = Environment( loader=FileSystemLoader("templates") )
        # self.template = Environment(
        #     loader=FileSystemLoader("templates") 
        # ).get_template("base_article.html")

        self.md = Markdown(
            extensions=[
                "fenced_code",
                "codehilite(css_class=highlight,linenums=None)",
                "meta",
                "admonition",
                "tables",
                "toc",
                "wikilinks",
            ],
        )
    STATIC_ROOT = "/static/"

    TAG_HTML_TEMPLATE = "<a href='/tag/{tag}/' class='tag-index'>{tag}</a>"
    AUTHOR_HTML_TEMPLATE = "<a href='' class='tag-index'>{author}</a>"
    TITLE_HTML_TEMPLATE = "<div class='sidebar-module-inset'><h5 class='sidebar-title'><i class='icon-circle-blank side-icon'></i>标题</h5><p>{title_str}</p></div>"

    def format_meta(self,meta):
        title = meta.get("title", [""])[0]
        publish_date = meta.get("publish_date", [datetime.now().strftime('%Y-%m-%d')])[0]

        return {
            "title": title,
            "summary": meta.get("summary", [u""])[0],
            "authors": meta.get("authors", [u"匿名"]),
            "publish_date": publish_date,
            "tags": meta.get("tags", [])
        }

    def parse(self, text):
        self.md.reset()
        html = self.md.convert(text)
        meta = self.md.Meta if hasattr(self.md, "Meta") else {}
        metaDict = self.format_meta(meta)
        toc = self.md.toc if hasattr(self.md, "toc") else ""
        return html, metaDict,toc

    def render_tags_html(self,tags):
        """渲染tags的html
        """
        tags_html = ""
        for tag in tags:
            tags_html += self.TAG_HTML_TEMPLATE.format(tag=tag)
        return tags_html


    def render_authors_html(self,authors):
        """渲染作者html
        """
        authors_html = ""
        for author in authors:
            authors_html += self.AUTHOR_HTML_TEMPLATE.format(author=author)
        return authors_html


    def render_title_html(self,title):
        """渲染标题html
        """
        title_html = ""
        if title.strip() != "":
            title_html = self.TITLE_HTML_TEMPLATE.format(title_str=title)
        return title_html


    def render(self, html, meta={}, toc=""):
        """渲染html页面
        """
        # template=self.template
        return render_template("base_article.html",
            blog_content=html,
            static_root=self.STATIC_ROOT,
            title=meta.get("title"),
            title_html=meta.get("title"),
            summary=meta.get("summary", ""),
            authors=meta.get("authors"),
            tags=self.render_tags_html(meta.get("tags")),
            toc=toc,
        )


if __name__ == "__main__":
    md = md2html()
    with open(r"About.md", "r", encoding="utf-8") as f:
        text = f.read()
        html, meta, toc = md.parse(text)     
        print(meta)    
        result = md.render(html, meta, toc)
        # print(result)