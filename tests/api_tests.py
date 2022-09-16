from app import app


class TestApi:

    def test_app_all_posts_status_code(self):
        """ ��������� ������� �� ������ ���������� ������ """
        response = app.test_client('/api/posts', follow_redirects=True)
        assert response.status_code == 200, "������ ��� ������� ���� ������ ��������"
        assert response.mimetype == 'application/json', "������� �� json"

    def test_app_one_post_status_code(self):
        """ ��������� ������� �� ������ ���������� ������ """
        response = app.test_client('/api/posts', follow_redirects=True)
        assert response.status_code == 200, "������ ��� ������� ���� ������ ��������"
        assert response.mimetype == 'application/json', "������� �� json"
