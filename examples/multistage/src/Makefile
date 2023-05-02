CC = gcc
CFLAGS = -O3 -static -fopenmp -Wall -Wextra

hello_world: hello_world.o
	$(CC) $(CFLAGS) -o $@ $<

clean:
	$(RM) $(wildcard *.o) hello_world
