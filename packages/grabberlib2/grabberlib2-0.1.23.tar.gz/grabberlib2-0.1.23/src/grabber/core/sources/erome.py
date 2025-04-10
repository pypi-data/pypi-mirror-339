import pathlib
import uuid
from typing import List, cast

from boltons.setutils import IndexedSet
from bs4 import Tag
from telegraph import Telegraph
from tqdm import tqdm
from unidecode import unidecode

from database.models import ExtractedPage
from database.repositories.extracted_page import ExtractedPageRepository
from grabber.core.utils import (
    get_all_posts_for_url,
    get_tags,
    headers_mapping,
    query_mapping,
    run_downloader,
    send_post_to_telegram,
)


async def get_sources_for_erome(
    sources: List[str],
    entity: str,
    telegraph_client: Telegraph,
    final_dest: str | pathlib.Path = "",
    save_to_telegraph: bool | None = False,
    **kwargs,
) -> None:
    query, src_attr = query_mapping[entity]
    video_attr = "src"
    headers = headers_mapping.get(entity, None)
    page_title = ""
    title_folder_mapping = {}
    posts_sent_counter = 0
    titles = IndexedSet()
    repository = ExtractedPageRepository(model=ExtractedPage)
    ordered_unique_img_urls = None
    ordered_unique_img_urls = None
    all_sources = []
    original_folder_path = final_dest
    is_video_enabled = kwargs.get("is_video_enabled")
    video_tags: list[Tag] = []

    tqdm_sources_iterable = tqdm(
        sources,
        total=len(sources),
        desc="Retrieving URLs...",
    )
    videos_query = "div.video video source"

    for source_url in tqdm_sources_iterable:
        final_dest = pathlib.Path(str(original_folder_path))
        all_sources += await get_all_posts_for_url(repository=repository, url=source_url)

        if source_url in all_sources:
            tqdm_sources_iterable.set_description(
                f"Skipping {source_url} since it was already posted"
            )
            continue

        image_tags, soup = await get_tags(source_url, headers=headers, query=query)

        title_tag = cast(Tag, soup.find("title"))
        page_title: str = title_tag.get_text(strip=True).strip().rstrip()
        page_title = (
            page_title
            .split("- Porn")[0]
        )
        titles.add(page_title)

        unique_media_urls = IndexedSet()
        for idx, img_tag in enumerate(image_tags):
            img_src = img_tag.attrs[src_attr].split("?")[0]
            image_name_prefix = f"{idx + 1}".zfill(3)
            img_name: str = img_src.split("?")[0]
            img_name = img_name.strip().rstrip()
            unique_media_urls.add((image_name_prefix, f"{img_name}", "", img_src))

        if is_video_enabled:
            video_tags = soup.select(videos_query)
            for idx, video_tag in enumerate(video_tags):
                video_name_prefix = f"{idx + 1}".zfill(3)
                video_src = video_tag.attrs[video_attr]
                video_name: str = video_src.split(".mp4")[0]
                video_name = video_name.strip().rstrip()
                unique_media_urls.add((video_name_prefix, f"{video_name}", "", video_src))

        ordered_unique_img_urls = IndexedSet(
            list(sorted(unique_media_urls, key=lambda x: list(x).pop(0)))
        )
        ordered_unique_img_urls = IndexedSet([a[1:] for a in ordered_unique_img_urls])
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
