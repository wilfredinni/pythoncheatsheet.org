import unittest
from config import Config
from app import db, create_app
from app.models import User, Post, Tag


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"  # use the db in the ram


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username="test_user")
        u.set_password("test_password")
        self.assertFalse(u.check_password("password"))
        self.assertTrue(u.check_password("test_password"))

    def test_avatar(self):
        u = User(username="john", email="john@example.com")
        self.assertEqual(
            u.avatar(128),
            (
                "https://www.gravatar.com/avatar/"
                "d4c74594d841139328695756648b6bd6"
                "?d=identicon&s=128"
            ),
        )

    def test_post(self):
        u = User(username="test_user")
        db.session.add(u)
        post = Post(body="test body", author=u, title="test_title")
        db.session.add(post)
        db.session.commit()
        post = Post.query.filter_by(id=1)

        self.assertEqual((post[0].title), ("test_title"))
        self.assertEqual((post[0].body), ("test body"))
        self.assertEqual((post[0].author.username), ("test_user"))

    def test_tags(self):
        u = User(username="test_user")
        db.session.add(u)
        db.session.commit()

        post = Post(body="test body", author=u, title="test_title")
        db.session.add(post)
        db.session.commit()

        post = Post.query.filter_by(id=1)

        tag1 = Tag(name="test_tag_1")
        tag2 = Tag(name="test_tag_2")
        db.session.add_all([tag1, tag2])
        db.session.commit()

        post[0].tag.append(tag1)
        post[0].tag.append(tag2)
        db.session.commit()
        self.assertEqual((post[0].tag[0].name), ("test_tag_1"))
        self.assertEqual((post[0].tag[1].name), ("test_tag_2"))

        post[0].tag.remove(tag1)
        db.session.commit()
        self.assertNotEqual((post[0].tag[0].name), ("test_tag_1"))
        self.assertEqual((post[0].tag[0].name), ("test_tag_2"))

        post[0].tag.remove(tag2)
        db.session.commit()
        self.assertNotIn((tag2), post[0].tag)


if __name__ == "__main__":
    unittest.main(verbosity=2)
