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
|    1 | 아카네 리제  | UNIVERSE | 384000 |    442582 |
|    2 | 아야츠노 유니 | EVERYS   | 378000 |    191203 |
|    3 | 시라유키 히나 | UNIVERSE | 335000 |    197343 |
|    4 | 아오쿠모 린  | CLICHE   | 308000 |    263393 |
|    5 | 아라하시 타비 | UNIVERSE | 281000 |    254390 |
|    6 | 텐코 시부키  | CLICHE   | 249000 |    297232 |
|    7 | 유즈하 리코  | CLICHE   | 245000 |    294298 |
|    8 | 하나코 나나  | CLICHE   | 229000 |    308567 |
|    9 | 네네코 마시로 | UNIVERSE | 201000 |    150064 |
|   10 | 사키하네 후야 | EVERYS   | 156000 |    137441 |


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
| 하나코 나나  | 229000 |  308567 |      134.7 |
| 유즈하 리코  | 245000 |  294298 |      120.1 |
| 텐코 시부키  | 249000 |  297232 |      119.4 |
| 아카네 리제  | 384000 |  442582 |      115.3 |
| 아라하시 타비 | 281000 |  254390 |       90.5 |
| 사키하네 후야 | 156000 |  137441 |       88.1 |
| 아오쿠모 린  | 308000 |  263393 |       85.5 |
| 네네코 마시로 | 201000 |  150064 |       74.7 |
| 시라유키 히나 | 335000 |  197343 |       58.9 |
| 아야츠노 유니 | 378000 |  191203 |       50.6 |


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
| UNIVERSE |    4 |  300250 |  261094 |        2.62 |
| EVERYS   |    2 |  267000 |  164322 |        2.78 |
| CLICHE   |    4 |  257750 |  290872 |        2.38 |


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
| 사키하네 후야 |      3.33 |       3.21 |
| 네네코 마시로 |      3.12 |       2.96 |
| 시라유키 히나 |      2.76 |       2.62 |
| 유즈하 리코  |      2.62 |       2.53 |
| 하나코 나나  |      2.47 |       2.38 |
| 텐코 시부키  |      2.33 |       2.26 |
| 아라하시 타비 |      2.32 |       2.23 |
| 아카네 리제  |      2.29 |       2.22 |
| 아야츠노 유니 |      2.23 |       2.09 |
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
| 텐코 시부키  |    5.91 |         32 |
| 하나코 나나  |    5.72 |         38 |
| 아카네 리제  |    5.36 |         38 |
| 유즈하 리코  |    5.28 |         40 |
| 아라하시 타비 |    4.76 |         18 |
| 시라유키 히나 |    4.23 |         30 |
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
| 아카네 리제  | 로스트원의 호곡 [ロストワンの号哭 / Neru]ㅣ아카네 리제(Akane Lize) 【COVER】      | 2218646 |
| 하나코 나나  | 오늘이 무슨 날이죠? #animation #shorts                             | 1462844 |
| 아오쿠모 린  | 불가행력 [不可幸力 / Vaundy ] / 아오쿠모 린 (Aokumo Rin) Cover          | 1350039 |
| 네네코 마시로 | 콧치노 켄토 - 네, 기꺼이 [はいよろこんで / こっちのけんと]ㅣ네네코 마시로 x 텐코 시부키 Cover | 1202227 |
| 텐코 시부키  | (소리주의) 붘몽가입니다 #vtuber #shorts #치이카와 #ちいかわ                  | 1092170 |
| 유즈하 리코  | 귀신 말고 유령 #vtuber #shorts #스텔라이브 #리코 #용사툰 #히요리 #하핫          |  848498 |
| 아라하시 타비 | 대체 캣파이트 미야오가 뭐냐고ㅋㅋㅋ                                        |  759934 |
| 아야츠노 유니 | L을 가져가~ 크림 치즈 허니 #스텔라이브 #유니 #stellive #shorts              |  706081 |
| 시라유키 히나 | 아틀란티스 소녀 (Atlantis Princess) | 시라유키 히나 Cover               |  705127 |
| 사키하네 후야 | 푸른 산호초(青い珊瑚礁) - 松田 聖子 l 사키하네 후야(Sakihane Huya) Cover       |  659268 |

