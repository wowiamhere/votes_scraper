import scrapy
import json
from scrapy.selector import Selector
from votes.items import VotesItem


class GetTheVotes(scrapy.Spider):
    """
    Scraping votes per year, per senate/house, per bill, per partisanship
    """

    name: str = 'votes'
    allowed_domains  = ['govtrack.us']

    congress_session: int = 229
    last_congress: int = 230


    def start_requests(self):

        for congress_sess in range(self.congress_session, self.last_congress+1):
            yield scrapy.Request(f'https://www.govtrack.us/congress/votes?session={congress_sess}&sort=-created&faceting=false&allow_redirect=true&do_search=1&page=1', callback=self.parse, cb_kwargs=dict(congress_session = congress_sess))


    def parse(self, response, congress_session=congress_session):

        data = json.loads(response.text)

        if len(response.url)>0:
            from scrapy.shell import inspect_response
            inspect_response(response, self)

        if data['page'] < data['num_pages']:
            self._parse_links(data['results'])

            for page in range(data['page']+1, data['num_pages']+1):
                next_page_url = response.url[:response.url.rfind('=')] + '=' + str(page)
                yield scrapy.Request(next_page_url, callback=self.parse, cb_kwargs=dict(congress_session=congress_session))

        elif data['page'] == data['num_pages']:
            self._parse_links(data['results'])
            return None


    def _parse_links(self, data_results):
        for result in data_results:
            result_url = Selector(text=result).xpath('//a/@href').get()
            yield scrapy.Request(f'http://www.{self.allowed_domains}{result_url}', callback=self._get_page_data)



    def _get_page_data(self, data):
        pass
