import abc
import requests
from bs4 import BeautifulSoup

# Base class for menu scraper, should be subclasses before use
class BaseMenuScraper(abc.ABC):

	_MENU_URL = None
	_SEARCH_URL = None

	def __init__(self):
		self._menu_lookup = {}

	# Any subclass must at least implement this to handle their specific menu pages
	@abc.abstractmethod
	def _extract_menu(self, soup):
		pass

	# GETs the menu as a Soup object
	def _get_menu_soup(self, url, params = {}):
		headers = {
			"User-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"
		}
		response = requests.get(url, headers = headers, params = params)
		soup = BeautifulSoup(response.text, 'html.parser')
		return soup

	# Uses the site's search to return results
	def search_menu(self, term):
		params = {
			'text' : term,
		}
		soup = self._get_menu_soup(self._SEARCH_URL, params)
		menu = self._extract_menu(soup)
		return menu

	# Gets a specific menu section of the website
	def get_menu(self, section):

		if section in self._menu_lookup:
			menu = self._menu_lookup[section]

		else:
			url = self._MENU_URL + section
			soup = self._get_menu_soup(url)
			menu = self._extract_menu(soup)

			self._menu_lookup[section] = menu
		

		return menu



