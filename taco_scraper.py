import menu_scraper


# TacoBell specific scraper
class TacoBellScraper(menu_scraper.BaseMenuScraper):
    _MENU_URL = "https://www.tacobell.com/food/"
    _SEARCH_URL = "https://www.tacobell.com/search"

    # Extracts the given field's text and strips it
    def _extract_field(self, card, field_name):
        result = card.find("div", class_=field_name).get_text()
        result = result.replace("&nbsp", " ")
        result = result.strip()
        return result

    # Extracts a menu item from the page's card
    def _extract_item(self, card):
        name = self._extract_field(card, "product-name")
        price = self._extract_field(card, "product-price")

        # Not all menu items have a calorie field
        try:
            calories = self._extract_field(card, "product-calorie")
        except:
            calories = "N/A"

        return name, price, calories

    # For a given menu page soup, this should return the items on it
    def _extract_menu(self, soup):
        try:
            cards = soup.find_all("div", class_="product-details")

            menu = {}
            for card in cards:
                name, price, calories = self._extract_item(card)

                menu[name] = {"price": price, "calories": calories}

            return menu
        except Exception:
            print("Error trying to parse menu")
            return {}
