### 1. Создание своего RPM пакета
Установим необходимые компоненты
```
yum install -y redhat-lsb-core wget rpmdevtools rpm-build createrepo yum-utils
```
Установим пакет с источником с оффициального сайта nginx
```
[dar@localhost /]$ sudo wget https://nginx.org/packages/centos/7/SRPMS/nginx-1.18.0-2.el7.ngx.src.rpm
--2020-12-26 00:20:27--  https://nginx.org/packages/centos/7/SRPMS/nginx-1.18.0-2.el7.ngx.src.rpm
Распознаётся nginx.org (nginx.org)... 3.125.197.172, 52.58.199.22, 2a05:d014:edb:5702::6, ...
Подключение к nginx.org (nginx.org)|3.125.197.172|:443... соединение установлено.
HTTP-запрос отправлен. Ожидание ответа... 200 OK
Длина: 1055846 (1,0M) [application/x-redhat-package-manager]
Сохранение в: «nginx-1.18.0-2.el7.ngx.src.rpm»
100%[=========================================================================================================================================================================>] 1 055 846   2,67MB/s   за 0,4s   
2020-12-26 00:20:28 (2,67 MB/s) - «nginx-1.18.0-2.el7.ngx.src.rpm» сохранён [1055846/1055846]
[dar@localhost /]$ ls -l | grep nginx
-rw-r--r--. 1 root          root          1055846 окт 29 18:35 nginx-1.18.0-2.el7.ngx.src.rpm
```
Повторим для OpenSSL
```
[dar@localhost ~]$ sudo wget https://www.openssl.org/source/latest.tar.gz
--2020-12-26 01:00:56--  https://www.openssl.org/source/latest.tar.gz
Распознаётся www.openssl.org (www.openssl.org)... 2a02:26f0:1200:3b4::c1e, 2a02:26f0:1200:39f::c1e
Подключение к www.openssl.org (www.openssl.org)|2a02:26f0:1200:3b4::c1e|:443... ошибка: Сеть недоступна.
Подключение к www.openssl.org (www.openssl.org)|2a02:26f0:1200:39f::c1e|:443... ошибка: Сеть недоступна.
[dar@localhost ~]$ sudo wget https://www.openssl.org/source/latest.tar.gz
--2020-12-26 01:00:57--  https://www.openssl.org/source/latest.tar.gz
Распознаётся www.openssl.org (www.openssl.org)... 23.13.40.208, 2a02:26f0:1200:3b4::c1e, 2a02:26f0:1200:39f::c1e
Подключение к www.openssl.org (www.openssl.org)|23.13.40.208|:443... соединение установлено.
HTTP-запрос отправлен. Ожидание ответа... 302 Moved Temporarily
Адрес: https://www.openssl.org/source/openssl-1.1.1i.tar.gz [переход]
--2020-12-26 01:00:59--  https://www.openssl.org/source/openssl-1.1.1i.tar.gz
Повторное использование соединения с www.openssl.org:443.
HTTP-запрос отправлен. Ожидание ответа... 200 OK
Длина: 9808346 (9,4M) [application/x-gzip]
Сохранение в: «latest.tar.gz»

100%[=========================================================================================================================================================================>] 9 808 346   10,2MB/s   за 0,9s   

2020-12-26 01:01:06 (10,1 MB/s) - «latest.tar.gz» сохранён [9808346/9808346]
```
Ставим необходимые зависимости
```
[dar@localhost ~]# sudo yum-builddep rpmbuild/SPECS/nginx.spec

Установлено:
  openssl-devel.x86_64 1:1.0.2k-21.el7_9                                    pcre-devel.x86_64 0:8.32-17.el7                                    zlib-devel.x86_64 0:1.2.7-18.el7                                   

Установлены зависимости:
  keyutils-libs-devel.x86_64 0:1.5.8-3.el7     krb5-devel.x86_64 0:1.15.1-50.el7     libcom_err-devel.x86_64 0:1.42.9-19.el7     libselinux-devel.x86_64 0:2.5-15.el7     libsepol-devel.x86_64 0:2.5-10.el7    
  libverto-devel.x86_64 0:0.2.5-4.el7         

Обновлены зависимости:
  e2fsprogs.x86_64 0:1.42.9-19.el7       e2fsprogs-libs.x86_64 0:1.42.9-19.el7       krb5-libs.x86_64 0:1.15.1-50.el7       krb5-workstation.x86_64 0:1.15.1-50.el7       libcom_err.x86_64 0:1.42.9-19.el7      
  libkadm5.x86_64 0:1.15.1-50.el7        libss.x86_64 0:1.42.9-19.el7                openssl.x86_64 1:1.0.2k-21.el7_9       openssl-libs.x86_64 1:1.0.2k-21.el7_9        

Выполнено!
```
Правим файл nginx.spec

