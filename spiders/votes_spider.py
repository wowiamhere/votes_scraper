import scrapy
import json
from scrapy.selector import Selector
from votes.items import VotesItem
import re


class GetTheVotes(scrapy.Spider):
    """
    Scraping votes per year, per senate/house, per bill, per partisanship
    """

    name: str = 'votes'
    allowed_domains  = ['govtrack.us']

    congress_session: int = 229
    last_congress: int = 229


    def start_requests(self):
        for congress_sess in range(self.congress_session, self.last_congress+1):
            yield scrapy.Request(f'https://www.govtrack.us/congress/votes?session={congress_sess}&sort=-created&faceting=false&allow_redirect=true&do_search=1&page=1', callback=self.parse, cb_kwargs=dict(congress_session = congress_sess))



    def parse(self, response, congress_session=None):
        data = json.loads(response.text)
        if data['page'] < data['num_pages']:
            #self._parse_links(data['results'], congress_session=congress_session)
            for result in data['results']:
                result_url = Selector(text=result).xpath('//a/@href').get()
                result_url = 'https://www.govtrack.us' + result_url
                yield scrapy.Request(result_url, callback=self._get_page_data, cb_kwargs=dict(congress_session=congress_session))
            for page in range(data['page']+1, data['num_pages']+1):
                next_page_url = response.url[:response.url.rfind('=')] + '=' + str(page)
                yield scrapy.Request(next_page_url, callback=self.parse, cb_kwargs=dict(congress_session=congress_session))
        elif data['page'] == data['num_pages']:
            for result in data['results']:
                result_url = Selector(text=result).xpath('//a/@href').get()
                result_url = 'https://www.govtrack.us' + result_url
                yield scrapy.Request(result_url, callback=self._get_page_data, cb_kwargs=dict(congress_session=congress_session))
            #self._parse_links(data['results'], congress_session=congress_session)
            return None



    def _parse_links(self, data_results, congress_session=None):
        for result in data_results:
            result_url = Selector(text=result).xpath('//a/@href').get()
            result_url = 'https://www.govtrack.us' + result_url
            yield scrapy.Request(result_url, callback=self._get_page_data, cb_kwargs=dict(congress_session=congress_session))



    def _get_page_data(self, response, congress_session=None):
        item = VotesItem()
        temp_string = response.xpath('//div[@id="breadcrumbs"]/div/ol/li[@class="active"]/text()[1]').get()
        item['congress_session'] = congress_session
        item['senate_or_house'] = temp_string[0]
        reg_exp_search = re.compile('#\d{1,5}\s')
        item['vote_number'] = int(reg_exp_search.search(temp_string).group().strip()[1:])
        item['resolution_name'] = response.xpath('//h1/text()').get().strip()
        item['resolution_date'] = response.xpath('//div[@id="content"]/div/text()').get().strip()[:-2]
        item['percent_yea_votes'] = int(response.xpath('//table[@class="stats"]/tbody/tr[1]/td[1]/text()').get().strip())
        item['total_yea_votes'] = int(response.xpath('//table[@class="stats"]/tbody/tr[1]/td[2]/div[last()]/text()').get().strip())
        item['total_democrat_yeas'] = int(response.xpath('//table[@class="stats"]/tbody/tr[1]/td[3]/div/text()').get().strip())
        item['total_republican_yeas'] = int(response.xpath('//table[@class="stats"]/tbody/tr[1]/td[4]/div/text()').get().strip())
        item['percent_nay_votes'] = int(response.xpath('//table[@class="stats"]/tbody/tr[2]/td[1]/text()').get().strip())
        item['total_nay_votes'] = int(response.xpath('//table[@class="stats"]/tbody/tr[2]/td[2]/div[last()]/text()').get().strip())
        item['total_democrat_nays'] = int(response.xpath('//table[@class="stats"]/tbody/tr[2]/td[3]/div/text()').get().strip())
        item['total_republican_nays'] = int(response.xpath('//table[@class="stats"]/tbody/tr[2]/td[4]/div/text()').get().strip())
        item['total_votes'] = int(item['total_yea_votes']) + int(item['total_nay_votes'])
        item['democrat_nay_voters'] = response.xpath('//table[@id="vote-list-template"]/tbody/tr[contains(@voter_group_0, "Nay") and contains(@voter_group_2,"Democrat")]/td[4]/a/text()').getall()
        item['republican_nay_voters'] = response.xpath('//table[@id="vote-list-template"]/tbody/tr[contains(@voter_group_0, "Nay") and contains(@voter_group_2,"Republican")]/td[4]/a/text()').getall()
        item['democrat_yea_voters'] = response.xpath('//table[@id="vote-list-template"]/tbody/tr[contains(@voter_group_0, "Yea") and contains(@voter_group_2,"Democrat")]/td[4]/a/text()').getall()
        item['republican_yea_voters'] = response.xpath('//table[@id="vote-list-template"]/tbody/tr[contains(@voter_group_0, "Yea") and contains(@voter_group_2,"Republican")]/td[4]/a/text()').getall()
        item['other_party_nay_voters'] = response.xpath('//table[@id="vote-list-template"]/tbody/tr[contains(@voter_group_0, "Nay") and contains(@voter_group_2,"Democrat")=False and contains(@voter_group_2,"Republican")=False]/td[4]/a/text()').getall()
        item['other_party_yea_voters'] = response.xpath('//table[@id="vote-list-template"]/tbody/tr[contains(@voter_group_0, "Yea") and contains(@voter_group_2,"Democrat")=False and contains(@voter_group_2,"Republican")=False]/td[4]/a/text()').getall()
        return item

