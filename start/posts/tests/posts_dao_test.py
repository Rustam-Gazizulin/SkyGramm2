import pytest

from start.posts.dao.posts_dao import PostsDAO


class TestsPostsDao:
    @pytest.fixture()
    def posts_dao(self):
        return PostsDAO('data/posts.json')

    @pytest.fixture()
    def keys_expected(self):
        return {'poster_name', 'poster_avatar', 'pic', 'content', 'views_count', 'likes_count', 'pk'}

    # Получение всех постов

    def test_get_all_check_type(self, posts_dao):
        posts = posts_dao.get_all()
        assert type(posts) == list, "Список постов должен иметь тип список"
        assert type(posts[0]) == dict, "Один пост должен иметь тип словарь"

    def test_get_all_has_keys(self, posts_dao, keys_expected):
        posts = posts_dao.get_all()
        first_post = posts[0]
        first_post_keys = set(first_post.keys())
        assert first_post_keys == keys_expected, "Полученные ключи неверны"

    # Получение одного поста

    def test_get_one_check_type(self, posts_dao):
        post = posts_dao.get_by_pk(1)
        assert type(post) == dict, "Пост должен быть словарем"

    def test_get_one_has_keys(self, posts_dao, keys_expected):
        post = posts_dao.get_by_pk(1)
        post_keys = set(post.keys())
        assert post_keys == keys_expected, "Полученные ключи неверны"

    parameters_to_get_by_pk = [1, 2, 3, 4, 5, 6, 7, 8]

    @pytest.mark.parametrize('post_pk', parameters_to_get_by_pk)
    def test_get_one_check_type_has_correct_pk(self, posts_dao, post_pk):
        post = posts_dao.get_by_pk(post_pk)
        assert post['pk'] == post_pk, "Номер полученного поста не соответствует запрошенному"

    # Получение постов по имени пользователя
    post_parameters_by_user = [('leo', {1, 5}), ('larry', {4, 8}), ('hank', {3, 7})]

    @pytest.mark.parametrize('poster_name, post_pks_correct', post_parameters_by_user)
    def test_get_posts_by_user(self, posts_dao, poster_name, post_pks_correct):
        """Проверяем что поиск по пользователю работает верно"""

        posts = posts_dao.get_by_user(poster_name)
        post_pks = set()
        for post in posts:
            post_pks.add(post['pk'])

        assert post_pks == post_pks_correct, f"Неверный список постов для пользователя {poster_name}"

    # Получение постов по ключевому слову
    post_parameters_search = [('тарелка', {1}), ('елки', {3}), ('проснулся', {4})]

    @pytest.mark.parametrize('query, post_pks_correct', post_parameters_search)
    def test_search_for_posts(self, posts_dao, query, post_pks_correct):
        """Проверяем что поиск работает"""

        posts = posts_dao.search(query)
        post_pks = set()
        for post in posts:
            post_pks.add(post['pk'])
        assert post_pks == post_pks_correct, f"Неверный список постов по ключевому слову {query}"

    def test_search_check_type(self, posts_dao):
        """Проверяем соответствие полученных данных нужному типу"""

        posts = posts_dao.search('а')
        assert type(posts) == list, "Результат поиска должен быть списком"
        assert type(posts[0]) == dict, "Элементы найденные поиском должны быть словарями"

    def test_search_has_keys(self, posts_dao, keys_expected):
        """Проверяем наличие всех ключей у поста"""

        post = posts_dao.search('а')[0]
        post_keys = set(post.keys())
        assert post_keys == keys_expected, "Полученные ключи неверны"

    queries_and_responses = [
        ("еда", [1]),
        ("дом", [2, 7, 8]),
        ("а", list(range(1, 9))),
        ("0000000", []),
        ("Дом", [2, 7, 8])
    ]

    @pytest.mark.parametrize('query, post_pks', queries_and_responses)
    def test_search_correct_math(self, posts_dao, query, post_pks):
        """Проверяем правильность выдачи при поиске по ключевому слову"""

        posts = posts_dao.search(query)
        pks = []
        for post in posts:
            pks.append(post['pk'])

        assert pks == post_pks, f"Неверный поиск по запросу {query}"
