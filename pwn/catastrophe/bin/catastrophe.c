#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include <string.h>

#define NUM_CHONKS 10

char *chonks[NUM_CHONKS];

uint64_t get_number() {
  char buf[16];
  printf("> ");
  fgets(buf, sizeof(buf), stdin);
  return strtoull(buf, NULL, 10);
}

uint64_t get_index() {
  uint64_t num = 0;
  while ((num = get_number()) >= NUM_CHONKS) {
    puts("Invalid!");
  }
  return num;
}

void print_menu() {
  puts("--- menu ---");
  puts("1) malloc");
  puts("2) free");
  puts("3) view");
  puts("4) leave");
  puts("------------");
}

void op_malloc() {
  puts("Index?");
  uint64_t idx = get_index();
  puts("Size?");
  uint64_t size = get_number();
  if (size < 1 || size > 0x200) {
    puts("Interesting...");
    return;
  }
  chonks[idx] = malloc(size);
  printf("Enter content: ");
  fgets(chonks[idx], size, stdin);
}

void op_free() {
  puts("Index?");
  uint64_t idx = get_index();
  free(chonks[idx]);
}

void op_view() {
  puts("Index?");
  uint64_t idx = get_index();
  puts(chonks[idx]);
}

int main() {
  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);

  while (1) {
    print_menu();
    switch (get_number()) {
      case 1:
        op_malloc();
        break;
      case 2:
        op_free();
        break;
      case 3:
        op_view();
        break;
      case 4:
        puts("Bye!");
        exit(0);
      default:
        puts("Invalid choice!");
    }
    printf("\n");
  }
}
