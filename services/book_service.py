import asyncio

from services.db_service import search_on_db, save_books_on_db, delete_book_on_db, book_exist
from services.google_service import search_on_google


async def search_service(id, title, subtitle, authors, categories, publish_date, editor):
    params = [id, title, subtitle, publish_date, editor, authors if authors != [''] else None, categories if categories != [''] else None]

    db_books = await search_on_db(params)

    if db_books != [] and db_books is not None:
        return db_books
    else:
        google_books = await search_on_google(title, authors, categories, editor)

        if google_books != [] and google_books is not None:
            await save_books_on_db(google_books)

            return google_books

    return None


async def delete_service(id):
    if await book_exist(id):
        await delete_book_on_db(id)
        return True

    return False
