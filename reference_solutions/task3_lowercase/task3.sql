select s.emp_no, first_name, last_name
FROM task3
INNER join (
    SELECT emp_no, avg(salary) avg_salary
    FROM salaries
    GROUP BY emp_no
) as s
ON task3.emp_no = s.emp_no
WHERE task3.dept_name="Research" && s.avg_salary>20000.00;

