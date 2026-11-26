# 커버곡 분석 쿼리 실행 결과

`sql/covers.db`(SQLite) 실행 결과입니다.

## 커버곡 조회수 TOP 15

```sql
SELECT name_ko AS 멤버, title AS 곡, views AS 조회수, likes AS 좋아요
FROM covers ORDER BY views DESC LIMIT 15;
```

| 멤버      | 곡                                                                  |      조회수 |    좋아요 |
|:--------|:-------------------------------------------------------------------|---------:|-------:|
| 아카네 리제  | 출항 [抜錨(발묘) / 나나호시 관현악단 ナナホシ管弦楽団] ㅣ아카네 리제(Akane Lize) 【COVER】       | 17499318 | 121847 |
| 아카네 리제  | Drowning (WOODZ)ㅣ아카네 리제 (Akane Lize) 【Cover】                       | 12582274 |  74643 |
| 아카네 리제  | 내일의 밤하늘 초계반(アスノヨゾラ哨戒班)ㅣ아카네 리제(Akane Lize) 【COVER】                  | 11671540 |  62892 |
| 시라유키 히나 | 낙향(都落ち) / 시라유키 히나 Cover                                            |  8340325 |  45724 |
| 아카네 리제  | 괴물 (怪物) / 아카네 리제 Cover                                             |  7947857 |  43575 |
| 텐코 시부키  | 너에게 메롱(一二三) / 텐코 시부키(Tenko Shibuki) cover                          |  7936906 |  46287 |
| 아카네 리제  | 선잠 (Leina) / 아카네 리제 Cover                                          |  6646866 |  37180 |
| 하나코 나나  | 비행정 [飛行艇 - King Gnu] / 하나코 나나 COVER                                |  6346540 |  41252 |
| 아오쿠모 린  | W/X/Y (Tani Yuuki) / 아오쿠모 린(Aokumo Rin) Cover                      |  5642041 |  34713 |
| 아오쿠모 린  | 유령도쿄(Ayase) / 아오쿠모 린(Aokumo Rin) Cover                             |  5547336 |  34220 |
| 아카네 리제  | Surges (Orangestar)ㅣ아카네 리제(Akane Lize) 【COVER】                     |  5483724 |  36926 |
| 시라유키 히나 | I Really Want to Stay At Your House (Arrange ver.) | 시라유키 히나 Cover |  5408731 |  50715 |
| 토키노 메리  | 도쿄 테디베어 [東京テディベア l Neru] / 토키노 메리 (Tokino Mary) Cover              |  5160059 |  75042 |
| 텐코 시부키  | 여우비 / 텐코 시부키(Tenko Shibuki) cover                                  |  5147968 |  33077 |
| 시라유키 히나 | 피날레(フィナーレ。) / 시라유키 히나 Cover                                        |  5122059 |  32033 |


## 멤버별 커버 성과 랭킹

```sql
SELECT rank AS 순위, name_ko AS 멤버, song_count AS 곡수, cover_count AS 영상수,
       total_views AS 총조회수, total_views_incl_topic AS 음원포함, CAST(avg_views AS INT) AS 영상당평균
FROM cover_metrics ORDER BY total_views DESC;
```

|   순위 | 멤버      |   곡수 |   영상수 |      총조회수 |      음원포함 |   영상당평균 |
|-----:|:--------|-----:|------:|----------:|----------:|--------:|
|    1 | 아카네 리제  |   40 |    42 | 128447400 | 128447400 | 3058271 |
|    2 | 아오쿠모 린  |   55 |    59 | 104076215 | 104076215 | 1764003 |
|    3 | 유즈하 리코  |   58 |    63 |  73319538 |  73319538 | 1163802 |
|    4 | 시라유키 히나 |   46 |    51 |  71733036 |  71733036 | 1406530 |
|    5 | 하나코 나나  |   43 |    50 |  69251752 |  69251752 | 1385035 |
|    6 | 텐코 시부키  |   35 |    38 |  50152273 |  50152273 | 1319796 |
|    7 | 아라하시 타비 |   24 |    25 |  33166725 |  33166725 | 1326669 |
|    8 | 아야츠노 유니 |   17 |    17 |  17209420 |  17209420 | 1012318 |
|    9 | 네네코 마시로 |   22 |    22 |  16420500 |  16420500 |  746386 |
|   10 | 토키노 메리  |    1 |     1 |   5160059 |   5160059 | 5160059 |
|   11 | 사키하네 후야 |    8 |     8 |   4985612 |   4985612 |  623201 |
|   12 | 시즈키 토아  |    2 |     2 |   2987078 |   2987078 | 1493539 |
|   13 | 코가네 랑   |    1 |     1 |   1732086 |   1732086 | 1732086 |
|   14 | 하나요 히요리 |    1 |     1 |   1579802 |   1579802 | 1579802 |


## 여러 판으로 올라온 곡

