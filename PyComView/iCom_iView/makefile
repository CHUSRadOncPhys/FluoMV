CXX = g++
CXXFLAGS = -std=gnu++11 -D_GLIBCXX_USE_CXX11_ABI=0
OPTION =  --enable-libstdcxx-time

DIRLIST = src
MAKE = make
MAINOBJ = main.o
EXEC = test_iCOM_iView.exe

LIB =  -Lsrc -liCom_iView -liCOMClient  -lXISL
INCLUDE= -Iinc


#################################
all: lib $(MAINOBJ)
	$(CXX) $(CXXFLAGS) $(INCLUDE) $(MAINOBJ) -o $(EXEC) $(LIB)

lib:
	@for dir in $(DIRLIST); do cd $$dir && $(MAKE) all && cd .. ; done;:



%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDE) -o $@ -c $<


clean:
	rm -fr $(MAINOBJ)
	rm -fr $(EXEC)
	@for dir in $(DIRLIST); do (cd $$dir && $(MAKE) clean && cd .. ); done;:
