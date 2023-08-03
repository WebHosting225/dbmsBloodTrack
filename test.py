import database as db


# 1. Create a new user
def create():
    db.users.add({
        "username": "test",
        "password": "test",
        "fullName": "test",
        "age": 20,
        "bloodGrp": "A+",
        "email": "test@test.com",
        "phoneNo": "1234567890",
    })


# 2. Read a user
def read():
    user = db.users.where("username", "==", "test").get()
    print(user)


# 3. Update a user
def update():
    user = db.users.where("username", "==", "test").get()[0]
    db.users.document(user.id).update({
        "fullName": "test1",
        "age": 21,
        "email": "test1@test.com",
        "phoneNo": "1234567891",
    })


# 4. Delete a user
def delete():
    user = db.users.where("username", "==", "test").get()[0]
    db.users.document(user.id).delete()


# 5. Add Bank
def addBank():
    user = db.users.where("username", "==", "test").get()[0]
    db.banks.add({
        "user": user.reference,
        "qnty": 100,
        "req": "blood",
        "bloodGrp": "B+",
        "donor": None,
        "for": {
            "fullName": user.get("fullName"),
            "age": user.get("age"),
            "email": user.get("email"),
            "phone": user.get("phoneNo"),
        }
    })


# 6. List Banks
def listBanks():
    user = db.users.where("username", "==", "test").get()[0]
    banks = db.banks.where("user", "!=", user.reference)
    items = list(map(lambda x: {**x.to_dict(), 'id': x.id}, banks.get()))
    print(items)