```
[dar@localhost ~]# sudo nano rpmbuild/SPECS/nginx.spec

%build
./configure %{BASE_CONFIGURE_ARGS} \
    --with-cc-opt="%{WITH_CC_OPT}" \
    --with-ld-opt="%{WITH_LD_OPT}" \
    --with-openssl=/root/openssl-1.1.1i \
    --with-debug
```
Собираем пакет
```
[dart@localhost ~]# sudo rpmbuild -bb rpmbuild/SPECS/nginx.spec
Выполняется(%prep): /bin/sh -e /var/tmp/rpm-tmp.OmVqti
+ umask 022
+ cd /root/rpmbuild/BUILD
+ cd /root/rpmbuild/BUILD
+ rm -rf nginx-1.18.0
+ /usr/bin/gzip -dc /root/rpmbuild/SOURCES/nginx-1.18.0.tar.gz
...
Записан: /root/rpmbuild/RPMS/x86_64/nginx-1.18.0-2.el7.ngx.x86_64.rpm
Записан: /root/rpmbuild/RPMS/x86_64/nginx-debuginfo-1.18.0-2.el7.ngx.x86_64.rpm
Выполняется(%clean): /bin/sh -e /var/tmp/rpm-tmp.OUatwG
+ umask 022
+ cd /root/rpmbuild/BUILD
+ cd nginx-1.18.0
+ /usr/bin/rm -rf /root/rpmbuild/BUILDROOT/nginx-1.18.0-2.el7.ngx.x86_64
+ exit 0
```
Проверим сборку 
```
[dar@localhost ~]# ls -la rpmbuild/RPMS/x86_64/
итого 2516
drwxr-xr-x. 2 root root      98 дек 21 02:54 .
drwxr-xr-x. 3 root root      20 дек 21 02:54 ..
-rw-r--r--. 1 root root  786404 дек 21 02:54 nginx-1.18.0-2.el7.ngx.x86_64.rpm
-rw-r--r--. 1 root root 1789388 дек 21 02:54 nginx-debuginfo-1.18.0-2.el7.ngx.x86_64.rpm
```
Установим наш пакет 
```
[dar@localhost ~]# sudo yum localinstall -y rpmbuild/RPMS/x86_64/nginx-1.18.0-2.el7.ngx.x86_64.rpm
Загружены модули: fastestmirror, langpacks, product-id, search-disabled-repos, subscription-manager
Проверка rpmbuild/RPMS/x86_64/nginx-1.18.0-2.el7.ngx.x86_64.rpm: 1:nginx-1.18.0-2.el7.ngx.x86_64
rpmbuild/RPMS/x86_64/nginx-1.18.0-2.el7.ngx.x86_64.rpm отмечен как обновление для 1:nginx-1.16.1-2.el7.x86_64
Разрешение зависимостей
--> Проверка сценария
---> Пакет nginx.x86_64 1:1.16.1-2.el7 помечен для обновления
---> Пакет nginx.x86_64 1:1.18.0-2.el7.ngx помечен как обновление
--> Проверка зависимостей окончена
Зависимости определены
==============================================================================================================================================================================
 Package                                  Архитектура                               Версия                                                 Репозиторий                                                       Размер
==============================================================================================================================================================================
Обновление:
 nginx                                    x86_64                                    1:1.18.0-2.el7.ngx                                     /nginx-1.18.0-2.el7.ngx.x86_64                                    2.7 M
Итого за операцию
==============================================================================================================================================================================
Обновить  1 пакет
Общий размер: 2.7 M
Downloading packages:
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Обновление  : 1:nginx-1.18.0-2.el7.ngx.x86_64                                                                                                                                                                1/2 
предупреждение: /etc/nginx/nginx.conf создан как /etc/nginx/nginx.conf.rpmnew
  Очистка     : 1:nginx-1.16.1-2.el7.x86_64                                                                                                                                                                    2/2 
  Проверка    : 1:nginx-1.18.0-2.el7.ngx.x86_64                                                                                                                                                                1/2 
  Проверка    : 1:nginx-1.16.1-2.el7.x86_64                                                                                                                                                                    2/2 
Обновлено:
  nginx.x86_64 1:1.18.0-2.el7.ngx                                                                                                                                             
Выполнено!
```
### 2.Создать репозиторий и загрузить туда rpm пакет
Создадим папку с пакетами
```
[dar@localhost ~]# sudo mkdir /usr/share/nginx/html/repo
[dar@localhost ~]# sudo cp rpmbuild/RPMS/x86_64/nginx-1.18.0-2.el7.ngx.x86_64.rpm /usr/share/nginx/html/repo/
[dar@localhost ~]# sudo wget https://repo.percona.com/centos/7Server/RPMS/noarch/percona-release-1.0-9.noarch.rpm -O /usr/share/nginx/html/repo/percona-release-1.0-9.noarch.rpm
--2020-12-26 02:42:02--  https://repo.percona.com/centos/7Server/RPMS/noarch/percona-release-1.0-9.noarch.rpm
Распознаётся repo.percona.com (repo.percona.com)... 157.245.68.135
Подключение к repo.percona.com (repo.percona.com)|157.245.68.135|:443... соединение установлено.
HTTP-запрос отправлен. Ожидание ответа... 200 OK
Длина: нет данных [application/x-redhat-package-manager]
Сохранение в: «/usr/share/nginx/html/repo/percona-release-1.0-9.noarch.rpm»
    [ <=>                                                                                                                                                                      ] 16 664      --.-K/s   за 0s      
2020-12-26 02:42:15 (175 MB/s) - «/usr/share/nginx/html/repo/percona-release-1.0-9.noarch.rpm» сохранён [16664]
```
Инициализируем репозиторий 
```
[dar@localhost ~]# createrepo /usr/share/nginx/html/repo/
Spawning worker 0 with 1 pkgs
Spawning worker 1 with 1 pkgs
Workers Finished
Saving Primary metadata
Saving file lists metadata
Saving other metadata
Generating sqlite DBs
Sqlite DBs complete
```
Добавим автоиндексирование в файл nginx.conf
```
location / {
            proxy_pass https://services;
            proxy_set_header Host $host;
            autoindex on;
}
```
Добавляем репозиторий
```
[dar@localhost ~]# sudo cat >> /etc/yum.repos.d/lab.repo << EOF
[lab]
name=lab6
baseurl=http://localhost/repo
gpgcheck=0
enabled=1
EOF
[dar@localhost ~]# sudo yum repolist enabled | grep lab
lab                         lab6
```
Переустановим nginx
```
[dar@localhost ~]# sudo yum reinstall nginx
...
Downloading Packages:
nginx-1.14.1-9.module_el8.0.0+184+e34fea82.x86_64.rpm                                                       1.4 MB/s | 570 kB     00:00    
--------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                       989 kB/s | 570 kB     00:00     
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                                                    1/1 
  Running scriptlet: nginx-1:1.14.1-9.module_el8.0.0+184+e34fea82.x86_64                                                                1/1 
  Reinstalling     : nginx-1:1.14.1-9.module_el8.0.0+184+e34fea82.x86_64                                                                1/2 
  Running scriptlet: nginx-1:1.14.1-9.module_el8.0.0+184+e34fea82.x86_64                                                                1/2 
  Running scriptlet: nginx-1:1.14.1-9.module_el8.0.0+184+e34fea82.x86_64                                                                2/2 
  Cleanup          : nginx-1:1.14.1-9.module_el8.0.0+184+e34fea82.x86_64                                                                2/2 
  Running scriptlet: nginx-1:1.14.1-9.module_el8.0.0+184+e34fea82.x86_64                                                                2/2 
  Verifying        : nginx-1:1.14.1-9.module_el8.0.0+184+e34fea82.x86_64                                                                1/2 
  Verifying        : nginx-1:1.14.1-9.module_el8.0.0+184+e34fea82.x86_64                                                                2/2 

Reinstalled:
  nginx-1:1.14.1-9.module_el8.0.0+184+e34fea82.x86_64                                                                                       

Complete!
