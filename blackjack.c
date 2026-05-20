#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

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

    int naipes_sorteados[3];
    int cartas_sorteadas[3];

    srand(time(NULL));

    naipes_sorteados[0] = rand() % 4;
    cartas_sorteadas[0] = rand() % 13;

    naipes_sorteados[1] = rand() % 4;
    cartas_sorteadas[1] = rand() % 13;

    while (naipes_sorteados[1] == naipes_sorteados[0] && cartas_sorteadas[1] == cartas_sorteadas[0])
    {
        naipes_sorteados[1] = rand() % 4;
        cartas_sorteadas[1] = rand() % 13;
    }

    printf("\n --- BLACKJACK --- \n");
    printf("\n O Mestre dará suas cartas... \n");
    fflush(stdout);

    sleep(5);

    total_pontos += calcular_valor(cartas_sorteadas[0]);
    total_pontos += calcular_valor(cartas_sorteadas[1]);

    printf("\n Suas cartas aleatórias: %s  %s\n",
           baralho[naipes_sorteados[0]][cartas_sorteadas[0]],
           baralho[naipes_sorteados[1]][cartas_sorteadas[1]]);

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
        naipes_sorteados[2] = rand() % 4;
        cartas_sorteadas[2] = rand() % 13;

        while ((naipes_sorteados[2] == naipes_sorteados[0] && cartas_sorteadas[2] == cartas_sorteadas[0]) ||
               (naipes_sorteados[2] == naipes_sorteados[1] && cartas_sorteadas[2] == cartas_sorteadas[1]))
        {
            naipes_sorteados[2] = rand() % 4;
            cartas_sorteadas[2] = rand() % 13;
        }

        total_pontos += calcular_valor(cartas_sorteadas[2]);
        printf("\n Sua carta comprada: %s \n", baralho[naipes_sorteados[2]][cartas_sorteadas[2]]);
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
