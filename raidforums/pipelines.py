from sqlalchemy.orm import sessionmaker
from raidforums.models import ForumSection, db_connect, create_table


class RaidforumsPipeline:

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.session = sessionmaker(bind=engine)
    
    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.
        """
        session = self.session()
        forumdb = ForumSection()

        forumdb.category = item["category"]
        if item["sub_category"] is None:
            forumdb.sub_category = None
        forumdb.sub_category = item["sub_category"]
        forumdb.forum_link = item["forum_link"]
        forumdb.forum_name = item["forum_name"]
        forumdb.forum_description = item["forum_description"]
        forumdb.threads_count = item["threads_count"]
        forumdb.posts_count = item["posts_count"]
        forumdb.forum_last_post = item["forum_last_post"]

        try:
            session.add(forumdb)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item