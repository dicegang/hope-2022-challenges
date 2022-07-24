#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef int (*comparator)(const void *, const void *);

typedef struct queue_t {
  void **data;
  size_t length;
  size_t size;
  comparator cmp;
} Queue;

Queue * queue_create(comparator cmp) {
  Queue *q = malloc(sizeof(Queue));
  assert(q);
  q->size = 8;
  q->data = malloc(sizeof(void *) * q->size);
  assert(q->data);
  q->length = 0;
  q->cmp = cmp;
  return q;
}

void queue_free(Queue *q) {
  free(q->data);
  free(q);
}

void queue_push(Queue *q, void *item) {
  if (q->size == q->length) {
    q->size = 2 * q->size;
    q->data = realloc(q->data, sizeof(void *) * q->size);
  }
  for (size_t i = q->length; i >= 0; i--) {
    if ((i == 0) || (q->cmp(item, q->data[i-1]) < 0)) {
      q->data[i] = item;
      break;
    } else {
      q->data[i] = q->data[i-1];
    }
  }
  q->length++;
}

void * queue_pop(Queue *q) {
  assert(q->length > 0);
  return q->data[--q->length];
}

void queue_compact(Queue *q) {
  q->size = q->length;
  q->data = realloc(q->data, sizeof(void *) * q->size);
}

#define NUM_QUEUES 8
const char *menu =
  "Menu:\n"
  "1: create queue\n"
  "2: free queue\n"
  "3: push queue\n"
  "4: pop queue\n"
  "5: compact queue\n\n"
  "> ";

int get_num(const char *prompt) {
  char buf[8];
  fputs(prompt, stdout);
  fgets(buf, sizeof(buf), stdin);
  return atoi(buf);
}

char *get_string(const char *prompt) {
  char buf[32];
  fputs(prompt, stdout);
  fgets(buf, sizeof(buf), stdin);
  buf[strcspn(buf, "\n")] = 0;
  return strdup(buf);
}

Queue *qs[NUM_QUEUES];

int main() {
  int choice;
  unsigned int idx;
  char *item;

  setbuf(stdin, NULL);
  setbuf(stdout, NULL);

  while (1) {
    choice = get_num(menu);
    idx = get_num("idx? ");
    assert(idx < NUM_QUEUES);
    switch (choice) {
      case 1:
        qs[idx] = queue_create((comparator) strcmp);
        break;
      case 2:
        assert(qs[idx]);
        queue_free(qs[idx]);
        qs[idx] = NULL;
        break;
      case 3:
        assert(qs[idx]);
        item = get_string("content? ");
        assert(item);
        queue_push(qs[idx], item);
        break;
      case 4:
        assert(qs[idx]);
        item = queue_pop(qs[idx]);
        printf("item: %s\n", item);
        free(item);
        break;
      case 5:
        assert(qs[idx]);
        queue_compact(qs[idx]);
        break;
      case 69:
        assert(qs[idx]);
        printf("data: %p\nlength: %zu\nsize: %zu\ncmp: %p\n", qs[idx]->data, qs[idx]->length, qs[idx]->size, qs[idx]->cmp);
        break;
    }
    fputc('\n', stdout);
  }
}
