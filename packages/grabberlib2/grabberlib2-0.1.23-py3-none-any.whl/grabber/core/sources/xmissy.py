import pathlib
import uuid
from typing import cast

from boltons.setutils import IndexedSet
from bs4 import Tag
from telegraph import Telegraph
from tqdm import tqdm
from unidecode import unidecode

from database.models import ExtractedPage
from database.repositories.extracted_page import ExtractedPageRepository
from grabber.core.utils import (
    build_unique_img_urls,
    downloader,
    get_all_posts_for_url,
    headers_mapping,
    get_tags,
    send_post_to_telegram,
)


async def get_sources_for_xmissy(
    sources: list[str],
    entity: str,
    telegraph_client: Telegraph | None = None,
    final_dest: str | pathlib.Path = "",
    save_to_telegraph: bool | None = False,
    is_tag: bool | None = False,
    limit: int | None = None,
    **kwargs,
) -> None:
    image_query = "div#gallery div.noclick-image img"
    first_image_src_attr = "src"
    second_image_src_attr = "data-src"
    headers = headers_mapping.get(entity, None)
    page_title = ""
    title_folder_mapping = {}
    posts_sent_counter = 0
    titles = IndexedSet()
    repository = ExtractedPageRepository(model=ExtractedPage)
    ordered_unique_img_urls = None
    all_sources = []
    original_folder_path = final_dest

    tqdm_sources_iterable = tqdm(
        sources,
        total=len(sources),
        desc="Retrieving URLs...",
    )

    for source_url in tqdm_sources_iterable:
        final_dest = pathlib.Path(str(original_folder_path))
        all_sources += await get_all_posts_for_url(repository=repository, url=source_url)

        if source_url in all_sources:
            tqdm_sources_iterable.set_description(
                f"Skipping {source_url} since it was already posted"
            )
            continue

        image_tags, soup = await get_tags(source_url, headers=headers, query=image_query)
        folder_name = ""

        page_title = (
            cast(Tag, soup.find("title")).get_text(strip=True).split("| xMissy")[0].strip().rstrip()
        )
        titles.add(page_title)

        ordered_unique_img_urls = await build_unique_img_urls(
            image_tags, first_image_src_attr, second_image_src_attr
        )
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
            )
        page_title = ""

    if final_dest:
        await downloader(
            titles=list(titles),
            title_folder_mapping=title_folder_mapping,
            headers=headers,
        )
