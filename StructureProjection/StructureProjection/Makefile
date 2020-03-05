CXX = nvcc
CXXFLAGS =  -std=c++11 -g 
SHELL = /bin/sh
BINNAME = $(shell /bin/ls *.cu | /bin/sed s/.cu//g )
DIRLIST = src
MAKE = make
MAINCPPFILE =  $(shell /bin/ls *.cu )
MAINOBJ =  $(shell /bin/ls *.cu | /bin/sed s/.cu/.o/g )

#Needed if files are present in src/
LIB = -Lsrc/  -l$(BINNAME)


INCLUDE = -Iinc

all: lib ${MAINOBJ}
	$(CXX) $(CXXFLAGS) $(INCLUDE) ${MAINOBJ} -o ${BINNAME} ${LIB}


lib:
	@for dir in $(DIRLIST); do cd $$dir && $(MAKE) all && cd .. ; done;:

%.o: %.cu
	$(CXX) $(CXXFLAGS) $(INCLUDE) -o $@ -c $<

clean:
	@for dir in $(DIRLIST); do (cd $$dir && $(MAKE) clean && cd .. ); done;:
	rm -fr *~
	rm -fr $(MAINOBJ)  $(BINFILE)

