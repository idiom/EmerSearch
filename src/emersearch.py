#!/usr/bin/env python

import argparse
from bs4 import BeautifulSoup
import requests

"""
MIT License

Copyright (c) 2020 Sean Wilson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class InvalidSearchException(Exception):
    pass


class EmerSearch(object):
    """
    Submit request to the emercoin explorer and return a list of results from teh parsed HTML.

    This doesn't use an API or other supported endpoint, so expect it to break.


    """

    def __init__(self, debug=False):
        self.base_url = "https://explorer.emercoin.com/nvs"
        self.user_agent_string = 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'
        self.debug = debug

    def _parse_response_html(self, html_data, table_id='block_table'):
        soup = BeautifulSoup(html_data, 'html.parser')
        result = []

        table_ref = soup.find('table', attrs={'id': table_id})
        if not table_ref:
            raise ValueError('Result table not found.')

        table_body = table_ref.find('tbody')
        for row in table_body.find_all('tr'):
            prop = row.find_all('td')
            nvs_result = [data.text.strip() for data in prop]
            result.append({
                'type': nvs_result[0],
                'name': nvs_result[1],
                'value': nvs_result[3],
                'block': nvs_result[5],
                'expires': nvs_result[6]})
        return result

    def _debug_print(self, msg):
        if self.debug:
            print(msg)

    def search(self, name='', value='', type='', page_size='all', ignore_empty_type=1, valid_only=1):
        """
        Perform a search using the name and/or value.

        :param name:  The name to search for.
        :param value: The value to search for.
        :param type:  The type of results
        :param page_size:  The page size to use. Default all
        :param ignore_empty_type:   Ignore empty type results. Default 1
        :param valid_only: Include only valid results. Default 1
        :return:

        """

        if not name and not value:
            raise InvalidSearchException("Either name or value must be set")

        if page_size not in [25, 50, 100, 'all']:
            page_size = 'all'
        headers = {'User-agent': self.user_agent_string}
        query_string = '/%s/%s/%s/%s/%s/%s' % (type, name, value, page_size, ignore_empty_type, valid_only)

        self._debug_print(' [*] Type: %s' % type)
        self._debug_print(' [*] Name: %s' % name)
        self._debug_print(' [*] Value: %s' % value)
        self._debug_print(' [*] Page Size: %s' % page_size)
        self._debug_print(' [*] Ignore Empty Type: %s' % ignore_empty_type)
        self._debug_print(' [*] Valid Only: %s' % valid_only)
        self._debug_print(' [*] Using query string: %s' % query_string)
        t = requests.get('%s%s' % (self.base_url, query_string), headers=headers)
        if t:
            self._debug_print(" [*] Status Code: %d" % t.status_code)
            if t.status_code == 200:
                return self._parse_response_html(t.text)


def display_results(results):

    if not results:
        print("No results found.")
        return

    print(" Found %d NVS records" % len(results))
    print("{0:<8}{1:<32}{2:<48}{3:<8}{4:<8}".format("Type", "Name", "Value", "Block", "Expires"))
    for record in results:
        print('{0:<8}{1:<32}{2:<48}{3:<8}{4:<8}'.format(record['type'], record['name'], record['value'], record['block'], record['expires']))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", help="The type of NVS records to search.", nargs="?", type=str, dest="type", const="", default="")
    parser.add_argument("--name", help="The name to search for.", nargs="?", type=str, dest="name", const="", default="")
    parser.add_argument("--value", help="The value to search for.", nargs="?", type=str, dest="value", const="", default="")
    parser.add_argument("--page_size", help="The page size for results [25, 50, 100, all]", nargs="?", type=int, dest="page_size", const=0, default=25)
    parser.add_argument("--include_empty", help="Include empty result types", action="store_true")
    parser.add_argument("--include_invalid", help="Include invalid/expired results.", action="store_true")
    parser.add_argument("-v", "--verbose", help="Include verbose output", action="store_true")
    args = parser.parse_args()

    if not args.name and not args.value:
        print("Error! You must specify either a name and/or value to search for.")
        return

    es = EmerSearch(debug=args.verbose)

    ignore_empty_type = 1
    valid_only = 1
    if args.include_empty:
        ignore_empty_type = 0

    if args.include_invalid:
        valid_only = 0

    results = es.search(args.name, args.value, args.type, args.page_size, ignore_empty_type, valid_only)
    display_results(results)


if __name__ == "__main__":
    main()
