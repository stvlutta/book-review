#!/usr/bin/env python3

import click
from services import BookService, ReaderService, ReviewService

@click.group()
def cli():
    """Book Review CLI - Track and manage your reading history"""
    pass

@cli.command()
@click.argument('name')
def register(name):
    """Register a new reader"""
    reader_service = ReaderService()
    reader = reader_service.register_reader(name)
    click.echo(f"Reader '{reader.name}' registered successfully!")

@cli.command()
@click.argument('title')
@click.argument('author')
@click.option('--genre', help='Book genre')
def add_book(title, author, genre):
    """Add a new book"""
    book_service = BookService()
    book = book_service.add_book(title, author, genre)
    click.echo(f"Book '{book.title}' by {book.author} added successfully!")

@cli.command()
def list_books():
    """List all books"""
    book_service = BookService()
    books = book_service.get_all_books()
    
    if not books:
        click.echo("No books found.")
        return
    
    click.echo("\nAll Books:")
    click.echo("-" * 50)
    for book in books:
        genre_str = f" ({book.genre})" if book.genre else ""
        click.echo(f"ID: {book.id} - {book.title} by {book.author}{genre_str}")

@cli.command()
@click.argument('book_id', type=int)
def delete_book(book_id):
    """Delete a book by ID"""
    book_service = BookService()
    if book_service.delete_book(book_id):
        click.echo(f"Book with ID {book_id} deleted successfully!")
    else:
        click.echo(f"Book with ID {book_id} not found.")

@cli.command()
@click.argument('book_id', type=int)
@click.argument('reader_name')
@click.argument('rating', type=int)
@click.option('--comment', help='Review comment')
def add_review(book_id, reader_name, rating, comment):
    """Add a review for a book"""
    if rating < 1 or rating > 5:
        click.echo("Rating must be between 1 and 5.")
        return
    
    book_service = BookService()
    reader_service = ReaderService()
    review_service = ReviewService()
    
    book = book_service.get_book_by_id(book_id)
    if not book:
        click.echo(f"Book with ID {book_id} not found.")
        return
    
    reader = reader_service.get_reader_by_name(reader_name)
    if not reader:
        click.echo(f"Reader '{reader_name}' not found. Please register first.")
        return
    
    review = review_service.add_review(book_id, reader.id, rating, comment)
    click.echo(f"Review added for '{book.title}' by {reader_name}!")

@cli.command()
@click.argument('book_id', type=int)
def book_reviews(book_id):
    """View all reviews for a book"""
    book_service = BookService()
    review_service = ReviewService()
    
    book = book_service.get_book_by_id(book_id)
    if not book:
        click.echo(f"Book with ID {book_id} not found.")
        return
    
    reviews = review_service.get_book_reviews(book_id)
    
    click.echo(f"\nReviews for '{book.title}' by {book.author}:")
    click.echo("-" * 50)
    
    if not reviews:
        click.echo("No reviews found for this book.")
        return
    
    for review in reviews:
        comment_str = f" - {review.comment}" if review.comment else ""
        click.echo(f"Rating: {review.rating}/5 by {review.reader.name}{comment_str}")

@cli.command()
@click.argument('reader_name')
def reader_reviews(reader_name):
    """View all reviews by a reader"""
    reader_service = ReaderService()
    
    reader = reader_service.get_reader_by_name(reader_name)
    if not reader:
        click.echo(f"Reader '{reader_name}' not found.")
        return
    
    reviews = reader_service.get_reader_reviews(reader.id)
    
    click.echo(f"\nReviews by {reader_name}:")
    click.echo("-" * 50)
    
    if not reviews:
        click.echo("No reviews found for this reader.")
        return
    
    for review in reviews:
        comment_str = f" - {review.comment}" if review.comment else ""
        click.echo(f"'{review.book.title}' by {review.book.author}: {review.rating}/5{comment_str}")

@cli.command()
@click.argument('book_id', type=int)
def book_stats(book_id):
    """View statistics for a book"""
    book_service = BookService()
    stats = book_service.get_book_stats(book_id)
    
    if not stats:
        click.echo(f"Book with ID {book_id} not found.")
        return
    
    book = stats['book']
    click.echo(f"\nStatistics for '{book.title}' by {book.author}:")
    click.echo("-" * 50)
    click.echo(f"Total Reviews: {stats['review_count']}")
    click.echo(f"Average Rating: {stats['average_rating']}/5")

if __name__ == '__main__':
    cli()