CXX = g++
CXXFLAGS =  -O2 
SHELL = /bin/sh
BINNAME = $(shell ls ../*.cpp | sed s/.cpp//g | sed s/"\.\.\/"//g )
LIBOBJECT = lib$(BINNAME).a
OBJECT_MAIN = $(shell ls *.cpp | sed s/.cpp/.o/g )

CCFILE_MAIN = $(shell ls *.cpp)

INCLUDE =  -g -I../inc 

all: ${OBJECT_MAIN} $(LIBOBJECT)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDE) -o $@ -c $<

%.so: $(CCFILE_MAIN)
	$(CXX) -shared $(CXXFLAGS) $(INCLUDE) -o $@ $(OBJECT_MAIN)

%.a: $(CCFILE_MAIN)
	ar cr $@ $(OBJECT_MAIN)

clean:
	rm -fr *~
	rm -fr ../inc/*~	
	rm -fr $(LIBOBJECT)
	rm -fr $(OBJECT_MAIN)
