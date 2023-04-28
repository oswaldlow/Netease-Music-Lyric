import requests
import json

while True:
    song_id = input("请输入歌曲id：")
    try:
        # 获取歌曲标题
        response = requests.get(f"https://music.163.com/api/song/detail/?id={song_id}&ids=[{song_id}]", timeout=5)
        data = json.loads(response.text)
        song_title = data['songs'][0]['name']
        
        #保存原文歌词
        response = requests.get(f"http://music.163.com/api/song/lyric?id={song_id}&lv=1&kv=1&tv=-1", timeout=5)
        data = json.loads(response.text)
        lyric_str = data['lrc']['lyric']
        lyrics = lyric_str.split('\n')
        with open(f"{song_title} (Original).lrc", "w", encoding="utf-8") as f:
            for lyric in lyrics:
                if lyric.strip():
                    timestamp = lyric[1:lyric.index(']')]
                    f.write(f"[{timestamp}] {lyric.split(']')[-1]}\n")
        print("原文歌词保存成功")
        #获取歌词
        if 'tlyric' in data:
            tlyric_str = data['tlyric']['lyric']
            tlyrics = tlyric_str.split('\n')
            with open(f"{song_title} (Translate).lrc", "w", encoding="utf-8") as f:
                for lyric in tlyrics:
                    if lyric.strip():
                        timestamp = lyric[1:lyric.index(']')]
                        f.write(f"[{timestamp}] {lyric.split(']')[-1]}\n")
            print("翻译歌词保存成功")
        #把两个歌词合并在一起
        with open(f"{song_title} (Original).lrc", "r", encoding="utf-8") as f1, \
             open(f"{song_title} (Translate).lrc", "r", encoding="utf-8") as f2, \
             open(f"{song_title} (Merged).lrc", "w", encoding="utf-8") as f3:
            orig_lyrics = f1.readlines()
            trans_lyrics = f2.readlines()
            merged_lyrics = []
            for i in range(len(orig_lyrics)):
                if not orig_lyrics[i].strip():
                    continue
                orig_timestamp = orig_lyrics[i][1:orig_lyrics[i].index(']')]
                trans_timestamp, trans_lyric = None, ""
                for j in range(len(trans_lyrics)):
                    if not trans_lyrics[j].strip():
                        continue
                    curr_trans_timestamp = trans_lyrics[j][1:trans_lyrics[j].index(']')]
                    if curr_trans_timestamp == orig_timestamp:
                        trans_timestamp = curr_trans_timestamp
                        trans_lyric = trans_lyrics[j].split(']')[-1].strip()
                        break
                if trans_lyric:
                    merged_lyrics.append(f"[{orig_timestamp}] {orig_lyrics[i].split(']')[-1].strip()} 【{trans_lyric}】\n")
                else:
                    merged_lyrics.append(f"[{orig_timestamp}] {orig_lyrics[i].split(']')[-1].strip()}\n")
            for line in merged_lyrics:
                f3.write(line)
        print("歌词合并成功")
        #beta版本，尝试获取歌曲地址
        headers = {
            'Referer': 'https://music.163.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        url = f'http://music.163.com/api/song/enhance/player/url?ids=[{song_id}]&br=320000'
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)

        if data['code'] == 200:
            song_url = data['data'][0]['url']
            if song_url is not None:
                song_title = "test"  # 歌曲名称，自行修改
                print('歌曲地址:', song_url)
                # 下载歌曲
                try:
                    response = requests.get(song_url)
                    with open(f"{song_title}.mp3", "wb") as f:
                        f.write(response.content)
                        print(f"歌曲 {song_title}.mp3 已下载成功")
                except:
                    print("歌曲下载失败")
            else:
                print('歌词提取成功，该歌曲有版权限制或者当前的网络环境为国外，无法下载')
    except:
        print("保存歌词错误，请检查你的网络/歌词id再来重试。")