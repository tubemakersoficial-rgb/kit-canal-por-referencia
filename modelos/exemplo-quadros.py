import json
S = ("Cena ilustrada em lápis de cor e aquarela sobre papel creme, no MESMO traço da referência: personagens com cabeça grande e redonda, "
     "olhos de pontinho, sorriso simples, orelhinhas, e braços e pernas de PALITO desenhados como linhas finas azul-marinho, mãos simples, "
     "corpos NÃO realistas, iguais à folha da família. Cenário simples, cores suaves, composição limpa. Desenhe SOMENTE os personagens citados. "
     "Sem texto, sem letras, sem números, sem moldura.")
A = ("Cena ilustrada em lápis de cor e aquarela sobre papel creme, no mesmo traço da referência, cenário simples, cores suaves, composição limpa. "
     "SEM personagens, sem pessoas. Sem texto, sem letras, sem números, sem moldura.")
N = " É noite: tons azul-escuros suaves, iluminação quente e amarelada só onde há lanterna ou chama."
ZE="o Zé (camiseta coral com gola azul-marinho, cabelo castanho)"; ESP="a esposa (cabelo castanho ondulado comprido, blusa lilás, saia azul)"
AVO="o avô (careca, cabelo grisalho dos lados, óculos redondos, bigode grisalho, camisa xadrez verde, calça marrom)"; AVOA="a avó (cabelo grisalho em coque, óculos redondos, cardigã rosa, vestido florido)"
THEO="o Theo (menino, cabelo cacheado escuro, camiseta turquesa, bermuda laranja)"; BIA="a Bia (menina, rabo de cavalo preto, vestido amarelo)"
PIP="o cachorro Pipoca (dourado, orelhas caídas, coleira azul)"
P = {
 1:(S,f"Sala de estar à noite, no exato momento em que a luz apaga: {ZE} sentado no sofá olha para a lâmpada do teto, surpreso."+N),
 3:(A,"Rua de bairro brasileiro à noite com todas as casas e postes apagados, só a lua e algumas nuvens iluminando."+N),
 5:(S,f"{BIA} e {THEO} sentados no sofá no escuro, emburrados, o rosto iluminado pela tela de um celular."+N),
 11:(A,"Uma vela caída no chão perto de uma cortina, e uma pequena chama começando a subir pela barra da cortina, numa sala escura."+N),
 15:(A,"Cozinha escura com uma geladeira branca iluminada pela luz da lua que entra pela janela."+N),
 20:(A,"Quintal aberto de dia com uma churrasqueira de tijolos acesa e a fumaça subindo e indo embora com o vento, céu azul."),
 29:(S,f"Sala escura com várias velas acesas espalhadas em pratinhos, uma delas perto da cortina e outra na mesinha; {THEO} passa caminhando perto delas."+N),
 32:(A,"Cidade americana de casas de madeira coberta de neve à noite, todas as janelas e postes apagados, neve caindo."+N),
 42:(A,"Rua à noite durante um temporal com chuva forte, uma árvore caída sobre os fios elétricos de um poste, sem luz nas casas."+N),
 45:(S,f"{ZE} sentado dentro de um carro azul-petróleo estacionado dentro de uma garagem fechada, ligando o cabo do celular no painel do carro."+N),
 48:(S,f"{ESP} abrindo a porta da geladeira no escuro, segurando uma lanterna e olhando dentro."+N),
 57:(S,f"{ZE} na sala escura acende uma lanterna e o facho de luz amarela ilumina a sala."+N),
 59:(S,f"{BIA} e {THEO} no quarto escuro, cada um segurando a sua própria lanterna acesa, sorrindo."+N),
 62:(A,"Quintal de uma casa com um gerador portátil amarelo funcionando bem longe da casa, perto do muro do fundo, com uma linha pontilhada no chão entre o gerador e a janela."),
 65:(S,f"Cozinha escura: {ZE} com a mão na porta da geladeira, parando e pensando antes de abrir, segurando uma lanterna."+N),
 69:(S,f"{ZE} agachado na sala escura, com uma lanterna, tirando o plugue da televisão da tomada da parede."+N),
 72:(S,f"Sala iluminada por uma lanterna: {ESP} com a mão na cabeça, com dor de cabeça; {BIA} bocejando, com sono; uma leve névoa cinza no ar."+N),
 73:(S,f"{PIP} deitado no tapete da sala, desanimado, de olhos meio fechados."+N),
 76:(S,f"{ZE} escancarando uma janela da sala com as duas mãos, o ar fresco da noite entrando."+N),
 78:(S,f"A família saindo pela porta da frente para o quintal à noite, com lanternas: {ZE}, {ESP}, {BIA} e {THEO}."+N),
 82:(S,f"{ZE}, {ESP}, {BIA} e {THEO} saindo rápido pela porta da frente da casa à noite; ao fundo, dentro de casa, um brilho alaranjado de fogo numa cortina."+N),
 85:(S,f"Na cozinha dele, à noite, {AVO} segurando uma caneta de insulina e uma lanterna, olhando para ela pensativo."+N),
 87:(S,f"{AVO} segurando uma caixinha de remédio sobre uma lixeira, em dúvida, na cozinha à luz de uma lanterna."+N),
 94:(S,f"{AVOA} colocando uma caixinha de remédio enrolada num pano dentro de uma caixa de isopor com gelo, na mesa da cozinha."+N),
 97:(S,f"{THEO} olhando fascinado para uma vela acesa sobre a mesa, a uma boa distância, com as mãos para trás."+N),
 98:(S,f"{BIA} e {THEO} fazendo sombras de bichinhos na parede do quarto com as lanternas, rindo."+N),
 99:(A,"Bairro de casas à noite visto de cima, tudo apagado, céu cheio de estrelas e a lua."+N),
 100:(A,"A casa da família num dia de sol, fachada simples com jardim, uma árvore na frente, céu azul."),
 112:(S,f"{PIP} sentado ao lado de um saco de ração e de um galão de água, abanando o rabo, numa despensa."),
 118:(S,f"{ZE} e {ESP} de dia na mesa da cozinha arrumando um kit de emergência: lanterna, pilhas, garrafas de água, rádio e remédios."),
 119:(S,f"A família na sala comemorando com os braços para cima no momento em que a luz da sala acende: {ZE}, {ESP}, {BIA} e {THEO}."),
 122:(S,f"{ZE} na sala religando os aparelhos na tomada, um de cada vez, começando pela televisão."),
 125:(A,"Freezer aberto mostrando pacotes de comida congelada cobertos de cristais de gelo, com um vapor frio saindo."),
 129:(S,f"Num consultório de hospital, um médico (mesmo traço de palito, jaleco branco, estetoscópio) examina {ESP}, sentada na maca."),
 130:(S,f"{ZE} na cozinha com a geladeira aberta, cheirando um pote de comida com a cara desconfiada."),
 141:(S,f"A família toda no quintal ao entardecer, acenando e sorrindo: {ZE}, {ESP}, {BIA}, {THEO}, {AVO}, {AVOA}, {PIP} e um gato cinza."),
}
if __name__=='__main__':
    R=[{'index':k,'params':{'model':'gpt_image_2_5','prompt':v[1]+' '+v[0],'aspect_ratio':'16:9','quality':'medium','resolution':'1k','medias':[{'value':'<ID_DA_FOLHA_DE_PERSONAGENS>','role':'image_references'}]}} for k,v in P.items()]
    print(len(R)); 
    for i in range(0,len(R),12): print(json.dumps(R[i:i+12]))
