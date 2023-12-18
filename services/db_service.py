import asyncpg

from domain.entities import Book


async def search_on_db(params):
    db_connection = await asyncpg.connect(
        user='r2_user',
        password='secret',
        database='r2_db',
        host='localhost',
        port='5432'
    )

    try:
        result = await db_connection.fetch(
            '''
            select
                book.id,
                book.title,
                book.subtitle,
                book.publish_date,
                book.editor,
                book.description,
                book.image,
                array_agg(distinct author.name) as authors,
                array_agg(distinct category.name) as categories
            from book
            left join book_author on book.id = book_author.book_id
            left join author on book_author.author_id = author.id
            left join book_category on book.id = book_category.book_id
            left join category on book_category.category_id = category.id
            where
                (cast($1 as varchar) is null or book.id = $1) and
                (cast($2 as varchar) is null or book.title ilike $2) and
                (cast($3 as varchar)is null or book.subtitle ilike $3) and
                (cast($4 as varchar) is null or book.publish_date ilike $4) and
                (cast($5 as varchar) is null or book.editor ilike $5) and
                (cast($6 as varchar[]) is null or author.name = any($6)) and
                (cast($7 as varchar[]) is null or category.name = any($7))
            group by book.id;
            ''',
            *params
        )

        return [Book(*row) for row in result]
    except:
        return None
    finally:
        await db_connection.close()


async def save_books_on_db(books):
    db_connection = await asyncpg.connect(
        user='r2_user',
        password='secret',
        database='r2_db',
        host='localhost',
        port='5432'
    )

    try:
        async with db_connection.transaction():
            for book in books:
                await db_connection.execute(
                    '''
                    insert into book (id, title, subtitle, publish_date, editor, description, image)
                    values ($1, $2, $3, $4, $5, $6, $7)
                    on conflict do nothing
                    ''',
                    book.id, book.title, book.subtitle, book.publish_date, book.editor, book.description, book.image
                )

                for author in book.authors:
                    author_id = await db_connection.fetchval(
                        '''
                        insert into author (name) values ($1)
                        on conflict (name) do update set name = excluded.name
                        returning id 
                        ''',
                        author
                    )

                    await db_connection.execute(
                        '''
                        insert into book_author (book_id, author_id)
                        values($1, $2)
                        on conflict do nothing
                        ''',
                        book.id, author_id
                    )

                for category in book.categories:
                    category_id = await db_connection.fetchval(
                        '''
                        insert into category (name) values ($1)
                        on conflict (name) do update set name = excluded.name
                        returning id
                        ''',
                        category
                    )

                    await db_connection.execute(
                        '''
                        insert into book_category (book_id, category_id)
                        values ($1, $2)
                        on conflict do nothing
                        ''',
                        book.id, category_id
                    )
    except:
        await db_connection.rollback()
    finally:
        await db_connection.close()


async def delete_book_on_db(id):
    db_connection = await asyncpg.connect(
        user='r2_user',
        password='secret',
        database='r2_db',
        host='localhost',
        port='5432'
    )

    try:
        async with db_connection.transaction():
            await db_connection.execute(
                '''
                delete from book_author
                where book_id = $1
                ''',
                id
            )

            await db_connection.execute(
                '''
                delete from book_category
                where book_id = $1
                ''',
                id
            )

            await db_connection.execute(
                '''
                delete from book
                where id = $1
                ''',
                id
            )
    except:
        db_connection.rollback()
    finally:
        db_connection.close()


async def book_exist(id):
    db_connection = await asyncpg.connect(
        user='r2_user',
        password='secret',
        database='r2_db',
        host='localhost',
        port='5432'
    )

    try:
        result = await db_connection.fetchval(
            '''
            select 'X' from book where id = $1
            ''',
            id
        )

        if result == 'X':
            return True

        return False
    except:
        return False
    finally:
        await db_connection.close()