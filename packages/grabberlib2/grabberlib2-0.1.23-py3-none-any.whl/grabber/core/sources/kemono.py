import asyncio
import pathlib
import uuid
from typing import Any, Dict, List, Optional, cast
from urllib.parse import urljoin, urlparse

from boltons.setutils import IndexedSet
from bs4 import BeautifulSoup, Tag
from lxml import etree
from telegraph import Telegraph
from tqdm import tqdm
from unidecode import unidecode
from pydoll.browser.chrome import Chrome
from pydoll.browser.options import Options

from database.models import ExtractedPage
from database.repositories.extracted_page import ExtractedPageRepository
from grabber.core.utils import (
    build_unique_img_urls,
    build_unique_video_urls,
    get_all_posts_for_url,
    get_webdriver,
    run_downloader,
    get_soup,
    get_tags,
    headers_mapping,
    query_mapping,
    query_pagination_mapping,
    send_post_to_telegram,
)


async def get_images_from_pagination(
    url: str, headers: dict[str, str] | None = None
) -> tuple[list[Tag], list[Tag]]:
    parsed_url = urlparse(url)
    base_url = f"https://{parsed_url.netloc}"
    pagination_query = "menu a[aria-current='page']"
    images_query = "div.post__files div.post__thumbnail figure a"
    videos_query = "div.post__body ul li div.fluid_video_wrapper video source"
    posts_query = "div.card-list__items article.post-card.post-card--preview a"
    pagination_links = IndexedSet()

    images_tags = IndexedSet()
    videos_tags = IndexedSet()
    sources = IndexedSet()
    pagination_set: set[Tag] = set()
    pagination_links.add(url)
    options = Options()
    options.add_argument("--headless")

    async with Chrome(connection_port=9222, options=options) as browser:
        await browser.start()
        page = await browser.get_page()
        await page.go_to(url)
        soup = BeautifulSoup(await page.page_source)

        if not soup.select(pagination_query) or not soup.select(posts_query):
            await page.refresh()
            soup = BeautifulSoup(await page.page_source) 

        for a in soup.select(pagination_query):
            a_tag_value = a.get_text(strip=True).strip().rstrip()
            if a_tag_value.isdigit() and a_tag_value != "1":
                pagination_set.add(a)

        posts_tags = [a for a in soup.select(posts_query)]
        for tag in posts_tags:
            href = tag.attrs["href"]
            sources.add(f"{base_url}{href}")

        if pagination_set:
            for page_url in pagination_set:
                link: str = page_url.attrs["href"]
                sources.add(f"{base_url}{link}")

        for link in sources:
            await page.go_to(link)
            # driver.refresh()
            soup = BeautifulSoup(await page.page_source)
            images_tags.update(*soup.select(images_query))
            videos = soup.select(videos_query)
            if videos:
                videos_tags.update(*videos)

    return list(images_tags), list(videos_tags)


async def get_sources_for_kemono(
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
    title_folder_mapping = {}
    posts_sent_counter = 0
    titles = IndexedSet()
    repository = ExtractedPageRepository(model=ExtractedPage)
    ordered_unique_img_urls = None
    all_sources = []
    original_folder_path = final_dest
    ordered_unique_video_urls = IndexedSet()

    for source_url in tqdm_sources_iterable:
        final_dest = pathlib.Path(str(original_folder_path))
        all_sources += await get_all_posts_for_url(
            repository=repository, url=source_url
        )

        # if source_url in all_sources:
        #     tqdm_sources_iterable.set_description(
        #         f"Skipping {source_url} since it was already posted"
        #     )
        #     continue

        if posts_sent_counter in [50, 100, 150, 200, 250]:
            await asyncio.sleep(10)

        folder_name = ""
        image_tags, videos_tags = [
            *await get_images_from_pagination(
                url=source_url,
                headers=headers,
            ),
        ]
        if not image_tags:
            tqdm_sources_iterable.set_postfix_str(
                f"Error retrieving image URLs for {source_url}. Skipping it.."
            )
            continue
        options = Options()
        options.add_argument("--headless")
        async with Chrome(connection_port=9222, options=options) as browser:
            await browser.start()
            page = await browser.get_page()
            await page.go_to(source_url)
            soup = BeautifulSoup(await page.page_source)


        page_title = cast(Tag, soup.find("title")).get_text(strip=True).strip().rstrip()
        page_title = page_title.split("| Kemono")[0]
        page_title = unidecode(
            " ".join(
                f"#{part.strip().replace(' ', '').replace('.', '_').replace('-', '_')}"
                for part in page_title.split("/")
            )
        )
        folder_name = f"{page_title}"
        titles.add(page_title)

        image_tags = sorted(image_tags, key=lambda tag: tag.attrs["href"] if "href" in tag.attrs else tag.attrs["src"])
        ordered_unique_img_urls = await build_unique_img_urls(image_tags, src_attr, "src")

        if videos_tags:
            ordered_unique_video_urls = await build_unique_video_urls(videos_tags, "src")

        tqdm_sources_iterable.set_description(
            f"Finished retrieving images for {page_title}"
        )

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
            all_sources += await send_post_to_telegram(
                ordered_unique_img_urls=ordered_unique_img_urls,
                ordered_unique_video_urls=ordered_unique_video_urls,
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
