import pathlib
import uuid
from typing import Any, Dict, List, Optional, cast
from urllib.parse import urljoin, urlparse

import httpx
from boltons.setutils import IndexedSet
from bs4 import BeautifulSoup, Tag
from lxml import etree
from telegraph import Telegraph
from tqdm import tqdm
from unidecode import unidecode

from database.models import ExtractedPage
from database.repositories.extracted_page import ExtractedPageRepository
from grabber.core.utils import (
    build_unique_img_urls,
    get_all_posts_for_url,
    run_downloader,
    get_tags,
    headers_mapping,
    query_mapping,
    send_post_to_telegram,
)


async def get_pages_from_pagination(url: str, headers: dict[str, str] | None = None, query: str = "") -> list[Tag]:
    first_page_response = httpx.get(url=url, headers=headers)
    page_content = first_page_response.content.decode("utf-8")
    images_tag = IndexedSet()

    while page_content:
        soup = BeautifulSoup(page_content, features="html.parser")
        image_tags = soup.select(query)
        images_tag.update(*[tag for tag in image_tags if ".svg" not in tag.attrs["src"]])

        pagination = soup.select(":-soup-contains-own('Next')")
        if pagination:
            next_page = pagination[0]
            target_url = next_page.attrs["href"]
            page_response = httpx.get(url=target_url, headers=headers)
            page_content = page_response.content.decode("utf-8")
        else:
            break

    return list(images_tag)


async def get_sources_for_fappening(
    sources: List[str],
    entity: str,
    telegraph_client: Optional[Telegraph] = None,
    final_dest: str | pathlib.Path = "",
    save_to_telegraph: bool | None = False,
    is_tag: Optional[bool] = False,
    limit: Optional[int] = None,
    **kwargs: Any,
) -> None:
    tqdm_sources_iterable = tqdm(
        sources,
        total=len(sources),
        desc="Retrieving URLs...",
    )
    query, src_attr = query_mapping[entity]
    headers = headers_mapping.get(entity, None)
    page_title = ""
    title_folder_mapping = {}
    posts_sent_counter = 0
    titles = IndexedSet()
    repository = ExtractedPageRepository(model=ExtractedPage)
    ordered_unique_img_urls = None
    all_sources = []
    posts_links = []
    original_folder_path = final_dest

    for source_url in tqdm_sources_iterable:
        final_dest = pathlib.Path(str(original_folder_path))
        all_sources += await get_all_posts_for_url(repository=repository, url=source_url)

        if source_url in all_sources:
            tqdm_sources_iterable.set_description(
                f"Skipping {source_url} since it was already posted"
            )
            continue

        image_tags: list[Tag] = [
            *await get_pages_from_pagination(
                url=source_url,
                headers=headers,
                query=query,
            ),
        ]

        _, soup = await get_tags(
            source_url,
            headers=headers,
            query=query,
        )
        page_title = cast(Tag, soup.find("title")).get_text(strip=True).strip().rstrip()
        page_title = (
            page_title
            .split("– The Fappening Plus!")[0]
            .replace("https:", "")
        )
        page_title = unidecode(" ".join(f"#{part.strip().replace(' ', '').replace('.', '_').replace('-', '_')}" for part in page_title.split("/")))
        page_title = f"{page_title} - {entity}"
        titles.add(page_title)

        image_tags = sorted(image_tags, key=lambda tag: tag.attrs["src"])
        ordered_unique_img_urls = await build_unique_img_urls(image_tags, src_attr)
        tqdm_sources_iterable.set_description(f"Finished retrieving images for {page_title}")

        if final_dest:
            final_dest = pathlib.Path(final_dest) / unidecode(f"{page_title} - {entity}")
            if not final_dest.exists():
                final_dest.mkdir(parents=True, exist_ok=True)

            folder_name = f"{page_title}"
            # title_dest = final_dest / folder_name / f"{str(uuid.uuid4())}"
            # if not title_dest.exists():
                # title_dest.mkdir(parents=True, exist_ok=True)
            title_folder_mapping[page_title] = (ordered_unique_img_urls, final_dest)

        if save_to_telegraph:
            all_sources = await send_post_to_telegram(
                ordered_unique_img_urls=ordered_unique_img_urls,
                page_title=page_title,
                telegraph_client=telegraph_client,
                posts_sent_counter=posts_sent_counter,
                tqdm_sources_iterable=tqdm_sources_iterable,
                all_sources=all_sources,
                source_url=source_url,
                entity=entity,
                send_to_telegram=False,
            )
            page_title = ""

    if final_dest and ordered_unique_img_urls:
        await run_downloader(
            final_dest=final_dest,
            page_title=page_title,
            unique_img_urls=ordered_unique_img_urls,
            titles=titles,
            title_folder_mapping=title_folder_mapping,
            headers=headers,
        )




