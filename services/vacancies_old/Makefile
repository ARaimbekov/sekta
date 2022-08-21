all: main
main: main.o functions.o
	gcc -o lab7 main.o functions.o -lm
functions.o: functions.c
	gcc -o functions.o -c functions.c -lm
main.o: main.c
	gcc -o main.o -c main.c -lm