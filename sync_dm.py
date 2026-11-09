# -*- coding: utf-8 -*-
"""
一键同步：抓 肥猫接口 站首页的真实配置地址 -> 调它的 /api/parse 解密 -> 重新生成动漫专仓。
用法：python sync_dm.py
"""
import io, json, os, re, sys, ssl, collections
import urllib.request, urllib.parse

SITE = "xn--z7x900a.net"          # 肥猫.net
HOME = "http://%s/" % SITE
API = "http://%s/api/parse" % SITE
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

OUT = os.path.dirname(os.path.abspath(__file__))
GH_USER = os.environ.get("GH_USER", "Night0317")
GH_REPO = os.environ.get("GH_REPO", "dm-tvbox")
GH_BRANCH = os.environ.get("GH_BRANCH", "main")
CACHE = os.path.join(OUT, "_decrypted")
HEAD_KEYS = ["spider", "wallpaper", "logo", "danmaku", "doh", "headers", "hosts",
             "parses", "flags", "ijk", "ads", "rules", "proxy"]
ANIME_PAT = re.compile(r"(动漫|番剧|哔哩|笔触|笔璃|番社|赏月|稀饭|巴士|吉里|花子|打盹|星绘|番薯|西瓜|曼波|咕咕|方舟)")
SKIP_PAT = re.compile(r"(音乐|听书|相声|小品|戏曲|演唱会|歌曲|小说|有声|短剧|体育|直播|课堂|教育|儿童|启蒙|网盘|磁力|壁纸|APP)")

ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE


def get(url, data=None, headers=None):
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=40, context=ctx) as r:
        return r.read()


def home_entries():
    """抓首页所有 data-url（真实配置地址）"""
    html = get(HOME).decode("utf-8", "replace")
    seen, out = set(), []
    for m in re.finditer(r'data-mode="(copy|link)"\s+data-url="([^"]+)"\s+data-text="([^"]+)"', html):
        mode, url, text = m.group(1), m.group(2), m.group(3)
        if mode != "copy":
            continue
        name = text.split(" ")[0]
        if url in seen:
            continue
        seen.add(url)
        out.append((name, url))
    return out


def decrypt(url):
    """服务端解密，返回配置 dict"""
    body = json.dumps({"url": url}, ensure_ascii=False).encode("utf-8")
    raw = get(API, data=body, headers={"Content-Type": "application/json", "X-Requested-With": "fetch"})
    j = json.loads(raw.decode("utf-8", "replace"))
    return j.get("config", j)


def to_ascii_url(u):
    """中文域名转 punycode，供 urllib 使用"""
    p = urllib.parse.urlsplit(u)
    host = p.netloc
    try:
        host.encode("ascii")
    except UnicodeEncodeError:
        host = host.encode("idna").decode("ascii")
    return urllib.parse.urlunsplit((p.scheme, host, p.path, p.query, p.fragment))


def main():
    os.makedirs(CACHE, exist_ok=True)
    ents = home_entries()
    sys.stdout.write("首页入口 %d 个\n" % len(ents))

    built = []
    for idx, (name, url) in enumerate(ents, 1):
        try:
            cfg = decrypt(to_ascii_url(url))
        except Exception as e:
            sys.stdout.write("  [skip] %-14s %s\n" % (name, e))
            continue
        sites = cfg.get("sites") or []
        anime = [s for s in sites if ANIME_PAT.search(str(s.get("name", "")) + str(s.get("api", "")))
                 and not SKIP_PAT.search(str(s.get("name", "")))]
        if not anime:
            sys.stdout.write("  [skip] %-14s 无动漫站 (%d 站)\n" % (name, len(sites)))
            continue

        tag = "dm_%s" % ("src%d" % idx)
        with io.open(os.path.join(CACHE, tag + "_raw.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)

        out = collections.OrderedDict()
        out["name"] = "%s·动漫仓" % name
        for k in HEAD_KEYS:
            if k in cfg and cfg[k] not in (None, "", [], {}):
                out[k] = cfg[k]
        out["sites"] = anime
        out["lives"] = []
        with io.open(os.path.join(OUT, tag + ".json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
            f.write("\n")
        built.append((tag, name, len(anime), [s.get("name") for s in anime]))
        sys.stdout.write("  [ok]   %-14s %2d 动漫站 -> %s.json\n" % (name, len(anime), tag))

    entry = collections.OrderedDict()
    entry["name"] = "动漫聚合总仓"
    entry["urls"] = [{"url": "https://raw.githubusercontent.com/%s/%s/%s/%s.json" % (GH_USER, GH_REPO, GH_BRANCH, t),
                      "name": "%s·动漫" % n} for t, n, _, _ in built]
    with io.open(os.path.join(OUT, "dm_entry.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(entry, f, ensure_ascii=False, indent=2)
        f.write("\n")
    sys.stdout.write("\n共生成 %d 个动漫仓，入口 dm_entry.json\nraw 前缀: https://raw.githubusercontent.com/%s/%s/%s/\n" % (len(built), GH_USER, GH_REPO, GH_BRANCH))


if __name__ == "__main__":
    main()
