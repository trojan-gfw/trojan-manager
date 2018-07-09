# Trojan Manager

## Current Update (July 9, 2018)
- Basic user authentication functionality
- Basic user management
    - Adding users
    - Deleting users

## Software description

This is a module for trojan server, which enables users the ability to store and verify users from a database (MySQL only at the moment). It will, in the future, also support user data usage statistics and more.

## Usages

This software is currently still a stand-alone python software. It will be wrapped by the trojan software in the future by embedding the python into CPP code. You can view the current project as a PoC that can run like a RADIUS authenticator.

Installation

```bash
git clone https://github.com/trojan-gfw/trojan-manager.git
cd trojan-manager  # Enter directory
```

Basic usages

```bash
python3 trojan_manager.py add user pass  # add user to database
python3 trojan_manager.py delte user     # delete user from database
python3 verify hash                      # verify if credentials are valid
```


## Examples

### Setup MySQL Server

Create a database, a user and then grant privileges

```
CREATE DATABASE trojan;
CREATE USER trojan;
GRANT ALL ON trojan.* TO trojan@’localhost’ IDENTIFIED BY ‘thisisthetrojandbpassword’;
```

</br>

Create a table to store user credentials

```
CREATE TABLE trojan (username VARCHAR(64), password VARCHAR(256), fullhash VARCHAR(256));
```

</br>

Then you will need to adjust the settings in the python file if changes are needed. If you execute all commands above as is, then you won't have to touch a thing in the python file. In case of Exceptions, read the error message.

</br>

Add a user named "testuser" into the database with password "password"

```
python3 trojan_manager.py add testuser password
```

</br>

Delete a user named "testuser" from the database

```
python3 trojan_manager.py delete testuser password
```

</br>

Verify the user "testuser" with password "password". Passwords stored in the database are hashed by SHA512. The server is supposed to pass a hash in the format of SHA224(username + ":" + SHA512(password)). Verification is successful if the return value (output) is 0, 1 otherwise.

```
python3 trojan_manager.py verify 2ce06815404ac8189d03df019361ffc6bd814384dea53bc1a66d135f
```