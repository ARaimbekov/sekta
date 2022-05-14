#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define PORT 8080
#define FAIL -1
#define VACANCY_MEMORY 2048

int server_fd;
struct sockaddr_in address;

void setup();
void serve(int socket_fd);
int sendLogo(int socket_fd);

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
    if (sendLogo(socket_fd) == FAIL)
    {
        return;
    }

    int valread;
    char buffer[1024] = {0};
    valread = read(socket_fd, buffer, 1024);
    printf("%s\n", buffer);
}

int sendLogo(int socket_fd)
{
    FILE *file = fopen("img.txt", "r");
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

int printVacancies(int socket_fd)
{
    FILE *file = fopen("vacancies.txt", "r");
    if (NULL == file)
    {
        printf("Err: file vacancies.txt can't be opened \n");
        return FAIL;
    }

    for (int i = 0; i < 40; i++)
    {
        // alloc memory
        // scan
        // send
        // free
    }

    return 0;
}