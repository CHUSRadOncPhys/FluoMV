CXX = nvcc
CXXFLAGS =  -std=c++11 -g
SHELL = /bin/sh
BINNAME = $(shell ls ../*.cu | sed s/.cu//g | sed s/"\.\.\/"//g )
LIBOBJECT = lib$(BINNAME).a
OBJECT_MAIN = $(shell ls *.cu | sed s/.cu/.o/g )
CCFILE_MAIN = $(shell ls *.cu)

INCLUDE =  -g -I../inc 

all: ${OBJECT_MAIN} $(LIBOBJECT)

%.o: %.cu
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
