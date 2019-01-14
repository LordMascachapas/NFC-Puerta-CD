# NFC-Puerta-CD

## Enabling Raspberry Pi SPI
	-raspi-config
	-Select Interfacing Options then SPI. Select Yes when prompted
	sudo reboot
	sudo nano /boot/config.txt
	find the line: dtparam=spi=on

## Install python 2.7
	sudo apt-get install python2.7-dev

## install septup.py
	sudo python setup.py install

## Conect the pins to rc522
	NAME	PIN #	PIN NAME
	SDA	24	GPIO8
	SCK	23	GPIO11
	MOSI	19	GPIO10
	MISO	21	GPIO9
	IRQ	None	None
	GND	Any	Any Ground
	RST	22	GPIO25
	3.3V	1	3V3
	probar los 5v.

## AVISO
Hacer el cron
