LDFLAGS=-L/opt/homebrew/opt/openssl@1.1/lib/ -lcrypto
CFLAGS=-Wall -g

.PHONY: all
all: aesgcm

aesgcm: aesgcm.o
	gcc -o $@ $< $(LDFLAGS)

.PHONY: clean
clean:
	rm -vf *.o aesgcm
