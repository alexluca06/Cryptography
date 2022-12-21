#include <openssl/evp.h>
#include <openssl/err.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

const int TAG_LEN = 16;

void hexdump(unsigned char * string, int length) {
    int i;
    for (i = 0; i < length; i++) {
        printf("%02x", string[i]);
    }
}


int aes_gcm_encrypt(unsigned char * ptext,
        int plen,
        unsigned char * key,
        unsigned char * iv,
        unsigned char ** ctext,
        int * clen) {

    EVP_CIPHER_CTX * ctx;
    int cipher_len = *clen;

    /* TODO Create new EVP Context */
    ctx = EVP_CIPHER_CTX_new();

    /* TODO Initialize context using 256-bit AES-GCM, Encryption operation */
    int result = EVP_CipherInit_ex(ctx, EVP_aes_256_gcm(), NULL, NULL, NULL, 1);
    if (result == 0) {
        printf("An error occured!");
        return -1;
    }
     
    /* TODO Initialize Key and IV for the new context */
    int init_key = EVP_CipherInit_ex(ctx, NULL, NULL, key, iv, 1);
    if (init_key == 0) {
        printf("An error occured!");
        return -1;
    }

    
    /* TODO Encrypt data */
    *ctext = malloc(256);
    int encrypt = EVP_CipherUpdate(ctx, *ctext, clen, ptext, plen);
    if (encrypt == 0) {
         printf("An error occured!");
         return -1;
    }
    
    /* TODO Finalize encryption context (computes and appends auth tag) */
    EVP_CipherFinal_ex(ctx, *ctext, &cipher_len);
    EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG, TAG_LEN, *ctext+17);

    /* TODO Print tag */
    printf("Tag: ");
    hexdump(*ctext+17, TAG_LEN);
    printf("\n");
    
    /* TODO Destroy context */
    EVP_CIPHER_CTX_free(ctx);
    
    return 0;
}

int aes_gcm_decrypt(unsigned char * ctext,
        int clen,
        unsigned char * key,
        unsigned char * iv,
        unsigned char ** ptext,
        int * plen) {

    EVP_CIPHER_CTX * ctx;
    int plain_len = *plen;
    
    /* TODO Create new EVP Context */
    ctx = EVP_CIPHER_CTX_new();
    
    /* TODO Initialize context using 256-bit AES-GCM, Decryption operation */
    int result = EVP_CipherInit_ex(ctx, EVP_aes_256_gcm(), NULL, NULL, NULL, 0);
    
    if (result == 0) {
        printf("An error occured at init!");
        return -1;
    }

    /* TODO Initialize Key and IV for the new context */
    int init_key = EVP_CipherInit_ex(ctx, NULL, NULL, key, iv, 0);
    if (init_key == 0) {
        printf("An error occured init key, iv!");
        return -1;
    }
    /* TODO Submit tag data */
    EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_TAG, TAG_LEN, ctext + clen);
   
    /* TODO Decrypt data */
    *ptext = malloc(256);
    int decrypt = EVP_CipherUpdate(ctx, *ptext, plen, ctext, clen);
    if (decrypt == 0) {
         printf("An error occured at decrypt!");
         return -1;
    }
   
    /* TODO Finalize decryption context (verifies auth tag) */
    int ret = EVP_CipherFinal_ex(ctx, *ptext, &plain_len);
    if (ret == 0) {
        printf("Authentification failed!");
        exit(-1);
    }

    /* TODO Destroy context */
    EVP_CIPHER_CTX_free(ctx);
    return 0;
}

int main(int argc, char * argv[]) {
    ERR_load_crypto_strings();

    unsigned char key[] = "0123456789abcdef0123456789abcdef"; /* 256-bit key */
    unsigned char iv[] = "0123456789ab";                      /* 96-bit IV   */

    unsigned char * ptext = (unsigned char *)"Hello, SSLWorld!\n";
    int plen = strlen((const char *)ptext);

    unsigned char * ctext;
    int clen;

    printf("Plaintext = %s\n", ptext);
    printf("Plaintext  (hex) = "); hexdump(ptext, plen); printf("\n");

    aes_gcm_encrypt(ptext, plen, key, iv, &ctext, &clen);
    printf("Ciphertext (hex) = "); hexdump(ctext, clen); printf("\n");
    unsigned char * ptext2;
    int plen2;
    aes_gcm_decrypt(ctext, clen, key, iv, &ptext2, &plen2);
    printf("Done decrypting!\n");

    ptext2[plen2] = '\0';
    printf("Plaintext = %s\n", ptext2);

    if (memcmp(ptext, ptext2, strlen((const char *)ptext)) == 0) {
        printf("Ok!\n");
    } else {
        printf("Not ok :(\n");
    }

    return 0;
}
