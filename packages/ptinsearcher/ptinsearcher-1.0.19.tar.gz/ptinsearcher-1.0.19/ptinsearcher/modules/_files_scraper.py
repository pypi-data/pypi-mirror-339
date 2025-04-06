import re

from bs4 import BeautifulSoup

from ptlibs import ptprinthelper
from modules import metadata, emails, comments, forms, phone_numbers, ip_addresses, urls

class FileScraper:
    def __init__(self, args, things_to_extract: dict, ptjsonlib: object):
        self.use_json: bool = args.json

    def process_file(self, path_to_local_file: str, args, things_to_extract: dict, ptjsonlib: object) -> dict:
        """Returns extracted info from <filepath>"""
        try:
            import magic
            import mimetypes
            mimetype       = mimetypes.guess_type(path_to_local_file)[0]
            content_type   = magic.from_file(path_to_local_file)
        except Exception as e:
            self.ptjsonlib.end_error("Dependency not found, please install: sudo apt install libmagic1", self.use_json)

        is_readable    = True if re.findall("text", content_type.lower()) else False
        file_extension = path_to_local_file.split("/")[-1].split(".")[-1] if "." in path_to_local_file.split("/")[-1] else None

        ptprinthelper.ptprint(f"Provided source.............: {path_to_local_file.split('/')[-1]}", "INFO", not self.use_json, colortext=True)
        ptprinthelper.ptprint(f"Extension...................: {file_extension}", "INFO", not self.use_json)
        ptprinthelper.ptprint(f"Source-Type.................: {content_type}", "INFO", not self.use_json)
        ptprinthelper.ptprint(f"MIME Type...................: {mimetype}", "INFO", not self.use_json)

        result = self._scrape_file(path_to_local_file, is_readable, mimetype, ptjsonlib, args, things_to_extract)
        return result

    def _scrape_file(self, path_to_local_file: str, is_readable, mimetype, ptjsonlib, args, extract_types: dict) -> dict:
        """Scrapes extract_types from <filepath>"""
        result_data = {"url": path_to_local_file.rsplit("/")[-1], "metadata": None, "emails": None, "phone_numbers": None, "ip_addresses": None, "abs_urls": None, "internal_urls": None, "internal_urls_with_parameters": None, "external_urls": None, "insecure_sources": None, "subdomains": None, "forms": None, "comments": None}

        if extract_types["metadata"]:
            extracted_metadata = metadata.MetadataExtractor().get_metadata(path_to_local_file=path_to_local_file)
            result_data["metadata"] = extracted_metadata
            if len(extracted_metadata.keys()) == 1 and "ExifTool" in list(extracted_metadata)[0]:
                result_data["metadata"] = {list(extracted_metadata)[0].split("ExifTool:")[-1]: list(extracted_metadata.values())[0]}

        if not is_readable:
            return result_data

        with open(path_to_local_file, "rb") as file:
            file_content = str(file.read())

            if extract_types["emails"]:
                result_data["emails"] = emails.find_emails(file_content)

            if extract_types["comments"]:
                result_data["comments"] = {}

            if extract_types["phone_numbers"]:
                result_data["phone_numbers"] = phone_numbers.find_phone_numbers(file_content)

            if extract_types["ip_addresses"]:
                result_data["ip_addresses"] = ip_addresses.find_ip_addresses(file_content)

            if any([extract_types["internal_urls"], extract_types["external_urls"], extract_types["internal_urls_with_parameters"], extract_types["subdomains"]]):
                result_data["external_urls"] = urls.find_urls_in_file(file_content)

            if extract_types["subdomains"]:
                result_data["subdomains"] = urls.get_subdomains_from_list(result_data["external_urls"])

            if extract_types["internal_urls_with_parameters"]:
                result_data["internal_urls_with_parameters"] = dict()
                """
                if args.grouping_complete:
                    result_data["internal_urls_with_parameters"] = dict()
                else:
                    result_data["internal_urls_with_parameters"] = "Not a HTML file"
                """

            if extract_types["forms"]:
                if str(mimetype) in ["text/html"]:
                    soup = self._get_soup(file_content)
                    result_data["forms"] = forms.get_forms(soup)
                else:
                    result_data["forms"] = {}
                    """
                    if args.grouping_complete:
                        result_data["forms"] = dict()
                    else:
                        result_data["forms"] = "Not a HTML file"
                    """
        return result_data

    def _get_soup(self, string, args):
        if "<!ENTITY".lower() in string.lower():
            ptprinthelper.ptprint(f"Forbidden entities found", "ERROR", not self.use_json, colortext=True)
            return False
        else:
            soup = BeautifulSoup(string, features="lxml")
            bdos = soup.find_all("bdo", {"dir": "rtl"})
            for item in bdos:
                item.string.replace_with(item.text[::-1])
            return soup
