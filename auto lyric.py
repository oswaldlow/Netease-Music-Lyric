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
        print("歌词合并成功，所有歌词已经保持在当前目录下")
        print(f"当前获取的歌名为：{song_title}")
    except:
        print("获取歌词错误，请检查你的网络/歌词id再来重试。也可能是请求过频繁，请稍后再试")
