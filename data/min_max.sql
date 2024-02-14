with grocery_stores_open_close as (
    select cid, day,
           percentile_disc(0) WITHIN GROUP (ORDER BY hour_idx) as opening_hour_idx,
           percentile_disc(0) WITHIN GROUP (ORDER BY hour_idx desc) as closing_hour_idx
    from grocery_stores_geom
    where popularity > 0
    group by cid, day
), grocery_stores_prev_next as (
    select gs.cid, gs.day, gs.hour_idx,
           LAG (popularity, 1) OVER (PARTITION BY cid, day ORDER BY hour_idx) prev_popularity,
           gs.popularity,
           LEAD (popularity, 1) OVER (PARTITION BY cid, day ORDER BY hour_idx) next_popularity
    from grocery_stores_geom gs
      natural inner join grocery_stores_open_close gsoc
    where gs.hour_idx between opening_hour_idx and closing_hour_idx
    order by cid, day, hour_idx
), gs_distinct as (
    select *
    from grocery_stores_prev_next gspn
    where popularity <> prev_popularity
       or prev_popularity is null
    order by cid, day, hour_idx
), gs_distinct_middles as (
    select cid, day,
           case when next_hour_idx is null then hour_idx
                when hour_idx = next_hour_idx - 1 then hour_idx
                else ceil((hour_idx + next_hour_idx - 1) / 2)
           end as hour_idx,
           popularity
    from (
        select cid, day, hour_idx, popularity,
              LEAD(hour_idx, 1) OVER (PARTITION BY cid, day ORDER BY hour_idx) next_hour_idx
        from gs_distinct gsnd
    ) t
), gs_local_min_max as (
select cid, day, hour_idx, popularity,
       case when ((prev_popularity is null or prev_popularity < popularity) and (next_popularity is null or popularity > next_popularity)) then '1'
            when ((prev_popularity is null or prev_popularity > popularity) and (next_popularity is null or popularity < next_popularity)) then '0'
       end as min_max
from (
    select cid, day, hour_idx,
       LAG (popularity, 1) OVER (PARTITION BY cid, day ORDER BY hour_idx) prev_popularity,
       popularity,
       LEAD (popularity, 1) OVER (PARTITION BY cid, day ORDER BY hour_idx) next_popularity
    from gs_distinct_middles
) t
), min_max_counts as (
select cid, day, count(*) cnt
from gs_local_min_max
where min_max is not null
group by cid, day
)
select cnt, count(*)
from min_max_counts
group by cnt
;
/*
2    11
3   337
4    63
5   849
6    58
7   106
8     3
9     1


1:
14433167278338911051,5,1 = 0-50-79-79-0
3544845922796547178,6,1 = 0-52-50-0
3798113314494586043,5,1 = 0-54-31-0
7313588904948400386,5,1 = 0-64-67-47-0
9535695463037162315,6,1 = 0-46-57-0

9:
4817342681680620522,4,9 = 0-9-9-9-4-0-0-9-9-19-23-23-23-19-14-9-14-47-14-0-4-4-4-4-0
 */

select *
from grocery_stores_geom
where cid = '4817342681680620522'
  and day = 4
;
