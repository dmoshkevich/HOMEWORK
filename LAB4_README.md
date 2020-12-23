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
sudo mdadm --create /dev/md0 -l 10 -n 4 /dev/sd{b..e}
```
------
Проверим корректность сборки
```
mdadm --detail /dev/md0
```
------
### 2. Имитация поломки и восстановления одного из дисков RAID массива

Отключаем и извлекаем
```
sudo mdadm /dev/md0 --fail /dev/sdb
```
----
```
sudo mdadm /dev/md0 --remove /dev/sdb
```
-----
Заменим его неповреждённым диском 
```
sudo mdadm --add /dev/md0 /dev/sdf
```
--------
```
mdadm --detail /dev/md0
```
-------
Вернём в систему диск, который мы оьключили ранее 
```
sudo mdadm --add /dev/md0 /dev/sde
```
-------
### 3. Проверка, что RAID собирается при перезагрузке
```
mkdir /etc/mdadm
echo "DEVICE partitions" > /etc/mdadm/mdadm.conf
mdadm --detail --scan --verbose | awk '/ARRAY/ {print}' >> /etc/mdadm/mdadm.conf
```
Содержание файла конфигурации
---------
Остановим массив 
```
sudo mdadm --stop /dev/md0 
```
-------
Перезапустим массив
```
sudo mdadm --assemble /dev/md0
```
-------
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
