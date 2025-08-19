import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional


def _lazy_import_bs4():
    try:
        from bs4 import BeautifulSoup  # type: ignore
    except Exception as exc:  # pragma: no cover
        print(
            "BeautifulSoup4 is required. Install dependencies with: pip install -r requirements.txt",
            file=sys.stderr,
        )
        raise exc
    return BeautifulSoup


CakeItem = Dict[str, Any]


def load_cakes_data(json_path: str) -> List[CakeItem]:
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Data file not found: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "items" in data:
        items = data["items"]
    elif isinstance(data, list):
        items = data
    else:
        raise ValueError("cakes.json must be a list of items or an object with an 'items' array")
    if not isinstance(items, list):
        raise ValueError("The 'items' field must be a list")
    return items


def ensure_image_present(item: CakeItem, images_dir: str) -> Optional[str]:
    image_rel = item.get("image")
    if not image_rel:
        return None
    dest_path = os.path.join(images_dir, image_rel).replace("/", os.sep)
    dest_dir = os.path.dirname(dest_path)
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    # Optionally copy from source_image if provided
    source_image = item.get("source_image")
    if source_image and os.path.exists(source_image) and not os.path.exists(dest_path):
        try:
            from shutil import copy2
        except Exception:  # pragma: no cover
            copy2 = None
        if copy2:
            copy2(source_image, dest_path)
    return dest_path


def generate_item_html(item: CakeItem, images_web_dir: str) -> str:
    # Required fields
    category_class = item.get("category", "other-cakes")
    image_rel = item.get("image")
    title = item.get("title", "")
    price = item.get("price")

    if not image_rel:
        raise ValueError(f"Item missing 'image': {item}")
    if not title:
        raise ValueError(f"Item missing 'title': {item}")

    img_path = f"{images_web_dir.rstrip('/')}/{image_rel}"

    price_html = f"\n\t\t\t\t\t\t\t<h5>৳{price}</h5>" if price not in (None, "") else ""

    # Mirrors the existing site structure/classes
    html = (
        f'<div class="col-lg-3 col-md-4 col-sm-6 mix {category_class}">\n'
        f'\t<div class="featured__item">\n'
        f'\t\t<div class="featured__item__pic set-bg" data-setbg="{img_path}">\n'
        f'\t\t\t<ul class="featured__item__pic__hover">\n'
        f'\t\t\t\t<li><a href="{img_path}" download><i class="fa fa-download"></i></a></li>\n'
        f"\t\t\t\t<li><a href=\"#\" onclick=\"openImageModal('{img_path}')\"><i class=\"fa fa-search-plus\"></i></a></li>\n"
        f'\t\t\t</ul>\n'
        f'\t\t</div>\n'
        f'\t\t<div class="featured__item__text">\n'
        f'\t\t\t<h6><a href="#">{title}</a></h6>'
        f"{price_html}\n"
        f'\t\t</div>\n'
        f'\t</div>\n'
        f'</div>'
    )
    return html


def update_html_file(html_path: str, items: List[CakeItem], images_web_dir: str) -> bool:
    BeautifulSoup = _lazy_import_bs4()
    if not os.path.exists(html_path):
        return False
    with open(html_path, "r", encoding="utf-8") as f:
        html_text = f.read()

    soup = BeautifulSoup(html_text, "html.parser")
    target_row = None
    # Find the featured grid container: <div class="row featured__filter">
    for div in soup.find_all("div", class_=True):
        classes = set(div.get("class", []))
        if {"row", "featured__filter"}.issubset(classes):
            target_row = div
            break

    if target_row is None:
        print(f"Could not find 'div.row.featured__filter' in {html_path}", file=sys.stderr)
        return False

    # Clear existing items (only immediate child columns)
    for child in list(target_row.children):
        # Remove elements (keep non-element strings like whitespace minimal to avoid reformatting)
        if getattr(child, "name", None):
            child.decompose()

    # Append generated items
    # Determine images web dir relative to this file if needed
    for item in items:
        item_html = generate_item_html(item, images_web_dir)
        fragment = BeautifulSoup(item_html, "html.parser")
        target_row.append(fragment)

    # Write back
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    return True


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Update the Featured Cakes grid in index.html from a JSON data file."
    )
    parser.add_argument(
        "--data",
        default="cakes.json",
        help="Path to JSON file with cake items (default: cakes.json)",
    )
    parser.add_argument(
        "--images-dir",
        default=os.path.join("img", "featured"),
        help="Destination images directory on disk (for optional copying). Default: img/featured",
    )
    parser.add_argument(
        "--images-web-dir",
        default="img/featured",
        help="Images directory as referenced in HTML (default: img/featured)",
    )
    parser.add_argument(
        "--html",
        nargs="*",
        default=["index.html", os.path.join("public", "index.html")],
        help="One or more HTML files to update (default: index.html public/index.html)",
    )
    parser.add_argument(
        "--no-copy",
        action="store_true",
        help="Do not attempt to copy images from 'source_image' to images-dir",
    )
    args = parser.parse_args(argv)

    try:
        items = load_cakes_data(args.data)
    except Exception as exc:
        print(f"Failed to load data: {exc}", file=sys.stderr)
        return 2

    # Ensure/copy images if source_image is provided
    if not args.no_copy:
        for item in items:
            ensure_image_present(item, args.images_dir)

    any_success = False
    for html_path in args.html:
        if os.path.exists(html_path):
            ok = update_html_file(html_path, items, args.images_web_dir)
            any_success = any_success or ok
            if ok:
                print(f"Updated: {html_path}")
        else:
            print(f"Skipped (not found): {html_path}")

    if not any_success:
        print("No HTML files were updated.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


