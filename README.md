# dm-tvbox · 动漫专属订阅源

给 **FongMi（蜂蜜影视）/ 影视仓 / OK影视 / TVBox** 用的动漫番剧订阅源。

参考 `http://肥猫.net/` 的接口站做法重建：抓取 → 解密 → 只保留动漫站点 → 输出明文配置。

---

## 直接可用的配置地址

### 多仓入口（推荐，一次挂上 6 个动漫仓）

```
https://raw.githubusercontent.com/Night0317/dm-tvbox/main/dm_entry.json
```

### 单仓

| 地址 | 站数 | 内容 |
|---|---|---|
| `https://raw.githubusercontent.com/Night0317/dm-tvbox/main/dm_src5.json` | 8 | 番社 / 赏月 / 稀饭 / 巴士 / 吉里 / 花子 / 哔哩合集 / 哔哩视频（**最全，推荐**） |
| `https://raw.githubusercontent.com/Night0317/dm-tvbox/main/dm_src4.json` | 8 | 打盹 / 星绘 / 番薯 / 西瓜 / 曼波 / 咕咕 / 笔触琉璃 / 笔璃合集 |
| `https://raw.githubusercontent.com/Night0317/dm-tvbox/main/dm_src1.json` | 4 | 哔哩合集 / 动漫巴士 / 方舟 / 番薯 |
| `https://raw.githubusercontent.com/Night0317/dm-tvbox/main/dm_src2.json` | 4 | 同上 |
| `https://raw.githubusercontent.com/Night0317/dm-tvbox/main/dm_src6.json` | 4 | 同上（无弹幕版，适配安卓 4） |
| `https://raw.githubusercontent.com/Night0317/dm-tvbox/main/dm_src3.json` | 1 | 巴士动漫 |
| `https://raw.githubusercontent.com/Night0317/dm-tvbox/main/dm_all.json` | 8 | 潇洒内核单文件全量 |

### jsDelivr 加速（国内 raw 被墙时换这个）

```
https://cdn.jsdelivr.net/gh/Night0317/dm-tvbox@main/dm_entry.json
```

---

## 导入步骤

1. 打开 FongMi / 影视仓 → **设置** → **配置地址**
2. 粘贴下面的地址：

```
https://raw.githubusercontent.com/Night0317/dm-tvbox/main/dm_entry.json
```

3. 确定 → 回首页下拉刷新
4. 出现「动漫聚合总仓」多仓界面 → 进仓 → 长按不要的站点取消勾选

---

## 为什么肥猫原地址用不了

肥猫站首页「点击复制」给的地址是加密配置：

```
http://hello.肥猫.net/tv  →  hex 解码后 = "$#tkvenckq8ll0f#$" + AES 密文
https://9877.kstore.space/sun.json → "$#1234567890123#$" + 密文
```

FongMi 原生不认这种格式，丢进去必然「配置解析失败」。本站的配置已经过解密并落成纯 JSON。

---

## 目录结构

```
dm_entry.json   多仓入口
dm_src1~6.json  六个动漫仓（各自独立，自带 spider）
dm_all.json     潇洒内核单文件全量仓
sync_dm.py      一键更新脚本（肥猫更新后重跑即可）
build_dm.py     从已解密配置重建动漫仓
```

---

## 一键更新

```powershell
python sync_dm.py
```

自动完成：抓首页真实地址 → 调 `POST /api/parse` 解密 → 过滤动漫站 → 重建 `dm_src*.json` 和 `dm_entry.json`。

---

## 已核对

- 6 个配置地址 HTTP 200，解密成功，原始站数 41 / 41 / 48 / 107 / 112 / 41
- 3 个 spider jar 可下载，MD5 与配置声明一致，均有效 dex
- jar 内类名命中：`AnimeTsukimi` `AnimeXifan` `AnimeBashi` `AnimeGiri` `AnimeHuazi` `XBPQ` `BiliYS` `DaDun` `XingHui` `FanShu` `XgAnime` `AppGet` `Dm84` `Bili`
- 站点域名存活：`girigirilove.com` / `m3u8.girigirilove.com/api.php/Vod/get_list` / `next.xifanacg.com` / `tsukimi.cc` / `dora.xiaoxinbk.com` / `dm84.net` / `www.cyfz.top` 全部 200

---

## 注意

- spider 走 dex 动态加载，FongMi 官方手机版 / TV 版均支持；精简魔改壳砍掉 jar 加载时会加载不出站点
- 哔哩系站点提示「获取失败」多为 Cookie 过期，FongMi 设置里有「B站 Cookie」入口
- jar 内域名会随站点换域名失效，失效时重跑 `sync_dm.py`

---

## 免责

本项目仅提供订阅源格式整理与转换工具，不含任何视频内容。所有索引均来自公开第三方接口，内容版权归原权利人所有。
