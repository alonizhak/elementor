with site_total_on_promotions as (
select s.site, sum(s.numberof_visitors) as tot_visitors_on_promotions
from site_visitors s
join promotions p
on s.site = p.site and s.date between p.start_date and p.end_date
group by )


with site_total_vistors as (

    select site, sum(numberof_visitors) as tot_num_of_visitors
    from site_visitors s
    group by 1
)

select site, 100.0*(case (when tot_visitors_on_promotions is null then tot_num_of_visitors 
    else tot_visitors_on_promotions))/ (numberof_visitors) as trafic_perc
from site_total_vistors t
left join site_total_on_promotions p
group by 1

