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
|    1 | 아카네 리제  | UNIVERSE | 381000 |    393578 |
|    2 | 아야츠노 유니 | EVERYS   | 377000 |    174185 |
|    3 | 시라유키 히나 | UNIVERSE | 334000 |    193176 |
|    4 | 아오쿠모 린  | CLICHE   | 306000 |    257098 |
|    5 | 아라하시 타비 | UNIVERSE | 280000 |    270566 |
|    6 | 텐코 시부키  | CLICHE   | 248000 |    301386 |
|    7 | 유즈하 리코  | CLICHE   | 243000 |    279114 |
|    8 | 하나코 나나  | CLICHE   | 228000 |    288822 |
|    9 | 네네코 마시로 | UNIVERSE | 201000 |    144879 |
|   10 | 사키하네 후야 | EVERYS   | 155000 |    139034 |


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
| 하나코 나나  | 228000 |  288822 |      126.7 |
| 텐코 시부키  | 248000 |  301386 |      121.5 |
| 유즈하 리코  | 243000 |  279114 |      114.9 |
| 아카네 리제  | 381000 |  393578 |      103.3 |
| 아라하시 타비 | 280000 |  270566 |       96.6 |
| 사키하네 후야 | 155000 |  139034 |       89.7 |
| 아오쿠모 린  | 306000 |  257098 |       84   |
| 네네코 마시로 | 201000 |  144879 |       72.1 |
| 시라유키 히나 | 334000 |  193176 |       57.8 |
| 아야츠노 유니 | 377000 |  174185 |       46.2 |


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
| UNIVERSE |    4 |  299000 |  250549 |        2.63 |
| EVERYS   |    2 |  266000 |  156609 |        2.91 |
| CLICHE   |    4 |  256250 |  281604 |        2.5  |


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
| 사키하네 후야 |      3.45 |       3.33 |
| 네네코 마시로 |      3.23 |       3.06 |
| 유즈하 리코  |      2.83 |       2.73 |
| 시라유키 히나 |      2.78 |       2.64 |
| 하나코 나나  |      2.59 |       2.49 |
| 아야츠노 유니 |      2.38 |       2.22 |
| 텐코 시부키  |      2.31 |       2.24 |
| 아오쿠모 린  |      2.28 |       2.18 |
| 아라하시 타비 |      2.26 |       2.16 |
| 아카네 리제  |      2.24 |       2.17 |


## 업로드 빈도 상위

```sql
SELECT name_ko AS 멤버, uploads_per_week AS 주간업로드,
       ROUND(shorts_share*100,0) AS 쇼츠비중_pct
FROM channel_metrics WHERE role='talent'
ORDER BY uploads_per_week DESC;
```

| 멤버      |   주간업로드 |   쇼츠비중_pct |
|:--------|--------:|-----------:|
| 텐코 시부키  |    6.12 |         36 |
| 하나코 나나  |    6.12 |         38 |
| 유즈하 리코  |    5.53 |         42 |
| 아카네 리제  |    5.36 |         38 |
| 아라하시 타비 |    4.76 |         16 |
| 아오쿠모 린  |    4.04 |         16 |
| 시라유키 히나 |    3.69 |         32 |
| 사키하네 후야 |    3.69 |         22 |
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
| 아카네 리제  | 로스트원의 호곡 [ロストワンの号哭 / Neru]ㅣ아카네 리제(Akane Lize) 【COVER】      | 1532905 |
| 아오쿠모 린  | 불가행력 [不可幸力 / Vaundy ] / 아오쿠모 린 (Aokumo Rin) Cover          | 1250593 |
| 하나코 나나  | 오늘이 무슨 날이죠? #animation #shorts                             | 1232186 |
| 네네코 마시로 | 콧치노 켄토 - 네, 기꺼이 [はいよろこんで / こっちのけんと]ㅣ네네코 마시로 x 텐코 시부키 Cover | 1168641 |
| 텐코 시부키  | (소리주의) 붘몽가입니다 #vtuber #shorts #치이카와 #ちいかわ                  | 1042630 |
| 아라하시 타비 | 물떼새[ヨルシカ - 千鳥]ㅣ아라하시 타비 Cover                               |  919619 |
| 유즈하 리코  | 참을 수 없는 본능 #vtuber #shorts #스텔라이브 #리코 #용사툰                 |  777475 |
| 시라유키 히나 | 아틀란티스 소녀 (Atlantis Princess) | 시라유키 히나 Cover               |  682887 |
| 아야츠노 유니 | L을 가져가~ 크림 치즈 허니 #스텔라이브 #유니 #stellive #shorts              |  665016 |
| 사키하네 후야 | 푸른 산호초(青い珊瑚礁) - 松田 聖子 l 사키하네 후야(Sakihane Huya) Cover       |  624651 |

