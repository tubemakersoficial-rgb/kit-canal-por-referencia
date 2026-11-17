import json
O="{}. Ilustração isolada em lápis de cor e aquarela, mesmo traço da referência, contorno fino azul-escuro. Inteiro, centralizado, FUNDO TRANSPARENTE, sem texto."
C="{}. Personagem de palito igual à folha de referência: cabeça grande e redonda, olhos de pontinho, braços e pernas de PALITO em linhas finas azul-marinho, lápis de cor e aquarela. Isolado, inteiro, centralizado, FUNDO TRANSPARENTE, sem texto."
FAM='<ID_DA_FOLHA_DE_PERSONAGENS>'; OBJ='<ID_DE_UM_RECORTE_APROVADO>'
CH={'bia_palito':"A Bia, menina de rabo de cavalo preto e vestido amarelo, em pé sorrindo",
'ze_dor':"O Zé (camiseta coral, cabelo castanho) com a mão na testa, com dor de cabeça, olhos apertados",
'dedo_silencio':"O rosto redondo do Zé fazendo sinal de silêncio com o dedo nos lábios, só a cabeça e a mão"}
OB={'aparelho_oxigenio':"Um concentrador de oxigênio doméstico com cateter nasal",'bula':"Uma bula de remédio dobrada, papel com linhas cinzas sem letras legíveis",
'caixa_fosforos':"Uma caixa de fósforos aberta com alguns palitos",'caixa_kit':"Uma caixa organizadora transparente com lanterna, pilhas, garrafas de água, rádio e remédios dentro",
'caixa_remedio':"Uma caixinha de remédio branca e azul, sem letras",'caneta_insulina':"Uma caneta de insulina azul e branca com tampa",
'carne':"Um bife de carne crua numa bandeja",'casa_corte':"Uma casa em corte lateral mostrando garagem, sala e quarto, como uma casinha de bonecas, sem pessoas",
'chama':"Uma chama de fogo amarela e laranja",'churrasqueira':"Uma churrasqueira portátil a carvão com fumacinha",
'copo_trincado':"Um copo de vidro trincado com uma vela dentro e água",'escapamento':"A traseira de um carro azul-petróleo com o escapamento soltando fumaça cinza",
'espiral_zzz':"Espirais de tontura e letras Z de sono flutuando, desenho simples",'fogareiro':"Um fogareiro de camping a gás com chama azul",
'fosforo':"Um palito de fósforo aceso com chama",'frango':"Um frango cru numa bandeja",'freezer_cheio':"Um freezer vertical aberto cheio de pacotes congelados",
'galao_agua':"Um galão de água azul de 20 litros",'gaveta':"Uma gaveta aberta bagunçada com pilhas soltas, fios, papéis e objetos",
'geladeira':"Uma geladeira branca duplex fechada",'geladeira_aberta':"Uma geladeira branca com a porta aberta e comida dentro, com ar frio azul saindo",
'gerador':"Um gerador portátil a gasolina amarelo e preto",'grafico_pizza':"Um gráfico de pizza desenhado à mão com uma fatia de um terço destacada em vermelho e o resto em cinza claro",
'janela_aberta':"Uma janela de madeira escancarada com a cortina balançando ao vento",'latas':"Latas de conserva e pacotes de biscoito empilhados, sem marcas",
'leite':"Uma caixa de leite sem marca",'luz_emergencia':"Uma luz de emergência de parede branca acesa, com dois faróis",
'maquininha':"Uma maquininha de cartão de crédito",'mochila_tatica':"Uma mochila militar tática verde cheia de equipamentos",
'notas_dinheiro':"Um maço de notas de dinheiro coloridas, sem números legíveis",'nuvem_gas':"Uma nuvem de gás cinza translúcida e esfumaçada, desenhada a lápis",
'ondas_som':"Ondas de som curvas saindo de um ponto, desenho simples",'pilhas':"Quatro pilhas AA",'power_bank':"Um carregador portátil (power bank) com cabo",
'radio':"Um rádio portátil de pilha com antena",'televisao':"Uma televisão de tela plana",'termometro':"Um termômetro de cozinha de ponteiro",
'tv_fumaca':"Uma televisão de tela plana com um fiozinho de fumaça e uma faísca saindo de trás",
'vela':"Uma vela branca acesa num pires",'vela_copo':"Uma vela acesa dentro de um copo de vidro com água",'vela_tombada':"Uma vela acesa tombada de lado com a chama pegando num pano"}
R=[{'name':k,'prompt':C.format(v),'ref':FAM} for k,v in CH.items()]+[{'name':k,'prompt':O.format(v),'ref':OBJ} for k,v in OB.items()]
json.dump(R,open('cuts.json','w',encoding='utf-8'),ensure_ascii=False)
for b in range(0,len(R),12):
    print(json.dumps([{'index':k,'params':{'model':'gpt_image_2_5','prompt':R[k]['prompt'],'aspect_ratio':'1:1','quality':'medium','resolution':'1k','background':'transparent','medias':[{'value':R[k]['ref'],'role':'image_references'}]}} for k in range(b,min(b+12,len(R)))]))
