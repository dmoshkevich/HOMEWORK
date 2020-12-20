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

