from lxml import etree
import requests, time
from urllib.parse import urljoin


def main():
    url = "https://www.shuzhaige.com/douluodalu/91693.html"
    first_chapter = True

    # 创建Session对象，保持会话状态
    session = requests.Session()

    # 更完整的浏览器头部信息
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://www.shuzhaige.com/douluodalu/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    while True:
        try:
            # 使用Session发送请求
            res = session.get(url, headers=headers, timeout=10)  # 设置10秒超时
            res.encoding = "utf-8"
            res.raise_for_status()  # 检查请求是否成功
        except requests.exceptions.Timeout:
            print(f"请求超时: {url}")
            break
        except requests.exceptions.ConnectionError as e:
            print(f"连接错误: {url} - {e}")
            # 尝试增加延迟后重试一次
            time.sleep(5)
            try:
                res = session.get(url, headers=headers, timeout=15)
                res.encoding = "utf-8"
                res.raise_for_status()
            except requests.exceptions.RequestException as retry_e:
                print(f"重试失败: {url} - {retry_e}")
                break
        except requests.exceptions.HTTPError as e:
            print(f"HTTP错误: {url} - {e}")
            break
        except requests.exceptions.RequestException as e:
            print(f"其他请求错误: {url} - {e}")
            import traceback

            traceback.print_exc()  # 打印详细错误信息
            break

        html = etree.HTML(res.text)

        # 提取章节标题和内容
        try:
            title_xpath = "/html/body/div[1]/div/div[2]/h1/text()"
            content_xpath = '//*[@id="content"]/p[position()>1]/text()'
            title_list = html.xpath(title_xpath)
            text_list = html.xpath(content_xpath)
            if not title_list or not text_list:
                print("无法提取章节内容，可能已到最后一章或页面结构变化")
                break  # 内容提取失败时终止循环
            title = title_list[0]
            text = text_list
        except IndexError:
            print("无法提取章节信息，可能页面结构已变化")
            break  # 提取失败时终止循环

        formatted_title = f"{title}\n\n\n"
        print("title", formatted_title.strip())

        # 写入文件
        try:
            with open("斗罗大陆.txt", "w" if first_chapter else "a") as f:
                f.write(formatted_title)
                f.write("\n".join(text) + "\n\n\n")
        except IOError as e:
            print(f"文件写入失败: {e}")
            break

        # 提取下一页链接
        try:
            next_url_xpath = "/html/body/div/div/div[6]/a[3]/@href"
            next_url_list = html.xpath(next_url_xpath)
            if not next_url_list:
                print("已到最后一章，没有下一页链接")
                break  # 没有下一页时终止循环
            next_url_relative = next_url_list[0]
            # 构建完整的下一页URL
            url = urljoin(url, next_url_relative)
            # 打印下一页链接以验证
            print(f"下一页链接: {url}")
        except IndexError:
            print("无法提取下一页链接，可能已到最后一章")
            break

        # 更新参数
        first_chapter = False
        # 循环调用前增加延迟
        time.sleep(0.2)  # 增加延迟时间到.2秒

    print("爬取完成!")


if __name__ == "__main__":
    main()
