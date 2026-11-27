"""멤버별 유튜브·노래 조회수 (루트 `멤버별_조회수.md` 를 만든다).

API 키·쿼터 없이 유튜브 웹(innertube)에서 받는다.
  1. 업로드 재생목록 `UU…` 를 `youtubei/v1/browse` continuation 으로 전부 나열
  2. 영상마다 `youtubei/v1/next` 의 `videoViewCountRenderer`(정확한 조회수)·`dateText`
  3. `youtube.com/shorts/{id}` 가 200 이면 쇼츠(리다이렉트면 일반 영상)
노래 목록은 스텔DB 사이트가 공개하는 `static/site-catalog.json` 의 `SONG_DATA`(리제 키는 `rize`).

  python member_views.py refresh              # 14명 전부 다시 받고 문서·README 갱신 (Actions member-views 가 매주 실행)
  python member_views.py fetch <key>          # 멤버 하나만 다시 받기
  python member_views.py report               # data/ 로 문서·README 다시 쓰기 (받지 않음)
  python member_views.py stats <key>          # 멤버 하나 상세
  python member_views.py summary              # 10명 요약표
결과는 data/<key>_full.json(채널 영상 전부)·data/<key>_songs.json(노래 통계 곡)·data/meta.json(수집일).
"""
import argparse, concurrent.futures as cf, datetime as dt, json, re, statistics as st, unicodedata, urllib.error, urllib.request
from pathlib import Path

DATA = Path(__file__).parent / "data"
ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "멤버별_조회수.md"
CATALOG_URL = "https://steldatabase.onrender.com/static/site-catalog.json"
KST = dt.timezone(dt.timedelta(hours=9))
CTX = {"client": {"clientName": "WEB", "clientVersion": "2.20251020.00.00", "hl": "ko", "gl": "KR"}}



def _meta():
    try:
        return json.loads((DATA / "meta.json").read_text(encoding="utf-8"))
    except FileNotFoundError:  # 2026-10-27 수동 수집분
        return {"collected": "2026-10-27"}


def _cutoff():
    """수집일 전날까지 올라온 영상 (수집 당일 영상은 조회수가 덜 쌓였다)."""
    d = dt.date.fromisoformat(_meta()["collected"]) - dt.timedelta(days=1)
    return d


CUTOFF_D = _cutoff()
CUTOFF = (CUTOFF_D.year, CUTOFF_D.month, CUTOFF_D.day)
_R = CUTOFF_D - dt.timedelta(days=364)
RECENT_FROM = (_R.year, _R.month, _R.day)
# 노래 통계에 없지만 노래인 영상(커버 쇼츠·3D 라이브 커버·노래 모음) — 영상 평균에서 뺀다
NOT_VIDEO = re.compile(r"cover|커버|Playlist|메들리|music video|\bMV\b|歌ってみた|Aiobahn Remix|유니의 SUPERPOWER", re.I)
CHANNELS = {"yuni": "UClbYIn9LDbbFZ9w2shX3K0g", "huya": "UC0YQnenKBCu5sGb7H61n6HA", "hina": "UC1afpiIuBDcjYlmruAa0HiA",
            "mashiro": "UC_eeSpMBz8PG4ssdBPnP07g", "lize": "UC7-m6jQLinZQWIbwm9W-1iw", "tabi": "UCAHVQ44O81aehLWfy9O6Elw",
            "shibuki": "UCYxLMfeX1CbMBll9MsGlzmw", "rin": "UCQmcltnre6aG9SkDRYZqFIg", "nana": "UCcA21_PzN1EhNe7xS4MJGsQ",
            "riko": "UCj0c1jUr91dTetIQP2pFeLA", "toa": "UClcSEuDF_g_6g4snw_nAavw", "ran": "UCQ6LlsI7Bbj2yhSqLMI1gGA",
            "hiyori": "UCHAr9pWGS30akL4MQCQT4uQ", "mary": "UCGSt1yNG5l-jpYRLpJ5oNtA"}
