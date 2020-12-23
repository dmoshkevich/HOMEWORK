# Работа с RAID массивами с использованием mdadm
### 1. Собрать R0/R5/R10 массив 
Добавим несколько виртуальных дисков

![](https://i.ibb.co/XWyf7cD/2020-12-21-000841.jpg)

Установим утилиту
```
sudo yum install mdadm
```
Соберем массив
```
[dar@localhost ~]$ sudo mdadm --create /dev/md0 -l 10 -n 4 /dev/sd{b..e}
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md0 started.
```
------
Проверим корректность сборки
```
[dar@localhost ~]$ sudo mdadm --detail /dev/md0
/dev/md0:
           Version : 1.2
     Creation Time : Wed Dec 23 21:45:34 2020
        Raid Level : raid10
        Array Size : 1019904 (996.00 MiB 1044.38 MB)
     Used Dev Size : 509952 (498.00 MiB 522.19 MB)
      Raid Devices : 4
     Total Devices : 4
       Persistence : Superblock is persistent

       Update Time : Wed Dec 23 21:46:11 2020
             State : clean 
    Active Devices : 4
   Working Devices : 4
    Failed Devices : 0
     Spare Devices : 0

            Layout : near=2
        Chunk Size : 512K

Consistency Policy : resync

              Name : localhost.localdomain:0  (local to host localhost.localdomain)
              UUID : 5e05a5bc:5c961908:d536df1f:1b05d3e4
            Events : 17

    Number   Major   Minor   RaidDevice State
       0       8       16        0      active sync set-A   /dev/sdb
       1       8       32        1      active sync set-B   /dev/sdc
       2       8       48        2      active sync set-A   /dev/sdd
       3       8       64        3      active sync set-B   /dev/sde
```
------
### 2. Имитация поломки и восстановления одного из дисков RAID массива

Отключаем и извлекаем
```
[dar@localhost ~]$ sudo mdadm /dev/md0 --fail /dev/sdb
mdadm: set /dev/sdb faulty in /dev/md0

[dar@localhost ~]$ sudo mdadm /dev/md0 --remove /dev/sdb
mdadm: hot removed /dev/sdb from /dev/md0
```
Заменим его неповреждённым диском 
```
[dar@localhost ~]$ sudo mdadm --add /dev/md0 /dev/sdf
mdadm: added /dev/sdf

[dar@localhost ~]$ mdadm --detail /dev/md0
mdadm: must be super-user to perform this action
[dar@localhost ~]$ sudo mdadm --detail /dev/md0
/dev/md0:
           Version : 1.2
     Creation Time : Wed Dec 23 21:45:34 2020
        Raid Level : raid10
        Array Size : 1019904 (996.00 MiB 1044.38 MB)
     Used Dev Size : 509952 (498.00 MiB 522.19 MB)
      Raid Devices : 4
     Total Devices : 4
       Persistence : Superblock is persistent

       Update Time : Wed Dec 23 21:49:45 2020
             State : clean 
    Active Devices : 4
   Working Devices : 4
    Failed Devices : 0
     Spare Devices : 0

            Layout : near=2
        Chunk Size : 512K

Consistency Policy : resync

              Name : localhost.localdomain:0  (local to host localhost.localdomain)
              UUID : 5e05a5bc:5c961908:d536df1f:1b05d3e4
            Events : 39

    Number   Major   Minor   RaidDevice State
       4       8       80        0      active sync set-A   /dev/sdf
       1       8       32        1      active sync set-B   /dev/sdc
       2       8       48        2      active sync set-A   /dev/sdd
       3       8       64        3      active sync set-B   /dev/sde
```
Вернём в систему диск, который мы оьключили ранее 
```
[dar@localhost ~]$ sudo mdadm --add /dev/md0 /dev/sdb
mdadm: added /dev/sdb
```
### 3. Проверка, что RAID собирается при перезагрузке
```
sudo mkdir /etc/mdadm
sudo echo "DEVICE partitions" > /etc/mdadm/mdadm.conf
sudo mdadm --detail --scan --verbose | awk '/ARRAY/ {print}' >> /etc/mdadm/mdadm.conf
```
Содержание файла конфигурации

DEVICE partitions
ARRAY /dev/md0 level=raid10 num-devices=4 metadata=1.2 spares=1 
name=localhost.localdomain:0 UUID=5e05a5bc:5c961908:d536df1f:1b05d3e4

Остановим массив 
```
[root@localhost dar]# mdadm --stop /dev/md0
mdadm: stopped /dev/md0
```
Перезапустим массив
```
[root@localhost dar]# mdadm --assemble /dev/md0
mdadm: /dev/md0 has been started with 4 drives and 1 spare.
```
Перезагрузим и проверим 
```
lsblk
```
-------
### 4. Создать на RAID массиве раздел и файловую систему
Добавим раздел 
```
sudo fdisk /dev/md0
```
----------
n - новый раздел, 
p - тип раздела (основной)
1 - номер раздела, указываем 
размер раздела 512M

Cохраним w и выходим (u). 
Создадим файловую систему 
```
sudo mkfs.ext4 /dev/md0p1
```
---------
### 5. Добавить запись в fstab для монтирования при перезагрузке
Узнаем нужный UUID
```
sudo blkid /dev/md0p1
```
Редактируем файл fstab - добавим туда UUID=<тутъ> /mnt ext4 defaults 0 0.
mount -a
