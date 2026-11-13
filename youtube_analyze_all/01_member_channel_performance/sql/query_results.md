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
|    1 | 아카네 리제  | UNIVERSE | 380000 |    395566 |
|    2 | 아야츠노 유니 | EVERYS   | 377000 |    171231 |
|    3 | 시라유키 히나 | UNIVERSE | 334000 |    187669 |
|    4 | 아오쿠모 린  | CLICHE   | 306000 |    250747 |
|    5 | 아라하시 타비 | UNIVERSE | 280000 |    288438 |
|    6 | 텐코 시부키  | CLICHE   | 247000 |    303947 |
|    7 | 유즈하 리코  | CLICHE   | 243000 |    273051 |
|    8 | 하나코 나나  | CLICHE   | 228000 |    289476 |
|    9 | 네네코 마시로 | UNIVERSE | 201000 |    142733 |
|   10 | 사키하네 후야 | EVERYS   | 155000 |    136936 |


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
| 하나코 나나  | 228000 |  289476 |      127   |
| 텐코 시부키  | 247000 |  303947 |      123.1 |
| 유즈하 리코  | 243000 |  273051 |      112.4 |
| 아카네 리제  | 380000 |  395566 |      104.1 |
| 아라하시 타비 | 280000 |  288438 |      103   |
| 사키하네 후야 | 155000 |  136936 |       88.3 |
| 아오쿠모 린  | 306000 |  250747 |       81.9 |
| 네네코 마시로 | 201000 |  142733 |       71   |
| 시라유키 히나 | 334000 |  187669 |       56.2 |
| 아야츠노 유니 | 377000 |  171231 |       45.4 |


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
| UNIVERSE |    4 |  298750 |  253601 |        2.64 |
| EVERYS   |    2 |  266000 |  154083 |        3.01 |
| CLICHE   |    4 |  256000 |  279305 |        2.48 |


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
| 사키하네 후야 |      3.55 |       3.42 |
| 네네코 마시로 |      3.31 |       3.13 |
| 유즈하 리코  |      2.88 |       2.77 |
| 시라유키 히나 |      2.83 |       2.69 |
| 아야츠노 유니 |      2.47 |       2.31 |
| 하나코 나나  |      2.44 |       2.36 |
| 아오쿠모 린  |      2.32 |       2.22 |
| 텐코 시부키  |      2.27 |       2.2  |
| 아카네 리제  |      2.22 |       2.16 |
| 아라하시 타비 |      2.18 |       2.08 |


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
| 유즈하 리코  |    5.44 |         42 |
| 아카네 리제  |    5.28 |         38 |
| 아라하시 타비 |    4.76 |         14 |
| 아오쿠모 린  |    4.13 |         16 |
| 시라유키 히나 |    3.69 |         32 |
| 사키하네 후야 |    3.69 |         24 |
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
| 아카네 리제  | 로스트원의 호곡 [ロストワンの号哭 / Neru]ㅣ아카네 리제(Akane Lize) 【COVER】      | 1314884 |
| 아오쿠모 린  | 불가행력 [不可幸力 / Vaundy ] / 아오쿠모 린 (Aokumo Rin) Cover          | 1226825 |
| 아라하시 타비 | High Hopes - Panic! At The Discoㅣ아라하시 타비 Cover             | 1223995 |
| 하나코 나나  | 오늘이 무슨 날이죠? #animation #shorts                             | 1191212 |
| 네네코 마시로 | 콧치노 켄토 - 네, 기꺼이 [はいよろこんで / こっちのけんと]ㅣ네네코 마시로 x 텐코 시부키 Cover | 1159957 |
| 텐코 시부키  | (소리주의) 붘몽가입니다 #vtuber #shorts #치이카와 #ちいかわ                  | 1026188 |
| 유즈하 리코  | 참을 수 없는 본능 #vtuber #shorts #스텔라이브 #리코 #용사툰                 |  774025 |
| 시라유키 히나 | 아틀란티스 소녀 (Atlantis Princess) | 시라유키 히나 Cover               |  677396 |
| 아야츠노 유니 | 다이죠부이데쇼 😎💜  #stellive #스텔라이브 #유니                           |  662006 |
| 사키하네 후야 | 푸른 산호초(青い珊瑚礁) - 松田 聖子 l 사키하네 후야(Sakihane Huya) Cover       |  616937 |

