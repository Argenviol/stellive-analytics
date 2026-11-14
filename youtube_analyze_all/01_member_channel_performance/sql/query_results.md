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
|    1 | 아카네 리제  | UNIVERSE | 380000 |    399523 |
|    2 | 아야츠노 유니 | EVERYS   | 377000 |    173584 |
|    3 | 시라유키 히나 | UNIVERSE | 334000 |    189978 |
|    4 | 아오쿠모 린  | CLICHE   | 306000 |    252784 |
|    5 | 아라하시 타비 | UNIVERSE | 280000 |    267979 |
|    6 | 텐코 시부키  | CLICHE   | 247000 |    305274 |
|    7 | 유즈하 리코  | CLICHE   | 243000 |    275022 |
|    8 | 하나코 나나  | CLICHE   | 228000 |    292861 |
|    9 | 네네코 마시로 | UNIVERSE | 201000 |    143500 |
|   10 | 사키하네 후야 | EVERYS   | 155000 |    137548 |


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
| 하나코 나나  | 228000 |  292861 |      128.4 |
| 텐코 시부키  | 247000 |  305274 |      123.6 |
| 유즈하 리코  | 243000 |  275022 |      113.2 |
| 아카네 리제  | 380000 |  399523 |      105.1 |
| 아라하시 타비 | 280000 |  267979 |       95.7 |
| 사키하네 후야 | 155000 |  137548 |       88.7 |
| 아오쿠모 린  | 306000 |  252784 |       82.6 |
| 네네코 마시로 | 201000 |  143500 |       71.4 |
| 시라유키 히나 | 334000 |  189978 |       56.9 |
| 아야츠노 유니 | 377000 |  173584 |       46   |


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
| UNIVERSE |    4 |  298750 |  250245 |        2.67 |
| EVERYS   |    2 |  266000 |  155565 |        2.96 |
| CLICHE   |    4 |  256000 |  281485 |        2.46 |


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
| 사키하네 후야 |      3.47 |       3.35 |
| 네네코 마시로 |      3.29 |       3.12 |
| 유즈하 리코  |      2.85 |       2.75 |
| 시라유키 히나 |      2.82 |       2.68 |
| 아야츠노 유니 |      2.46 |       2.3  |
| 하나코 나나  |      2.41 |       2.33 |
| 아오쿠모 린  |      2.32 |       2.21 |
| 아라하시 타비 |      2.28 |       2.19 |
| 아카네 리제  |      2.27 |       2.21 |
| 텐코 시부키  |      2.26 |       2.19 |


## 업로드 빈도 상위

```sql
SELECT name_ko AS 멤버, uploads_per_week AS 주간업로드,
       ROUND(shorts_share*100,0) AS 쇼츠비중_pct
FROM channel_metrics WHERE role='talent'
ORDER BY uploads_per_week DESC;
```

| 멤버      |   주간업로드 |   쇼츠비중_pct |
|:--------|--------:|-----------:|
| 하나코 나나  |    6.24 |         38 |
| 텐코 시부키  |    6.12 |         34 |
| 유즈하 리코  |    5.53 |         42 |
| 아카네 리제  |    5.28 |         40 |
| 아라하시 타비 |    4.76 |         16 |
| 아오쿠모 린  |    4.13 |         16 |
| 시라유키 히나 |    3.69 |         32 |
| 사키하네 후야 |    3.69 |         22 |
| 아야츠노 유니 |    2.86 |         12 |
| 네네코 마시로 |    2.47 |          8 |


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
| 아카네 리제  | 로스트원의 호곡 [ロストワンの号哭 / Neru]ㅣ아카네 리제(Akane Lize) 【COVER】      | 1435859 |
| 아오쿠모 린  | 불가행력 [不可幸力 / Vaundy ] / 아오쿠모 린 (Aokumo Rin) Cover          | 1239341 |
| 하나코 나나  | 오늘이 무슨 날이죠? #animation #shorts                             | 1209296 |
| 네네코 마시로 | 콧치노 켄토 - 네, 기꺼이 [はいよろこんで / こっちのけんと]ㅣ네네코 마시로 x 텐코 시부키 Cover | 1164468 |
| 텐코 시부키  | (소리주의) 붘몽가입니다 #vtuber #shorts #치이카와 #ちいかわ                  | 1034501 |
| 아라하시 타비 | 물떼새[ヨルシカ - 千鳥]ㅣ아라하시 타비 Cover                               |  913442 |
| 유즈하 리코  | 참을 수 없는 본능 #vtuber #shorts #스텔라이브 #리코 #용사툰                 |  776173 |
| 시라유키 히나 | 아틀란티스 소녀 (Atlantis Princess) | 시라유키 히나 Cover               |  680451 |
| 아야츠노 유니 | 다이죠부이데쇼 😎💜  #stellive #스텔라이브 #유니                           |  662523 |
| 사키하네 후야 | 푸른 산호초(青い珊瑚礁) - 松田 聖子 l 사키하네 후야(Sakihane Huya) Cover       |  621169 |

