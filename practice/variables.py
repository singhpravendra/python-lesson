name='Pravendra'
department='Tech'
age=31
role='Software Engineer'
emp_id='FBS7077'
salary=10000
monthly_expense=salary/12
print(f"Name: {name}")
print(f"Department: {department}")
print(f"Age: {age}")
print(f"Role: {role}")
print(f"Employee ID: {emp_id}")
print(f"Salary: {salary}")
print(f"Monthly Expense: {monthly_expense}")

print(f"Type of name: {type(name)}")
print(f"Type of department: {type(department)}")
print(f"Type of age: {type(age)}")
print(f"Type of role: {type(role)}")
print(f"Type of emp_id: {type(emp_id)}")
print(f"Type of salary: {type(salary)}")
print(f"Type of monthly_expense: {type(monthly_expense)}")

compete_details=f"""
Name: {name * 2 }
Department: {department}
Age: {age}
Role: {role}
Employee ID: {emp_id}
Salary: {salary}
Monthly Expense: {monthly_expense}
"""
print(compete_details)