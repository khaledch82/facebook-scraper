import app.scraper as scraper

def test_unittest():
    input = '10 likes'
    assert(10==scraper.FacebookScraper.format(input))
test_unittest()