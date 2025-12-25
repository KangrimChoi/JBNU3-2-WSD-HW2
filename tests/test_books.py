# 도서 API 테스트
import pytest


class TestBookCreate:
    """도서 등록 테스트"""

    def test_create_book_as_admin(self, client, admin_token):
        """관리자가 도서 등록 성공"""
        response = client.post(
            "/api/books",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "title": "New Book",
                "description": "A new book description",
                "isbn": "9780111111111",
                "cover_image_url": "http://example.com/cover.jpg",
                "price": 29.99,
                "publication_date": "2024-01-15",
                "authors": ["Author One"],
                "categories": ["Fiction"]
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["is_success"] is True
        assert data["payload"]["title"] == "New Book"
        assert data["payload"]["isbn"] == "9780111111111"

    def test_create_book_as_user(self, client, user_token):
        """일반 사용자가 도서 등록 실패 (권한 부족)"""
        response = client.post(
            "/api/books",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "title": "New Book",
                "description": "A new book description",
                "isbn": "978-0-222222-22-2",
                "cover_image_url": "http://example.com/cover.jpg",
                "price": 29.99,
                "publication_date": "2024-01-15",
                "authors": ["Author One"],
                "categories": ["Fiction"]
            }
        )
        assert response.status_code == 403

    def test_create_book_duplicate_isbn(self, client, admin_token, test_book):
        """ISBN 중복으로 도서 등록 실패"""
        response = client.post(
            "/api/books",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "title": "Another Book",
                "description": "Description",
                "isbn": test_book.isbn,  # 중복 ISBN
                "cover_image_url": "http://example.com/cover.jpg",
                "price": 19.99,
                "publication_date": "2024-01-15",
                "authors": ["Author Two"],
                "categories": ["Fiction"]
            }
        )
        assert response.status_code == 409
        data = response.json()
        assert data["code"] == "DUPLICATE_ISBN"


class TestBookRead:
    """도서 조회 테스트"""

    def test_get_books_list(self, client, test_book):
        """도서 목록 조회 성공"""
        response = client.get("/api/books")
        assert response.status_code == 200
        data = response.json()
        assert data["is_success"] is True
        assert "books" in data["payload"]
        assert "pagination" in data["payload"]

    def test_get_book_detail(self, client, test_book):
        """도서 상세 조회 성공"""
        response = client.get(f"/api/books/{test_book.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["is_success"] is True
        assert data["payload"]["title"] == "Test Book"
        assert data["payload"]["isbn"] == test_book.isbn

    def test_get_book_not_found(self, client):
        """존재하지 않는 도서 조회 실패"""
        response = client.get("/api/books/99999")
        assert response.status_code == 404
        data = response.json()
        assert data["code"] == "BOOK_NOT_FOUND"


class TestBookUpdate:
    """도서 수정 테스트"""

    def test_update_book_as_admin(self, client, admin_token, test_book):
        """관리자가 도서 수정 성공"""
        response = client.patch(
            f"/api/books/{test_book.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "title": "Updated Book Title",
                "price": 24.99
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_success"] is True
        assert data["payload"]["title"] == "Updated Book Title"
        assert data["payload"]["price"] == "24.99"


class TestBookDelete:
    """도서 삭제 테스트"""

    def test_delete_book_as_admin(self, client, admin_token, test_book):
        """관리자가 도서 삭제 성공"""
        response = client.delete(
            f"/api/books/{test_book.id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 204

        # 삭제 확인 (조회 시 404)
        get_response = client.get(f"/api/books/{test_book.id}")
        assert get_response.status_code == 404
