from math import sqrt


class Calculator():
    """
    Class for calculating the score of a movie, to see if it is going to be a BlockBuster.
    """

    def confidence(self, words, positive_percent):
        """Confidence uses Wilson score interval to approximate what a large group says about the movie, given
        the number of words used, and how positive the score is.
        The formula is taken and modified from:

        http://amix.dk/blog/post/19588

        Which uses the formula to explain how the Reddit voting comment system is working.

        :param words:
        :param positive_percent:
        :return number:
        """
        n = int(words)

        if n == 0:
            return 0

        z = 1.0
        phat = float(positive_percent)
        return sqrt(phat+z*z/(2*n)-z*((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)


    def calculate_score(self, words, pos_percent, pageviews_for_one_year):
        """Calculate a score, given number of words, percentages of words witch was positice and page views over a year.
        The score that indicates if a movie is going to be a blockbuster,
        scores over 500 indicates blockbusters, score over 100 indicates a good seller,
        scores under 100 indicates under performers.

        Words is a int.
        pos_percent is a float e.g. 0.435909050542391
        pageviews_for_one_year is a int

        :param words:
        :param pos_percent:
        :param pageviews_for_one_year:
        :return score:
        """

        confidence = self.confidence(words, pos_percent)
        views_per_day = pageviews_for_one_year / 365
        return confidence + (views_per_day/10)


# john wick
# print calculate_score(8225, 0.0014210927907387838, 506420)
# 138.038488266

# the gambler
# print calculate_score(663, 0.435909050542391, 94024)
# 25.6595290813

# interstellar
# print calculate_score(11764, 1, 2959665)
# 810.99993625

# the pyramid
# print calculate_score(10157, 0.000252202653361454, 91290)
# 25.0173592396

# guardians of the galaxy
# print calculate_score(4763, 0.003281085402914509, 5577894)
# 1528.05817166

# dumb and dumber to
# print calculate_score(5157, 0.000015064795769595154, 1402891)
# 384.010581335

# the hunger games mockingjay part 1
# print calculate_score(9862, 0.9999974571356898, 2565702)
# 702.999922685

# fury
# print calculate_score(15251, 1, 1424819)
# 390.999950825