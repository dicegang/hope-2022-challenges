# include <stdio.h>
# include <stdlib.h>

int read_numbers(int numbers[6]) {
    printf("input: ");
    fflush(stdout);

    char input[256];
    fgets(input, sizeof(input), stdin);

    return sscanf(input, "%d %d %d %d %d %d",
        &numbers[0],
        &numbers[1],
        &numbers[2],
        &numbers[3],
        &numbers[4],
        &numbers[5]
    ) == 6;
}

int check() {
    int nums[6];
    if (!read_numbers(nums)) return 0;

    if (nums[0] != 12) return 0;
    for (int i = 1; i < 6; i++) {
        if (nums[i] != (nums[i - 1] * 3 + 7) % 16) {
            return 0;
        }
    }

    return 1;
}

int main() {
    if (check()) {
        char* flag = getenv("FLAG");
        if (flag == NULL) printf("no flag provided!\n");
        else printf("%s\n", flag);
    } else {
        printf("nope\n");
    }
    return 0;
}
