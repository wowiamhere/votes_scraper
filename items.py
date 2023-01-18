import scrapy

class CongressItem(scrapy.Item):
    congress_year = scrapy.Field()
    congress_number = scrapy.Field()
    total_resolutions_year = scrapy.Field()


class VotesItem(CongressItem):

    congress_session = scrapy.Field()

    resolution_name = scrapy.Field()
    resolution_date = scrapy.Field()
    
    total_votes = scrapy.Field()
    total_yea_votes = scrapy.Field()
    total_nay_votes = scrapy.Field()
    total_present_votes = scrapy.Field()
    total_not_voting_votes = scrapy.Field()

    nay_voters = scrapy.Field()
    yea_voters = scrapy.Field()
    present_voters = scrapy.Field()
    not_voting_voters = scrapy.Field()
    total_nay_voters = scrapy.Field()
    total_yea_voters = scrapy.Field()
    total_present_voters = scrapy.Field()
    total_non_voting_voters = scrapy.Field()