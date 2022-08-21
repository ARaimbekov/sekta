#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define PORT 8080
#define FAIL -1

#define LOGO_IMG "logo_img.txt"
#define VACANCIES_IMG "vacancies_img.txt"

#define VACANCY_MEMORY 2048
#define VACANCIES_AMOUNT 40
#define VACANCY_FORMAT "#%d\nName: %s\nDescription: %s\n\n"

int server_fd;
struct sockaddr_in address;
struct vacancy
{
    char *name;
    char *description;
};

void setup();
void serve(int socket_fd);
int printImg(int socket_fd, char *path);
int printVacanciesImg(int socket_fd);

int scanVacancies(struct vacancy vs[VACANCIES_AMOUNT]);
int scanVacancy(FILE *file, struct vacancy *vs);

int printVacancies(int socket_fd, int amount, struct vacancy vs[VACANCIES_AMOUNT]);

int main(int argc, char const *argv[])
{
    setup();

    int addrlen = sizeof(address);
    while (1)
    {
        int new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen);
        if (new_socket == FAIL)
        {
            perror("connection failed");
        }

        serve(new_socket);
        close(new_socket);
    }
}

void setup()
{
    int opt = 1;

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (!server_fd)
    {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt)))
    {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0)
    {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 3) < 0)
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }
}

void serve(int socket_fd)
{
    if (printImg(socket_fd, LOGO_IMG) == FAIL)
        return;

    while (1)
    {
        struct vacancy vs[VACANCIES_AMOUNT];
        int size = scanVacancies(vs);
        if (size == FAIL)
            break;

        if (printVacancies(socket_fd, size, vs) == FAIL)
            break;

        int valread;
        char buffer[1024] = {0};
        valread = read(socket_fd, buffer, 1024);
        printf("%s\n", buffer);
    }
}

int printImg(int socket_fd, char *path)
{
    FILE *file = fopen(path, "r");
    if (NULL == file)
    {
        printf("Err: file img.txt can't be opened \n");
        return FAIL;
    }

    int size;
    char *img = malloc(1337);

    for (int i = 0; i < 1337; i++)
    {
        img[i] = fgetc(file);
        if (img[i] == EOF)
        {
            img[i] = 0;
            size = i - 1;
            break;
        }
    }

    fclose(file);
    send(socket_fd, img, size, 0);
    free(img);

    return 0;
}

int scanVacancies(struct vacancy vs[VACANCIES_AMOUNT])
{
    FILE *file = fopen("vacancies.txt", "r");
    if (NULL == file)
    {
        printf("Err: file vacancies.txt can't be opened \n");
        return FAIL;
    }

    for (int i = 0; i < VACANCIES_AMOUNT; i++)
        if (scanVacancy(file, &vs[i]) == FAIL)
            return i - 1;
}

int scanVacancy(FILE *file, struct vacancy *vs)
{
    vs->name = malloc(100);
    int i;

    for (i = 0; i < 100; i++)
    {
        vs->name[i] = fgetc(file);

        if (vs->name[i] == EOF)
            return FAIL;

        if (vs->name[i] == ' ')
            break;
    }
    vs->name[i] = 0;

    vs->description = malloc(200);
    for (i = 0; i < 200; i++)
    {
        vs->description[i] = fgetc(file);

        if (vs->description[i] == EOF)
            return FAIL;

        if (vs->description[i] == '\n')
            break;
    }
    vs->description[i] = 0;

    return 0;
}

int printVacancies(int socket_fd, int amount, struct vacancy vs[VACANCIES_AMOUNT])
{
    if (printImg(socket_fd, VACANCIES_IMG) == FAIL)
        return FAIL;

    for (int i = 0; i < amount; i++)
    {
        char str[300];
        int size = sprintf(str, VACANCY_FORMAT, i, vs[i].name, vs[i].description);

        if (send(socket_fd, str, size, 0) == FAIL)
        {
            printf("Err: sending vacancy failed \n");
            return FAIL;
        }
    }

    return 0;
}
