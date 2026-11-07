# 분석 쿼리 실행 결과

`sql/stellive.db`(SQLite)에 대해 `analysis_queries.sql`을 실행한 결과입니다.

## 구독자 상위 랭킹

```sql
SELECT rank_subs AS 순위, name_ko AS 멤버, unit AS 유닛,
       subscribers AS 구독자, recent_avg_views AS 최근평균조회수
FROM channel_metrics ORDER BY subscribers DESC;
```

|   순위 | 멤버      | 유닛       |    구독자 |   최근평균조회수 |
|-----:|:--------|:---------|-------:|----------:|
|    1 | 아카네 리제  | UNIVERSE | 377000 |    358916 |
|    2 | 아야츠노 유니 | EVERYS   | 376000 |    174636 |
|    3 | 시라유키 히나 | UNIVERSE | 334000 |    181311 |
|    4 | 아오쿠모 린  | CLICHE   | 304000 |    233096 |
|    5 | 아라하시 타비 | UNIVERSE | 279000 |    282400 |
|    6 | 텐코 시부키  | CLICHE   | 246000 |    301953 |
|    7 | 유즈하 리코  | CLICHE   | 241000 |    280398 |
|    8 | 하나코 나나  | CLICHE   | 226000 |    293780 |
|    9 | 네네코 마시로 | UNIVERSE | 200000 |    137441 |
|   10 | 사키하네 후야 | EVERYS   | 154000 |    135700 |


## 도달 효율(평균조회수/구독자) 상위

```sql
SELECT name_ko AS 멤버, subscribers AS 구독자,
       recent_avg_views AS 평균조회수,
       ROUND(reach_ratio*100,1) AS 도달효율_pct
FROM channel_metrics WHERE role='talent'
ORDER BY reach_ratio DESC;
```

| 멤버      |    구독자 |   평균조회수 |   도달효율_pct |
|:--------|-------:|--------:|-----------:|
| 하나코 나나  | 226000 |  293780 |      130   |
| 텐코 시부키  | 246000 |  301953 |      122.7 |
| 유즈하 리코  | 241000 |  280398 |      116.3 |
| 아라하시 타비 | 279000 |  282400 |      101.2 |
| 아카네 리제  | 377000 |  358916 |       95.2 |
| 사키하네 후야 | 154000 |  135700 |       88.1 |
| 아오쿠모 린  | 304000 |  233096 |       76.7 |
| 네네코 마시로 | 200000 |  137441 |       68.7 |
| 시라유키 히나 | 334000 |  181311 |       54.3 |
| 아야츠노 유니 | 376000 |  174636 |       46.4 |


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
| UNIVERSE |    4 |  297500 |  240017 |        2.73 |
| EVERYS   |    2 |  265000 |  155168 |        2.94 |
| CLICHE   |    4 |  254250 |  277307 |        2.49 |


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
| 네네코 마시로 |      3.37 |       3.18 |
| 사키하네 후야 |      3.36 |       3.23 |
| 시라유키 히나 |      3.02 |       2.87 |
| 유즈하 리코  |      2.92 |       2.81 |
| 아야츠노 유니 |      2.52 |       2.36 |
| 아오쿠모 린  |      2.42 |       2.31 |
| 하나코 나나  |      2.38 |       2.3  |
| 아카네 리제  |      2.31 |       2.25 |
| 텐코 시부키  |      2.24 |       2.18 |
| 아라하시 타비 |      2.21 |       2.12 |


## 업로드 빈도 상위

```sql
SELECT name_ko AS 멤버, uploads_per_week AS 주간업로드,
       ROUND(shorts_share*100,0) AS 쇼츠비중_pct
FROM channel_metrics WHERE role='talent'
ORDER BY uploads_per_week DESC;
```

| 멤버      |   주간업로드 |   쇼츠비중_pct |
|:--------|--------:|-----------:|
| 하나코 나나  |    6.73 |         38 |
| 텐코 시부키  |    6.24 |         34 |
| 유즈하 리코  |    5.28 |         42 |
| 아카네 리제  |    5.2  |         38 |
| 아라하시 타비 |    4.7  |         16 |
| 아오쿠모 린  |    4.04 |         16 |
| 사키하네 후야 |    3.69 |         24 |
| 시라유키 히나 |    3.61 |         34 |
| 아야츠노 유니 |    2.88 |         14 |
| 네네코 마시로 |    2.33 |          8 |


## 멤버별 최고 조회수 영상

```sql
SELECT m.name_ko AS 멤버, v.title AS 영상, v.views AS 조회수
FROM videos v
JOIN (SELECT channel_id, MAX(views) AS mx FROM videos GROUP BY channel_id) t
  ON v.channel_id=t.channel_id AND v.views=t.mx
JOIN channel_metrics m ON m.channel_id=v.channel_id
ORDER BY v.views DESC;
```

| 멤버      | 영상                                                                    |     조회수 |
|:--------|:----------------------------------------------------------------------|--------:|
| 유즈하 리코  | 오늘 나는 찌그러진 클리셰가 될 거야 #vtuber #shorts #리코 #스텔라이브 #챌린지 #meme | 1284244 |
| 아라하시 타비 | High Hopes - Panic! At The Discoㅣ아라하시 타비 Cover                        | 1197128 |
| 아오쿠모 린  | 불가행력 [不可幸力 / Vaundy ] / 아오쿠모 린 (Aokumo Rin) Cover                     | 1157371 |
| 네네코 마시로 | 콧치노 켄토 - 네, 기꺼이 [はいよろこんで / こっちのけんと]ㅣ네네코 마시로 x 텐코 시부키 Cover            | 1137382 |
| 하나코 나나  | 오늘이 무슨 날이죠? #animation #shorts                                        | 1039250 |
| 텐코 시부키  | (소리주의) 붘몽가입니다 #vtuber #shorts #치이카와 #ちいかわ                             |  961434 |
| 아카네 리제  | 픽셀 병약 담당 vs 스텔 병약 담당                                                  |  834435 |
| 아야츠노 유니 | 아 르 냥 일 어 나 🕗 !! #stellive #스텔라이브 #유니 #알람                             |  711416 |
| 시라유키 히나 | 아틀란티스 소녀 (Atlantis Princess) | 시라유키 히나 Cover                          |  663248 |
| 사키하네 후야 | 푸른 산호초(青い珊瑚礁) - 松田 聖子 l 사키하네 후야(Sakihane Huya) Cover                  |  595406 |

