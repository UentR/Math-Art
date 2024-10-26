.SUFFIXES: .o .cpp

CXX = g++
CXXFLAGS = -std=c++17 -lstdc++ -Wall -pedantic -O3 -I/usr/local/include/eigen-3.4.0

OBJDIR = object

PROGS = main 

all: $(PROGS)

clean: 
	rm -rf $(PROGS) $(OBJDIR)/*.o

main: object/main.o
	$(CXX) $(CXXFLAGS) $^ -o $@ -lsfml-graphics -lsfml-window -lsfml-system 

$(OBJDIR)/%.o : %.cpp
	$(CXX) -c $(CXXFLAGS) $< -o $@
