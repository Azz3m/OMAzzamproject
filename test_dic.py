dic={529: {'author': ' Zeina Rahib', 'url': ' http://www.youtube.com/channel/UCREYrNVFDg_nUpgrakP0FqQ', 'img': ' https://yt3.ggpht.com/a/AATXAJxJhehnlz26CRIeaXcLrO8yABTOGJ5qoNgpbA=s48-c-k-c0xffffffff-no-rj-mo', 'date': ' 2019-05-24T21:34:11Z','single_comment': '❤ 25/5/2019  12:34 am 💗🇸🇾', 'i': 529}, 848: {'author': ' Firas Abrash', 'url': ' http://www.youtube.com/channel/UCvOXBZnLx5DiyfMMs5zapWA', 'img': ' https://yt3.ggpht.com/a/AATXAJxjcTvQKqsVE7uGQvcgOJ5yMBibr1GAn2sQCw=s48-c-k-c0xffffffff-no-rj-mo', 'date': ' 2018-10-07T18:11:10Z', 'single_comment': 'in 2018 😍', 'i': 848}, 868: {'author':' Abo Al-yazone', 'url': ' http://www.youtube.com/channel/UCZLrzcxw-h3zryrlzC0mDTw', 'img': ' https://yt3.ggpht.com/a/AATXAJy3WzDDDV6Zy-Uc3q58LJNaNtaFTPfaRSx7IQ=s48-c-k-c0xffffffff-no-rj-mo', 'date': ' 2018-09-23T09:42:29Z', 'single_comment': 'f 2019 ??? 😍😍😍😍', 'i': 868}}

texts = list()
authors = list()
images = list()
channelsURL = list()
dates = list()

for key,item in dic.items():
    authors.append(item['author'])
    texts.append(item['single_comment'])
    images.append(item['img'])
    channelsURL.append(item['url'])
    dates.append(item['date'])
print(dates)
