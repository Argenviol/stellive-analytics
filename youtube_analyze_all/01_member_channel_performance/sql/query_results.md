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
|    1 | 아카네 리제  | UNIVERSE | 381000 |    406054 |
|    2 | 아야츠노 유니 | EVERYS   | 377000 |    178680 |
|    3 | 시라유키 히나 | UNIVERSE | 335000 |    198325 |
|    4 | 아오쿠모 린  | CLICHE   | 307000 |    262205 |
|    5 | 아라하시 타비 | UNIVERSE | 280000 |    267639 |
|    6 | 텐코 시부키  | CLICHE   | 248000 |    301568 |
|    7 | 유즈하 리코  | CLICHE   | 243000 |    285451 |
|    8 | 하나코 나나  | CLICHE   | 228000 |    293816 |
|    9 | 네네코 마시로 | UNIVERSE | 201000 |    146739 |
|   10 | 사키하네 후야 | EVERYS   | 155000 |    137878 |


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
| 하나코 나나  | 228000 |  293816 |      128.9 |
| 텐코 시부키  | 248000 |  301568 |      121.6 |
| 유즈하 리코  | 243000 |  285451 |      117.5 |
| 아카네 리제  | 381000 |  406054 |      106.6 |
| 아라하시 타비 | 280000 |  267639 |       95.6 |
| 사키하네 후야 | 155000 |  137878 |       89   |
| 아오쿠모 린  | 307000 |  262205 |       85.4 |
| 네네코 마시로 | 201000 |  146739 |       73   |
| 시라유키 히나 | 335000 |  198325 |       59.2 |
| 아야츠노 유니 | 377000 |  178680 |       47.4 |


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
| UNIVERSE |    4 |  299250 |  254689 |        2.64 |
| EVERYS   |    2 |  266000 |  158278 |        2.86 |
| CLICHE   |    4 |  256500 |  285760 |        2.47 |


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
| 사키하네 후야 |      3.35 |       3.23 |
| 네네코 마시로 |      3.21 |       3.04 |
| 유즈하 리코  |      2.79 |       2.7  |
| 시라유키 히나 |      2.77 |       2.63 |
| 하나코 나나  |      2.54 |       2.44 |
| 아라하시 타비 |      2.37 |       2.27 |
| 아야츠노 유니 |      2.36 |       2.2  |
| 아오쿠모 린  |      2.27 |       2.17 |
| 텐코 시부키  |      2.27 |       2.2  |
| 아카네 리제  |      2.22 |       2.15 |


## 업로드 빈도 상위

```sql
SELECT name_ko AS 멤버, uploads_per_week AS 주간업로드,
       ROUND(shorts_share*100,0) AS 쇼츠비중_pct
FROM channel_metrics WHERE role='talent'
ORDER BY uploads_per_week DESC;
```

| 멤버      |   주간업로드 |   쇼츠비중_pct |
|:--------|--------:|-----------:|
| 텐코 시부키  |    6.02 |         34 |
| 하나코 나나  |    6.02 |         38 |
| 유즈하 리코  |    5.53 |         42 |
| 아카네 리제  |    5.36 |         38 |
| 아라하시 타비 |    4.9  |         18 |
| 시라유키 히나 |    4.13 |         32 |
| 아오쿠모 린  |    4.04 |         16 |
| 사키하네 후야 |    3.65 |         20 |
| 아야츠노 유니 |    2.83 |         10 |
| 네네코 마시로 |    2.45 |          8 |


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
| 아카네 리제  | 로스트원의 호곡 [ロストワンの号哭 / Neru]ㅣ아카네 리제(Akane Lize) 【COVER】      | 1725537 |
| 하나코 나나  | 오늘이 무슨 날이죠? #animation #shorts                             | 1280074 |
| 아오쿠모 린  | 불가행력 [不可幸力 / Vaundy ] / 아오쿠모 린 (Aokumo Rin) Cover          | 1277296 |
| 네네코 마시로 | 콧치노 켄토 - 네, 기꺼이 [はいよろこんで / こっちのけんと]ㅣ네네코 마시로 x 텐코 시부키 Cover | 1178271 |
| 텐코 시부키  | (소리주의) 붘몽가입니다 #vtuber #shorts #치이카와 #ちいかわ                  | 1055463 |
| 아라하시 타비 | 물떼새[ヨルシカ - 千鳥]ㅣ아라하시 타비 Cover                               |  934737 |
| 유즈하 리코  | 참을 수 없는 본능 #vtuber #shorts #스텔라이브 #리코 #용사툰                 |  780966 |
| 시라유키 히나 | 아틀란티스 소녀 (Atlantis Princess) | 시라유키 히나 Cover               |  688715 |
| 아야츠노 유니 | L을 가져가~ 크림 치즈 허니 #스텔라이브 #유니 #stellive #shorts              |  680304 |
| 사키하네 후야 | 푸른 산호초(青い珊瑚礁) - 松田 聖子 l 사키하네 후야(Sakihane Huya) Cover       |  633523 |

