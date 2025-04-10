import asyncio
import pathlib
import uuid
from typing import Any, Dict, List, Optional, cast
from urllib.parse import urljoin

from boltons.setutils import IndexedSet
from bs4 import Tag
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
    get_soup,
    get_tags,
    headers_mapping,
    query_mapping,
    query_pagination_mapping,
    send_post_to_telegram,
)


async def get_images_from_pagination(url: str, headers: dict[str, str] | None = None) -> list[Tag]:
    pagination_query = "div.pagination div.pagination-holder ul li a"
    images_query = "div.main-content div.main-container div#list_videos_common_videos_list div.box div.list-videos div.margin-fix div.item a div img"
    pagination_links = IndexedSet()

    images_tags = IndexedSet()
    pagination_links.add(url)
    soup = await get_soup(url, headers=headers)
    pagination_set = soup.select(pagination_query)

    if not pagination_set:
        images_tags = soup.select(images_query)
        return list(images_tags)

    for page_url in pagination_set:
        link: str = page_url.attrs["href"]
        if "https:" not in link:
            link = f"https:{link}"
        pagination_links.add(link)

    # image_posts_url: list[str] = []
    for link in pagination_links:
        soup = await get_soup(link, headers=headers)
        images_tags.update(*soup.select(images_query))

        # for tag in images_tags:
        #     image_link = tag.attrs["href"]
        #     if "https:" not in image_link:
        #         image_link = f"https:{image_link}"
        #         image_posts_url.append(image_link)
        #     else:
        #         image_posts_url.append(image_link)
        #
        # for post_url in image_posts_url:
        #     images_links.add(post_url)

    return list(images_tags)


async def get_sources_for_nudogram(
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
    images_query = "div.box div div div a"
    headers = headers_mapping.get(entity, None)
    page_title = ""
    first_page_title = ""
    title_folder_mapping = {}
    posts_sent_counter = 0
    titles = IndexedSet()
    repository = ExtractedPageRepository(model=ExtractedPage)
    ordered_unique_img_urls = None
    all_sources = []
    original_folder_path = final_dest

    for source_url in tqdm_sources_iterable:
        final_dest = pathlib.Path(str(original_folder_path))
        first_page_title = ""
        all_sources += await get_all_posts_for_url(repository=repository, url=source_url)

        if source_url in all_sources:
            tqdm_sources_iterable.set_description(
                f"Skipping {source_url} since it was already posted"
            )
            continue

        if posts_sent_counter in [50, 100, 150, 200, 250]:
            await asyncio.sleep(10)

        folder_name = ""
        image_tags: list[Tag] = [
            *await get_images_from_pagination(
                url=source_url,
                headers=headers,
            ),
        ]
        if not image_tags:
            tqdm_sources_iterable.set_postfix_str(f"Error retrieving image URLs for {source_url}. Skipping it..")
            continue

        _, soup = await get_tags(
            source_url,
            headers=headers,
            query=query,
        )

        page_title = cast(Tag, soup.find("title")).get_text(strip=True).strip().rstrip()
        page_title = (
            page_title
            .split("- Nudogram")[0]
            .split("Nude")[0]
            .replace("https:", "")
        )
        page_title = unidecode(" ".join(f"#{part.strip().replace(' ', '').replace('.', '_').replace('-', '_')}" for part in page_title.split("/")))
        first_page_title = page_title
        folder_name = f"{page_title}"
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
                page_title=first_page_title,
                telegraph_client=telegraph_client,
                posts_sent_counter=posts_sent_counter,
                tqdm_sources_iterable=tqdm_sources_iterable,
                all_sources=all_sources,
                source_url=source_url,
                entity=entity,
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

