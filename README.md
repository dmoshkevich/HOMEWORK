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

```bash
Cоздадим виртуальную группу 
sudo vgcreate labgr /dev/sdb 
sudo vgdisplay -v labgr
sudo vgs
```