```sql
SELECT name_ko AS 멤버, title AS 대표제목, n_versions AS 판수, views AS 판합계조회수, topic_views AS 음원조회수
FROM cover_songs WHERE n_versions > 1 ORDER BY views DESC;
```

| 멤버      | 대표제목                                                                                          |   판수 |   판합계조회수 |   음원조회수 |
|:--------|:----------------------------------------------------------------------------------------------|-----:|---------:|--------:|
| 아카네 리제  | 선잠 (Leina) / 아카네 리제 Cover                                                                     |    2 |  8394256 |       0 |
| 텐코 시부키  | 너에게 메롱(一二三) / 텐코 시부키(Tenko Shibuki) cover                                                     |    2 |  8117235 |       0 |
| 하나코 나나  | Enemy [Imagine Dragons x J.I.D] / 하나코 나나 COVER                                                |    2 |  5575500 |       0 |
| 텐코 시부키  | 여우비 / 텐코 시부키(Tenko Shibuki) cover                                                             |    2 |  5388115 |       0 |
| 아카네 리제  | Golden - HUNTR/X (KPop Demon Hunters)ㅣ아카네 리제 x 아오쿠모 린 x 하나코 나나 【COVER】                        |    2 |  4443419 |       0 |
| 유즈하 리코  | Henceforth / 유즈하 리코(Yuzuha Riko) cover                                                        |    3 |  4051104 |       0 |
| 아오쿠모 린  | IRIS OUT (요네즈 켄시) / 아오쿠모 린(Aokumo Rin) Cover                                                  |    2 |  3114246 |       0 |
| 시라유키 히나 | LADY - KenshiYonezu(米津玄師) | 시라유키 히나 Cover                                                     |    2 |  3056968 |       0 |
| 텐코 시부키  | UNDEAD (YOASOBI) / 텐코 시부키(Tenko Shibuki) cover                                                |    2 |  2893296 |       0 |
| 시라유키 히나 | Summertime (cinnamons × evening cinema) | 시라유키 히나(Shirayuki Hina) x 하나코 나나(Hanako Nana) Cover |    2 |  2114706 |       0 |
| 유즈하 리코  | 맑은 날(ヨルシカ - 晴る)  / 유즈하 리코(Yuzuha Riko) cover                                                  |    2 |  2076539 |       0 |
| 시라유키 히나 | Melt (メルト/supercell ) | 시라유키 히나 Cover                                                         |    2 |  1543746 |       0 |
| 아오쿠모 린  | Ｗ●ＲＫ (MILLENNIUM PARADE × 시이나 링고) / 아오쿠모 린 x 하나코 나나 Cover                                     |    2 |  1429264 |       0 |
| 아오쿠모 린  | PLAY(プレイ) - Giga📸 #Live2D #shorts #cover                                                      |    2 |  1180246 |       0 |
| 하나코 나나  | [ 당신의 연인이 되고 싶어 / ChoQMay ] 하나코 나나 Short cover #vtuber #shorts                                |    2 |  1054195 |       0 |
| 유즈하 리코  | [4K] 네모네모(NEMONEMO) - YENA(최예나) / 유즈하 리코 (Yuzuha Riko) cover                                  |    2 |   983530 |       0 |
| 아오쿠모 린  | Unbreakable Sphere (승리의 여신: 니케 OST) / 아오쿠모 린(Aokumo Rin) Cover                                |    2 |   835164 |       0 |
| 하나코 나나  | [4K] 飛行艇(비행정) - King Gnu / 하나코 나나 3D Live Cover                                               |    2 |   749684 |       0 |
| 시라유키 히나 | [4K] 앨리스 인 냉동고 (Alice in 冷凍庫) / 시라유키 히나 3D Live Cover                                         |    2 |   714980 |       0 |
| 아라하시 타비 | [4K] LADY (요네즈 켄시)ㅣ아라하시 타비(Arahashi Tabi) 「Live Cover」                                        |    2 |   550899 |       0 |
| 하나코 나나  | Dynamite - BTS(방탄소년단) / 하나코 나나 3D Cover #shorts #vtuber                                       |    2 |   542328 |       0 |
| 하나코 나나  | [4K] LAST STARDUST - Aimer / 하나코 나나 3D Cover                                                  |    2 |   467388 |       0 |
| 유즈하 리코  | [4K] No title - REOL / 유즈하 리코 (Yuzuha Riko) cover                                             |    2 |   418642 |       0 |
| 시라유키 히나 | [4K] 세계는 사랑에 빠져있어 (世界は恋に落ちている) | 시라유키 히나 3D Live Cover                                        |    2 |   382010 |       0 |
| 하나코 나나  | [4K] キミに100パーセント(너에게 100퍼센트) / 하나코 나나 3D Cover                                                |    2 |   380901 |       0 |
| 하나코 나나  | [4K] Dance The Night Away - TWICE(트와이스) / 하나코 나나 3D Cover                                     |    2 |   336953 |       0 |


## 곡당 평균 조회수 상위(5곡 이상)

