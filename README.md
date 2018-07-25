# Trojan Manager

## Current Update (Version 1.3.5, July 25, 2018)

- Main thread catches MySQL connection exceptions

## Software Description

This is a module for trojan server, which enables users the ability to store and verify users from a database (MySQL only at the moment). It will, in the future, also support user data usage statistics and more.

![trojan-manager](https://user-images.githubusercontent.com/21986859/42651139-7d7692fa-85dc-11e8-83aa-12f6a4fad173.png)

## Usages

The arguments will be passed onto the command interpreter. The first command line argument will be the first command. Vice versa.

### Installation

```bash
git clone https://github.com/trojan-gfw/trojan-manager.git
cd trojan-manager  # Enter directory
pip3 install -r requirements.txt  # Install python packages
```

### Pass arguments directly from command line

```bash
python3 trojan_manager.py adduser user pass  # add user to database
python3 trojan_manager.py deluser user       # delete user from database
python3 verify hash                          # verify if credentials are valid
```

### Using interactive shell

```bash
python3 trojan_manager interactive  # Enter interactive shell
python3 trojan_manager int          # A shorter version
[trojan]> adduser user pass
[trojan]> deluser user
[trojan]> verify hash
```

### Interactive Shell

The trojan manager interactive shell is an interface that can simplify trojan manager operations. Available commands can be listed with `Help` command. The interactive shell interpreter is **NOT case sensitive**, similar to SoftEther vpncmd.

## More Examples

### Setup MySQL Server

The database must be created manually, where the tables can be created automatically by trojan manager. To create a database, a user and then grant privileges, use the following commands in MySQL with root privilege.

```sql
CREATE DATABASE trojan;
CREATE USER trojan;
GRANT ALL ON trojan.* TO trojan@'localhost' IDENTIFIED BY 'thisisthetrojandbpassword';
```

Trojan Manager can create a table to store user information automatically. Simply use `CreateUserTable` to create the table automatically.

```bash
python3 trojan_manager.py createusertable
[trojan]> createusertable
```

Alternatively, you can also create the table manually.

```sql
use trojan;

CREATE TABLE users (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    username VARCHAR(64) NOT NULL,
    password CHAR(56) NOT NULL,
    quota BIGINT NOT NULL DEFAULT 0,
    download BIGINT UNSIGNED NOT NULL DEFAULT 0,
    upload BIGINT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    INDEX (password)
);
```

### User Management

Then you will need to adjust the settings in the python file if changes are needed. If you execute all commands above as is, then you won't have to touch a thing in the python file. In case of Exceptions, read the error message.

Now you have finished setting up the database, you may perform user management operations. You can now add or delete users, set user quota and so on. For full help page please use `Help` command in trojan manager.

### Trojan Authentication

Verify the user "testuser" with password "password". The server is supposed to pass a hash in the format of SHA224(username + ":" + password). Verification is successful if the return value (output) is 0, 1 otherwise.

```bash
python3 trojan_manager.py verify 75a47a2c85e939b3c92cb5c657b7ded4669243c1bfdf4cf812739a0d
```

For more information on trojan's authentication mechanism, please refer to [Trojan Authenticator](https://trojan-gfw.github.io/trojan/authenticator) Page.
