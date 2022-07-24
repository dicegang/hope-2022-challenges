#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char *dice_faces[6][3] = {
  {
    "     ",
    "  o  ",
    "     ",
  },
  {
    "o    ",
    "     ",
    "    o",
  },
  {
    "o    ",
    "  o  ",
    "    o",
  },
  {
    "o   o",
    "     ",
    "o   o",
  },
  {
    "o   o",
    "  o  ",
    "o   o",
  },
  {
    "o   o",
    "o   o",
    "o   o",
  },
};

int* roll_dice (size_t num_dice) {
  int *dice = calloc(num_dice, sizeof(int));
  for (size_t i = 0; i < num_dice; i++) {
    dice[i] = rand() % 6;
  }
  return dice;
}

char* print_dice (int num) {
  char *dice;
  asprintf(&dice, "┌───────┐\n│ %s │\n│ %s │\n│ %s │\n└───────┘", dice_faces[num][0], dice_faces[num][1], dice_faces[num][2]);
  return dice;
}

int main () {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);

  char buf[64];
  printf("How many dice do you want to roll? ");
  fgets(buf, sizeof(buf), stdin);
  size_t num_dice = strtoul(buf, NULL, 0);
  if (num_dice < 1 || num_dice > 50) {
    puts("no!!!");
    exit(EXIT_FAILURE);
  }

  int *dice = roll_dice(num_dice);

  printf("Use a lucky charm: ");
  fgets(buf, sizeof(buf), stdin);
  char *charm;
  asprintf(&charm, "applying magic ✨✨✨ %s", buf);
  printf(charm);
  sleep(1);
  free(charm);

  for (size_t i = 0; i < num_dice; i++) {
    char *print = print_dice(dice[i]);
    puts(print);
    free(print);
    if (dice[i] + 1 == 13) {
      puts("winner!");
      system("/bin/sh");
      return 0;
    }
  }
  free(dice);
  puts("unlucky...");
  return 1;
}
