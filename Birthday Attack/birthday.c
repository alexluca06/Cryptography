/*
*   We want to show that SHA-1 is not collision resistant, for two different
* messages(m1 and m2) we get the same hash:
*   -> SHA-1(m1) == SHA-1(m2)
*/

#include <openssl/sha.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <time.h>
#include <string.h>

/* We want a collision in the first 4 bytes = 2^16 attempts */
#define N_BITS  16

/* Represent a pair <message, hash(message)[0:3] */
struct pair {
    char msg[11];  // random message
    int hash;  // first 4 bytes from message's hash
};

int raw2int4(unsigned char * digest) {
    int i;
    int sum = 0;

    for (i = 0; i < 3; i++) {
        sum += sum * 256 + digest[i];
    }

    return sum;
}

void hexdump(unsigned char * string, int length) {
    int i;
    for (i = 0; i < length; i++) {
        printf("%02x", string[i]);
    }
}

int main(int argc, char * argv[]) {
   
    unsigned char md[20]; /* SHA-1 outputs 160-bit digests */
    int msg_number = 2 << 16;
    int msg_len = 11;  /* length of a random message*/
    struct pair pairs[msg_number];  /* vectors of struct pairs: <message, hash(message)[0:3]> */
    
    
    REPEAT_ATTACK:
    /* Try to find a collision on the first 4 bytes (32 bits) */

    /* Step 1. Generate 2^16 different random messages */
    srand(time(NULL));
    for (int i = 0; i < msg_number; i++) {
        for (int j = 0; j < 10; j++) {
            char rnd_char = 32 + rand() % (126 - 32);
            pairs[i].msg[j] = rnd_char;  /* create random messages */
        }
        pairs[i].msg[10] = '\0'; /* string terminator */

        /* Step 2. Compute hashes */
        SHA_CTX context;
        SHA1_Init(&context);
        SHA1_Update(&context, pairs[i].msg, msg_len);
        SHA1_Final(md, &context);
        pairs[i].hash = raw2int4(md); /* get first 4 bytes from message's hash */
    }
    

    /* Step 3. Check if there exist two hashes that match in the first four bytes */

    for (int i = 0; i < msg_number - 1; i++) {
        for (int j = i + 1; j < msg_number; j++) {

            /* Step 3a. If a match is found, print the messages and hashes */

            if ((strcmp(pairs[i].msg, pairs[j].msg) != 0) && (pairs[i].hash == pairs[j].hash)) {
                printf("Msg 1: %s\n", pairs[i].msg);
                printf("Msg 2: %s\n", pairs[j].msg);
                printf("Hash Msg 1: %d\n", pairs[i].hash);
                printf("Hash Msg 2: %d\n", pairs[j].hash);
                return 0;
            }
        }
    }
    
    /* Step 3b. If no match is found, repeat the attack with a new set of random messages */
    goto REPEAT_ATTACK;

    

    return 0;
}
