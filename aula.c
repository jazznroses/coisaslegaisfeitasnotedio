#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int calcular_valor(int indice_carta)
{
    if (indice_carta == 0)
    {
        return 11;
    }
    else if (indice_carta >= 10)
    {
        return 10;
    }
    else
    {
        return indice_carta + 1;
    }
}

int main()
{
    int chose;
    int total_pontos = 0;

    char baralho[4][13][5] = {
        {"🂡", "🂢", "🂣", "🂤", "🂥", "🂦", "🂧", "🂨", "🂩", "🂪", "🂫", "🂭", "🂮"}, // Espadas
        {"🂱", "🂲", "🂳", "🂴", "🂵", "🂶", "🂷", "🂸", "🂹", "🂺", "🂻", "🂽", "🂾"}, // Copas
        {"🃁", "🃂", "🃃", "🃄", "🃅", "🃆", "🃇", "🃈", "🃉", "🃊", "🃋", "🃍", "🃎"}, // Ouros
        {"🃑", "🃒", "🃓", "🃔", "🃕", "🃖", "🃗", "🃘", "🃙", "🃚", "🃛", "🃝", "🃞"}  // Paus
    };

    srand(time(NULL));

    int naipe1 = rand() % 4;
    int carta1 = rand() % 13;

    int naipe2 = rand() % 4;
    int carta2 = rand() % 13;

    while (naipe1 == naipe2 && carta1 == carta2)
    {
        naipe2 = rand() % 4;
        carta2 = rand() % 13;
    }

    printf("\n --- BLACKJACK --- \n");
    printf("\n O Mestre dará suas cartas... \n");
    fflush(stdout);

    sleep(5);
    total_pontos += calcular_valor(carta1);
    total_pontos += calcular_valor(carta2);

    printf("\n Suas cartas aleatórias: %s  %s\n", baralho[naipe1][carta1], baralho[naipe2][carta2]);
    printf(" Pontuação atual: %d pontos\n", total_pontos);

    if (total_pontos == 21)
    {
        printf("\n BLACKJACK! Você fechou 21 e GANHOU direto! \n");
        return 0;
    }

    printf("\n Digite 0 para comprar outra carta ou 1 para parar: ");
    scanf("%d", &chose);

    if (chose == 0)
    {
        int naipe3 = rand() % 4;
        int carta3 = rand() % 13;

        while ((naipe3 == naipe1 && carta3 == carta1) || (naipe3 == naipe2 && carta3 == carta2))
        {
            naipe3 = rand() % 4;
            carta3 = rand() % 13;
        }

        total_pontos += calcular_valor(carta3);
        printf("\n Sua carta comprada: %s \n", baralho[naipe3][carta3]);
        printf(" Pontuação total: %d pontos\n", total_pontos);
    }

    printf("\n --- RESULTADO FINAL --- \n");
    if (total_pontos == 21)
    {
        printf("Parabéns! Você fechou 21 perfeitos e GANHOU! \n");
    }
    else if (total_pontos > 21)
    {
        printf("Você estourou com %d pontos! O Mestre ganhou. \n", total_pontos);
    }
    else
    {
        printf("Você parou com %d pontos. O jogo terminou! \n", total_pontos);
    }

    return 0;
}