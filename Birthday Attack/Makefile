LDFLAGS=-L/opt/homebrew/opt/openssl@1.1/lib/ -lcrypto
CFLAGS=-Wall -g
.PHONY: all
all: birthday

birthday: birthday.o
	gcc -o $@ $< $(LDFLAGS)

.PHONY: clean
clean:
	rm -vf *.o birthday
