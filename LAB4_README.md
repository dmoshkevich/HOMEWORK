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
[dar@localhost ~]$ sudo lsblk
NAME        MAJ:MIN RM  SIZE RO TYPE   MOUNTPOINT
sda           8:0    0   20G  0 disk   
├─sda1        8:1    0    1G  0 part   /boot
└─sda2        8:2    0   19G  0 part   
  ├─cl-root 253:0    0   17G  0 lvm    /
  └─cl-swap 253:1    0    2G  0 lvm    [SWAP]
sdb           8:16   0  500M  0 disk   
└─md0         9:0    0  996M  0 raid10 
sdc           8:32   0  500M  0 disk   
└─md0         9:0    0  996M  0 raid10 
sdd           8:48   0  500M  0 disk   
└─md0         9:0    0  996M  0 raid10 
sde           8:64   0  500M  0 disk   
└─md0         9:0    0  996M  0 raid10 
sdf           8:80   0  500M  0 disk   
└─md0         9:0    0  996M  0 raid10 
sr0          11:0    1 1024M  0 rom  
```
-------
### 4. Создать на RAID массиве раздел и файловую систему
Добавим раздел 
```
[dar@localhost ~]$ sudo fdisk /dev/md0

Welcome to fdisk (util-linux 2.32.1).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table.
Created a new DOS disklabel with disk identifier 0xbcb5ca80.

Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (1-4, default 1): 1
First sector (2048-2039807, default 2048): 
Last sector, +sectors or +size{K,M,G,T,P} (2048-2039807, default 2039807): +512M

Created a new partition 1 of type 'Linux' and of size 512 MiB.

Command (m for help): 

```
n - новый раздел, 
p - тип раздела (основной)
1 - номер раздела, указываем 
размер раздела 512M

Cохраним w и выходим (u). 
Создадим файловую систему 
```
[dar@localhost ~]$ sudo mkfs.ext4 /dev/md0p1
mke2fs 1.45.4 (23-Sep-2019)
Creating filesystem with 131072 4k blocks and 32768 inodes
Filesystem UUID: 54d87259-ab53-4fad-b534-25ca60bf13c4
Superblock backups stored on blocks: 
	32768, 98304

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (4096 blocks): done
Writing superblocks and filesystem accounting information: done

```
### 5. Добавить запись в fstab для монтирования при перезагрузке
Узнаем нужный UUID
```
[dar@localhost ~]$ sudo blkid /dev/md0p1
/dev/md0p1: UUID="54d87259-ab53-4fad-b534-25ca60bf13c4" TYPE="ext4" PARTUUID="bcb5ca80-01"
```
Редактируем файл fstab - добавим туда UUID=<тутъ> /mnt ext4 defaults 0 0.
```
#
# /etc/fstab
# Created by anaconda on Mon Sep 14 06:20:53 2020
#
# Accessible filesystems, by reference, are maintained under '/dev/disk/'.
# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info.
#
# After editing this file, run 'systemctl daemon-reload' to update systemd
# units generated from this file.
#
/dev/mapper/cl-root     /                       xfs     defaults	0 0
UUID=54d87259-ab53-4fad-b534-25ca60bf13c4 /boot                   ext4    defau$
/dev/mapper/cl-swap     swap                    swap    defaults	0 0
```
mount -a