```sql
SELECT name_ko AS 멤버, cover_count AS 곡수, CAST(avg_views AS INT) AS 평균조회수
FROM cover_metrics WHERE cover_count>=5 ORDER BY avg_views DESC;
```

| 멤버      |   곡수 |   평균조회수 |
|:--------|-----:|--------:|
| 아카네 리제  |   42 | 3058271 |
| 아오쿠모 린  |   59 | 1764003 |
| 시라유키 히나 |   51 | 1406530 |
| 하나코 나나  |   50 | 1385035 |
| 아라하시 타비 |   25 | 1326669 |
| 텐코 시부키  |   38 | 1319796 |
| 유즈하 리코  |   63 | 1163802 |
| 아야츠노 유니 |   17 | 1012318 |
| 네네코 마시로 |   22 |  746386 |
| 사키하네 후야 |    8 |  623201 |


## 멤버별 최고 커버

```sql
SELECT name_ko AS 멤버, best_cover AS 최고커버, max_views AS 조회수
FROM cover_metrics ORDER BY max_views DESC;
```

| 멤버      | 최고커버                                                         |      조회수 |
|:--------|:-------------------------------------------------------------|---------:|
| 아카네 리제  | 출항 [抜錨(발묘) / 나나호시 관현악단 ナナホシ管弦楽団] ㅣ아카네 리제(Akane Lize) 【COVER】 | 17499318 |
| 시라유키 히나 | 낙향(都落ち) / 시라유키 히나 Cover                                      |  8340325 |
| 텐코 시부키  | 너에게 메롱(一二三) / 텐코 시부키(Tenko Shibuki) cover                    |  7936906 |
| 하나코 나나  | 비행정 [飛行艇 - King Gnu] / 하나코 나나 COVER                          |  6346540 |
| 아오쿠모 린  | W/X/Y (Tani Yuuki) / 아오쿠모 린(Aokumo Rin) Cover                |  5642041 |
| 토키노 메리  | 도쿄 테디베어 [東京テディベア l Neru] / 토키노 메리 (Tokino Mary) Cover        |  5160059 |
| 아라하시 타비 | 낮에 뜨는 달 ( 안예은 ) / 아라하시 타비 Cover                              |  4262183 |
| 유즈하 리코  | 케세라세라 (Mrs. GREEN APPLE)  / 유즈하 리코(Yuzuha Riko) cover        |  3719845 |
| 아야츠노 유니 | 【아야츠노 유니 X 아이리 칸나】 점묘의 노래 (点描の唄) | Cover                     |  3153400 |
| 시즈키 토아  | 제육감 [第六感 l Reol] / 시즈키 토아(Shizuki Toa) Cover                 |  2488005 |
| 네네코 마시로 | Pale (MIMI) / 네네코 마시로 Cover                                  |  2419768 |
| 코가네 랑   | 호랑풍류가 [나와 호랑이님 OST] / 코가네 랑 (Cogane Rang) Cover              |  1732086 |
| 사키하네 후야 | 별자리가 될 수 있다면 (星座になれたら) l 사키하네 후야(Sakihane Huya) Cover        |  1586410 |
| 하나요 히요리 | 유령이 되고싶어 [ゆうれいになりたい / 유이카] / 하나요 히요리 (Hanayo Hiyori) Cover   |  1579802 |


## 유닛별 커버 요약

```sql
SELECT unit AS 유닛, COUNT(*) AS 멤버수, SUM(cover_count) AS 총곡수,
       SUM(total_views) AS 총조회수
FROM cover_metrics GROUP BY unit ORDER BY 총조회수 DESC;
```

| 유닛       |   멤버수 |   총곡수 |      총조회수 |
|:---------|------:|------:|----------:|
| CLICHE   |     4 |   210 | 296799778 |
| UNIVERSE |     4 |   140 | 249767661 |
| EVERYS   |     2 |    25 |  22195032 |
| ABYSS    |     4 |     5 |  11459025 |


## 솔로 vs 콜라보 비중

```sql
SELECT name_ko AS 멤버, ROUND(collab_share*100,0) AS 콜라보비중_pct, cover_count AS 곡수
FROM cover_metrics ORDER BY collab_share DESC;
```

| 멤버      |   콜라보비중_pct |   곡수 |
|:--------|------------:|-----:|
| 아오쿠모 린  |          20 |   59 |
| 하나코 나나  |          14 |   50 |
| 네네코 마시로 |          14 |   22 |
| 유즈하 리코  |          13 |   63 |
| 사키하네 후야 |          13 |    8 |
| 시라유키 히나 |          12 |   51 |
| 아야츠노 유니 |          12 |   17 |
| 텐코 시부키  |          11 |   38 |
| 아라하시 타비 |           8 |   25 |
| 아카네 리제  |           7 |   42 |
| 토키노 메리  |           0 |    1 |
| 시즈키 토아  |           0 |    2 |
| 코가네 랑   |           0 |    1 |
| 하나요 히요리 |           0 |    1 |

