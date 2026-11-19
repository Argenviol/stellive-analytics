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
|    1 | 아카네 리제  | UNIVERSE | 382000 |    404169 |
|    2 | 아야츠노 유니 | EVERYS   | 377000 |    181932 |
|    3 | 시라유키 히나 | UNIVERSE | 335000 |    192803 |
|    4 | 아오쿠모 린  | CLICHE   | 307000 |    258491 |
|    5 | 아라하시 타비 | UNIVERSE | 281000 |    271412 |
|    6 | 텐코 시부키  | CLICHE   | 248000 |    301600 |
|    7 | 유즈하 리코  | CLICHE   | 244000 |    285740 |
|    8 | 하나코 나나  | CLICHE   | 229000 |    295464 |
|    9 | 네네코 마시로 | UNIVERSE | 201000 |    147208 |
|   10 | 사키하네 후야 | EVERYS   | 155000 |    134930 |


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
| 하나코 나나  | 229000 |  295464 |      129   |
| 텐코 시부키  | 248000 |  301600 |      121.6 |
| 유즈하 리코  | 244000 |  285740 |      117.1 |
| 아카네 리제  | 382000 |  404169 |      105.8 |
| 아라하시 타비 | 281000 |  271412 |       96.6 |
| 사키하네 후야 | 155000 |  134930 |       87.1 |
| 아오쿠모 린  | 307000 |  258491 |       84.2 |
| 네네코 마시로 | 201000 |  147208 |       73.2 |
| 시라유키 히나 | 335000 |  192803 |       57.6 |
| 아야츠노 유니 | 377000 |  181932 |       48.3 |


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
| UNIVERSE |    4 |  299750 |  253898 |        2.64 |
| EVERYS   |    2 |  266000 |  158430 |        2.86 |
| CLICHE   |    4 |  257000 |  285323 |        2.43 |


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
| 사키하네 후야 |      3.41 |       3.28 |
| 네네코 마시로 |      3.16 |       2.99 |
| 유즈하 리코  |      2.75 |       2.66 |
| 시라유키 히나 |      2.73 |       2.59 |
| 하나코 나나  |      2.5  |       2.42 |
| 아카네 리제  |      2.34 |       2.27 |
| 아라하시 타비 |      2.33 |       2.23 |
| 아야츠노 유니 |      2.31 |       2.15 |
| 텐코 시부키  |      2.27 |       2.2  |
| 아오쿠모 린  |      2.21 |       2.11 |


## 업로드 빈도 상위

```sql
SELECT name_ko AS 멤버, uploads_per_week AS 주간업로드,
       ROUND(shorts_share*100,0) AS 쇼츠비중_pct
FROM channel_metrics WHERE role='talent'
ORDER BY uploads_per_week DESC;
```

| 멤버      |   주간업로드 |   쇼츠비중_pct |
|:--------|--------:|-----------:|
| 텐코 시부키  |    5.91 |         34 |
| 하나코 나나  |    5.91 |         38 |
| 유즈하 리코  |    5.44 |         42 |
| 아카네 리제  |    5.36 |         38 |
| 아라하시 타비 |    4.9  |         18 |
| 시라유키 히나 |    3.99 |         30 |
| 아오쿠모 린  |    3.9  |         14 |
| 사키하네 후야 |    3.73 |         18 |
| 아야츠노 유니 |    2.88 |         10 |
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
| 아카네 리제  | 로스트원의 호곡 [ロストワンの号哭 / Neru]ㅣ아카네 리제(Akane Lize) 【COVER】      | 1898443 |
| 하나코 나나  | 오늘이 무슨 날이죠? #animation #shorts                             | 1333404 |
| 아오쿠모 린  | 불가행력 [不可幸力 / Vaundy ] / 아오쿠모 린 (Aokumo Rin) Cover          | 1303191 |
| 네네코 마시로 | 콧치노 켄토 - 네, 기꺼이 [はいよろこんで / こっちのけんと]ㅣ네네코 마시로 x 텐코 시부키 Cover | 1186855 |
| 텐코 시부키  | (소리주의) 붘몽가입니다 #vtuber #shorts #치이카와 #ちいかわ                  | 1067435 |
| 아라하시 타비 | 물떼새[ヨルシカ - 千鳥]ㅣ아라하시 타비 Cover                               |  949031 |
| 유즈하 리코  | 참을 수 없는 본능 #vtuber #shorts #스텔라이브 #리코 #용사툰                 |  783745 |
| 시라유키 히나 | 아틀란티스 소녀 (Atlantis Princess) | 시라유키 히나 Cover               |  694594 |
| 아야츠노 유니 | L을 가져가~ 크림 치즈 허니 #스텔라이브 #유니 #stellive #shorts              |  690357 |
| 사키하네 후야 | 푸른 산호초(青い珊瑚礁) - 松田 聖子 l 사키하네 후야(Sakihane Huya) Cover       |  642701 |

