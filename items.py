import scrapy

class CongressItem(scrapy.Item):
    congress_year = scrapy.Field()
    congress_number = scrapy.Field()
    total_resolutions_year = scrapy.Field()


class VotesItem(CongressItem):

    congress_session = scrapy.Field()
    senate_or_house = scrapy.Field()
    vote_number = scrapy.Field()

    resolution_name = scrapy.Field()
    resolution_date = scrapy.Field()

    total_votes = scrapy.Field()
    total_yea_votes = scrapy.Field()
    total_nay_votes = scrapy.Field()

    total_republican_nays = scrapy.Field()
    total_republican_yeas = scrapy.Field()
    total_democrat_nays = scrapy.Field()
    total_democrat_yeas = scrapy.Field()

    percent_yea_votes = scrapy.Field()
    percent_nay_votes = scrapy.Field()

    democrat_nay_voters = scrapy.Field()
    republican_nay_voters = scrapy.Field()

    democrat_yea_voters = scrapy.Field()
    republican_yea_voters = scrapy.Field()

    other_party_nay_voters = scrapy.Field()
    other_party_yea_voters = scrapy.Field()