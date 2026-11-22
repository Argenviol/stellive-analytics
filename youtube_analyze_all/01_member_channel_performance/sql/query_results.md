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
|    1 | 아카네 리제  | UNIVERSE | 383000 |    429607 |
|    2 | 아야츠노 유니 | EVERYS   | 378000 |    188772 |
|    3 | 시라유키 히나 | UNIVERSE | 335000 |    195638 |
|    4 | 아오쿠모 린  | CLICHE   | 308000 |    261580 |
|    5 | 아라하시 타비 | UNIVERSE | 281000 |    258456 |
|    6 | 텐코 시부키  | CLICHE   | 249000 |    297761 |
|    7 | 유즈하 리코  | CLICHE   | 244000 |    291162 |
|    8 | 하나코 나나  | CLICHE   | 229000 |    306837 |
|    9 | 네네코 마시로 | UNIVERSE | 201000 |    149464 |
|   10 | 사키하네 후야 | EVERYS   | 156000 |    136442 |


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
| 하나코 나나  | 229000 |  306837 |      134   |
| 텐코 시부키  | 249000 |  297761 |      119.6 |
| 유즈하 리코  | 244000 |  291162 |      119.3 |
| 아카네 리제  | 383000 |  429607 |      112.2 |
| 아라하시 타비 | 281000 |  258456 |       92   |
| 사키하네 후야 | 156000 |  136442 |       87.5 |
| 아오쿠모 린  | 308000 |  261580 |       84.9 |
| 네네코 마시로 | 201000 |  149464 |       74.4 |
| 시라유키 히나 | 335000 |  195638 |       58.4 |
| 아야츠노 유니 | 378000 |  188772 |       49.9 |


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
| UNIVERSE |    4 |  300000 |  258291 |        2.62 |
| EVERYS   |    2 |  267000 |  162607 |        2.79 |
| CLICHE   |    4 |  257500 |  289334 |        2.37 |


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
| 사키하네 후야 |      3.34 |       3.22 |
| 네네코 마시로 |      3.13 |       2.96 |
| 시라유키 히나 |      2.77 |       2.63 |
| 유즈하 리코  |      2.71 |       2.62 |
| 하나코 나나  |      2.42 |       2.33 |
| 아라하시 타비 |      2.31 |       2.21 |
| 아카네 리제  |      2.28 |       2.22 |
| 텐코 시부키  |      2.26 |       2.19 |
| 아야츠노 유니 |      2.24 |       2.09 |
| 아오쿠모 린  |      2.1  |       2    |


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
| 하나코 나나  |    5.72 |         36 |
| 아카네 리제  |    5.36 |         38 |
| 유즈하 리코  |    5.2  |         42 |
| 아라하시 타비 |    4.76 |         18 |
| 시라유키 히나 |    4.13 |         30 |
| 아오쿠모 린  |    3.81 |         12 |
| 사키하네 후야 |    3.65 |         18 |
| 아야츠노 유니 |    2.86 |         10 |
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
| 아카네 리제  | 로스트원의 호곡 [ロストワンの号哭 / Neru]ㅣ아카네 리제(Akane Lize) 【COVER】      | 2146449 |
| 하나코 나나  | 오늘이 무슨 날이죠? #animation #shorts                             | 1435529 |
| 아오쿠모 린  | 불가행력 [不可幸力 / Vaundy ] / 아오쿠모 린 (Aokumo Rin) Cover          | 1339327 |
| 네네코 마시로 | 콧치노 켄토 - 네, 기꺼이 [はいよろこんで / こっちのけんと]ㅣ네네코 마시로 x 텐코 시부키 Cover | 1198672 |
| 텐코 시부키  | (소리주의) 붘몽가입니다 #vtuber #shorts #치이카와 #ちいかわ                  | 1084983 |
| 유즈하 리코  | 귀신 말고 유령 #vtuber #shorts #스텔라이브 #리코 #용사툰 #히요리 #하핫          |  830135 |
| 아라하시 타비 | 대체 캣파이트 미야오가 뭐냐고ㅋㅋㅋ                                        |  758218 |
| 시라유키 히나 | 아틀란티스 소녀 (Atlantis Princess) | 시라유키 히나 Cover               |  702682 |
| 아야츠노 유니 | L을 가져가~ 크림 치즈 허니 #스텔라이브 #유니 #stellive #shorts              |  702104 |
| 사키하네 후야 | 푸른 산호초(青い珊瑚礁) - 松田 聖子 l 사키하네 후야(Sakihane Huya) Cover       |  655761 |

