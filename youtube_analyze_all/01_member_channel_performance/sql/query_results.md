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
|    1 | 아카네 리제  | UNIVERSE | 378000 |    366993 |
|    2 | 아야츠노 유니 | EVERYS   | 376000 |    175635 |
|    3 | 시라유키 히나 | UNIVERSE | 334000 |    182936 |
|    4 | 아오쿠모 린  | CLICHE   | 305000 |    236294 |
|    5 | 아라하시 타비 | UNIVERSE | 279000 |    281679 |
|    6 | 텐코 시부키  | CLICHE   | 247000 |    304799 |
|    7 | 유즈하 리코  | CLICHE   | 242000 |    286072 |
|    8 | 하나코 나나  | CLICHE   | 227000 |    298022 |
|    9 | 네네코 마시로 | UNIVERSE | 200000 |    138773 |
|   10 | 사키하네 후야 | EVERYS   | 154000 |    136374 |


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
| 하나코 나나  | 227000 |  298022 |      131.3 |
| 텐코 시부키  | 247000 |  304799 |      123.4 |
| 유즈하 리코  | 242000 |  286072 |      118.2 |
| 아라하시 타비 | 279000 |  281679 |      101   |
| 아카네 리제  | 378000 |  366993 |       97.1 |
| 사키하네 후야 | 154000 |  136374 |       88.6 |
| 아오쿠모 린  | 305000 |  236294 |       77.5 |
| 네네코 마시로 | 200000 |  138773 |       69.4 |
| 시라유키 히나 | 334000 |  182936 |       54.8 |
| 아야츠노 유니 | 376000 |  175635 |       46.7 |


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
| UNIVERSE |    4 |  297750 |  242595 |        2.75 |
| EVERYS   |    2 |  265000 |  156004 |        2.93 |
| CLICHE   |    4 |  255250 |  281296 |        2.47 |


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
| 네네코 마시로 |      3.46 |       3.27 |
| 사키하네 후야 |      3.35 |       3.22 |
| 시라유키 히나 |      3.01 |       2.86 |
| 유즈하 리코  |      2.87 |       2.76 |
| 아야츠노 유니 |      2.51 |       2.36 |
| 아오쿠모 린  |      2.41 |       2.3  |
| 하나코 나나  |      2.36 |       2.29 |
| 아카네 리제  |      2.31 |       2.24 |
| 텐코 시부키  |      2.23 |       2.17 |
| 아라하시 타비 |      2.21 |       2.11 |


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
| 아카네 리제  |    5.36 |         38 |
| 유즈하 리코  |    5.28 |         42 |
| 아라하시 타비 |    4.7  |         14 |
| 아오쿠모 린  |    4.04 |         16 |
| 사키하네 후야 |    3.69 |         24 |
| 시라유키 히나 |    3.61 |         34 |
| 아야츠노 유니 |    2.88 |         14 |
| 네네코 마시로 |    2.38 |          8 |


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
| 유즈하 리코  | 오늘 나는 찌그러진 클리셰가 될 거야 #vtuber #shorts #리코 #스텔라이브 #챌린지 #meme | 1286540 |
| 아라하시 타비 | High Hopes - Panic! At The Discoㅣ아라하시 타비 Cover                        | 1201818 |
| 아오쿠모 린  | 불가행력 [不可幸力 / Vaundy ] / 아오쿠모 린 (Aokumo Rin) Cover                     | 1169532 |
| 네네코 마시로 | 콧치노 켄토 - 네, 기꺼이 [はいよろこんで / こっちのけんと]ㅣ네네코 마시로 x 텐코 시부키 Cover            | 1140998 |
| 하나코 나나  | 오늘이 무슨 날이죠? #animation #shorts                                        | 1103042 |
| 텐코 시부키  | (소리주의) 붘몽가입니다 #vtuber #shorts #치이카와 #ちいかわ                             |  975174 |
| 아카네 리제  | 픽셀 병약 담당 vs 스텔 병약 담당                                                  |  839514 |
| 아야츠노 유니 | 아 르 냥 일 어 나 🕗 !! #stellive #스텔라이브 #유니 #알람                             |  711823 |
| 시라유키 히나 | 아틀란티스 소녀 (Atlantis Princess) | 시라유키 히나 Cover                          |  665501 |
| 사키하네 후야 | 푸른 산호초(青い珊瑚礁) - 松田 聖子 l 사키하네 후야(Sakihane Huya) Cover                  |  598818 |

