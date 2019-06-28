"""详情页测试案例"""
import unittest
from pprint import pprint

import requests

from wenshu_utils.document.parse import parse_detail
from wenshu_utils.wzws.decrypt import decrypt_wzws


class DetailPageTestCase(unittest.TestCase):
    def setUp(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        })

        self.error_msg = "请开启JavaScript并刷新该页"

    def tearDown(self):
        self.session.close()

    def test_detail_page(self):
        url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx"
        params = {
            "DocID": "a8b745f3-43ac-402c-99bf-68b9a9cae635",
        }
        response = self.session.get(url, params=params)
        text = response.content.decode()

        if self.error_msg in text:
            retry = 3
            for _ in range(retry):
                redirect_url = decrypt_wzws(text)
                response = self.session.get(redirect_url)
                text = response.content.decode()
                if self.error_msg not in text:
                    break
            else:
                self.fail("连续{}次获取数据失败".format(retry))

        group_dict = parse_detail(response.text)
        pprint(group_dict)


if __name__ == '__main__':
    unittest.main()
