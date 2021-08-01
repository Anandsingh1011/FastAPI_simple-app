import re
from fastapi import FastAPI
from fastapi import Path
from model import Employee
from mongoengine import connect
from fastapi import Query
from mongoengine.queryset.visitor import Q

import json
app = FastAPI()


connect(db="hrms", host="localhost",port=27017)

@app.get("/")
def home():
    return {"message":"Hello Anand"}

@app.get("/get_all_employee") 
def get_all_employee():
    employee = Employee.objects().to_json()
    employee_list =json.loads(employee)
    return {"employee":employee_list}

@app.get("/get_employee/{emp_id}")
def get_employee(emp_id: int = Path(...,gt=0)):
    employee = Employee.objects().get(emp_id=emp_id)
    employee_dict = {
        "emp_id" : employee.emp_id,
        "name": employee.name,
        "age": employee.age,
        "teams": employee.teams
    }

    return employee_dict



@app.get("/search_employee")
def search_employee(name : str ,age : int = Query(None,gt=18)):
    employee = json.loads(Employee.objects().filter(Q(name__icontains=name) | Q(age=age)).to_json())
    return {
        "employee" :employee
    }

from pydantic import BaseModel
from fastapi import Body

class NewEmployee(BaseModel):
    emp_id : int
    name : str
    age : int = Body(None, gt =18)
    teams : list

@app.post("/add_employee")
def add_employee(employee: NewEmployee):
    new_employee =  Employee(emp_id = employee.emp_id,
        name = employee.name,
        age = employee.age,
        teams = employee.teams)

    new_employee.save()

    return {"message": "Employee added successfully"}
    