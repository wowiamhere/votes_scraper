        for result in data['results']:
            url_to_get = Selector(text=result).xpath('//a/@href').getall()
            yield scrapy.Request(url=f'https://www.{self.allowed_domains}{url_to_get}', callback=self.get_data)

        if data['page'] <= data['num_pages']:
            self.page += 1
            url = url_string
            yield scrapy.Request(url=url, callback=self.parse)

    def get_data(self, response):
        pass
        # response.xpath('//table[@class='stats']/thead/tr/th[3]')
