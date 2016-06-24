CXX=clang++
CPPFLAGS=-I. -O3
DEPS = edge.h graph.h bmath.h scoped_ptr.h
OBJS = edge.o graph.o main.o bmath.o

%.o: %.c $(DEPS)
	$(CXX) -c -o $@ $< $(CPPFLAGS)

bundle: $(OBJS)
	$(CXX) -o $@ $^ $(CPPFLAGS) -lm