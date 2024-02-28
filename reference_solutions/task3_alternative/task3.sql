select s.emp_no, tt.first_name, tt.last_name
FROM task3 as tt
INNER join (SELECT emp_no, avg(salary) avg_salary FROM salaries GROUP BY emp_no ) as s
ON tt.emp_no = s.emp_no WHERE tt.dept_name="Research" && s.avg_salary>20000.00;