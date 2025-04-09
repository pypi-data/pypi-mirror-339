from scraipe_cyber.ukraine.cert_ua_scraper import CertUaScraper
from scraipe.defaults import MultiScraper, IngressRule, TextScraper
from scraipe.extended import TelegramMessageScraper
from scraipe import IScraper
class UkraineCyberMultiScraper(MultiScraper):
    """
    MultiScraper that combines multiple scrapers for scraping documents about Ukrainian cyber incidents.
    """
    def __init__(
        self, 
        telegram_message_scraper:IScraper,
        debug: bool = False, debug_delimiter:str = "; "):
        """
        Initializes the UkraineCyberMultiScraper with specific scrapers and rules.
        """    
                
        # Define the ingress rules for the scraper
        ingress_rules = [
            # Cert-UA article scraper 
            IngressRule.from_scraper(CertUaScraper(),exclusive=True),
            # Telegram message scrapers
            IngressRule.from_scraper(telegram_message_scraper,exclusive=True) if telegram_message_scraper else None,
            # Fallback to NewsScraper
            IngressRule.from_scraper(TextScraper()),
            # Fallback to TextScraper
            IngressRule.from_scraper(TextScraper()),
        ]
        print(ingress_rules)
        
        super().__init__(
            ingress_rules=ingress_rules,
            debug=debug,
            debug_delimiter=debug_delimiter)