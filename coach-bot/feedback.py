from rating import Rating


class FeedBack():
    def __init__(self, rating=Rating.oneStar, comment=""):
        self._rating = rating
        self._comment = comment
    
    def setRating(self, rating):
        self._rating = rating
    
    def setComment(self, comment):
        self._comment = comment
    
    def __str__(self):
        rating = ""
        for self._rating in Rating:
            rating += "*"

        return "rating: {0}\ncomment: {1}\n".format(rating, self._comment)