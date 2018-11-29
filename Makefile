#NAME: Alejandra Cervantes,Ryan Miyahara
#EMAIL: alecer@ucla.edu,rmiyahara144@gmail.com
#ID: 104844623,804585999

ifndef VERBOSE
.SILENT:
endif

default:
	gcc -Wall -Wextra -g lab3b.c -o lab3b

clean:
	rm -f ./lab3b-804585999.tar.gz ./lab3b

dist: default
	tar -zcf lab3b-804585999.tar.gz ./Makefile ./README ./lab3b.c
