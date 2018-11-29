#NAME: Alejandra Cervantes,Ryan Miyahara
#EMAIL: alecer@ucla.edu,rmiyahara144@gmail.com
#ID: 104844623,804585999

ifndef VERBOSE
.SILENT:
endif

default:
	chmod +x lab3b
	echo "Compilation successful"

clean:
	rm -f ./lab3b-804585999.tar.gz

dist: default
	tar -zcf lab3b-804585999.tar.gz ./Makefile ./README ./lab3b.py ./lab3b
