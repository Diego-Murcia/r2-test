import asyncio

from flask import Blueprint, request, jsonify

from domain.responses import BookSearchResponse
from services.book_service import search_service, delete_service
from utils.utilities import validate_date

library_blueprint = Blueprint('library_controller', __name__)

@library_blueprint.route('/search', methods=['GET'])
async def find_book():
    get_or_default_single = lambda key, default=None: request.args.get(key) or default
    get_or_default_list = lambda key, default='': request.args.get(key, '') or default

    book_id = get_or_default_single('id')
    book_title = get_or_default_single('title')
    book_subtitle = get_or_default_single('subtitle')
    book_authors = get_or_default_list('authors').replace(' ', '').split(',')
    book_categories = get_or_default_list('categories').replace(' ', '').split(',')
    book_publish_date = get_or_default_single('publish_date')
    book_editor = get_or_default_single('editor')

    if book_id is None and book_title is None and book_subtitle is None and book_authors == [''] and book_categories == [''] and book_publish_date is None and book_editor is None:
        books_response_class = BookSearchResponse(400, 'Bad Request - No Arguments', None)
        books_response = books_response_class.to_dic()

        return jsonify(books_response), 400

    if book_publish_date is not None:
        if validate_date(book_publish_date):
            books_response_class = BookSearchResponse(400, 'Bad Request - Bad Date Format (yyyy-MM-dd)', None)
            books_response = books_response_class.to_dic()

            return jsonify(books_response), 400

    try:
        books = await search_service(book_id, book_title, book_subtitle, book_authors, book_categories,
                                     book_publish_date, book_editor)

        if books is not None and books != []:
            books_dic = [book.to_dict() for book in books]
            books_response_class = BookSearchResponse(200, 'Success', books_dic)
            books_response = books_response_class.to_dic()

            return jsonify(books_response), 200
        else:
            books_response_class = BookSearchResponse(404, 'No Books Found', None)
            books_response = books_response_class.to_dic()

            return jsonify(books_response), 404
    except Exception:
        books_response_class = BookSearchResponse(500, 'Internal Server Error', None)
        books_response = books_response_class.to_dic()

        return jsonify(books_response), 500


@library_blueprint.route('/<book_id>', methods=['DELETE'])
async def delete_book(book_id):
    if await delete_service(book_id):
        books_response_class = BookSearchResponse(200, 'Success - Book Delete', None)
        books_response = books_response_class.to_dic()

        return jsonify(books_response), 200
    else:
        books_response_class = BookSearchResponse(404, 'Book Not Found', None)
        books_response = books_response_class.to_dic()

        return jsonify(books_response), 404
