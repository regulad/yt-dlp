from typing import Any, Literal, cast
from time import sleep
from urllib.parse import urlencode
import warnings

from .common import InfoExtractor
from ..networking.common import Request, Response


_MODEL_TYPE = dict[str, Any]
_POST_TYPE = dict[str, Any]
_INFO_DICT_TYPE = dict[Any, Any]


class OnlyFansBaseIE(InfoExtractor):
    _PAGE_DELAY_TIME = 3

    __RAPID_API_HOST = 'onlyfans-signer.p.rapidapi.com'
    __RAPID_API_URL = 'https://onlyfans-signer.p.rapidapi.com/sign'
    __USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'

    def __get_signing_headers(self, video_id: Any, /, path: str, query_params: dict[str, str] | None = None) -> dict[str, str]:
        api_key = self._configuration_arg('rapidapi_key', ie_key='onlyfans')
        if not api_key:
            raise RuntimeError('A Rapid key is needed to download from OnlyFans!')
        headers = {
            'x-rapidapi-key': api_key[-1],
            'x-rapidapi-host': self.__RAPID_API_HOST,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        payload_raw = {
            'url': f'{path}?{urlencode(query_params)}' if query_params is not None else path,
            'useragent': self.__USER_AGENT,
        }
        req = Request(
            self.__RAPID_API_URL,
            urlencode(payload_raw).encode('utf-8'),
            headers,
            None,
            None,
            'POST'
        )
        res: Response = self._downloader.urlopen(req)
        json_parsed: dict = self._parse_json(res.read(), video_id, fatal=True)
        return {item[0]: str(item[1]) for item in json_parsed.items()}

    def _init_per_request(self, video_id: Any, /):
        login_response = self._call_api_get(video_id, '/api2/v2/users/me')
        if not login_response['isAuth']:
            self.raise_login_required()

    def _call_api_get(self, video_id: Any, /, path: str, query_params: dict[str, str] | None = None, headers: dict[str, str] | None = None) -> dict[str, Any]:
        # _download_json will automatically deal with headers
        base_headers = self.__get_signing_headers(video_id, path, query_params).copy()
        if headers is not None:
            base_headers.update(headers)
        return self._download_json(
            f'https://onlyfans.com{path}',
            video_id,
            query=query_params,
            expected_status=200,
            fatal=True,
            headers=base_headers,
            impersonate="chrome-110"
        )


# post type
# returned from /api2/v2/posts/<post_id> in addition to the list
# (picture)
# {
#     "author": {
#         "id": 263157959,
#         "_view": "a"
#     },
#     "responseType": "post",
#     "id": 2555058519,
#     "postedAt": "2026-06-22T05:37:18+00:00",
#     "postedAtPrecise": "1782106638.000000",
#     "text": "<p>peekaboob? did you miss me??<br><br>I've been resting up a lil more &gt;.&lt; had a bad fall recently!! </p>",
#     "isMarkdownDisabled": true,
#     "canReport": true,
#     "canComment": true,
#     "favoritesCount": 34,
#     "mediaCount": 1,
#     "isMediaReady": true,
#     "isOpened": true,
#     "canToggleFavorite": true,
#     "commentsCount": 1,
#     "tipsAmount": "$0",
#     "media": [
#         {
#             "id": 4524917793,
#             "type": "photo",
#             "convertedToVideo": false,
#             "canView": true,
#             "hasError": false,
#             "createdAt": null,
#             "isReady": true,
#             "files": {
#                 "full": {
#                     "url": "https://cdn2.onlyfans.com/files/b/be/be09832d22e7f78476acc807900214d6/2048x1536_1f9f6562ae6c788d72ad2bd067d7c578.jpg?Tag=2&u=575056578&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6XC9cL2NkbjIub25seWZhbnMuY29tXC9maWxlc1wvYlwvYmVcL2JlMDk4MzJkMjJlN2Y3ODQ3NmFjYzgwNzkwMDIxNGQ2XC8yMDQ4eDE1MzZfMWY5ZjY1NjJhZTZjNzg4ZDcyYWQyYmQwNjdkN2M1NzguanBnP1RhZz0yJnU9NTc1MDU2NTc4IiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzgyMjYyODAwfSwiSXBBZGRyZXNzIjp7IkFXUzpTb3VyY2VJcCI6IjE3My43MC4xOTEuMjNcLzMyIn19fV19&Signature=ZQwLMtg5sGEHgltlXX9QqTsIgwnfA~n9mPKW9eSw8G7C7H5HG05iGNgRAzAmcWgP-R5r5Jy6Q9jBTusWVDw0tM~24L7oK-nhJfaS027IEsHbSajJoFiKRKU~fefde401W3axYZE-DcVVAAiBMiNGCOVVgcIDxQjGhMLhVXV2rteTS3A5qZ1RR1K2f50zX~uX7BlGfDy5IxNk5RvaOn2oKrFBHDr1VICkPXIGMxrUUl3surj1VXd7UW3iA5-QBhgSrf9hI2YLqBaEuGFjESx1Tde65ub7I2rhbguePsUwedJaF~KU6XHBEOxEyK4PsSM1ZPMny6nCjms32tnqNGYgbg__&Key-Pair-Id=APKAUSX4CWPPATFK2DGD",
#                     "width": 2048,
#                     "height": 1536,
#                     "size": 0,
#                     "sources": []
#                 },
#                 "thumb": {
#                     "url": "https://cdn2.onlyfans.com/files/3/3c/3c95bab55eaff2d369a54017e5e41975/300x300_1f9f6562ae6c788d72ad2bd067d7c578.jpg?Tag=2&u=575056578&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6XC9cL2NkbjIub25seWZhbnMuY29tXC9maWxlc1wvM1wvM2NcLzNjOTViYWI1NWVhZmYyZDM2OWE1NDAxN2U1ZTQxOTc1XC8zMDB4MzAwXzFmOWY2NTYyYWU2Yzc4OGQ3MmFkMmJkMDY3ZDdjNTc4LmpwZz9UYWc9MiZ1PTU3NTA1NjU3OCIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc4MjI2MjgwMH0sIklwQWRkcmVzcyI6eyJBV1M6U291cmNlSXAiOiIxNzMuNzAuMTkxLjIzXC8zMiJ9fX1dfQ__&Signature=Y9Iosz9ZaIzK1Q9Mrq75grdwvB4CNtdaP5xwgQ8KzWBUJ6d6ZQSHLN3oUdeXfeye~iWikmtc8naMdoQdZ~iqWRmXgiBplCnKiDn2ANa0j3LRcy9DhKYMCewXngiUlB1Ldlr6q09d4Q5ofWjv1hg2ahVPfwPX-7C04Xepg4lCiRddVkZ-dToRC90bOxRJpUeXp4B7A9cdSUNpeZvtLyvovHpXvR6d2qv54UAM-2nr7lDV6tKUmigBhnS0VtWbbyZkXjD1dLtqzDU-jRJ3mdkMg2gQWVT21cvouacdk6PPAkEQD~EUYhJFLt5kjsooLbCiS~AHgtmTrUCeThl~W~mP5w__&Key-Pair-Id=APKAUSX4CWPPATFK2DGD",
#                     "width": 300,
#                     "height": 300,
#                     "size": 0
#                 },
#                 "preview": {
#                     "url": "https://cdn2.onlyfans.com/files/5/56/563233e599d5742d0ac80a497beff8b5/960x720_1f9f6562ae6c788d72ad2bd067d7c578.jpg?Tag=2&u=575056578&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6XC9cL2NkbjIub25seWZhbnMuY29tXC9maWxlc1wvNVwvNTZcLzU2MzIzM2U1OTlkNTc0MmQwYWM4MGE0OTdiZWZmOGI1XC85NjB4NzIwXzFmOWY2NTYyYWU2Yzc4OGQ3MmFkMmJkMDY3ZDdjNTc4LmpwZz9UYWc9MiZ1PTU3NTA1NjU3OCIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc4MjI2MjgwMH0sIklwQWRkcmVzcyI6eyJBV1M6U291cmNlSXAiOiIxNzMuNzAuMTkxLjIzXC8zMiJ9fX1dfQ__&Signature=Sqt8HM1HHmhLXhtLOfxFegG2awjpowJR0XXXp1XzXDqq30KD1CsfJMVQASswSNcfkAETIzq2JpXYLwM0R26jPV8hAZTk5VgkS5dKbIIa9lgwRy-sppk0gjcNfvBiz73Kxz~mvbYj23-F5P33W5vuDpZ5r8GqOXrosAl8sxGtqhTxVi9W-BX8MU8z0eLRVMz8Om8EYioX5BPD0f5ogbBBiLv1uQkMZHB6Xu-itX6nTtndsawBtz4SudiY0Rw6dcM~4InCb1KHGDD~A6wfFpCK~ejKbgMpBgvZ~iuBPxit3hjWWtase8vPN2V5Eis~p-1cURv3HYWyBVjWa8k75zPnQA__&Key-Pair-Id=APKAUSX4CWPPATFK2DGD",
#                     "width": 960,
#                     "height": 720,
#                     "size": 0
#                 },
#                 "squarePreview": {
#                     "url": "https://cdn2.onlyfans.com/files/7/7a/7afff110dfc532930df075d4ae304ecb/960x960_1f9f6562ae6c788d72ad2bd067d7c578.jpg?Tag=2&u=575056578&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6XC9cL2NkbjIub25seWZhbnMuY29tXC9maWxlc1wvN1wvN2FcLzdhZmZmMTEwZGZjNTMyOTMwZGYwNzVkNGFlMzA0ZWNiXC85NjB4OTYwXzFmOWY2NTYyYWU2Yzc4OGQ3MmFkMmJkMDY3ZDdjNTc4LmpwZz9UYWc9MiZ1PTU3NTA1NjU3OCIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc4MjI2MjgwMH0sIklwQWRkcmVzcyI6eyJBV1M6U291cmNlSXAiOiIxNzMuNzAuMTkxLjIzXC8zMiJ9fX1dfQ__&Signature=c151GxNL2dOJVROJRphqsrNqVJnG3c~ogCbMNWqNnyjwttHdbqs6FTi254pdAzD3Gl2q6xlmMMm~Hi0AS6naCt-zo2gE04lgYhMF8u-dnL9r1FGvH6LDaj2VJM0R6VKj7PpnofmzP43kBhLiB9SzAsx7-HRK8RxLKasaaOEutC57xFoXpyOnT2EJodVg5wsLFmoO4~Tl6~xKc9xvXiLBCfPjvk90~vrGSB06-8WlR6tCibdW6sP3fAgVLwvCTTmPwu6YlDxGfUpkkTh~9qkB55TDBB9kpe-G80JgOAR3c3lGKAZhj~hvrZzzVO11SrWDNVJKJICL5m4QCjIZ5h7AHg__&Key-Pair-Id=APKAUSX4CWPPATFK2DGD",
#                     "width": 960,
#                     "height": 960,
#                     "size": 0
#                 }
#             },
#             "duration": 0,
#             "hasCustomPreview": false,
#             "videoSources": {
#                 "240": null,
#                 "720": null
#             }
#         }
#      ],
#      "canViewMedia": true
# }
# (video)
# {
#     "author": {
#         "id": 263157959,
#         "_view": "a"
#     },
#     "responseType": "post",
#     "id": 2465835143,
#     "postedAt": "2026-05-18T08:24:33+00:00",
#     "postedAtPrecise": "1779092673.000000",
#     "text": "<p><span class=\"m-editor-fc__blue-1\"><em><strong>NEW PPV DROP!!! (DM me PRETTYBLUEMIA for it &lt;3)</strong></em></span><br>♡ blue lingerie<br>♡ solo masturbation<br>♡ b/g from a few angles<br>♡ special bonus cumshot at the end :3<br><br>yall I could hear my neighbours next door and was really hoping they don't hear my moans &gt;.&lt; </p>",
#     "isMarkdownDisabled": true,
#     "canReport": true,
#     "canComment": true,
#     "isPinned": true,
#     "favoritesCount": 99,
#     "mediaCount": 1,
#     "isMediaReady": true,
#     "isOpened": true,
#     "canToggleFavorite": true,
#     "commentsCount": 1,
#     "tipsAmount": "$0",
#     "media": [
#         {
#             "id": 4451687810,
#             "type": "video",
#             "convertedToVideo": false,
#             "canView": true,
#             "hasError": false,
#             "createdAt": null,
#             "isReady": true,
#             "files": {
#                 "full": {
#                     "url": null,
#                     "width": 1280,
#                     "height": 720,
#                     "size": 0,
#                     "sources": []
#                 },
#                 "thumb": {
#                     "url": "https://cdn2.onlyfans.com/files/e/ee/ee2a4587df082a99a2dce825cc28822c/300x300_45055e8d39ff4c653b56c52505fdfc58_frame_0.jpg?Tag=2&u=575056578&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6XC9cL2NkbjIub25seWZhbnMuY29tXC9maWxlc1wvZVwvZWVcL2VlMmE0NTg3ZGYwODJhOTlhMmRjZTgyNWNjMjg4MjJjXC8zMDB4MzAwXzQ1MDU1ZThkMzlmZjRjNjUzYjU2YzUyNTA1ZmRmYzU4X2ZyYW1lXzAuanBnP1RhZz0yJnU9NTc1MDU2NTc4IiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzgyMjY2NDAwfSwiSXBBZGRyZXNzIjp7IkFXUzpTb3VyY2VJcCI6IjE3My43MC4xOTEuMjNcLzMyIn19fV19&Signature=KajzTI1-l4EUVtEC6JLNRxHjo9jbV9sV5wP7AnvUyxt2KNadodIh15Jbz0-APTjX8sYHz6oIouwbYLXNfHimWeUX9QrpI68kQ~JdF-5D3U5gJa1KWz2ARiM0OexjiDKgxZjYToajWXgYx1fZcPPXtFxB99OnJByAvAwPpnzMKmy2IFneWMZRSbzls5diD-3vczfLRhC6Log4bC3q3fPAFrzV9DBHVbzgrOV94kXOYwxqcjkHemK204UE4gSYCdfHlzKP0hnWgxD~OusNAQcie-zSKDRT5tdKNaSCKjaRGzjL6PkTyhdvRH9KeO36tgRSc48a3csG5tnjS925IEahlw__&Key-Pair-Id=APKAUSX4CWPPATFK2DGD",
#                     "width": 300,
#                     "height": 300,
#                     "size": 0
#                 },
#                 "preview": {
#                     "url": "https://cdn2.onlyfans.com/files/7/7c/7cfce668f3a15b6f5825eeaee28c3463/960x540_45055e8d39ff4c653b56c52505fdfc58_frame_0.jpg?Tag=2&u=575056578&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6XC9cL2NkbjIub25seWZhbnMuY29tXC9maWxlc1wvN1wvN2NcLzdjZmNlNjY4ZjNhMTViNmY1ODI1ZWVhZWUyOGMzNDYzXC85NjB4NTQwXzQ1MDU1ZThkMzlmZjRjNjUzYjU2YzUyNTA1ZmRmYzU4X2ZyYW1lXzAuanBnP1RhZz0yJnU9NTc1MDU2NTc4IiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzgyMjY2NDAwfSwiSXBBZGRyZXNzIjp7IkFXUzpTb3VyY2VJcCI6IjE3My43MC4xOTEuMjNcLzMyIn19fV19&Signature=Zbfj2UrCLMP~1yLRkIhzO-9FET~b6fAxST0ZsYGt5n-6DY-qBEKOvX5yIUSXocW7gTpzZ2Lkyp2KKOQwLVCMDyW8YHea0UtdF~NvkvO0IBRqAjYDEUayEcXCQATUWHVTpqvjvuZ7NIjd2ZZsvs-JIauFXxcD~YNXhXe1Zoa3mCCTsbEDZ6SAMVPR9H1WL1OVpVCRglFSg1lYo5-AgVVg-xM9uIw-pk-5O3~rCbSR~7nBBMKifIAxLCBTRvvYBRPvn3yQ-KhHzv2aKy6AJ0N~1cg4odVVtrp~i0Oth0NIJNXwTfhL1EV6JWXIufsMaAvvNOeruU29s2ODeFdRvJG6qg__&Key-Pair-Id=APKAUSX4CWPPATFK2DGD",
#                     "width": 960,
#                     "height": 540,
#                     "size": 0
#                 },
#                 "squarePreview": {
#                     "url": "https://cdn2.onlyfans.com/files/c/c4/c4af74b964e2b48a35a71d7eae330ede/960x960_59fe113d4fd1ad4bbc0919005b19eb6d_frame_0.jpg?Tag=2&u=575056578&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6XC9cL2NkbjIub25seWZhbnMuY29tXC9maWxlc1wvY1wvYzRcL2M0YWY3NGI5NjRlMmI0OGEzNWE3MWQ3ZWFlMzMwZWRlXC85NjB4OTYwXzU5ZmUxMTNkNGZkMWFkNGJiYzA5MTkwMDViMTllYjZkX2ZyYW1lXzAuanBnP1RhZz0yJnU9NTc1MDU2NTc4IiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzgyMjY2NDAwfSwiSXBBZGRyZXNzIjp7IkFXUzpTb3VyY2VJcCI6IjE3My43MC4xOTEuMjNcLzMyIn19fV19&Signature=FndAoonpsy~azCCIeMULOnStoZ3Yy2LIv2hYNZguycgrx6jrlU~y4hKLso2uMqD0pE-n0YQ9a0oY8sBNgGhgaqSQXHvTdbGfUz9TvYwfd-bg12T~c95yrXZpJu1Zo5RmPITyuIKhBStK3YV8wVIyWlc0fM~dHULk7wB64vYf24yDJZLwJ70g5AN1Wns8fjGYEAaY9lgX3Lm~BW7SfSYF~Y5NfQE~31UOHvpO9aZNaRWHoZInrTp2L1Y93Ksdb4ZDmZpXu5vGU-Yhbz6q8GsBhxg54MAgnBGQtn2tWrycwQsWOri6YITDpm3KFa~SFlBBvMwbPYvmUnp4RUT4of6Pgg__&Key-Pair-Id=APKAUSX4CWPPATFK2DGD",
#                     "width": 960,
#                     "height": 960,
#                     "size": 0
#                 },
#                 "drm": {
#                     "manifest": {
#                         "hls": "https://cdn3.onlyfans.com/hls/files/b/b0/b000210d12b89739e2aa54d6ce9b9ef7/0id337ikahpl913u6y4x5.m3u8",
#                         "dash": "https://cdn3.onlyfans.com/dash/files/b/b0/b000210d12b89739e2aa54d6ce9b9ef7/0id337ikahpl913u6y4x5.mpd"
#                     },
#                     "signature": {
#                         "hls": {
#                             "CloudFront-Policy": "eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6XC9cL2NkbjMub25seWZhbnMuY29tXC9obHNcL2ZpbGVzXC9iXC9iMFwvYjAwMDIxMGQxMmI4OTczOWUyYWE1NGQ2Y2U5YjllZjdcLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3ODIyNjY0MDB9LCJJcEFkZHJlc3MiOnsiQVdTOlNvdXJjZUlwIjoiMTczLjcwLjE5MS4yM1wvMzIifX19XX0_",
#                             "CloudFront-Signature": "nsSK6IYXEOgUL~TS7bJo1jpbEeSdTHLlbAsMrCXnn-X9gddz9Qxp56hgtyHf-seO5g23viNMv1bT-1EHzIdxhGTCFSwTfTyfvxx4jbdGZeUzb98llujJAhPa7aKbh-LsJCQesa3PiCDntRPSrUU4K89yvfg7taCLffFrijMKHCs-SpPR-NFRUN56geq2wpyDALlMUT~l-ul7id9fZNrYEDAcHwBxPoV79CiacFGPlxWBt~4NLvpYh4nStsxvrFrVl5lUGTsoUEBgtr~hozHOsyD9FrdDBbskELCYtyE8FYEzgJ-JhD0uZ88~Fz4zpjJTgvsXbMvlp5RDLmlBlWqZtg__",
#                             "CloudFront-Key-Pair-Id": "K1JM1KV0NHNR73"
#                         },
#                         "dash": {
#                             "CloudFront-Policy": "eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6XC9cL2NkbjMub25seWZhbnMuY29tXC9kYXNoXC9maWxlc1wvYlwvYjBcL2IwMDAyMTBkMTJiODk3MzllMmFhNTRkNmNlOWI5ZWY3XC8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzgyMjY2NDAwfSwiSXBBZGRyZXNzIjp7IkFXUzpTb3VyY2VJcCI6IjE3My43MC4xOTEuMjNcLzMyIn19fV19",
#                             "CloudFront-Signature": "QRFemAYUDVrapgM-BsKHh92WOlfOh69Ylff4KlafcqDMJSYGgJxk4tn-x5OwmQ5u48cK4SUCEap50YRQp4SmG138tXLCMOaxWjPHLrq32TalNA~Y-Hr1XN23yBcdx6lyfo-L3RkPpsL3x0l3LrCm0r3R~hGB1ho6qY-kjiL0KGyPN4T4U63sOEyGH~Veru7eGPeZZEyeRhr4KX6stKaPWFN3loNReG7A2Tg6fl8ZNpDgey-9AFSoJMwinbGmUpepvfigCI~Z29ZGQijX8plc8TRnLI0feICTOVr2ePZfBxeqGvRzfrS~D2t3ON5-1L-kpiVj46EobVzJS5xL~z3uGw__",
#                             "CloudFront-Key-Pair-Id": "K1JM1KV0NHNR73"
#                         }
#                     }
#                 }
#             },
#             "duration": 32,
#             "hasCustomPreview": false,
#             "videoSources": {
#                 "240": null,
#                 "720": null
#             }
#         }
#     ],
#     "canViewMedia": true
# }

    def _post_response_to_entry(self, /, model_data: _MODEL_TYPE, post_data: _POST_TYPE) -> _INFO_DICT_TYPE:
        entry = {}

        assert post_data['responseType'] == 'post'

        if 'name' in model_data:
            entry['uploader'] = model_data['name']
        if 'username' in model_data:
            username = entry['uploader_id'] = model_data['username']
            entry['uploader_url'] = f'https://onlyfans.com/{username}'
        if 'id' in post_data:
            post_id = entry['id'] = post_data['id']
        if 'text' in post_data:
            entry['description'] = post_data['text']
        if 'postedAtPrecise' in post_data:
            entry['release_timestamp'] = int(float(post_data['postedAtPrecise']))

        if 'username' in model_data and 'id' in post_data:
            entry['webpage_url'] = f'https://onlyfans.com/{post_id}/{username}'

        if 'media' in post_data:
            common_entry = entry.copy()
            entry['_type'] = 'playlist'
            entries = []
            for media_data in post_data['media']:
                media_entry = common_entry.copy()
                media_thumbnails = media_entry['thumbnails'] = []

                media_id = media_entry['id'] = media_data['id']
                media_type = media_data.get('type')
                media_files = media_files.get('files', {})

                # thumbnails
                if 'thumb' in media_files:
                    media_thumbnails.append({
                        'id': 'thumb',
                        'url': media_files['thumb']['url'],
                        'width': media_files['thumb']['width'],
                        'height': media_files['thumb']['height'],
                        'preference': 1,
                    })
                if 'preview' in media_files:
                    media_thumbnails.append({
                        'id': 'preview',
                        'url': media_files['preview']['url'],
                        'width': media_files['preview']['width'],
                        'height': media_files['preview']['height'],
                        'preference': 3,
                    })
                if 'squarePreview' in media_files:
                    media_thumbnails.append({
                        'id': 'squarePreview',
                        'url': media_files['squarePreview']['url'],
                        'width': media_files['squarePreview']['width'],
                        'height': media_files['sqaurePreview']['height'],
                        'preference': 2,
                    })

                # rest of media
                if media_type == 'video':
                    if (full_url := media_files['full']['url']) is None:
                        warnings.warn(f'video {media_id} is DRM protected; DRM protected video downloading not yet implemented')
                    else:
                        warnings.warn(f'video {media_id} is not DRM protected; non-DRM protected video downloading not yet implemented')
                elif media_type == 'photo':
                    if (full_url := media_files['full']['url']) is None:
                        warnings.warn(f'picture {media_id} is DRM protected; DRM protected picture downloading not yet implemented')
                    else:
                        media_data['formats'] = [{
                            'url': full_url,
                        }]
                else:
                    warnings.warn(f'media {media_id} is unknown type {media_type}', UserWarning)

                entries.append(media_entry)
            entry['entries'] = entries

        return entry



class OnlyFansIE(OnlyFansBaseIE):
    """OnlyFans InfoExtractor for a single post"""
    IE_NAME = 'OnlyFans'
    IE_DESC = 'OnlyFans video'
    _VALID_URL = r'https?://(?:www\.)?onlyfans\.com/(?P<id>\d+)/(?P<model>[a-z0-9.-]{6,20})'

    _TESTS = [{
        'url': 'https://onlyfans.com/2465835143/perky.mia'
    }]

    def _real_extract(self, url):
        groups = self._match_valid_url(url)
        model_id_str = groups.group('model')
        post_id = groups.group('id')

        self._init_per_request(post_id)

        model_page_json = self._call_api_get(
            post_id,
            f'/api2/v2/users/{model_id_str}',
        )

        post_page_json = self._call_api_get(
            post_id,
            f'/api2/v2/posts/{post_id}',
            {
                'skip_users': 'all'
            },
            {
                'Referrer': url,
            }
        )

        return self._post_response_to_entry(cast(_POST_TYPE, post_page_json),
            cast(_MODEL_TYPE, model_page_json))


# /api2/v2/users/<user_id>/posts/{posts,medias,photos,videos}
# query params to paginate, always from newest posts to oldest posts
# sample qparams: limit=10&order=publish_date_desc&skip_users=all&format=infinite&label=archived&counters=0
#                 limit=10&order=publish_date_desc&skip_users=all&format=infinite&pinned=0&counters=0&beforePublishTime=1781003044.000000
#     five attributes in return object
#         counters?: counters type, only present on first pull of paginator
#         hasMore: boolean - if pagination can return more
#         headMarker: float of unix timestamp as string, i.e. "1780322643.000000" - postedAtPrecise of most recent post in this pagination
#         list: list of post types
#         tailMarker: float of unix timestamp as string - postedAtPrecise of oldest post in this pagination
# tailMarker is used as beforePublishTime of next paginator call, beforePublishTime is exclusive


class OnlyFansModelIE(OnlyFansBaseIE):
    # a model has two pages: "Posts" and "Media"
    IE_NAME = 'OnlyFans model'
    IE_DESC = 'OnlyFans model'
    _VALID_URL = r'https?://(?:www\.)?onlyfans\.com/(?P<model>[a-z0-9.-]{6,20})(?:/(?P<subpage>media|photos|videos))?'

    _TESTS = [{
        'url': 'https://onlyfans.com/perky.mia'
    }, {
        'url': 'https://onlyfans.com/perky.mia/media'
    }, {
        'url': 'https://onlyfans.com/perky.mia/photos'
    }, {
        'url': 'https://onlyfans.com/perky.mia/videos'
    }]

    def _real_extract(self, url):
        groups = self._match_valid_url(url)

        model_id_str = groups.group('model')
        self._init_per_request(model_id_str)

        model_page_json = self._call_api_get(
            model_id_str,
            f'/api2/v2/users/{model_id_str}',
            {
                'httpreferrer': 'onlyfans.com'
            }
        )

        model_name = model_page_json['name']
        model_id_int = model_page_json['id']

        subpage: Literal[None, 'media', 'photos', 'videos'] = groups.group('subpage')
        if subpage is None:
            post_path = ''
        elif subpage == 'media':
            post_path = '/medias'
        else:
            post_path = f'/{subpage}'

        entries = []
        before_publish_time: str | None = None
        has_more: bool = True
        while has_more:
            this_page_query_params = {
                'order': 'publish_date_desc',
                'skip_users': 'all',
                'format': 'infinite',
                'pinned': '0',
                'counters': '1' if before_publish_time is not None else '0', # not parsed
            }
            if before_publish_time is not None:
                this_page_query_params['beforePublishTime'] = before_publish_time
            page = self._call_api_get(model_id_str,
                f'/api2/v2/users/{model_id_int}/posts{post_path}', this_page_query_params)
            before_publish_time = page['tailMarker']
            has_more = page['hasMore'] = False  # TODO: debug

            for post in page['list']:
                entries.append(self._post_response_to_entry(cast(_MODEL_TYPE, model_page_json),
                    cast(_POST_TYPE, post)))

            sleep(self._PAGE_DELAY_TIME)

        return self.playlist_result(entries, model_id_str, f'{model_name} {subpage}')
