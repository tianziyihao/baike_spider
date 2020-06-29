

class UrlManage(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, new_urls):
        if not new_urls:
            return
        for url in new_urls:
            self.add_new_url(url)

    def has_new_url(self):
        if self.new_urls:
            return 1
        return 0

    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url


class HtmlDownLoader(object):

    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"}

    def download(self, new_url):
        if not new_url:
            return None
        import requests
        html_res = requests.get(new_url, headers=self.headers)
        if html_res.status_code != 200:
            return None
        html_res = html_res.content.decode(encoding='utf8')
        return html_res


class HtmlParser(object):
    def parse(self, page_url, html_res):
        if not page_url or not html_res:
            return
        from lxml import etree
        html_dom = etree.HTML(html_res)
        new_urls = self._get_new_urls(html_dom)
        new_data = self._get_new_data(page_url, html_dom)
        return new_urls, new_data

    def _get_new_urls(self, html_dom):
        partial_urls = html_dom.xpath('//a[contains(@href,"item")]/text()')
        base_url = 'https://baike.baidu.com'
        return set([base_url+r'/item/'+partial_url for partial_url in partial_urls])

    def _get_new_data(self, page_url,  html_dom):
        res_data = {}
        res_data['title'] = html_dom.xpath('//div[@class="main-content"]//dd/h1/text()')
        res_data['url'] = page_url
        res_data['jj'] = ''.join(html_dom.xpath('//div[@class="lemma-summary"]/div[@class="para"]//text()'))
        return res_data


class HtmlOutputer(object):

    def __init__(self):
        self.data = []

    def collect_data(self, data):
        if data is None:
            return
        self.data.append(data)

    def output_html(self):
        with open('output.html', 'w', encoding='utf8') as f:
            f.write("<!DOCTYPE html>")
            f.write("<html>")
            f.write('<meta charset="utf-8">')
            f.write("<body>")
            f.write("<table>")
            for d in self.data:
                f.write("<tr>")
                f.write("<td>{}</td>".format(d['url']))
                f.write("<td>{}</td>".format(d.get('title', 'None')))
                f.write("<td>{}</td>".format(d['jj']))
                f.write("</tr>")
            f.write("</table>")
            f.write("</body>")
            f.write("</html>")





class SpiderMain(object):

    def __init__(self):
        self.urls = UrlManage()
        self.downloader = HtmlDownLoader()
        self.parser = HtmlParser()
        self.outputer = HtmlOutputer()

    def craw(self, root_url):
        counter = 1
        self.urls.add_new_url(root_url)

        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print("第{}个url:{}".format(counter, new_url))
                html_res = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_res)

                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)
                if counter == 100:
                    break
                counter += 1
            except:
                print("craw fail")

        self.outputer.output_html()


if __name__ == '__main__':

    root_url = 'https://baike.baidu.com/item/Python/407313'
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
