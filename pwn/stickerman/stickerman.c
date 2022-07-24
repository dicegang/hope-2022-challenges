#include <fcntl.h>
#include <seccomp.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <stddef.h>
#include <stdio.h>

scmp_filter_ctx ctx;

void init_seccomp(){
    ctx = seccomp_init(SCMP_ACT_KILL);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve), 0);
}


int main(){
    char buf[64];
    puts("hey there, have you checked out the stickers at the in person event at hope, they're really cool");
    puts("they call me the sticker man >:)");
    init_seccomp();
    gets(buf);
    printf("%s", buf);
    seccomp_release(ctx);
}

