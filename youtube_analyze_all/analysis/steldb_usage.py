"""
스텔 DB 이용 분석 — 누가 얼마나 오고, 다시 오고, 무엇을 보고, 어디서 들어와 어디로 나가나.

자료: collect/data/steldb_usage.json (collect/steldb_usage.py, 스텔 DB Supabase `stel_usage_export()` 집계).
기준: 방문자 = 브라우저 하나(visitor_id, 계정이 아니다). 주 = 한국 시각 월요일 시작. 관리자 조회·점검 자동화는 수집 단계에서 빠진다.
산출: analysis/out/steldb_usage.md
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "collect" / "data" / "steldb_usage.json"
OUT = HERE / "out" / "steldb_usage.md"

PAGE = {"main": "메인", "news": "소식", "schedule": "일정", "feed": "방송", "vod": "VOD", "members": "멤버", "info": "정보",
        "goods": "굿즈", "settings": "설정", "alarms": "알림", "favs": "보관함", "inquiry": "건의사항", "fanzone": "팬 콘텐츠",
        "notice": "공지", "admin": "관리자", "daylook": "지난 날"}
SOURCE = {"direct": "직접 접속(주소·앱·북마크)", "internal": "사이트 안 이동", "search": "검색", "instagram": "인스타그램",
          "dcinside": "디시인사이드", "cafe": "네이버 카페", "arcalive": "아카라이브", "x": "X", "threads": "스레드",
          "youtube": "유튜브", "social": "기타 SNS", "other": "기타", "unknown": "모름"}
OUTCLICK = {"x": "X", "chzzk": "치지직", "cafe": "네이버 카페", "youtube": "유튜브", "fanding": "팬딩", "instagram": "인스타그램",
            "shop": "굿즈 판매처", "stellive": "공식 사이트", "namuwiki": "나무위키", "dcinside": "디시", "soundcloud": "사운드클라우드",
            "arcalive": "아카라이브", "threads": "스레드", "naver": "네이버", "other": "기타"}
NEWS = {"x": "X", "cafe": "카페", "youtube": "유튜브", "chzzk": "치지직", "fanding": "팬딩", "insta": "인스타"}
DOW = "월화수목금토일"


def pct(a, b) -> str:
    return f"{a / b * 100:.1f}%" if b else "—"


def n(v) -> str:
    return f"{int(v):,}" if v is not None else "—"


def tbl(head: list[str], rows: list[list]) -> str:
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def bar(v: float, mx: float, w: int = 20) -> str:
    return "█" * max(1, round(v / mx * w)) if mx and v else ""


def main() -> None:
    d = json.loads(SRC.read_text(encoding="utf-8"))
    gen = d["generated_at"][:16].replace("T", " ") + " UTC"
    weekly = [w for w in d["weekly"] if w["wk"] >= "2026-09-21"]  # 9/21 이전은 운영자 혼자 보던 시험 기간
    cur, last = weekly[-1], weekly[-2]
    L = ["# 스텔 DB 이용 분석", "", f"기준: {gen} · 방문자 = 브라우저 하나(계정 아님) · 주 = 한국 시각 월요일 시작 · 관리자·점검 자동화 제외", ""]

    # 요약
    days = d["visit_days_30d"]
    tot30 = sum(x["visitors"] for x in days)
    rep30 = sum(x["visitors"] for x in days if x["days"] >= 2)
    core30 = sum(x["visitors"] for x in days if x["days"] >= 6)
    full = [w for w in weekly[:-1]]
    peak = max(full, key=lambda w: w["visitors"])
    pages = d["pages_30d"]
    pv30 = sum(p["views"] for p in pages)
    devs = d["devices_30d"]
    dv = sum(x["visitors"] for x in devs)
    mob = next((x["visitors"] for x in devs if x["device"] == "mobile"), 0)
    U, P = d["users"], d["push"]
    L += ["## 한눈에", "",
          f"- 최근 30일 방문자 **{n(tot30)}명**, 그중 이틀 이상 들른 사람 **{n(rep30)}명({pct(rep30, tot30)})**, 엿새 이상 {n(core30)}명({pct(core30, tot30)}).",
          f"- 지난주(완료된 주) 방문자 {n(last['visitors'])}명 · 새 방문자 {n(last['new_visitors'])}명 · 로그인 방문자 {n(last['member_visitors'])}명. 가장 많았던 주는 {peak['wk']} 주({n(peak['visitors'])}명).",
          f"- 이번 주({cur['wk']}~, 진행 중) 지금까지 {n(cur['visitors'])}명 · 새 방문자 {n(cur['new_visitors'])}명 · 로그인 방문자 {n(cur['member_visitors'])}명.",
          f"- 폰이 방문자의 {pct(mob, dv)} — 화면은 폰을 먼저 본다.",
          f"- 회원 {n(U['total'])}명(팬덤을 고른 회원 {n(U['with_fandom'])}명) · 알림 구독 {n(P['subs'])}개(회원 {n(P['member_subs'])}개, 7일 안 접속 {n(P['active_7d'])}개).",
          f"- 최근 30일 탭 조회 {n(pv30)}회 중 메인·소식이 {pct(pages[0]['views'] + pages[1]['views'], pv30)}.", ""]

    # 주별
    L += ["## 주별 방문", "", tbl(["주", "방문자", "새 방문자", "다시 온 사람", "로그인 방문자", "세션", "탭 조회", "탭당 머문 시간(초)"],
          [[w["wk"] + (" (진행 중)" if w is cur else ""), n(w["visitors"]), n(w["new_visitors"]), n(w["visitors"] - w["new_visitors"]),
            n(w["member_visitors"]), n(w["sessions"]), n(w["views"]), w["avg_dwell_s"] or "—"] for w in weekly]), "",
          "- '다시 온 사람' = 그 주 방문자 중 전에 온 적 있는 사람. 새 방문자가 갑자기 는 주는 홍보 글·큰 행사가 있던 주인지 운영 기록과 맞춰 볼 것.",
          "- 탭당 머문 시간은 1초~1시간만 평균했다. 10월 말부터 길어진 것은 알림·즐겨찾기·이어보기처럼 오래 머무는 기능이 늘어서다(같은 사람의 시간 변화가 아니다).", ""]

    # 재방문 코호트
    today = d["generated_at"][:10]
    from datetime import date, timedelta
    def seen(c, dd, k):
        if str(date.fromisoformat(c["fw"]) + timedelta(days=dd + 7)) > today:
            return "측정 중"
        return f"{n(c[k])} ({pct(c[k], c['n'])})"
    coh = [c for c in d["cohorts"] if c["fw"] >= "2026-09-21" and c["n"] >= 20]
    L += ["## 다시 오는 비율 (첫 방문 주 기준)", "",
          tbl(["첫 방문 주", "사람", "다음 주에 다시 옴", "2~4주 뒤에 다시 옴"],
              [[c["fw"], n(c["n"]), seen(c, 7, "w1"), seen(c, 28, "w2_4")] for c in coh]), "",
          "- 기간이 아직 다 지나지 않은 칸은 '측정 중'이다.", ""]

    # 방문 일수 분포
    mxd = max(x["visitors"] for x in days)
    L += ["## 최근 30일에 며칠 들렀나", "", tbl(["들른 날", "사람", ""],
          [[("10일 이상" if x["days"] >= 10 else f"{x['days']}일"), n(x["visitors"]), bar(x["visitors"], mxd)] for x in days]), "",
          f"- 하루만 왔다 간 사람이 {pct(days[0]['visitors'], tot30)}이고, 10일 이상 오는 사람이 {n(days[-1]['visitors'])}명 따로 있다 — 처음 온 사람을 이틀째로 잇는 것이 가장 큰 숙제다.", ""]

    # 탭
    mxp = max(p["views"] for p in pages)
    rep = max((p for p in pages if p["visitors"] >= 50), key=lambda p: p["views"] / p["visitors"])
    dwell = max((p for p in pages if p["visitors"] >= 50 and p["avg_dwell_s"]), key=lambda p: p["avg_dwell_s"])
    L += ["## 어느 탭을 보나 (최근 30일)", "", tbl(["탭", "조회", "본 사람", "평균 머문 시간(초)", ""],
          [[PAGE.get(p["page"], p["page"]), n(p["views"]), n(p["visitors"]), p["avg_dwell_s"] or "—", bar(p["views"], mxp)] for p in pages]), "",
          f"- 한 사람이 가장 여러 번 여는 탭은 {PAGE.get(rep['page'], rep['page'])}(1인당 {rep['views'] / rep['visitors']:.1f}회), 가장 오래 머무는 탭은 {PAGE.get(dwell['page'], dwell['page'])}({dwell['avg_dwell_s']}초).", ""]

    # 유입
    src = d["sources_30d"]
    st = sum(s["sessions"] for s in src)
    ext = [s for s in src if s["source"] not in ("direct", "internal")]
    L += ["## 어디서 들어오나 (최근 30일 세션 첫 화면)", "", tbl(["경로", "세션", "비율"],
          [[SOURCE.get(s["source"], s["source"]), n(s["sessions"]), pct(s["sessions"], st)] for s in src]), "",
          f"- 바깥 경로 중에서는 {', '.join(SOURCE.get(s['source'], s['source']) for s in ext[:4])} 순이다.",
          "- 직접 접속에는 설치 앱·홈 화면 아이콘·알림을 눌러 들어온 것이 섞인다(브라우저가 출처를 주지 않는다)."]
    if d.get("campaigns"):
        L += ["", tbl(["홍보 링크 이름(utm_content)", "채널", "세션"], [[c["campaign"], SOURCE.get(c["source"], c["source"]), n(c["sessions"])] for c in d["campaigns"]])]
    L += [""]

    # 기기·시간
    hrs = d["hours_30d"]
    mxh = max(h["views"] for h in hrs)
    top = sorted(hrs, key=lambda h: -h["views"])[:3]
    L += ["## 언제 보나 (최근 30일, 한국 시각)", "", tbl(["시", "탭 조회", ""], [[f"{h['hr']:02d}시", n(h["views"]), bar(h["views"], mxh)] for h in hrs]), "",
          "- 많이 보는 시각: " + ", ".join(f"{h['hr']:02d}시" for h in top) + ".",
          "", tbl(["요일", "탭 조회"], [[DOW[w["dow"] - 1], n(w["views"])] for w in d["weekday_30d"]]), "",
          tbl(["기기", "방문자", "비율"], [[{"mobile": "폰", "desktop": "PC", "tablet": "태블릿"}.get(x["device"], x["device"]), n(x["visitors"]), pct(x["visitors"], dv)] for x in devs]), ""]

    # 바깥 링크·기능
    ev = d["events_30d"]
    oc = [e for e in ev if e["event"] == "outclick"]
    ot = sum(e["n"] for e in oc)
    g = {e["event"] + ":" + e["target"]: e for e in ev}
    def ev_n(k, f="n"):
        return g[k][f] if k in g else 0
    L += ["## 어디로 나가나 (바깥 링크, 최근 30일)", "", tbl(["나간 곳", "클릭", "누른 사람", "비율"],
          [[OUTCLICK.get(e["target"], e["target"]), n(e["n"]), n(e["visitors"]), pct(e["n"], ot)] for e in oc]), "",
          f"- 위 세 곳({', '.join(OUTCLICK.get(e['target'], e['target']) for e in oc[:3])})이 바깥 클릭의 {pct(sum(e['n'] for e in oc[:3]), ot)} — 스텔 DB는 원래 글로 보내 주는 길목으로 쓰인다.", "",
          "## 기능 쓰임 (최근 30일)", "", tbl(["기능", "횟수", "사람"], [
              ["설치 앱으로 열기", n(ev_n("app_open:")), n(ev_n("app_open:", "visitors"))],
              ["앱 설치", n(ev_n("install:")), n(ev_n("install:", "visitors"))],
              ["알림 켜기", n(ev_n("push_on:")), n(ev_n("push_on:", "visitors"))],
              ["첫 방문 안내를 본 사람", n(ev_n("welcome:show")), n(ev_n("welcome:show", "visitors"))],
              ["첫 방문 안내에서 알림 켜기", n(ev_n("welcome:alerts")), n(ev_n("welcome:alerts", "visitors"))],
              ["팝업 굿즈 현황 펼침", n(ev_n("stock_open:")), n(ev_n("stock_open:", "visitors"))],
              ["공유 버튼", n(sum(e["n"] for e in ev if e["event"] == "share")), n(sum(e["visitors"] for e in ev if e["event"] == "share"))],
          ]), "",
          f"- 첫 방문 안내를 본 {n(ev_n('welcome:show', 'visitors'))}명 중 안내에서 바로 알림을 켠 사람은 {pct(ev_n('welcome:alerts', 'visitors'), ev_n('welcome:show', 'visitors'))}. 알림은 대부분 설정·알림 카드에서 켠다.",
          ""]

    # 가입·팬덤·알림
    su = [s for s in d["signups_weekly"] if s["wk"] >= "2026-09-21"]
    fd = d["fandoms"]
    L += ["## 가입", "", tbl(["주", "가입", "구글 로그인 가입"], [[s["wk"], n(s["n"]), n(s["oauth_n"])] for s in su]), "",
          f"- 가입의 {pct(sum(s['oauth_n'] for s in su), sum(s['n'] for s in su))}가 구글 로그인이다.", "",
          "## 회원이 고른 팬덤 (여러 개 선택 가능)", "", tbl(["팬덤", "회원"], [[f["fandom"], n(f["n"])] for f in fd]), "",
          "- 스텔라이브 시청자 규모와 같은 뜻이 아니다 — 스텔 DB 회원 안의 분포다.", "",
          "## 알림 구독 기기", "", tbl(["기기", "구독"], [[{"mobile": "폰", "pc": "PC", "unknown": "모름"}.get(k["kind"], k["kind"]), n(k["n"])] for k in d["push_kind"]]), ""]

    # 소식 수집량
    nw = [x for x in d["news_weekly"] if x["wk"] >= "2026-10-19"]
    wks = sorted({x["wk"] for x in nw})
    types = ["x", "cafe", "youtube", "chzzk", "fanding"]
    cell = {(x["wk"], x["type"]): x["n"] for x in nw}
    L += ["## 스텔 DB가 모은 소식 (주별)", "", tbl(["주"] + [NEWS[t] for t in types] + ["합계"],
          [[w] + [n(cell.get((w, t), 0)) for t in types] + [n(sum(cell.get((w, t), 0) for t in types))] for w in wks]), "",
          "- X는 멤버 답글·리트윗까지 모은다. 치지직은 방송 시작·종료·채팅·후원 알림이다.", "",
          "## 건의사항", "", f"- 받은 건의 {n(d['inquiries']['total'])}건, 답변 {n(d['inquiries']['answered'])}건.", "",
          "## 읽을 때 주의", "",
          "- 방문자는 브라우저 기준이라 폰·PC를 둘 다 쓰는 사람은 두 명으로, 브라우저 기록을 지운 사람은 새 사람으로 센다.",
          "- 9월 21일 이전은 운영자 혼자 보던 시험 기간이라 표에서 뺐다.",
          "- 알림을 눌러 들어온 것은 따로 세지 않는다(알림 누름 기록은 일부 기기에서만 남는다).",
          "- 숫자는 전부 `collect/data/steldb_usage.json` 에서 계산했다. 자동 갱신은 Actions 비밀값 `STELDB_SUPABASE_URL`·`STELDB_SUPABASE_KEY` 가 있을 때만 된다."]
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"[steldb] {OUT}")


if __name__ == "__main__":
    main()
