import dataclasses
import requests, bs4


@dataclasses.dataclass
class MenuItem:
    name: str
    price: str
    calories: str

    def __str__(self) -> str:
        return f"{self.name}\n   {self.price}   {self.calories}"


class TacoBellScraper:
    _SEARCH_URL = "https://www.tacobell.com/search"

    def _get_menu_soup(self, url: str, params: dict = {}) -> bs4.BeautifulSoup:
        headers = {
            "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"
        }
        response = requests.get(url, headers=headers, params=params)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        return soup

    # Uses the site's search to return results
    def search_menu(self, term: str) -> list[MenuItem]:
        params = {
            "text": term,
        }
        soup = self._get_menu_soup(self._SEARCH_URL, params)
        menu = self._extract_menu(soup)
        return menu

    # Extracts the given field's text and strips it
    def _extract_field(self, card: bs4.Tag, field_name: str) -> str:
        result = card.find("div", class_=field_name).get_text()
        result = result.replace("&nbsp", " ")
        result = result.strip()
        return result

    # Extracts a menu item from the page's card
    def _extract_item(self, card: bs4.Tag) -> MenuItem:
        name = self._extract_field(card, "product-name")
        price = self._extract_field(card, "product-price")

        # Not all menu items have a calorie field
        try:
            calories = self._extract_field(card, "product-calorie")
        except:
            calories = None

        return MenuItem(name, price, calories)

    # For a given menu page soup, this should return the items on it
    def _extract_menu(self, soup: bs4.BeautifulSoup) -> list[MenuItem]:
        try:
            cards = soup.find_all("div", class_="product-details")

            menu = []
            for card in cards:
                menu.append(self._extract_item(card))

            return menu

        except Exception as err:
            print("Error trying to parse menu", err)
            return []
