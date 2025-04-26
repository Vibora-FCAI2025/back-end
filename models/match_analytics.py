from .document import Document
from .user import User
from bson import ObjectId

class MatchAnalytics(Document):
    REQUIRED_FIELDS = ['user_id', 'data', 'annotated_video_url']

    def __init__(self, data=None):
        super().__init__('match_analysis', data, required_fields=self.REQUIRED_FIELDS)

    @property
    def user_id(self):
        return self.data.get('user_id')

    @property
    def data(self):
        return self.data.get('data')

    @property
    def annotated_video_url(self):
        return self.data.get('annotated_video_url')

    @property
    def owner(self):
        """
        This is to mimic the relationship to the `User` model in the SQLAlchemy class.
        Returns the `User` object associated with the `user_id` of the match.
        """
        return User.find_one('users', {"_id": ObjectId(self.user_id)})

    def __str__(self):
        return f"MatchAnalytics(user_id={self.user_id}, annotated_video_url={self.annotated_video_url})"
