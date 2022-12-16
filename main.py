from gppt import GetPixivToken
from pixivpy3 import AppPixivAPI


g = GetPixivToken()
#pixiv ID =  https://www.pixiv.net/setting_user.php
res = g.login(headless=True, user="pixiv ID", pass_="Password")
print(res)
refreshToken = res['refresh_token']

print(refreshToken)

aapi = AppPixivAPI()
aapi.auth(refresh_token=refreshToken)
#https://www.pixiv.net/en/users/{PixivUserId}/bookmarks/artworks
json_result = aapi.user_bookmarks_illust("PixivUserId")  ##### Remove String use int PixivUserId Number
NextURL = ""
while NextURL != None:

    NextURL = json_result.next_url
    print(NextURL)
    print(json_result)
    size = len(json_result.illusts)
    print(f"Object Size: {size}")

    for index in range(size):
        illust = json_result.illusts[index]
        downloadURL = illust.meta_single_page.original_image_url
        if downloadURL == None:
            subdata = illust.meta_pages
            subSize = len(subdata)
            for subindex in range(subSize):
                downloadURL = subdata[subindex].image_urls.original
                print(f"Mutiple Title: {illust.title}, URL: {downloadURL}")
                aapi.download(downloadURL)
            continue
        print(f"Title: {illust.title}, URL: {downloadURL}")
        aapi.download(downloadURL)

    if NextURL != None:
        next_qs = aapi.parse_qs(json_result.next_url)
        json_result = aapi.user_bookmarks_illust(**next_qs)
    print(f"Download Bookmark Per page Complate")
print("All Download Complate")