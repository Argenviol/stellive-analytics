# 분석 쿼리 실행 결과

`sql/stellive.db`(SQLite)에 대해 `analysis_queries.sql`을 실행한 결과입니다.

## 구독자 상위 랭킹

```sql
SELECT rank_subs AS 순위, name_ko AS 멤버, unit AS 유닛,
       subscribers AS 구독자, recent_avg_views AS 최근평균조회수
FROM channel_metrics ORDER BY subscribers DESC;
```

|   순위 | 멤버      | 유닛       |    구독자 |          최근평균조회수 |
|-----:|:--------|:---------|-------:|-----------------:|
|    1 | 아카네 리제  | UNIVERSE | 385000 | 450051           |
|    2 | 아야츠노 유니 | EVERYS   | 378000 | 189437           |
|    3 | 시라유키 히나 | UNIVERSE | 336000 | 189592           |
|    4 | 아오쿠모 린  | CLICHE   | 308000 | 267682           |
|    5 | 아라하시 타비 | UNIVERSE | 281000 | 247451           |
|    6 | 텐코 시부키  | CLICHE   | 249000 | 302962           |
|    7 | 유즈하 리코  | CLICHE   | 245000 | 299185           |
|    8 | 하나코 나나  | CLICHE   | 230000 | 314224           |
|    9 | 토키노 메리  | ABYSS    | 206000 |      1.23393e+06 |
|   10 | 네네코 마시로 | UNIVERSE | 202000 | 151073           |
|   11 | 사키하네 후야 | EVERYS   | 156000 | 138990           |


## 도달 효율(평균조회수/구독자) 상위

```sql
SELECT name_ko AS 멤버, subscribers AS 구독자,
       recent_avg_views AS 평균조회수,
       ROUND(reach_ratio*100,1) AS 도달효율_pct
FROM channel_metrics WHERE role='talent'
ORDER BY reach_ratio DESC;
```

| 멤버      |    구독자 |            평균조회수 |   도달효율_pct |
|:--------|-------:|-----------------:|-----------:|
| 토키노 메리  | 206000 |      1.23393e+06 |      599   |
| 하나코 나나  | 230000 | 314224           |      136.6 |
| 유즈하 리코  | 245000 | 299185           |      122.1 |
| 텐코 시부키  | 249000 | 302962           |      121.7 |
| 아카네 리제  | 385000 | 450051           |      116.9 |
| 사키하네 후야 | 156000 | 138990           |       89.1 |
| 아라하시 타비 | 281000 | 247451           |       88.1 |
| 아오쿠모 린  | 308000 | 267682           |       86.9 |
| 네네코 마시로 | 202000 | 151073           |       74.8 |
| 시라유키 히나 | 336000 | 189592           |       56.4 |
| 아야츠노 유니 | 378000 | 189437           |       50.1 |


## 유닛별 요약

```sql
SELECT unit AS 유닛, COUNT(*) AS 인원,
       CAST(AVG(subscribers) AS INT) AS 평균구독자,
       CAST(AVG(recent_avg_views) AS INT) AS 평균조회수,
       ROUND(AVG(recent_avg_engagement_rate)*100,2) AS 평균참여율_pct
FROM channel_metrics WHERE role='talent'
GROUP BY unit ORDER BY 평균구독자 DESC;
```

| 유닛       |   인원 |   평균구독자 |   평균조회수 |   평균참여율_pct |
|:---------|-----:|--------:|--------:|------------:|
| UNIVERSE |    4 |  301000 |  259541 |        2.62 |
| EVERYS   |    2 |  267000 |  164213 |        2.87 |
| CLICHE   |    4 |  258000 |  296013 |        2.35 |
| ABYSS    |    1 |  206000 | 1233934 |        3.57 |


## 참여율 상위

```sql
SELECT name_ko AS 멤버,
       ROUND(recent_avg_engagement_rate*100,2) AS 참여율_pct,
       ROUND(recent_avg_like_rate*100,2) AS 좋아요율_pct
FROM channel_metrics WHERE role='talent'
ORDER BY recent_avg_engagement_rate DESC;
```

