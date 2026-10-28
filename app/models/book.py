from app.database.connection import get_connection

COLUMNS = "id, title, author, publication_year, price, available"


def create_book(data: dict) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                INSERT INTO books (title, author, publication_year, price, available)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING {COLUMNS}
                """,
                (data["title"], data["author"], data["publication_year"],
                 data["price"], data["available"]),
            )
            return cur.fetchone()


def get_all_books() -> list[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT {COLUMNS} FROM books ORDER BY id")
            return cur.fetchall()


def get_book_by_id(book_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT {COLUMNS} FROM books WHERE id = %s", (book_id,))
            return cur.fetchone()


def update_book(book_id: int, data: dict) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                UPDATE books
                SET title = %s, author = %s, publication_year = %s,
                    price = %s, available = %s
                WHERE id = %s
                RETURNING {COLUMNS}
                """,
                (data["title"], data["author"], data["publication_year"],
                 data["price"], data["available"], book_id),
            )
            return cur.fetchone()


def delete_book(book_id: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM books WHERE id = %s", (book_id,))
            return cur.rowcount > 0