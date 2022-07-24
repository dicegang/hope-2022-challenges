# include <stdio.h>
# include <string.h>

int main() {
    char flag[46] = {
        8, 72, 105, 142, 252, 73, 74, 152, 107, 178, 171, 53, 96, 223, 224,
        117, 140, 92, 194, 190, 167, 47, 180, 114, 29, 222, 105, 244, 209, 125,
        88, 186, 32, 141, 17, 28, 184, 154, 8, 76, 19, 46, 196, 200, 159, 0
    };

    flag[12] ^= flag[44];
    flag[44] ^= flag[12];
    flag[12] ^= flag[44];
    flag[40] ^= flag[43];
    flag[43] ^= flag[40];
    flag[40] ^= flag[43];
    flag[1] ^= flag[42];
    flag[42] ^= flag[1];
    flag[1] ^= flag[42];
    flag[3] ^= flag[41];
    flag[41] ^= flag[3];
    flag[3] ^= flag[41];
    flag[39] ^= flag[40];
    flag[40] ^= flag[39];
    flag[39] ^= flag[40];
    flag[26] ^= flag[39];
    flag[39] ^= flag[26];
    flag[26] ^= flag[39];
    flag[4] ^= flag[38];
    flag[38] ^= flag[4];
    flag[4] ^= flag[38];
    flag[2] ^= flag[37];
    flag[37] ^= flag[2];
    flag[2] ^= flag[37];
    flag[33] ^= flag[35];
    flag[35] ^= flag[33];
    flag[33] ^= flag[35];
    flag[4] ^= flag[34];
    flag[34] ^= flag[4];
    flag[4] ^= flag[34];
    flag[12] ^= flag[33];
    flag[33] ^= flag[12];
    flag[12] ^= flag[33];
    flag[16] ^= flag[32];
    flag[32] ^= flag[16];
    flag[16] ^= flag[32];
    flag[29] ^= flag[31];
    flag[31] ^= flag[29];
    flag[29] ^= flag[31];
    flag[22] ^= flag[30];
    flag[30] ^= flag[22];
    flag[22] ^= flag[30];
    flag[21] ^= flag[29];
    flag[29] ^= flag[21];
    flag[21] ^= flag[29];
    flag[10] ^= flag[28];
    flag[28] ^= flag[10];
    flag[10] ^= flag[28];
    flag[25] ^= flag[26];
    flag[26] ^= flag[25];
    flag[25] ^= flag[26];
    flag[5] ^= flag[25];
    flag[25] ^= flag[5];
    flag[5] ^= flag[25];
    flag[7] ^= flag[24];
    flag[24] ^= flag[7];
    flag[7] ^= flag[24];
    flag[14] ^= flag[23];
    flag[23] ^= flag[14];
    flag[14] ^= flag[23];
    flag[3] ^= flag[22];
    flag[22] ^= flag[3];
    flag[3] ^= flag[22];
    flag[19] ^= flag[21];
    flag[21] ^= flag[19];
    flag[19] ^= flag[21];
    flag[11] ^= flag[20];
    flag[20] ^= flag[11];
    flag[11] ^= flag[20];
    flag[0] ^= flag[19];
    flag[19] ^= flag[0];
    flag[0] ^= flag[19];
    flag[9] ^= flag[18];
    flag[18] ^= flag[9];
    flag[9] ^= flag[18];
    flag[12] ^= flag[17];
    flag[17] ^= flag[12];
    flag[12] ^= flag[17];
    flag[12] ^= flag[16];
    flag[16] ^= flag[12];
    flag[12] ^= flag[16];
    flag[11] ^= flag[15];
    flag[15] ^= flag[11];
    flag[11] ^= flag[15];
    flag[8] ^= flag[14];
    flag[14] ^= flag[8];
    flag[8] ^= flag[14];
    flag[1] ^= flag[13];
    flag[13] ^= flag[1];
    flag[1] ^= flag[13];
    flag[6] ^= flag[12];
    flag[12] ^= flag[6];
    flag[6] ^= flag[12];
    flag[10] ^= flag[11];
    flag[11] ^= flag[10];
    flag[10] ^= flag[11];
    flag[6] ^= flag[10];
    flag[10] ^= flag[6];
    flag[6] ^= flag[10];
    flag[1] ^= flag[9];
    flag[9] ^= flag[1];
    flag[1] ^= flag[9];
    flag[5] ^= flag[8];
    flag[8] ^= flag[5];
    flag[5] ^= flag[8];
    flag[3] ^= flag[7];
    flag[7] ^= flag[3];
    flag[3] ^= flag[7];
    flag[3] ^= flag[6];
    flag[6] ^= flag[3];
    flag[3] ^= flag[6];
    flag[2] ^= flag[5];
    flag[5] ^= flag[2];
    flag[2] ^= flag[5];
    flag[2] ^= flag[4];
    flag[4] ^= flag[2];
    flag[2] ^= flag[4];
    flag[1] ^= flag[2];
    flag[2] ^= flag[1];
    flag[1] ^= flag[2];
    flag[0] ^= flag[1];
    flag[1] ^= flag[0];
    flag[0] ^= flag[1];

    int state_one = 0x68;
    int state_two = 0x11;
    for (int i = 0; i < 45; i++) {
        flag[i] ^= state_one;
        flag[i] ^= state_two;
        state_one = ((state_one * state_one + 0x54) >> 3) & 0xff;
        state_two = ((state_two ^ 0xaa) << 1) + state_two & 0xff;
    }

    printf("what's the flag? ");
    fflush(stdout);

    char input[46] = {0};
    scanf("%45s", input);

    if (strcmp(input, flag) == 0) puts("correct!");
    else puts("incorrect.");
}