| 멤버      |   참여율_pct |   좋아요율_pct |
|:--------|----------:|-----------:|
| 토키노 메리  |      3.57 |       3.36 |
| 사키하네 후야 |      3.56 |       3.42 |
| 네네코 마시로 |      3.11 |       2.94 |
| 시라유키 히나 |      2.8  |       2.66 |
| 유즈하 리코  |      2.6  |       2.51 |
| 하나코 나나  |      2.44 |       2.35 |
| 아라하시 타비 |      2.31 |       2.21 |
| 텐코 시부키  |      2.3  |       2.24 |
| 아카네 리제  |      2.27 |       2.2  |
| 아야츠노 유니 |      2.17 |       2.04 |
| 아오쿠모 린  |      2.07 |       1.97 |


## 업로드 빈도 상위

```sql
SELECT name_ko AS 멤버, uploads_per_week AS 주간업로드,
       ROUND(shorts_share*100,0) AS 쇼츠비중_pct
FROM channel_metrics WHERE role='talent'
ORDER BY uploads_per_week DESC;
```

| 멤버      |   주간업로드 |   쇼츠비중_pct |
|:--------|--------:|-----------:|
| 텐코 시부키  |    5.72 |         32 |
| 하나코 나나  |    5.72 |         38 |
| 아카네 리제  |    5.36 |         38 |
| 유즈하 리코  |    5.28 |         40 |
| 아라하시 타비 |    4.7  |         18 |
| 시라유키 히나 |    4.23 |         32 |
| 아오쿠모 린  |    3.81 |         12 |
| 사키하네 후야 |    3.73 |         16 |
| 아야츠노 유니 |    2.88 |         10 |
| 네네코 마시로 |    2.45 |          8 |
| 토키노 메리  |    0.74 |         20 |


## 멤버별 최고 조회수 영상

```sql
SELECT m.name_ko AS 멤버, v.title AS 영상, v.views AS 조회수
FROM videos v
JOIN (SELECT channel_id, MAX(views) AS mx FROM videos GROUP BY channel_id) t
  ON v.channel_id=t.channel_id AND v.views=t.mx
JOIN channel_metrics m ON m.channel_id=v.channel_id
ORDER BY v.views DESC;
```

| 멤버      | 영상                                                         |     조회수 |
|:--------|:-----------------------------------------------------------|--------:|
| 토키노 메리  | 도쿄 테디베어 [東京テディベア l Neru] / 토키노 메리 (Tokino Mary) Cover      | 5104290 |
| 아카네 리제  | 로스트원의 호곡 [ロストワンの号哭 / Neru]ㅣ아카네 리제(Akane Lize) 【COVER】      | 2385708 |
| 하나코 나나  | 오늘이 무슨 날이죠? #animation #shorts                             | 1503781 |
| 아오쿠모 린  | 불가행력 [不可幸力 / Vaundy ] / 아오쿠모 린 (Aokumo Rin) Cover          | 1378260 |
| 네네코 마시로 | 콧치노 켄토 - 네, 기꺼이 [はいよろこんで / こっちのけんと]ㅣ네네코 마시로 x 텐코 시부키 Cover | 1210657 |
| 텐코 시부키  | (소리주의) 붘몽가입니다 #vtuber #shorts #치이카와 #ちいかわ                  | 1102352 |
| 유즈하 리코  | 귀신 말고 유령 #vtuber #shorts #스텔라이브 #리코 #용사툰 #히요리 #하핫          |  876944 |
| 아야츠노 유니 | L을 가져가~ 크림 치즈 허니 #스텔라이브 #유니 #stellive #shorts              |  720468 |
| 시라유키 히나 | 타상연화『打上花火』[DAOKO × 요네즈켄시] | 시라유키 히나 x 아오쿠모 린 Cover 스       |  670001 |
| 사키하네 후야 | 푸른 산호초(青い珊瑚礁) - 松田 聖子 l 사키하네 후야(Sakihane Huya) Cover       |  667705 |
| 아라하시 타비 | 아니 스트리머 유즈하 리코님;; #shorts #vtuber #땁툰                      |  593901 |

