select d.department_name, e.employee_id, e.first_name, last_name,rank() over (partition by e.department_id order by e.salary desc) as rank,
 salary-lead(salary) over (partition by e.department_id order by e.salary desc) as sal_diff
from employees e
left join departments d on e.department_id=department_id
where rank = 1