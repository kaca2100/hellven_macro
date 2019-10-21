import requests
from bs4 import BeautifulSoup
from time import sleep

lastId = {'2ddal': 1, 'unkl': 1, 'realdada': 1, 'realcos': 1, 'jyd': 1}

page = 1

comment_list = ['감사합니다.', '감사합니다']


comment_index = 0
comment_len = len(comment_list)
bbs_index = 0

print('DPI 우회 후 이용 해주세요.')
print('hellven.net 갤러리 및 일본 행위예술 게시판 댓글 매크로 이며')
print('10레벨 이하 유저는 캡차 때문에 사용할 수 없습니다. 10레벨 이상부터 사용하세요.')

_id = input('ID를 입력해주세요 : ')
_pw = input('PW를 입력해주세요 : ')

with requests.Session() as s:

	param = {'mb_id' : _id, 'mb_password' : _pw}
	req = s.post('https://hellven.net/bbs/login_check.php', param)

	keys = list(lastId.keys())

	for key in keys:
		req = s.get('https://hellven.net/bbs/board.php?bo_table=' + key + '&page=' + str(page))
		html = req.text
		bs = BeautifulSoup(html, 'html.parser')

		rowTags = bs.findAll('div', attrs={'class':'list-row'})
		url = rowTags[0].find('a').get_attribute_list('href')[0]
		wr_id = url[url.find('wr_id')+6:url.find('&page')]
		lastId[key] = int(wr_id)
		print("set lastId : ", key , " -> ", wr_id)


	while True:

		bbs = keys[bbs_index]
		req = s.get('https://hellven.net/bbs/board.php?bo_table=' + bbs + '&page=' + str(page))
		html = req.text

		bs = BeautifulSoup(html, 'html.parser')

		rowTags = bs.findAll('div', attrs={'class':'list-row'})
		rowTags.reverse()

		for tag in rowTags:
			url = tag.find('a').get_attribute_list('href')[0]
			wr_id = url[url.find('wr_id')+6:url.find('&page')]

			if int(wr_id) > lastId[bbs]:
				fviewcomment = {}
				fviewcomment['w'] = 'c'
				fviewcomment['bo_table'] = bbs
				fviewcomment['wr_id'] = wr_id
				fviewcomment['comment_id'] = ''
				fviewcomment['comment_url'] = './view_comment.page.php?bo_table=' + bbs + '&wr_id=' + wr_id + '&crows=70'
				fviewcomment['crows'] = '70'
				fviewcomment['page'] = ''
				fviewcomment['is_good'] = ''
				fviewcomment['wr_content'] = comment_list[comment_index]

				req = s.post('https://hellven.net/bbs/write_comment_update.page.php', fviewcomment)

				lastId[bbs] = int(wr_id)
				comment_index += 1
				if comment_index > comment_len-1:
					comment_index = 0
				print(bbs, 'lastId :' , lastId[bbs])
				sleep(5)
		sleep(5)
		bbs_index += 1
		if bbs_index > len(keys)-1:
			bbs_index = 0


