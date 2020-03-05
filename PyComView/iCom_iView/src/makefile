CXX = g++
#LIBFLAGS = -static-libgcc -static-libstdc++
LIBFLAGS = -shared
CXXFLAGS = -std=gnu++11 -D_GLIBCXX_USE_CXX11_ABI=0
BINNAME = iCom_iView
OPTION =  --enable-libstdcxx-time

LIBOBJECT = lib$(BINNAME).a
DLL = $(BINNAME).dll

SHELL = /bin/sh

OBJECT_MAIN = $(shell ls *.cpp | sed s/.cpp/.o/g )
CCFILE_MAIN = $(shell ls *.cpp)

INCLUDE =  -I../inc
LIB = -L. -liCOMClient -lXISL --enable-libstdcxx-time

#################################
all: $(OBJECT_MAIN) $(LIBOBJECT) $(DLL)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDE) -o $@ -c $< 

%.dll: $(CCFILE_MAIN)
	$(CXX) $(LIBFLAGS) $(CXXFLAGS) $(INCLUDE) -o $@ $(OBJECT_MAIN) $(LIB)

%.a: $(CCFILE_MAIN)
	echo $(BINNAME)
	ar cr $@ $(OBJECT_MAIN)

clean:
	rm -fr $(LIBOBJECT)
	rm -fr $(OBJECT_MAIN)
	rm -fr $(DLL)
