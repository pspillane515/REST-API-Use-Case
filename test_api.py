import requests

URL = "https://rest-api-use-case.onrender.com/"
TASK = "task"
TODOLIST = "todolist"
CATEGORY = "category"
USER = "user"

def construct_url(common_url, api):
    return common_url + api

user1 = "user1"
user2 = "user2"
pw = "1234"

# User Operations

def register(user, password):
    url = construct_url(URL, "register")
    response = requests.post(url, json={"username": user, "password": password})
    return response.text

def login(user, password):
    url = construct_url(URL, "login")
    response = requests.post(url, json={"username": user, "password": password})
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        return access_token
    return response.text

def logout(user, password, access_token):
    url = construct_url(URL, "logout")
    response = requests.post(url, headers={"Authorization": f"Bearer {access_token}"}, json={"username": user, "password": password})
    return response.text

def delete_user(user_id):
    url = construct_url(URL, USER) + f"/{user_id}"
    response = requests.delete(url)
    return response.text

def get_user(user_id):
    url = construct_url(URL, USER) + f"/{user_id}"
    response = requests.get(url)
    return response.text

print("################ USER OPERATIONS ################\n")
print(f"REGISTER USER1: {register(user1, pw)}")
print(f"GET USER1: {get_user(user_id=1)}")
token = login(user1, pw)
print(f"LOGIN USER1: access_token: {token} \n")
print(f"FAILED LOGIN: {login(user1, 'wrong-password')}")
print(f"REGISTER USER2: {register(user2, pw)}")
print(f"GET USER2: {get_user(user_id=2)}")
print(f"DELETE USER2: {delete_user(2)}")
print(f"GET USER2: {get_user(user_id=2)}")
print(f"REREGISTER USER2: {register(user2, pw)}")

print("\n#####################################################\n")
# Todo List Operations

def get_all_todolist():
    url = construct_url(URL, TODOLIST)
    response = requests.get(url)
    return response.text

def get_todolist(todolist_id, access_token):
    url = construct_url(URL, TODOLIST) + f"/{todolist_id}"
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    return response.text

def create_todolist(name, user_id, access_token):
    url = construct_url(URL, TODOLIST)
    response = requests.post(url, headers={"Authorization": f"Bearer {access_token}"}, json={"name": name, "user_id": user_id})
    return response.text

def delete_todolist(todolist_id, access_token):
    url = construct_url(URL, TODOLIST) + f"/{todolist_id}"
    response = requests.delete(url, headers={"Authorization": f"Bearer {access_token}"})
    return response.text

def update_todolist(todolist_id, access_token, name, user_id):
    url = construct_url(URL, TODOLIST) + f"/{todolist_id}"
    response = requests.put(url, headers={"Authorization": f"Bearer {access_token}"}, json={"name": name, "user_id": user_id})
    return response.text
    
user1_todolist_id = 1
user2_todolist_id = 3

token = login(user1, pw)

print("################ TODOLIST OPERATIONS ################\n")
print(f"GET ALL TODOLIST (BEFORE CREATION): {get_all_todolist()}")
print(f"CREATE TODOLIST USER1: {create_todolist(name='User 1 To-do List', user_id=1, access_token=token)}")
print(f"GET SPECIFIC TODOLIST: {get_todolist(todolist_id=user1_todolist_id, access_token=login(user1, pw))}")

print(f"LOGOUT USER1: {logout(user=user1, password=pw, access_token=token)}")
print(f"GET SPECIFIC TODOLIST: {get_todolist(todolist_id=user1_todolist_id, access_token=token)}")

token = login(user1, pw)

print(f"ATTEMPT SECOND CREATE TODOLIST USER1: {create_todolist(name='User 1 To-do List 2?', user_id=1, access_token=token)}")
print(f"UPDATE TODOLIST: {update_todolist(todolist_id=user1_todolist_id, access_token=login(user1, pw), name='User 1 New To-do List', user_id=1)}")

print(f"ATTEMPT CREATE TODOLIST USER2: {create_todolist(name='User 2 To-do List?', user_id=3, access_token=token)}")

token = login(user2, pw)
print(f"LOGIN USER2 AND CREATE TODOLIST: {create_todolist(name='User 2 To-do List', user_id=3, access_token=token)}")
print(f"ATTEMPT TO ACCESS USER1 TODOLIST: {get_todolist(todolist_id=user1_todolist_id, access_token=token)}")

print(f"DELETE TODOLIST: {delete_todolist(todolist_id=user2_todolist_id, access_token=token)}")
print("\n#################################################\n")

# Task Operations

def get_all_tasks(access_token):
    url = construct_url(URL, TASK)
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    return response.text

def get_task(task_id, access_token):
    url = construct_url(URL, TASK) + f"/{task_id}"
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    return response.text

