from __future__ import annotations

import asyncio
import dataclasses
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import pyperclip
from beni import bcolor, btask, bhttp
from beni.bfunc import syncCall
from bs4 import BeautifulSoup, Tag

app: Final = btask.app


@app.command()
@syncCall
async def make_markdown():
    '创建 markdown 内容'

    # 整理复制的内容
    ary = pyperclip.paste().strip().split('</body></html>')
    ary = [x.strip() for x in ary if x.strip()]
    for i, data in enumerate(ary):
        if not data.endswith('</body></html>'):
            ary[i] += '</body></html>'
    dataList = [makeData(x) for x in ary]

    # 生成 markdown 内容
    contentAry = [
        '## 基本资料',
        '',
        '| ASIN | 图片 | 颜色 | 价格 | 标题 |',
        '| :--: | ---- | --- | ---- | --- |',
    ]
    contentAry.extend([x.makeLine() for x in dataList])
    contentAry.append('')
    contentAry.append('## 5点描述')
    contentAry.append('')
    contentAry.append('| # | 描述 |')
    contentAry.append('| :--: | -- |')
    bulletList: list[set[str]] = []
    for data in dataList:
        for i, bullet in enumerate(data.bulletList):
            if len(bulletList) <= i:
                bulletList.append(set())
            bulletList[i].add(bullet)
    for i, bulletSet in enumerate(bulletList):
        for bullet in bulletSet:
            contentAry.append(f'| {i + 1} | {bullet} |')

    # 下载产品图片
    await asyncio.gather(*[
        bhttp.download(x.image, f'./images/{Path(x.image).name}') for x in dataList
    ])

    pyperclip.copy('\n'.join(contentAry))
    bcolor.printGreen('已复制到剪贴板')
    bcolor.printGreen('OK')


@dataclass
class Data:
    asin: str = ''
    title: str = ''
    color: str = ''
    price: str = ''
    image: str = ''
    bulletList: list[str] = dataclasses.field(default_factory=list)

    def makeLine(self):
        return f'| [{self.asin}](https://www.amazon.com/dp/{self.asin}) | ![](./images/{Path(self.image).name}) | {self.color} | {self.price} | {self.title} |'


def makeData(content: str):

    soup = BeautifulSoup(content, 'html.parser')
    data = Data()

    # ASIN
    asinMatch: list[str] = re.findall(r'  , asin: "(.*?)"', content)
    assert len(asinMatch) == 1
    data.asin = asinMatch[0]

    # Title
    tag = soup.find('div', {'id': 'titleSection'})
    assert type(tag) is Tag
    data.title = tag.get_text(strip=True)

    # Color
    tag = soup.find('span', {'id': 'inline-twister-expanded-dimension-text-color_name'})
    if type(tag) is Tag:
        data.color = tag.get_text(strip=True)
    else:
        data.color = 'Unknown'

    # Price
    priceList = re.findall(r'"displayPrice":"\$(.*?)"', content)
    assert priceList
    data.price = priceList[0]

    # Image
    imageMatch = re.search(r'"hiRes":"(https://[^"]+)"', content)
    assert imageMatch
    data.image = imageMatch.group(1)

    # Bullets
    tag = soup.find('div', id='feature-bullets')
    assert type(tag) is Tag
    spans = tag.find_all('span', {'class': 'a-list-item'})
    data.bulletList = [span.get_text(strip=True) for span in spans]

    return data
