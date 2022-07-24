#include <stdio.h>

#define CUBED(x) ((x) * (x) * (x))

int get_number(int* number) {
    char input[32];
    scanf("%s", input);

    if (sscanf(input, "%d", number) < 1) {
        printf("invalid input: %s.\n", input);
        return 0;
    }

    if (*number < 1) {
        puts("number must be positive!");
        return 0;
    }

    if (*number > 1 << 20) {
        puts("number is too large!");
        return 0;
    }

    return 1;
}

void message(int success) {
    if (success) {
        char flag[256];
        FILE* file = fopen("flag.txt", "r");
        if (file == NULL) puts("flag file missing!");
        else fgets(flag, sizeof(flag), file);
        fclose(file);
        printf("great work. here's your reward: %s\n", flag);
    } else {
        puts("a ^ 3 + b ^ 3 is not c ^ 3.");
    }
}

int main() {
    setbuf(stdout, NULL);

    puts("welcome to the anti-flt league!");
    puts("do you have a counterexample for us?");

    char labels[] = { 'a', 'b', 'c' };
    int nums[3];
    for (int i = 0; i < 3; i++) {
        printf("%c: ", labels[i]);
        if (!get_number(&nums[i])) return 0;
    }

    message(CUBED(nums[0]) + CUBED(nums[1]) == CUBED(nums[2]));

    return 0;
}
