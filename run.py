import requests
import re
from collections import defaultdict


URL = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?"

headers = {
    "origin": "https://y.qq.com",
    "referer": "https://y.qq.com/n/yqq/song/004Z8Ihr0JIu5s.html",
    "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}

params = {
    "ct": "24",
    "qqmusic_ver": "1298",
    "remoteplace": "txt.yqq.lyric",
    "searchid": "103347689276433275",
    "aggr": "0",
    "catZhida": "1",
    "lossless": "0",
    "sem": "1",
    "t": "7",
    "p": "1",
    "n": "5",
    "w": "周杰伦",
    "g_tk_new_20200303": "5381",
    "g_tk": "5381",
    "loginUin": "0",
    "hostUin": "0",
    "format": "json",
    "inCharset": "utf8",
    "outCharset": "utf-8",
    "notice": "0",
    "platform": "yqq.json",
    "needNewCode": "0",
}


def main():
    singer = input("请输入歌手名：")
    params["w"] = singer

    album_dic = defaultdict(list)

    def check(songname, albumname):
        if singer not in songname or "-" not in songname:
            return False

        if albumname in album_dic:
            for song in album_dic[albumname]:
                if songname in song[0]:
                    return False

        if singer == "周杰伦":
            if "范特西PLUS" in albumname:
                return True
            if "周大侠" in songname:
                return True

        song_remove = ["Live", "醇享版", "纯音乐", "暂无歌词"]
        album_remove = ["Live", "演唱会", "音乐会"]
        for sn in song_remove:
            if sn in songname:
                return False
        for an in album_remove:
            if an in albumname:
                return False
        return True

    for p in range(1, 100):
        params["p"] = p
        res = requests.get(URL, headers=headers, params=params).json()
        list_lyric = res["data"]["lyric"]["list"]
        if len(list_lyric) == 0:
            counts = 0
            for albumname in album_dic.keys():
                counts += len(album_dic[albumname])
            print("总共下载{}首歌词！".format(counts))
            break
        for lyric in list_lyric:
            content = re.sub(r"\\n ", "\n", lyric["content"]).strip()
            songname = content.split("\n")[0].strip()
            albumname = lyric["albumname"].strip()
            if check(songname, albumname):
                if len(albumname) == 0:
                    albumname = "其它"
                album_dic[albumname].append((songname, content))
                print(albumname + "\n  " + songname)

    album_list = sorted(album_dic.items(), key=lambda d: len(d[1]), reverse=True)

    f_lyric = open("output/{}_歌词.txt".format(singer), "w")
    f_album = open("output/{}_歌名.txt".format(singer), "w")
    for album in album_list:
        f_album.write(album[0] + "\n")
        for song in album[1]:
            f_album.write("  " + song[0] + "\n")
            f_lyric.write(song[1])
            f_lyric.write("\n----------------------------------------------\n")
    f_lyric.close()
    f_album.close()


if __name__ == "__main__":
    main()
