import aiohttp

from domain.entities import Book


async def search_on_google(title, authors, categories, editor):
    try:
        url = 'https://www.googleapis.com/books/v1/volumes?q='

        if title is not None:
            url += f'+intitle:{title}'

        if authors != ['']:
            for author in authors:
                url += f'+inauthor:{author}'

        if categories != ['']:
            for category in categories:
                url += f'+subject:{category}'

        if editor is not None:
            url += f'inpublisher:{editor}'

        async with aiohttp.ClientSession() as session:
            google_response = await fetch_data(session, url)
            books_result = list()

            for book in google_response['items']:
                books_result.append(
                    Book(
                        book['id'],
                        book['volumeInfo']['title'],
                        '',
                        book['volumeInfo']['publishedDate'],
                        book['volumeInfo']['publisher'],
                        book['volumeInfo']['description'],
                        book['volumeInfo']['imageLinks']['thumbnail'],
                        book['volumeInfo']['categories'],
                        book['volumeInfo']['authors']
                    )
                )

            return books_result
    except Exception as e:
        return None


async def fetch_data(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            return None