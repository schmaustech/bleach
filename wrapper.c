#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NEWSUID 0
#define NEWSGID 0
#define PROGRAM1 "/usr/local/bleach/bleach"

int main(int argc,char *argv[]) {
        int i;
        setegid(NEWSGID);
        setgid(NEWSGID);
        seteuid(NEWSUID);
        setuid(NEWSUID);

        if (strcmp(argv[1],"1") == 0)
                execl(PROGRAM1,PROGRAM1,argv[2],argv[3],NULL);
        exit(0);
}
