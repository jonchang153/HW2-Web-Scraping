import scrapy

# create a class that inherits from Spider
class ImdbSpider(scrapy.Spider):

  name = 'imdb_spider' # give this spider a name that can be called from the terminal
    
  # paste the url of the IMDB page of the movie to be scraped
  start_urls = ['https://www.imdb.com/title/tt0111161/']


  def parse(self, response):
    """
    Accesses the full credits (including the full cast) of the specified IMDB page
    and passes this to the parse_full_credits() method.
    """

    # use urljoin(), which appends the argument to the current url stored in the 
    # response object, to access the full credits of the movie's main IMDB page
    next_page = response.urljoin('fullcredits/')

    # use scrapy.Request to yield this new URL while calling parse_full_credits()
    yield scrapy.Request(next_page, callback = self.parse_full_credits)


  def parse_full_credits(self, response):
    """
    Uses css selectors to get the link to each actor's page found in the full credits
    page of the movie. Then passes each actor's page to the parse_actor_page() method.
    """

    # this css gets the href attribute of all a tags that have a td ancestor with 
    # class primary_photo, which gets the url of each actor listed in the full 
    # credits page
    actor_pages = response.css('td.primary_photo a::attr(href)').getall()

    # loop through each actor's url
    for actor_page in actor_pages:
      # use urljoin() to yield the url of this actor while calling parse_actor_page()
      yield scrapy.Request(response.urljoin(actor_page), callback = self.parse_actor_page)


  def parse_actor_page(self, response):
    """
    Uses css selectors to get the actor name and the name of every movie and TV show
    they starred in, for a given actor's url page. Each of these movie or TV show's 
    name is yielded in a dictionary with the actor's name.
    """

    # select the text of the FIRST span tag with class itemprop with an h1 ancestor
    actor_name = response.css('h1 span.itemprop::text').get()

    # select the text of ALL a tags that are ancestors of b tags that are ancestors
    # of div tags with class containing filmo-row and id containing actor
    names = response.css('div.filmo-row[id*=actor] b a::text').getall()

    # loop through each movie or TV show name
    for movie_or_TV_name in names:
      # yield a dictionary containing the actor's name and the movie or TV show's name
      yield {
        "actor" : actor_name, 
        "movie_or_TV_name" : movie_or_TV_name
      }