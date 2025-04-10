import pathlib
import uuid
from typing import Dict, List, Optional, cast
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


async def get_pages_from_pagination(
    url: str,
    target: str,
    headers: Optional[Dict[str, str]] = None,
) -> List[str]:
    pagination_params = query_pagination_mapping[target]
    source_urls = IndexedSet()
    soup = await get_soup(url, headers=headers)
    dom = etree.HTML(str(soup))
    pagination_set = soup.select(pagination_params.pages_count_query)

    if not pagination_set:
        for a_tag in dom.xpath(pagination_params.posts_query_xpath):
            if a_tag is not None and a_tag.attrib["href"] not in source_urls:
                source_urls.add(a_tag.attrib["href"])
        return list(source_urls)

    base_pagination_url = url.rsplit("/", 1)[0]
    for a_tag in dom.xpath(pagination_params.posts_query_xpath):
        page_link = a_tag.attrib["href"]
        target_url = urljoin(base_pagination_url, page_link)
        source_urls.add(target_url)

    return list(source_urls)


async def get_sources_for_buondua(
    sources: List[str],
    entity: str,
    telegraph_client: Optional[Telegraph] = None,
    final_dest: str | pathlib.Path = "",
    save_to_telegraph: bool | None = False,
    is_tag: Optional[bool] = False,
    limit: Optional[int] = None,
    **kwargs,
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
    original_folder_path = final_dest

    for source_url in tqdm_sources_iterable:
        final_dest = pathlib.Path(str(original_folder_path))
        # all_sources += await get_all_posts_for_url(repository=repository, url=source_url)
        #
        # if source_url in all_sources:
        #     tqdm_sources_iterable.set_description(
        #         f"Skipping {source_url} since it was already posted"
        #     )
        #     continue

        folder_name = ""
        urls = [
            source_url,
            *await get_pages_from_pagination(
                url=source_url,
                target=entity,
                headers=headers,
            ),
        ]
        image_tags: list[Tag] = []

        for index, url in enumerate(urls):
            tags, soup = await get_tags(
                url,
                headers=headers,
                query=query,
            )
            image_tags.extend(tags or [])
            page_title = cast(Tag, soup.find("title")).get_text(strip=True).split("- Page")[0]

            if index == 0 or not page_title:
                folder_name = f"{page_title}"
                titles.add(page_title)

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
