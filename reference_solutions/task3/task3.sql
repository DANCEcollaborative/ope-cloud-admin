/* This is the your final query of Task2

 Important!!
 Put your optimized query which contains all the required fields (DO NOT use COUNT(*) in the final query).
 Replace "Your query" below with your final query.*/

-- CREATE TABLE tt AS
-- (SELECT t.emp_no, t.title, e.first_name, e.last_name from titles t INNER JOIN employees e ON e.emp_no = t.emp_no 
-- );

/* create index title_emp_ind on title_emp (title);*/

select s.emp_no, tt.first_name, tt.last_name FROM task3 tt INNER join (SELECT emp_no, avg(salary) avg_salary FROM salaries GROUP BY emp_no ) s ON tt.emp_no = s.emp_no WHERE tt.dept_name="Research" && s.avg_salary>20000.00;