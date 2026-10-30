#!/usr/bin/env python3
"""Join the covers and the interior into the finished book PDF.

Usage: python assemble.py covers.pdf interior.pdf output.pdf

Page order: front cover, blank inside front cover, interior, blank pages as
needed so the back cover lands on an even page, back cover. The interior's
PDF bookmarks are kept and shifted to the new page numbers.
"""
import sys

from pypdf import PdfReader, PdfWriter


def main(covers_path: str, interior_path: str, out_path: str) -> int:
    covers, interior = PdfReader(covers_path), PdfReader(interior_path)
    front, back = covers.pages[0], covers.pages[1]
    width, height = front.mediabox.width, front.mediabox.height

    writer = PdfWriter()
    writer.add_page(front)
    writer.add_blank_page(width=width, height=height)  # inside front cover
    offset = len(writer.pages)
    for page in interior.pages:
        writer.add_page(page)
    if (len(writer.pages) + 1) % 2:
        writer.add_blank_page(width=width, height=height)  # inside back cover
    writer.add_page(back)

    writer.add_metadata({
        "/Title": "AI-Assisted Coding with Claude",
        "/Author": "Ronald Allan V. Tomimbang",
        "/Subject": "A practical guide for developers, learners and the leaders who govern them",
    })

    def copy(outline, parent=None):
        last = None
        for item in outline:
            if isinstance(item, list):
                copy(item, last)
            else:
                page = interior.get_destination_page_number(item) + offset
                last = writer.add_outline_item(item.title, page, parent=parent)

    writer.add_outline_item("Front cover", 0)
    copy(interior.outline)
    writer.add_outline_item("Back cover", len(writer.pages) - 1)
    with open(out_path, "wb") as handle:
        writer.write(handle)
    print(f"{out_path}: {len(writer.pages)} pages")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(*sys.argv[1:]))
