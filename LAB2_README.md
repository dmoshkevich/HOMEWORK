## ЧАСТЬ 1
### 1. Cоздать несколько пользователей с паролями и шеллом
```
sudo useradd -d /home/Dir1 -s /path/to/shell user_1
sudo useradd -d /home/Dir2 -s /path/to/shell user_2
sudo useradd -d /home/Dir3 -s /path/to/shell user_3

sudo passwd user_1
sudo passwd user_2
sudo passwd user_3
```
### 2. Создать группу admin и включить туда пару пользователе и root
```
sudo groupadd admin
sudo usermod -aG admin user_1
sudo usermod -aG admin user_2
sudo usermod -aG admin root
```
### 3.Запретить всем пользователям, кроме группы admin, логин в систему по SSH в выходные дни (суббота и воскресенье, без учета праздников)
Установим pam_script:
```
sudo yum install pam pam_script openssh-server openssh-clients
```
Создадим скрипт для проверки пользователя
```
sudo nano /etc/pam_script_acct

#!bin/bash
script="$1"
shift

if groups $PAM_USER | grep admin > /dev/null
then
       exit 0
else
       if [[ $(date +%u) -lt 6 ]]
       then
               exit 0
       else
               exit 1
       fi
fi

if [ ! -e "$script" ]
then
       exit 0
fi
```
Тут нужно не забыть сделать файл исполняемым)
```
sudo chmod +x /etc/pam_script_acct
```
Занесем команду исполнения скрипта
```
sudo nano /etc/pam.d/sshd
После строки account    required     pam_nologin.so добавим: account    required     pam_script.so
```
Проверяем вход по ssh
ssh user_1@localhost
## ЧАСТЬ 2

### 4. Выдать пользователю право использовать докер
* Установим докер по [инструкции](https://docs.docker.com/engine/install/)
* Чтобы дать пользователю права работать с docker, добавим его в группу
```
sudo usermod -aG docker user_3
```
* Зайдем в пользователя и проверим версию docker
```
[dar@localhost etc]$ ssh user_3@localhost
The authenticity of host 'localhost (::1)' can't be established.
ECDSA key fingerprint is SHA256:3o1VvbYibCFgkKTWDSDNYXAJRtuPsmqw8dqTdd4Z0yI.
Are you sure you want to continue connecting (yes/no/[fingerprint])? y
Please type 'yes', 'no' or the fingerprint: yes
Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.
user_3@localhost's password: 
Permission denied, please try again.
user_3@localhost's password: 
Connection closed by ::1 port 22
[dar@localhost etc]$ docker --version
Docker version 19.03.13, build 4484c46d9d
[dar@localhost etc]$ 

```
