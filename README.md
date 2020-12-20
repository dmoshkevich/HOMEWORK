## 1. Создать файловую систему на логическом томе и смонтировать её 
Для лабораторной работы был собран стенд - 5 виртуальных жёстких дисков по 2Гб. Установим необходимый пакет и проверим базовую конфигурацию.
```bash
sudo yum install -y lvm2
```
![](https://i.ibb.co/6n5PLQx/00-ivm2.png)
```bash
lsblk
lvmdiskscan
```
![](https://i.ibb.co/2c040WY/image.png)

Добавим диск b как физический том
```
sudo pvcreate /dev/sdb
sudo pvdisplay
sudo pvs
```
![](https://i.ibb.co/2nkxRfW/111.png)

Cоздадим виртуальную группу 

```bash
sudo vgcreate lvmlab /dev/sdb 
sudo vgdisplay -v lvmlab
sudo vgs
```
![](https://i.ibb.co/5hLNmYd/1-Volume-Group.png)

Создадим логическую группу
```bash
sudo lvcreate -l+100%FREE -n achu lvmlab 
sudo lvdisplay 
sudo lvs
```
![](https://i.ibb.co/HLSKJp9/3-Logic-Volume-1.png)
![](https://i.ibb.co/GJyFs82/2-Logic-Volume-2.png)

Создадим и смонтируем файловую систему
```bash
sudo mkfs.ext2 /dev/lvmlab/achu
```
![](https://i.ibb.co/d2Yy9C4/4-ext2.png)

```bash
sudo mount /dev/lvmlab/achu /mnt 
sudo mount
```
![](https://i.ibb.co/ccjMv8V/5.png)

## 2. Создать файл, заполенный нулями на весь размер точки монтирования
Побайтово скопируем в файл 4500 кусков по 1 Мб
```bash
sudo dd if=/dev/zero of=/mnt/mock.file bs=1M count=4500 status=progress
df -h
```
![](https://i.ibb.co/WvvtxpJ/6-Logic-Volume.png)

## 3. Расширить vg, lv и файловую систему
```bash
sudo pvcreate /dev/sdc
sudo vgextend lvmlab /dev/sdc
sudo lvextend -l+100%FREE /dev/lvmlab/achu
sudo lvdisplay
sudo lvs
sudo df -h
```

![](https://i.ibb.co/f21rm3s/7-Volume-Group-1.png)

Расширим файловую систему

```bash
sudo resize2fs /dev/lvmlab/achu
sudo df -h
```

![](https://i.ibb.co/WFZwgCF/9.png)

## 4. Уменьшить файловую систему

Отмонтируем файловую систему, после чего пересоберём том и систему. При уменьшении размеров системы необходимо учитывать минимальное пространство, которое ей необходимо, чтобы не обрезать нужные файлы, поэтому был оставлен небольшой запас:

```bash
sudo umount /mnt
sudo fsck -fy /dev/lvmlab/achu
sudo resize2fs /dev/lvmlab/achu 2100M             
sudo mount /dev/lvmlab/achu /mnt
sudo df -h
```
![](https://i.ibb.co/tMmFwCh/11-FS.png)

## 5. Создать несколько новых файлов и создать снэпшот.

```bash
sudo touch /mnt/mock{A..E}
ls /mnt
```
![](https://i.ibb.co/BKM2qkY/16-5.png)

```bash
sudo lvcreate -L 100M -s -n snshot /dev/lvmlab/achu
sudo lvs
sudo lsblk
```
![](https://i.ibb.co/KNs9wZq/17.png)

## 6. Удалить файлы и после монтирования снимка убедиться, что созданные нами файлы присутствуют.

![](https://i.ibb.co/SXq1Rbr/18.png)

sudo mkdir /snapsh
sudo mount /dev/mai/log_snapsh /snapsh
ls /snapsh
sudo umount /snapsh

