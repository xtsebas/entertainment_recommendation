from model.node import Node

class Rating(Node):
    def __init__(self, rating_id: str, rating: int, comment: str, final_feeling: str, recommend: bool):
        super().__init__(rating_id, "Rating",
                         rating=rating,
                         comment=comment,
                         final_feeling=final_feeling,
                         recommend=recommend)

    @property
    def rating_id(self):
        return self.node_id

    @property
    def rating(self):
        return self.properties['rating']

    @rating.setter
    def rating(self, value: int):
        self.properties['rating'] = value

    @property
    def comment(self):
        return self.properties['comment']

    @comment.setter
    def comment(self, value: str):
        self.properties['comment'] = value

    @property
    def final_feeling(self):
        return self.properties['final_feeling']

    @final_feeling.setter
    def final_feeling(self, value: str):
        self.properties['final_feeling'] = value

    @property
    def recommend(self):
        return self.properties['recommend']

    @recommend.setter
    def recommend(self, value: bool):
        self.properties['recommend'] = value
