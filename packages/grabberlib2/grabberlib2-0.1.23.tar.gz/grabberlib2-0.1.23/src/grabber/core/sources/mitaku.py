import pathlib
import uuid
from typing import List, Optional

from boltons.setutils import IndexedSet
from telegraph import Telegraph
from tqdm import tqdm
from unidecode import unidecode

from database.models import ExtractedPage
from database.repositories.extracted_page import ExtractedPageRepository
from grabber.core.utils import (
    build_unique_img_urls,
    get_all_posts_for_url,
    get_tags,
    headers_mapping,
    query_mapping,
    run_downloader,
    send_post_to_telegram,
)


async def get_images_from_pagination(url: str, headers: Optional[dict] = None) -> List[str]:
    page_nav_query = "div.page-link-box li a.page-numbers"
    tags, _ = await get_tags(url, headers=headers, query=page_nav_query, bypass_cloudflare=True)
    return [a.attrs["href"] for a in tags if tags]


async def get_sources_for_mitaku(
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
        all_sources += await get_all_posts_for_url(repository=repository, url=source_url)

        if source_url in all_sources:
            tqdm_sources_iterable.set_description(
                f"Skipping {source_url} since it was already posted"
            )
            continue
        folder_name = ""
        urls = [
            source_url,
            *await get_images_from_pagination(url=source_url, headers=headers),
        ]
        image_tags = []

        for index, url in enumerate(urls):
            tags, soup = await get_tags(
                url,
                headers=headers,
                query=query,
                bypass_cloudflare=True,
            )
            image_tags.extend(tags or [])

            if index == 0:
                folder_name = soup.select("title")[0].get_text()  # type: ignore
                page_title = folder_name.strip().rstrip()
                titles.add(page_title)

        if not page_title:
            page_title = soup.find("title").get_text(strip=True)
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
