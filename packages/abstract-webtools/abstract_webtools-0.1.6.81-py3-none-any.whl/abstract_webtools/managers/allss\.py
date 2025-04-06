from abstract_apis import *
from abstract_webtools import *
url = 'https://clownworld.biz/media/download_from_url'
video_url = 'https://www.youtube.com/watch?v=Tn7fks2UDRE'
downloadvideo(video_url,directory=directory,safari_optimize=True)
response= postRequest(url,data={"url":video_url})
input(response)
