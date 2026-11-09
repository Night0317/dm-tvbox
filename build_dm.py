# -*- coding: utf-8 -*-
"""从解密后的肥猫系配置中抽取动漫站点，生成 FongMi/TVBox 可直接导入的动漫专仓。"""
import json, os, sys, io, collections

SRC = os.path.join(os.environ.get("TEMP", "/tmp"), "fm_dec")
OUT = os.path.dirname(os.path.abspath(__file__))

HEAD_KEYS = ["name", "spider", "wallpaper", "logo", "danmaku", "doh", "headers",
             "hosts", "parses", "flags", "ijk", "ads", "rules", "proxy"]

# key 白名单：只留动漫/番剧相关
ANIME_KEYS = {
    "cfg1": ["csp_Bili", "csp_Dm84", "方舟", "番薯"],
    "cfg2": ["csp_Bili", "csp_Dm84", "方舟", "番薯"],
    "cfg3": ["Dm84", "Bili"],
    "cfg4": ["bili", "dadun", "XingHui", "FanShu", "XgAnime", "Manbo", "Gugu", "BiliHeji"],
    "cfg5": ["哔哩合集", "哔哩视频", "番社动漫", "赏月", "稀饭", "巴士动漫", "吉里动漫", "花子动漫"],
}

LABEL = {
    "cfg1": ("dm_feimao", "肥猫动漫仓"),
    "cfg2": ("dm_feimao2", "肥猫动漫仓2"),
    "cfg3": ("dm_fantaiying", "饭太硬动漫仓"),
    "cfg4": ("dm_moyu", "摸鱼动漫仓"),
    "cfg5": ("dm_xiaosa", "潇洒动漫仓"),
}


def load(cfg):
    p = os.path.join(SRC, cfg + ".json")
    with io.open(p, encoding="utf-8-sig") as f:
        j = json.load(f)
    return j.get("config", j)


def build(cfg):
    j = load(cfg)
    want = ANIME_KEYS[cfg]
    picked, seen = [], set()
    for s in j.get("sites", []):
        k = str(s.get("key", ""))
        if k in want and k not in seen:
            seen.add(k)
            picked.append(s)
    out = collections.OrderedDict()
    out["name"] = LABEL[cfg][1]
    for k in HEAD_KEYS:
        if k == "name":
            continue
        if k in j and j[k] not in (None, "", [], {}):
            out[k] = j[k]
    out["sites"] = picked
    out["lives"] = []
    return out, [s.get("name") for s in picked]


def main():
    report = []
    for cfg in ["cfg5", "cfg4", "cfg1", "cfg3"]:
        data, names = build(cfg)
        fn = LABEL[cfg][0] + ".json"
        with io.open(os.path.join(OUT, fn), "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        report.append((fn, len(names), names))

    # 多仓入口（地址需替换成自己的托管地址）
    entry = collections.OrderedDict()
    entry["name"] = "动漫聚合总仓"
    entry["urls"] = [
        {"url": "https://raw.githubusercontent.com/USER/REPO/main/dm_xiaosa.json", "name": "动漫仓A·潇洒内核"},
        {"url": "https://raw.githubusercontent.com/USER/REPO/main/dm_moyu.json", "name": "动漫仓B·摸鱼内核"},
        {"url": "https://raw.githubusercontent.com/USER/REPO/main/dm_feimao.json", "name": "动漫仓C·肥猫内核"},
        {"url": "https://raw.githubusercontent.com/USER/REPO/main/dm_fantaiying.json", "name": "动漫仓D·饭太硬内核"},
    ]
    with io.open(os.path.join(OUT, "dm_entry.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(entry, f, ensure_ascii=False, indent=2)
        f.write("\n")

    for fn, n, names in report:
        line = "%-22s %2d sites  %s" % (fn, n, " / ".join(names))
        sys.stdout.write(line.encode("utf-8", "replace").decode("utf-8", "replace") + "\n")


if __name__ == "__main__":
    main()
