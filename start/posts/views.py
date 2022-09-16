import logging
from json import JSONDecodeError

from flask import Blueprint, render_template, request, abort
from start.posts.dao.posts_dao import PostsDAO
from start.posts.dao.comments_dao import CommentsDAO

posts_blueprint = Blueprint('posts_blueprint', __name__, template_folder='templates')
posts_dao = PostsDAO('data/posts.json')
comments_dao = CommentsDAO('data/comments.json')

logger = logging.getLogger('basic')


@posts_blueprint.route('/')
def post_all():
    logger.debug('Запрошены все посты')
    try:
        posts = posts_dao.get_all()
        return render_template('index.html', posts=posts)
    except:
        return "Что пошло не так"


@posts_blueprint.route('/posts/<int:post_pk>/')
def post_one(post_pk):
    logger.debug(f'Запрошен пост {post_pk}')
    try:
        post = posts_dao.get_by_pk(post_pk)
        comments = comments_dao.get_by_post_pk(post_pk)
    except (JSONDecodeError, FileNotFoundError) as error:
        return render_template('error.html', error=error)
    except BaseException as e:
        return render_template('error.html', error='Неизвестная ошибка')
    else:
        if post is None:
            abort(404)
        number_of_comments = len(comments)
        return render_template('post.html', post=post, comments=comments, number_of_comments=number_of_comments)


@posts_blueprint.errorhandler(404)
def post_error(e):
    return "Такой пост не найден", 404


@posts_blueprint.route('/search/')
def posts_search():
    query = request.args.get('s', "")
    if query != "":
        posts = posts_dao.search(query)
        count_posts = len(posts)
    else:
        posts = []
        count_posts = 0
    return render_template('search.html', query=query, posts=posts, count_posts=count_posts)


@posts_blueprint.route('/users/<username>/')
def posts_by_user(username):
    posts = posts_dao.get_by_user(username)
    count_posts = len(posts)

    return render_template('user-feed.html', posts=posts, count_posts=count_posts)

@posts_blueprint.route('/bookmarks/')
def posts_by_bookmarks():
    return render_template('bookmarks.html')

@posts_blueprint.route('/tag/')
def posts_by_tag():
    return render_template('tag.html')

