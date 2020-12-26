## ЧАСТЬ 1
### 1. Cоздать несколько пользователей с паролями и шеллом
```
sudo useradd -p password -s /bin/bash user_1
sudo useradd -p password -s /bin/bash user_2
sudo useradd -p password -s /bin/bash user_3
```
### 2. Создать группу admin и включить туда пару пользователе и root
```
sudo groupadd admin
sudo usermod -aG admin user_1
sudo usermod -aG admin user_1
sudo usermod -aG admin root
```
### 3.Запретить всем пользователям, кроме группы admin, логин в систему по SSH в выходные дни (суббота и воскресенье, без учета праздников)
Установим pam_script:
```
sudo apt install libpam-script
```
Создадим скрипт для проверки пользователя
```
sudo vim /usr/share/libpam-script/pam_script_acct

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
sudo chmod +x /usr/share/libpam-script/pam_script_acct
```
Занесем команду исполнения скрипта
```
sudo vim /etc/pam.d/sshd
После строки : account    required     pam_nologin.so
Добавим: account    required     pam_script.so
```
Проверяем вход по ssh
ssh user_1@localhost
## ЧАСТЬ 2

### 4. Выдать пользователю право использовать докер
* Установим докер по [инструкции](https://docs.docker.com/engine/install/)
* Чтобы дать пользователю права работать с docker, добавим его в группу
```
sudo usermod -aG docker victim1
```
* Зайдем в пользователя и проверим версию docker
```
ssh user_3@localhost
docker --version
```
