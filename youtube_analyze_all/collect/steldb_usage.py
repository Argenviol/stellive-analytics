"""
스텔 DB(steldatabase.onrender.com) 이용 집계를 받아 collect/data/steldb_usage.json 에 쓴다.

자료: 스텔 DB Supabase 함수 `stel_usage_export()` — 방문·탭·유입·기기·시간대·재방문 코호트·바깥 링크·
  가입·알림 구독·소식 수집량을 **집계값만** 돌려준다(방문자 id·IP·글 내용은 나오지 않는다).
필요한 환경변수: STELDB_SUPABASE_URL, STELDB_SUPABASE_KEY (service_role — 함수 실행 권한은 이 역할에만 있다).
  없으면 아무것도 바꾸지 않고 끝낸다(지난 스냅샷을 그대로 둔다).
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent / "data" / "steldb_usage.json"


def main() -> int:
    url, key = os.environ.get("STELDB_SUPABASE_URL", "").rstrip("/"), os.environ.get("STELDB_SUPABASE_KEY", "")
    if not url or not key:
        print("[steldb] STELDB_SUPABASE_URL/KEY 없음 — 지난 스냅샷 유지")
        return 0
    req = urllib.request.Request(f"{url}/rest/v1/rpc/stel_usage_export", data=b"{}", method="POST",
                                 headers={"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    if not isinstance(data, dict) or "weekly" not in data:
        print("[steldb] 응답 형식이 다름 — 저장 안 함", file=sys.stderr)
        return 1
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[steldb] 저장 {data.get('generated_at')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
