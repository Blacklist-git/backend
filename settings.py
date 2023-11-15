# settings.py
ALLOWED_HOSTS = [ '*' ] # 전체 설정
ALLOWED_HOSTS = [ '34.197.212.64' ] # 예) 54.180.49.81

CORS_ALLOW_ALL_ORIGINS = True # 전체 설정
CORS_ALLOWED_ORIGINS = [
		'{http://34.197.212.64/', # 예) 'http://15.164.191.46/',
		'http://www.clubblacklist.kro.kr/', # 예) 'https://movietrip.click/',
]