def create_task(name, details, completed, todolist_id, access_token):
    url = construct_url(URL, TASK)
    response = requests.post(url, headers={"Authorization": f"Bearer {access_token}"}, json={
        "name": name, "details": details, "completed": completed, "todolist_id": todolist_id})
    return response.text

def delete_task(task_id, access_token):
    url = construct_url(URL, TASK) + f"/{task_id}"
    response = requests.delete(url, headers={"Authorization": f"Bearer {access_token}"})
    return response.text

def update_task(task_id, access_token, name, details, completed, todolist_id):
    url = construct_url(URL, TASK) + f"/{task_id}"
    response = requests.put(url, headers={"Authorization": f"Bearer {access_token}"}, json={
        "name": name, "details": details, "completed": completed, "todolist_id": todolist_id})
    return response.text


print("################ TASK OPERATIONS ################\n")
token = login(user1, pw)

print(f"GET ALL TASKS (BEFORE CREATION): {get_all_tasks(access_token=token)}")

first_task = create_task(name='First Task', details='My Details', completed=False, todolist_id=user1_todolist_id, access_token=token)
print(f"CREATE TASK: {first_task}")

print(f"GET SPECIFIC TASK: {get_task(task_id=1, access_token=login(user1, pw))}")
print(f"GET SPECIFIC TASK (UNKNOWN ID): {get_task(task_id=10, access_token=login(user1, pw))}")

print(f"CREATE TASK 2: {create_task(name='Second Task', details='My Second Details', completed=False, todolist_id=user1_todolist_id, access_token=token)}")
print(f"GET ALL TASKS: {get_all_tasks(access_token=token)}")

print(f"DELETE TASK: {delete_task(task_id=2, access_token=login(user1, pw))}")
print(f"GET ALL TASKS: {get_all_tasks(access_token=token)}")

print(f"UPDATE TASK: {update_task(task_id=1, access_token=token, name='First Task EDIT', details='My Details EDIT', completed=True, todolist_id=user1_todolist_id)}")
print("\n#####################################################\n")

# Category Operations

def get_category(category_id):
    url = construct_url(URL, CATEGORY) + f"/{category_id}"
    response = requests.get(url)
    return response.text

def get_categories_from_list(todolist_id):
    url = construct_url(URL, TODOLIST) + f"/{todolist_id}/{CATEGORY}"
    response = requests.get(url)
    return response.text

def create_category(name, todolist_id):
    url = construct_url(URL, TODOLIST) + f"/{todolist_id}/{CATEGORY}"
    response = requests.post(url, json={"name": name})
    return response.text

def assign_category(task_id, category_id, access_token):
    url = construct_url(URL, TASK) + f"/{task_id}/{CATEGORY}/{category_id}"
    response = requests.post(url, headers={"Authorization": f"Bearer {access_token}"})
    return response.text

def delete_category(category_id):
    url = construct_url(URL, CATEGORY) + f"/{category_id}"
    response = requests.delete(url)
    return response.text

def remove_task_from_category(task_id, category_id):
    url = construct_url(URL, TASK) + f"/{task_id}/{CATEGORY}/{category_id}"
    response = requests.delete(url)
    return response.text


print("################ CATEGORY OPERATIONS ################\n")
token = login(user1, pw)

print(f"GET ALL CATEGORIES OF LIST (BEFORE CREATION): {get_categories_from_list(todolist_id=user1_todolist_id)}")

first_category = create_category(name='First Category', todolist_id=user1_todolist_id)
print(f"CREATE CATEGORY: {first_category}")

print(f"GET SPECIFIC CATEGORY: {get_category(category_id=1)}")
print(f"GET SPECIFIC CATEGORY (DOESN'T EXIST): {get_category(category_id=2)}")


print(f"CREATE CATEGORY 2: {create_category(name='Second Category', todolist_id=user1_todolist_id)}")
print(f"GET ALL CATEGORIES OF LIST: {get_categories_from_list(todolist_id=user1_todolist_id)}")

print(f"ASSIGN CATEGORY: {assign_category(task_id=1, category_id=1, access_token=token)}")
print(f"GET TODOLIST: {get_todolist(todolist_id=user1_todolist_id, access_token=token)}")

print(f"DELETE CATEGORY (WHILE ASSIGNED TO TASK): {delete_category(category_id=1)}")
print(f"REMOVE TASK FROM CATEGORY: {remove_task_from_category(task_id=1, category_id=1)}")
print(f"DELETE CATEGORY: {delete_category(category_id=1)}")
print(f"GET ALL CATEGORIES OF LIST: {get_categories_from_list(todolist_id=user1_todolist_id)}")
print("\n##############################################\n")