SONG_KEY = {"lize": "rize"}
SONG_KINDS = ("orig", "game", "multi", "ext", "cover")
MEMBERS = [("yuni", "유니"), ("huya", "후야"), ("hina", "히나"), ("mashiro", "마시로"), ("lize", "리제"),
           ("tabi", "타비"), ("shibuki", "시부키"), ("rin", "린"), ("nana", "나나"), ("riko", "리코")]


def _post(ep, body):
    req = urllib.request.Request(f"https://www.youtube.com/youtubei/v1/{ep}?prettyPrint=false",
                                 json.dumps({"context": CTX, **body}).encode(), {"Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=30).read().decode()


def list_uploads(channel_id):
    seen, out, body = set(), [], {"browseId": "VLUU" + channel_id[2:]}

    def walk(o):
        if isinstance(o, dict):
            lv = o.get("lockupViewModel")
            if lv and lv.get("contentId") and lv["contentId"] not in seen:
                seen.add(lv["contentId"])
                title = lv.get("metadata", {}).get("lockupMetadataViewModel", {}).get("title", {}).get("content", "")
                out.append({"id": lv["contentId"], "title": title})
            for x in o.values():
                walk(x)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    while body:
        s = _post("browse", body)
        walk(json.loads(s))
        tok = re.findall(r'"continuationItemViewModel".{0,1500}?"token":"([^"]+)"', s)
        body = {"continuation": tok[0]} if tok else None
    return out


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def video_info(v, shorts=None):
    err = ""
    for _ in range(3):
        try:
            s = _post("next", {"videoId": v["id"]})
            m = re.search(r'"videoViewCountRenderer":\{"viewCount":\{(?:"simpleText":"([^"]+)"|"runs":\[\{"text":"([^"]+)")', s)
            d = re.search(r'"dateText":\{"simpleText":"([^"]+)"', s)
            if not (m and d):
                raise ValueError("조회수·날짜 없음")
            n = int(re.sub(r"\D", "", m.group(1) or m.group(2)))
            if shorts is not None:
                return {**v, "views": n, "date": d.group(1), "shorts": shorts}
            try:
                sh = urllib.request.build_opener(_NoRedirect).open(
                    urllib.request.Request("https://www.youtube.com/shorts/" + v["id"], method="HEAD"), timeout=20).status == 200
            except urllib.error.HTTPError:
                sh = False
            return {**v, "views": n, "date": d.group(1), "shorts": int(sh)}
        except Exception as e:  # 일시 오류는 다시 시도, 세 번 실패하면 err 로 남긴다
            err = str(e)
    return {**v, "views": None, "date": "", "shorts": -1, "err": err}


def song_catalog():
    req = urllib.request.Request(CATALOG_URL, headers={"User-Agent": "stellive-analytics member_views"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read().decode())["SONG_DATA"]


def song_items(catalog, song_key):
    row = catalog.get(song_key) or {}
    return [{"id": x["id"], "title": x.get("t", ""), "kind": k} for k in SONG_KINDS for x in row.get(k) or [] if x.get("id")]


def _old_shorts(key):
    """쇼츠 여부는 바뀌지 않으니 지난번 판별을 다시 쓴다 (HEAD 요청 절약)."""
    out = {}
    for name in ("full", "songs"):
        f = DATA / f"{key}_{name}.json"
        if f.exists():
            out.update({x["id"]: x["shorts"] for x in json.loads(f.read_text(encoding="utf-8")) if x.get("shorts") in (0, 1)})
    return out


def fetch(key, catalog):
    DATA.mkdir(exist_ok=True)
    known = _old_shorts(key)

    def info(v):
        return video_info(v, known.get(v["id"]))

    with cf.ThreadPoolExecutor(8) as ex:
        for name, items in (("full", list_uploads(CHANNELS[key])), ("songs", song_items(catalog, SONG_KEY.get(key, key)))):
            rows = list(ex.map(info, items))
            bad = sum(r["views"] is None for r in rows)
            if items and bad > len(items) * 0.2:
                raise RuntimeError(f"{key} {name}: {bad}/{len(items)} 실패 — 기존 데이터를 그대로 둔다")
            (DATA / f"{key}_{name}.json").write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
            print(key, name, len(rows), "실패", bad)


def _day(d):
    m = re.search(r"(\d{4})\. (\d+)\. (\d+)\.", d)
    return (int(m[1]), int(m[2]), int(m[3])) if m else None


def _ok(x):
    return x.get("views") is not None and _day(x["date"]) and _day(x["date"]) <= CUTOFF


def load(key):
    full = [x for x in json.loads((DATA / f"{key}_full.json").read_text(encoding="utf-8")) if _ok(x)]
    songs = [x for x in json.loads((DATA / f"{key}_songs.json").read_text(encoding="utf-8")) if _ok(x)]
    ids = {x["id"] for x in songs}
    videos = [x for x in full if x["id"] not in ids and not NOT_VIDEO.search(unicodedata.normalize("NFKC", x["title"]))]
    return videos, songs


def man(v):
    return f"{round(v / 1e4):,}만"


def _avg(rows):
    return st.mean(x["views"] for x in rows) if rows else 0


def stats(key):
    videos, songs = load(key)
    for name, rows in (("영상(노래 제외)", videos), ("일반 영상", [x for x in videos if x["shorts"] != 1]),
                       ("쇼츠", [x for x in videos if x["shorts"] == 1]), ("노래", songs)):
        print(f"\n{name} {len(rows)}개  평균 {man(_avg(rows))}")
        for x in sorted(rows, key=lambda x: -x["views"])[:5]:
            print(f"  {man(x['views']):>7} {x['date'][-13:]} {x.get('kind', '')} {x['title'][:70]}")


def summary():
    print("멤버 | 영상 평균 | 일반 평균 | 쇼츠 평균 | 최근1년 | 쇼츠 최고 | 일반 최고 | 곡 | 노래 평균 | 노래 최고")
    for key, name in MEMBERS:
        v, s = load(key)
        reg, sh = [x for x in v if x["shorts"] != 1], [x for x in v if x["shorts"] == 1]
        top = lambda rows: max(rows, key=lambda x: x["views"])
        rec = [x for x in v if _day(x["date"]) >= RECENT_FROM]
        print(" | ".join([name, man(_avg(v)), man(_avg(reg)), man(_avg(sh)), man(_avg(rec)),
                          f"{man(top(sh)['views'])} {top(sh)['title'][:30]}", f"{man(top(reg)['views'])} {top(reg)['title'][:30]}",
                          str(len(s)), man(_avg(s)), f"{man(top(s)['views'])} {top(s)['title'][:20]}"]))


# 3절 멤버별 특징은 상위 영상 제목을 보고 쓴 해석이라 손으로 둔다 (FEATURES_DATE 자료 기준)
FEATURES_DATE = "2026-10-27"
FEATURES = {
    "리제": "커버 노래가 강함, 1,000만 회 넘는 커버가 여럿",
    "시부키": "귀여움 + 게임 + \"아빠\" 상황극.<br>듀엣곡이 많음",
    "린": "웃긴 밈 쇼츠가 강함.<br>영어 콘텐츠, 노래가 고르게 높음",
    "리코": "상황극·챌린지 쇼츠.<br>노래는 고르지만 뮤지컬 커버는 낮음",
    "유니": "귀여움·놀리는 맛, 초기 쇼츠가 강했음.<br>오리지널 곡이 노래 상위권",
    "나나": "봉누도 상황극, 친근한 이미지.<br>파워풀한 커버, 2인 이상 곡이 많음",
    "히나": "밈 쇼츠 하나가 크게 터짐.<br>일반 영상은 합방이 강하고, 대표곡이 큼",
    "타비": "웃긴 밈·상황극, 영상 수가 가장 많음.<br>한국 곡 커버가 강함",
    "후야": "데뷔가 늦어 같은 기간으로 맞추면 유니와 비슷.<br>쇼츠 비중이 높음",
    "마시로": "전체적으로 낮음.<br>쇼츠를 거의 안 올림",
}


def _title(t, n=26):
    t = re.sub(r"(\s*#\S+)+\s*$", "", unicodedata.normalize("NFKC", t)).replace("|", "/").strip()
    return t if len(t) <= n else t[:n].rstrip() + "…"


def _top(rows):
    return max(rows, key=lambda x: x["views"]) if rows else None


def _cell(x):
    return f"{man(x['views'])}<br>「{_title(x['title'])}」" if x else "—"


def report():
    collected = _meta()["collected"]
    cut = CUTOFF_D.isoformat()
    rows = []
    for key, name in MEMBERS:
        v, s = load(key)
        reg, sh = [x for x in v if x["shorts"] != 1], [x for x in v if x["shorts"] == 1]
        rows.append({"name": name, "v": v, "s": s, "reg": reg, "sh": sh})
    vid = sorted(rows, key=lambda r: -_avg(r["v"]))
    song = sorted(rows, key=lambda r: -_avg(r["s"]))
    out = ["# 멤버별 유튜브·노래 조회수 정리", "",
           f"기준: 각 멤버 유튜브 채널에 **{cut}까지 올라온 영상**, 조회수는 **{collected}** 기준(매주 월요일 자동 갱신).",
           "숫자는 만 단위로 반올림했습니다. 4기 ABYSS·창립자·졸업 멤버는 표에서 뺐습니다.", "",
           "## 바로 보기", "", "| 무엇을 | 어디서 |", "|---|---|",
           "| 영상 조회수 순위 (노래 제외) | [1. 영상](#1-영상-노래-제외) |", "| 노래 조회수 순위 | [2. 노래](#2-노래) |",
           "| 멤버별 특징 | [3. 멤버별 특징](#3-멤버별-특징) |", "| 어떻게 셌나 | [4. 기준](#4-기준) |", "",
           "## 1. 영상 (노래 제외)", "", "평균 조회수 순입니다. 최고 조회수는 쇼츠와 일반 영상을 따로 적었습니다.", "",
           "| 순위 | 멤버 | 평균 | 쇼츠 최고 | 일반 영상 최고 |", "|---|---|---|---|---|"]
    out += [f"| {i} | {r['name']} | {man(_avg(r['v']))} | {_cell(_top(r['sh']))} | {_cell(_top(r['reg']))} |" for i, r in enumerate(vid, 1)]
    out += ["", "## 2. 노래", "", "| 순위 | 멤버 | 곡 수 | 평균 | 최고 |", "|---|---|---|---|---|"]
    out += [f"| {i} | {r['name']} | {len(r['s'])} | {man(_avg(r['s']))} | {_cell(_top(r['s']))} |" for i, r in enumerate(song, 1)]
    ratio_sh = [_avg(r["sh"]) / _avg(r["reg"]) for r in rows if r["sh"] and r["reg"] and _avg(r["reg"])]
    ratio_song = [_avg(r["s"]) / _avg(r["v"]) for r in rows if r["s"] and _avg(r["v"])]
    top_is_short = sum(1 for r in rows if r["v"] and _top(r["v"])["shorts"] == 1)
    out += ["", "## 3. 멤버별 특징", "",
            f"상위 영상 제목을 보고 정리한 해석입니다({FEATURES_DATE} 자료 기준, 손으로 고친다). 조회수로 잴 수 없는 이유는 적지 않았습니다.", "",
            "| 멤버 | 특징 |", "|---|---|"]
    out += [f"| {r['name']} | {FEATURES.get(r['name'], '')} |" for r in vid]
    out += ["", "**공통점** (이번 수집 자료로 계산)", "",
            f"- 멤버 {len(rows)}명 중 {top_is_short}명의 최고 영상이 쇼츠입니다.",
            f"- 쇼츠 평균이 일반 영상 평균의 {min(ratio_sh):.1f}~{max(ratio_sh):.1f}배입니다." if ratio_sh else "- 쇼츠 비교: 측정 불가",
            f"- 노래 평균이 노래가 아닌 영상 평균의 {min(ratio_song):.1f}~{max(ratio_song):.1f}배입니다." if ratio_song else "- 노래 비교: 측정 불가",
            "", "## 4. 기준", "", "| 항목 | 기준 |", "|---|---|",
            f"| 영상 범위 | 각 멤버 채널의 업로드 전체(쇼츠·다시보기 포함), {cut}까지 |",
            f"| 조회수 | 유튜브 영상 페이지에 표시되는 정확한 조회수, {collected} 수집 |",
            "| 쇼츠 판별 | `youtube.com/shorts/{id}` 주소가 열리면 쇼츠 |",
            "| 노래 | 스텔DB 노래 통계(오리지널·게임 콜라보·2인 이상·외부곡·커버)의 곡. 다른 멤버 채널에 올라간 듀엣곡 포함 |",
            "| 영상에서 뺀 것 | 노래 통계 곡 + 제목에 cover·커버·MV·Playlist·메들리가 든 영상(커버 쇼츠, 3D 라이브 커버, 노래 모음) |",
            "| 갱신 | GitHub Actions `member-views` 가 매주 월요일 다시 받는다(`youtube_analyze_all/member_views/member_views.py refresh`) |",
            "| 한계 | 오래된 영상일수록 조회수가 더 쌓여 있어, 데뷔 시기가 다른 멤버끼리는 평균이 유리·불리할 수 있습니다 |", ""]
    DOC.write_text("\n".join(out), encoding="utf-8")
    readme = ROOT / "README.md"
    r = readme.read_text(encoding="utf-8")
    r2 = re.sub(r"멤버별 유튜브·노래 조회수 정리 \([0-9-]+ 기준\)", f"멤버별 유튜브·노래 조회수 정리 ({collected} 기준)", r)
    r2 = re.sub(r"\[`멤버별_조회수[^`]*\.md`\]\(멤버별_조회수[^)]*\.md\)", "[`멤버별_조회수.md`](멤버별_조회수.md)", r2)
    if r2 != r:
        readme.write_text(r2, encoding="utf-8")
    print("문서 갱신:", DOC.name, collected)


def refresh():
    catalog = song_catalog()
    failed = []
    for key in CHANNELS:
        try:
            fetch(key, catalog)
        except Exception as e:  # 한 멤버가 실패해도 나머지는 받는다, 실패한 멤버는 지난 자료
            failed.append(key)
            print("실패", key, e)
    if len(failed) > len(CHANNELS) // 2:
        raise SystemExit(f"절반 넘게 실패({failed}) — 문서를 바꾸지 않는다")
    (DATA / "meta.json").write_text(json.dumps({"collected": dt.datetime.now(KST).date().isoformat(), "failed": failed},
                                               ensure_ascii=False), encoding="utf-8")
    global CUTOFF_D, CUTOFF, RECENT_FROM
    CUTOFF_D = _cutoff()
    CUTOFF = (CUTOFF_D.year, CUTOFF_D.month, CUTOFF_D.day)
    _r = CUTOFF_D - dt.timedelta(days=364)
    RECENT_FROM = (_r.year, _r.month, _r.day)
    report()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("fetch").add_argument("key", choices=list(CHANNELS))
    sub.add_parser("stats").add_argument("key")
    for c in ("summary", "report", "refresh"):
        sub.add_parser(c)
    a = ap.parse_args()
    if a.cmd == "fetch":
        fetch(a.key, song_catalog())
    elif a.cmd == "stats":
        stats(a.key)
    elif a.cmd == "report":
        report()
    elif a.cmd == "refresh":
        refresh()
    else:
        summary()
