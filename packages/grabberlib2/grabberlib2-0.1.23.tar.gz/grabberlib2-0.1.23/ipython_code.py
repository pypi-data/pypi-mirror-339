import asyncio
from grabber.core.utils import get_new_telegraph_client
from grabber.core.bot.core import send_message
from telegraph import TelegraphException, exceptions
from time import sleep


def upload_file(file, retry_count=5, telegraph=None):
    try:
        print(f"Trying to upload {file.name}")
        resp = telegraph.upload_file(file)
    except (TelegraphException, exceptions.RetryAfterError) as exc:
        print(f"Error trying to upload {file.name}: {exc}")
        if retry_count in [10, 15, 20, 25] or retry_count > 25:
            print("Creating new account for new token")
            account = telegraph.create_account(
                short_name=SHORT_NAME,
                author_name=AUTHOR_NAME,
                author_url=AUTHOR_URL,
                replace_token=True,
            )
            telegraph = Telegraph(access_token=account["access_token"])
        print(f"Sleeping {retry_count} before trying to upload again")
        sleep(retry_count)
        retry_count += 1
        resp = upload_file(file, retry_count=retry_count, telegraph=telegraph)
    if not resp:
        resp = upload_file(file, retry_count=retry_count, telegraph=telegraph)
    print(f"Uploaded {file.name}! URL: {resp[0]['src']}")
    file_resp = resp[0]
    return file_resp["src"]


def upload_files(files, retry_count=5, telegraph=None):
    urls = set()
    for file in files:
        urls.add(upload_file(file=file, retry_count=retry_count, telegraph=telegraph))
    return urls


def create_page(
    title: str,
    html_content: str,
    telegraph_client,
    try_again=True,
) -> str:
    try:
        page = telegraph_client.create_page(title=title, html_content=html_content)
    except (
        Exception,
        exceptions.TelegraphException,
        exceptions.RetryAfterError,
    ) as exc:
        error_message = str(exc)
        if "try again" in error_message.lower() or "retry" in error_message.lower():
            sleep(5)
            if try_again:
                telegraph_client = get_new_telegraph_client()
                return create_page(
                    title=title,
                    html_content=html_content,
                    telegraph_client=telegraph_client,
                    try_again=False,
                )
    return page["url"]


def create_new_page(title, urls, telegraph_client) -> str:
    html_template = """<figure contenteditable="false"><img src="{file_path}"><figcaption dir="auto" class="editable_text" data-placeholder="{title}"></figcaption></figure>"""
    contents = []

    for url in urls:
        contents.append(html_template.format(file_path=url, title=title))

    content = "\n".join(contents)
    page_url = create_page(
        title=title,
        html_content=content,
        telegraph_client=telegraph_client,
    )

    post = f"{title} - {page_url}"
    asyncio.run(send_message(post))

    return post
