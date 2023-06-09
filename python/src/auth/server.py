import jwt
import datetime
import os
from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

print("MYSQL_HOST: ", os.environ.get("MYSQL_HOST"))
print("MYSQL_USER: ", os.environ.get("MYSQL_USER"))
print("MYSQL_PASSWORD: ", os.environ.get("MYSQL_PASSWORD"))
print("MYSQL_DB: ", os.environ.get("MYSQL_DB"))
print("MYSQL_PORT: ", os.environ.get("MYSQL_PORT"))


@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401

    # check db for username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        " SELECT email, password FROM users WHERE email = %s AND password = %s ", (auth.username, auth.password))

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        # create token
        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid credentials", 401

@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers.get("Authorization")

    if not encoded_jwt:
        return "missing token", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
    except:
        return "not authorized", 403
    
    return decoded, 200


# create JWT
def createJWT(username, secret, is_admin):
    payload = {
        "username": username,
        "is_admin": is_admin,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow()
    }
    return jwt.encode(payload, secret, algorithm="HS256")

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000, debug=True)

# export MYSQL_HOST= localhost
# export MYSQL_USER= auth_user
# export MYSQL_PASSWORD= strong_password
# export MYSQL_DB= auth
# export MYSQL_PORT= 3306