"""Vídeo 09 (apagão): o que aparece em cada cena, no tempo de cada palavra (usado pelo gen_ref.py)."""
from gen_ref import *

def P(n, color='teal'):
    return FRAME(f'panels/{n:03d}.jpg', 960, 610, 1240, 698, st(n, .05), color)
def CF(n, color='teal'):
    return FRAME(None, 960, 610, 1240, 698, st(n, .05), color)
CLIP_RECT = (340, 261, 1240, 698)

def row(names, keys, sid, y=620, w=300, xs=None, enter='wipe'):
    xs = xs or [round(960 + (k - (len(names) - 1) / 2) * (1680 / len(names))) for k in range(len(names))]
    out = []
    for n, k, x in zip(names, keys, xs):
        at = st(sid, .1) if k is None else (k if isinstance(k, float) else wt(sid, k))
        out.append(CUT(n, x, y, w, at, enter=enter))
    return out, xs

def GAS(x, y, w, at, dur=2.0):        # nuvem de gás que flutua
    return MOVE('nuvem_gas', [(x - 60, y + 30), (x, y), (x + 60, y - 20)], w, at, dur)

SPEC = {}
S = SPEC

# ---------------------------------------------------------------- bloco 1: gancho
S[1] = [T('20H'), CF(1)]
S[2] = [T('SILÊNCIO'), CUT('geladeira', 820, 650, 360, st(2, .05)), CUT('ondas_som', 1200, 560, 260, st(2, .1), wiggle=True),
        XX(1200, 560, 150, wt(2, 'barulho'))]
S[3] = [T('RUA ESCURA'), CF(3)]
S[4] = [T('10 MIN... 30 MIN'), CUT('relogio', 760, 640, 400, st(4, .05), wiggle=True),
        COUNTER(10, 30, 1300, 620, 200, wt(4, 'depois'), wt(4, 'volta'), suf=' min'), XX(1300, 860, 120, wt(4, 'volta', d=.3))]
S[5] = [T('15%'), CF(5)]
S[6] = [T('SÓ ESPERAR?'), CUT('relogio', 760, 640, 360, st(6, .1)), CUT('placa_alerta', 1280, 620, 320, wt(6, 'perigos'), wiggle=True)]
S[7] = [T('UMA ÚNICA COISA'), CUT('cerebro', 900, 640, 500, st(7, .1), wiggle=True),
        T('?', 1380, 560, 220, wt(7, 'coisa'), ticks=False, color=RED)]
S[8] = [T('ACENDER.', px=150), CUT('fosforo', 960, 660, 380, st(8, .02), enter='pop', wiggle=True)]
r, xs = row(['vela', 'fogareiro', 'carro'], ['vela', 'fogareiro', 'carro'], 9, w=360)
S[9] = [T('VELA, FOGAREIRO, CARRO')] + r
S[10] = [T('O ERRO QUE MAIS MATA', color=RED), CUT('casa', 960, 660, 520, st(10, .05)), CUT('chama', 960, 640, 200, wt(10, 'fogo'), enter='pop', wiggle=True),
         NO(960, 640, 290, wt(10, 'erro'))]
S[11] = [T('INCÊNDIO', color=RED), CF(11, 'red')]
S[12] = [T('SEM COR, SEM CHEIRO'), CUT('fogareiro', 560, 700, 300, st(12, .05)), GAS(980, 560, 420, wt(12, 'gas'), 2.4),
         CUT('nariz_fumaca', 1460, 520, 220, wt(12, 'cheiro')), XX(1460, 520, 130, wt(12, 'cheiro', d=.3))]
S[13] = [T('DORMINDO'), CUT('cama', 960, 700, 640, st(13, .05)), GAS(980, 480, 380, wt(13, 'mata'), 2.0)]
S[14] = [T('UM PLANO'), CUT('prancheta', 960, 640, 420, st(14, .1)), CHECK(1220, 460, 130, wt(14, 'plano'))]
S[15] = [T('QUE APARELHO?'), CF(15), T('?', 1580, 420, 200, wt(15, 'aparelho'), ticks=False, color=RED)]
S[16] = [T('QUANDO A LUZ VOLTA'), CUT('lampada', 960, 620, 380, st(16, .05)), FLASH(wt(16, 'volta')), T('?', 1300, 520, 200, wt(16, 'erro'), ticks=False, color=RED)]
S[17] = [T('R$ 5'), CUT('moedas', 900, 680, 380, st(17, .05), enter='pop'), T('?', 1300, 520, 220, wt(17, 'item'), ticks=False, color=RED),
         TAG('SUBSTITUI TODAS AS VELAS', 960, 950, 52, wt(17, 'substitui'))]

# ---------------------------------------------------------------- bloco 2: o perigo invisível
S[18] = [T('O FOGO RESPIRA'), CUT('chama', 760, 640, 300, st(18, .05), wiggle=True), CUT('pulmoes', 1260, 640, 360, wt(18, 'respirando'), beat=True)]
S[19] = [T('CONSOME O OXIGÊNIO'), CUT('chama', 960, 660, 300, st(19, .05), wiggle=True),
         ARROW(560, 640, 840, 660, wt(19, 'oxigenio'), bend=-.1, color=GREEN), TAG('OXIGÊNIO', 600, 540, 50, wt(19, 'oxigenio')),
         GAS(1360, 500, 340, wt(19, 'gas'), 1.8)]
S[20] = [T('AO AR LIVRE'), CF(20, 'green')]
S[21] = [T('SE ACUMULA', color=RED), CUT('casa_corte', 960, 660, 820, st(21, .05)), GAS(800, 640, 300, wt(21, 'casa'), 1.6),
         GAS(1100, 600, 340, wt(21, 'fechadas'), 1.6), GAS(960, 700, 420, wt(21, 'acumula'), 1.6)]
S[22] = [T('MONÓXIDO DE CARBONO', px=104), CUT('nuvem_gas', 960, 640, 640, st(22, .05), wiggle=True), TAG('CO', 960, 640, 120, wt(22, 'monoxido'))]
S[23] = [T('NO LUGAR DO OXIGÊNIO'), CUT('coracao', 760, 640, 380, st(23, .05), beat=True), ARROW(980, 640, 1180, 640, wt(23, 'sangue'), bend=0),
         CUT('nuvem_gas', 1380, 620, 300, wt(23, 'lugar'))]
S[24] = [T('DOR DE CABEÇA'), CUT('ze_dor', 960, 650, 340, st(24, .05), wiggle=True)]
r, xs = row(['espiral_zzz', 'balde', 'cama'], ['tontura', 'enjoo', 'sono'], 25, w=340)
S[25] = [T('TONTURA, ENJOO, SONO')] + r
S[26] = [T('NÃO ACORDA', color=RED), CUT('cama', 900, 700, 600, st(26, .05)), GAS(900, 500, 340, st(26, .2), 2.0),
         CUT('despertador', 1420, 600, 240, wt(26, 'acorda'), wiggle=True)]
S[27] = [T('ASSASSINO SILENCIOSO'), CUT('nuvem_gas', 760, 620, 460, st(27, .05), wiggle=True), CUT('dedo_silencio', 1320, 640, 300, wt(27, 'silencioso'))]
S[28] = [T('A VELA'), CUT('vela', 960, 650, 300, st(28, .05), wiggle=True)]
S[29] = [T('VELAS POR TODA PARTE'), CF(29, 'red')]
S[30] = [T('UM ESBARRÃO'), CUT('vela', 760, 650, 280, st(30, .05)), ARROW(900, 560, 1120, 640, wt(30, 'esbarrao'), bend=.25, color=RED),
         CUT('vela_tombada', 1320, 700, 360, wt(30, 'fogo'), enter='pop')]

# ---------------------------------------------------------------- bloco 3: a prova
S[31] = [T('EM GRANDE ESCALA'), CUT('lupa', 960, 640, 420, st(31, .1), wiggle=True)]
S[32] = [T('TEXAS, 2021'), CF(32)]
S[33] = [T('DENTRO DE CASA', color=RED), CUT('casa_corte', 960, 660, 780, st(33, .05)), CUT('gerador', 760, 760, 220, wt(33, 'geradores'), enter='pop'),
         CUT('churrasqueira', 1160, 740, 220, wt(33, 'churrasqueiras'), enter='pop'), NO(960, 700, 300, wt(33, 'garagem'))]
S[34] = [T('+1.400'), CUT('hospital', 760, 650, 460, st(34, .05)), COUNTER(0, 1400, 1320, 640, 180, st(34, .4), en(34, .4)),
         TAG('INTOXICADOS', 1320, 820, 54, wt(34, 'intoxicacao'))]
S[35] = [T('10 MORTES', color=RED), CUT('gerador', 960, 650, 440, st(35, .05)), XX(960, 640, 230, wt(35, 'geradores'))]
S[36] = [T('O BRASIL NO ESCURO'), CUT('mapa_brasil', 960, 660, 560, st(36, .05)), DARK(960, 660, 600, 600, wt(36, 'escuro'))]
S[37] = [T('2009: 18 ESTADOS'), CUT('mapa_brasil', 760, 660, 480, st(37, .05)), COUNTER(0, 18, 1320, 640, 220, wt(37, 'apagao'), wt(37, 'estados'))]
S[38] = [T('2023: 25 ESTADOS + DF'), CUT('mapa_brasil', 760, 660, 480, st(38, .05)), COUNTER(0, 25, 1320, 640, 220, wt(38, 'luz'), wt(38, 'estados')),
         TAG('+ DF', 1320, 820, 60, wt(38, 'distrito'))]
S[39] = [T('BOATO DO DIA 17'), CUT('celular', 760, 640, 300, st(39, .05)), CUT('balao', 1020, 480, 220, wt(39, 'redes'), wiggle=True),
         CUT('calendario', 1380, 640, 320, wt(39, 'marcado'))]
S[40] = [T('SEM AVISO OFICIAL'), CUT('prancheta', 960, 640, 400, st(40, .1)), XX(960, 640, 220, wt(40, 'aviso'))]
S[41] = [T('NÃO MARCA DATA'), CUT('calendario', 960, 640, 400, st(41, .1)), XX(960, 640, 220, wt(41, 'data'))]
S[42] = [T('TEMPORAL'), CF(42, 'red')]
S[43] = [T('APRENDA ANTES', color=GREEN), CHECK(960, 640, 260, st(43, .2))]

# ---------------------------------------------------------------- bloco 4: os três truques falsos
S[44] = [T('3 TRUQUES FALSOS')] + [CARD(str(j + 1), x, 640, 300, st(44, .3 + .4 * j)) for j, x in enumerate([560, 960, 1360])]
S[45] = [T('1. CARRO NA GARAGEM'), CF(45, 'red')]
S[46] = [T('O MESMO GÁS'), CUT('escapamento', 760, 660, 480, st(46, .05)), GAS(1200, 600, 380, wt(46, 'escapamento'), 2.0)]
S[47] = [T('EM MINUTOS', color=RED), CUT('casa_corte', 960, 660, 820, st(47, .05)),
         ARROW(620, 780, 1300, 560, wt(47, 'entra'), bend=-.2, color=GRAY), CUT('relogio', 1600, 420, 180, wt(47, 'minutos'), enter='pop')]
S[48] = [T('2. ABRIR A GELADEIRA'), CF(48, 'red')]
S[49] = [T('O FRIO VAI EMBORA'), CUT('geladeira_aberta', 900, 650, 420, st(49, .05)),
         MOVE('gota', [(1080, 600), (1500, 520)], 90, wt(49, 'abre'), 1.0, n=3, gap=.3)]
S[50] = [T('ESTRAGA MAIS RÁPIDO'), CUT('carne', 760, 650, 320, st(50, .05)), CUT('relogio', 1260, 640, 320, wt(50, 'estragar'), wiggle=True)]
S[51] = [T('3. VELA NO COPO'), CARD('3', 560, 640, 260, st(51, .05)), CUT('vela_copo', 1200, 650, 320, wt(51, 'vela')),
         T('?', 1440, 480, 160, wt(51, 'segura'), ticks=False, color=RED)]
S[52] = [T('TRINCA', color=RED), CUT('copo_trincado', 960, 650, 380, st(52, .05), wiggle=True)]
S[53] = [T('VELA NO QUARTO NÃO', color=RED), CUT('cama', 820, 700, 520, st(53, .05)), CUT('vela', 1320, 640, 220, wt(53, 'vela')),
         NO(1320, 640, 170, wt(53, 'incendio'))]
S[54] = [T('1 EM CADA 3'), CUT('grafico_pizza', 760, 640, 420, st(54, .05)), CUT('cama', 1320, 680, 380, wt(54, 'quarto'))]

# ---------------------------------------------------------------- bloco 5: os quatro passos
S[55] = [T('A SEQUÊNCIA'), ROWS([('lanterna', '1. LUZ SEM FOGO'), ('churrasqueira', '2. FOGO SÓ LÁ FORA'), ('geladeira', '3. GELADEIRA FECHADA'),
                                 ('plugue', '4. DESLIGUE DA TOMADA')], st(55, .1), en(55), top=300, step=150)]
S[56] = [T('1. LUZ SEM FOGO'), NUM('1', 600, 620, st(56, .05), 180), CUT('lanterna', 1200, 640, 380, wt(56, 'luz'), enter='pop')]
S[57] = [T('A LANTERNA', color=GREEN), CF(57, 'green')]
S[58] = [T('LANTERNA OU LUZ DE EMERGÊNCIA', px=96), CUT('lanterna', 760, 640, 340, st(58, .05)), CUT('luz_emergencia', 1260, 640, 360, wt(58, 'emergencia'))]
S[59] = [T('UMA EM CADA QUARTO'), CF(59, 'green')]
S[60] = [T('2. FOGO SÓ LÁ FORA'), NUM('2', 560, 620, st(60, .05), 180), CUT('churrasqueira', 1000, 650, 340, wt(60, 'fogo')),
         ARROW(1200, 640, 1520, 640, wt(60, 'fora'), bend=0, color=GREEN)]
r, xs = row(['gerador', 'churrasqueira', 'fogareiro', 'carro'], ['gerador', 'churrasqueira', 'fogareiro', 'carro'], 61, w=300)
S[61] = [T('AO AR LIVRE')] + r
S[62] = [T('6 METROS'), CF(62, 'green'), TAG('+6 M', 1500, 380, 70, wt(62, 'metros'))]
S[63] = [T('NUNCA NA GARAGEM', color=RED), CUT('casa_corte', 960, 660, 720, st(63, .05)), CUT('gerador', 700, 760, 200, st(63, .2)),
         NO(700, 740, 160, wt(63, 'garagem'))]
S[64] = [T('3. GELADEIRA FECHADA'), NUM('3', 600, 620, st(64, .05), 180), CUT('geladeira', 1200, 650, 360, wt(64, 'geladeira')),
         CHECK(1400, 440, 120, wt(64, 'fechada'))]
S[65] = [T('NÃO ABRA'), CF(65, 'green')]
S[66] = [T('4 HORAS'), CUT('geladeira', 760, 650, 380, st(66, .05)), CUT('relogio', 1260, 600, 260, wt(66, 'conserva')),
         COUNTER(0, 4, 1260, 840, 120, wt(66, 'conserva'), wt(66, 'horas'), suf=' h')]
S[67] = [T('48 HORAS'), CUT('freezer_cheio', 760, 650, 400, st(67, .05)), COUNTER(0, 48, 1300, 640, 200, wt(67, 'aguenta'), wt(67, 'horas'), suf=' h'),
         TAG('SE NINGUÉM ABRIR', 1300, 830, 50, wt(67, 'ninguem'))]
S[68] = [T('4. DESLIGUE DA TOMADA'), CUT('tomada', 760, 640, 340, st(68, .05)),
         MOVE('plugue', [(1000, 640), (1360, 640)], 260, wt(68, 'desligue'), .8)]
S[69] = [T('TIRE TUDO'), CF(69)]
S[70] = [T('UMA LÂMPADA DE AVISO'), CUT('lampada', 960, 620, 380, st(70, .05)), CHECK(1240, 440, 130, wt(70, 'avisar'))]

# ---------------------------------------------------------------- bloco 6: e se der errado?
S[71] = [T('PASSOU MAL?'), CUT('ze_dor', 960, 650, 320, st(71, .05)), T('?', 1300, 520, 200, wt(71, 'mal'), ticks=False, color=RED)]
S[72] = [T('SINAL DE ALARME', color=RED), P(72, 'red')]
S[73] = [T('O CACHORRO TAMBÉM'), P(73, 'red')]
S[74] = [T('DEITAR?'), CUT('cama', 960, 680, 560, st(74, .05)), T('?', 1340, 520, 200, wt(74, 'deitar'), ticks=False, color=RED)]
S[75] = [T('NÃO DEITE', color=RED), CUT('cama', 960, 680, 560, st(75, .05)), NO(960, 660, 300, wt(75, 'pior'))]
S[76] = [T('ABRA TUDO', color=GREEN), CF(76, 'green')]
S[77] = [T('DESLIGUE'), CUT('fogareiro', 960, 650, 400, st(77, .05)), XX(960, 640, 220, wt(77, 'queimando'))]
S[78] = [T('AR LIVRE', color=GREEN), CF(78, 'green')]
S[79] = [T('SAMU 192'), CUT('celular_192', 960, 640, 420, st(79, .05), beat=True)]
S[80] = [T('193 + MASSAGEM'), CUT('celular_193', 700, 640, 340, wt(80, 'bombeiros'), beat=True), CUT('maos_rcp', 1260, 660, 440, wt(80, 'massagem')),
         PRESS(1260, 610, wt(80, 'massagem', d=.3))]
S[81] = [T('INCÊNDIO?', color=RED), CUT('vela_tombada', 960, 680, 460, st(81, .05)), T('?', 1300, 500, 200, wt(81, 'incendio'), ticks=False, color=RED)]
S[82] = [T('SAIA PRIMEIRO', color=GREEN), P(82, 'green')]
S[83] = [T('FECHE A PORTA'), CUT('porta', 820, 650, 360, st(83, .05)), CUT('televisao', 1320, 640, 300, wt(83, 'objetos')), XX(1320, 640, 170, wt(83, 'volte')),
         CHECK(820, 420, 130, wt(83, 'feche'))]

# ---------------------------------------------------------------- bloco 7: mude a cena: o remédio
S[84] = [T('MUDE A CENA'), CUT('caneta_insulina', 960, 640, 440, st(84, .1), wiggle=True)]
S[85] = [T('O SEU PAI'), CF(85)]
S[86] = [T('6 HORAS'), CUT('relogio', 760, 640, 380, st(86, .05), wiggle=True), COUNTER(0, 6, 1260, 640, 220, wt(86, 'caiu'), wt(86, 'horas'), suf=' h')]
S[87] = [T('JOGAR FORA?', color=RED), P(87, 'red')]
S[88] = [T('NO SOL?', color=RED), CUT('janela_sol', 820, 640, 460, st(88, .05)), CUT('caixa_remedio', 1300, 680, 260, wt(88, 'caixa')),
         XX(1300, 680, 150, wt(88, 'esquecida'))]
S[89] = [T('DOIS ERROS', color=RED), XX(800, 640, 220, st(89, .3)), XX(1120, 640, 220, wt(89, 'erros'))]
S[90] = [T('LUGAR FRESCO'), CUT('caneta_insulina', 760, 640, 400, st(90, .05)), CUT('termometro', 1260, 640, 300, wt(90, 'fresco'), wiggle=True)]
S[91] = [T('CONFIRA A BULA'), CUT('bula', 900, 650, 460, st(91, .05)), CUT('lupa', 1260, 600, 300, wt(91, 'bula'), enter='pop')]
S[92] = [T('FAÇA ASSIM', color=GREEN), CHECK(960, 640, 240, st(92, .2))]
S[93] = [T('1. GELADEIRA FECHADA'), CUT('caixa_remedio', 760, 660, 280, st(93, .05)), CUT('geladeira', 1260, 650, 340, wt(93, 'geladeira')),
         ARROW(920, 640, 1100, 640, wt(93, 'dentro'), bend=0)]
S[94] = [T('2. ISOPOR COM GELO'), CF(94, 'green')]
S[95] = [T('3. UM PLANO'), CUT('aparelho_oxigenio', 760, 650, 380, wt(95, 'aparelho')), ARROW(980, 640, 1160, 640, wt(95, 'plano'), bend=0),
         CUT('hospital', 1360, 650, 380, wt(95, 'luz'))]
S[96] = [T('AS CRIANÇAS'), CUT('bia_palito', 820, 660, 260, st(96, .05)), CUT('theo_palito', 1120, 670, 240, st(96, .2))]
S[97] = [T('BRINCADEIRA?', color=RED), P(97, 'red')]
S[98] = [T('LANTERNA NA MÃO', color=GREEN), CF(98, 'green')]

# ---------------------------------------------------------------- bloco 8: dentro de casa: o kit
S[99] = [T('ATÉ AQUI'), CF(99)]
S[100] = [T('NUM DIA COMUM'), CF(100, 'green')]
S[101] = [T('O KIT', color=GREEN), CUT('caixa_kit', 960, 650, 480, st(101, .05), enter='pop')]
S[102] = [T('SEM EXAGERO'), CUT('mochila_tatica', 960, 650, 400, st(102, .05)), XX(960, 640, 220, wt(102, 'guerra'))]
S[103] = [T('1. ÁGUA'), CUT('galao_agua', 960, 650, 380, st(103, .05), enter='pop')]
S[104] = [T('4 L POR PESSOA POR DIA', px=104), CUT('galao_agua', 760, 650, 340, st(104, .05)), CUT('boneco_palito', 1160, 660, 220, wt(104, 'pessoa')),
          COUNTER(0, 4, 1500, 640, 160, wt(104, 'litros'), wt(104, 'dia'), suf=' L')]
S[105] = [T('~50 LITROS')] + [CUT('boneco_palito', 480 + 150 * j, 660, 140, st(105, .1 + .12 * j), enter='pop') for j in range(4)] + \
          [CUT('galao_agua', 1360, 650, 300, wt(105, 'precisa')), COUNTER(0, 48, 1360, 880, 90, wt(105, 'precisa'), en(105, .3), suf=' L')]
S[106] = [T('LANTERNA E PILHAS'), CUT('lanterna', 760, 640, 340, st(106, .05)), CUT('pilhas', 1260, 660, 300, wt(106, 'pilhas'), enter='pop')]
S[107] = [T('CARREGADOR'), CUT('power_bank', 960, 650, 360, st(107, .05), enter='pop')]
S[108] = [T('RÁDIO DE PILHA'), CUT('radio', 960, 650, 400, st(108, .05), wiggle=True)]
S[109] = [T('COMIDA PRONTA'), CUT('latas', 960, 660, 460, st(109, .05), enter='pop')]
S[110] = [T('REMÉDIOS'), CUT('caixa_remedio', 960, 660, 400, st(110, .05), enter='pop')]
S[111] = [T('DINHEIRO'), CUT('notas_dinheiro', 760, 650, 380, st(111, .05)), CUT('maquininha', 1280, 650, 300, wt(111, 'maquininha')),
          XX(1280, 650, 160, wt(111, 'apaga'))]
S[112] = [T('A RAÇÃO'), CF(112, 'green')]
S[113] = [T('SINAIS'), CUT('placa_alerta', 960, 640, 400, st(113, .05), beat=True)]
S[114] = [T('ONDE ESTÁ?'), CUT('gaveta', 900, 660, 460, st(114, .05)), T('?', 1300, 520, 200, wt(114, 'lanternas'), ticks=False, color=RED)]
S[115] = [T('O QUADRO DE LUZ'), CUT('quadro_luz', 900, 650, 380, st(115, .05)), T('?', 1260, 500, 200, wt(115, 'quadro'), ticks=False, color=RED)]
S[116] = [T('BATERIA NO FIM'), CUT('celular', 820, 650, 300, st(116, .05)), CUT('bateria', 1260, 640, 260, wt(116, 'bateria'), beat=True)]
S[117] = [T('SÓ FÓSFOROS?'), CUT('caixa_fosforos', 960, 650, 380, st(117, .05), wiggle=True)]
S[118] = [T('PREPARE ANTES', color=GREEN), CF(118, 'green')]

# ---------------------------------------------------------------- bloco 9: quando a luz volta
S[119] = [T('A LUZ VOLTOU!', color=GREEN), CF(119, 'green')]
S[120] = [T('O ERRO DA VOLTA'), CUT('lampada', 960, 620, 360, st(120, .05)), T('!', 1260, 500, 220, wt(120, 'erro'), ticks=False, color=RED)]
S[121] = [T('PICO DE TENSÃO', color=RED), CUT('tomada', 700, 640, 300, st(121, .05)),
          MOVE('raio', [(840, 600), (1000, 600), (1160, 600)], 140, wt(121, 'oscilacoes'), 1.0, n=3, gap=.25),
          CUT('tv_fumaca', 1340, 640, 360, wt(121, 'queimam'))]
S[122] = [T('AOS POUCOS'), CF(122, 'green')]
S[123] = [T('A COMIDA'), CUT('geladeira', 960, 650, 400, st(123, .05))]
r, xs = row(['carne', 'leite', 'frango'], ['carne', 'leite', 'frango'], 124, y=600, w=260, xs=[560, 860, 1160])
S[124] = [T('+4 °C POR +2 H')] + r + [CUT('termometro', 1480, 600, 220, wt(124, 'graus')), CUT('lixeira', 1480, 860, 200, wt(124, 'lixo'), enter='pop')]
S[125] = [T('CRISTAIS DE GELO'), CF(125, 'green')]
S[126] = [T('NÃO PROVE', color=RED), CUT('boca', 960, 640, 400, st(126, .05)), NO(960, 640, 240, wt(126, 'prove'))]
S[127] = [T('SEM CHEIRO'), CUT('bacterias', 760, 640, 360, st(127, .05), wiggle=True), CUT('nariz_fumaca', 1260, 640, 300, wt(127, 'cheiro')),
          XX(1260, 640, 160, wt(127, 'gosto'))]
sy = [(380, 'DIARREIA'), (520, 'VÔMITO'), (660, 'FEBRE')]
S[128] = [T('PROCURE ATENDIMENTO')] + [TAG(t, 700, y, 62, wt(128, k)) for (y, t), k in zip(sy, ['diarreia', 'vomito', 'febre'])] + \
          [CUT('hospital', 1300, 640, 420, wt(128, 'atendimento'))]
S[129] = [T('HOSPITAL'), CF(129, 'green')]
S[130] = [T('"DEIXA EU CHEIRAR"', px=104, color=RED), P(130, 'red'), XX(1450, 450, 180, wt(130, 'cheirar', d=.3))]

# ---------------------------------------------------------------- bloco 10: a regra completa
S[131] = [T('A REGRA COMPLETA'), CUT('prancheta', 960, 640, 420, st(131, .1))]
S[132] = [T('LANTERNA, NÃO VELA'), CUT('lanterna', 760, 640, 340, wt(132, 'lanterna')), CHECK(760, 440, 120, wt(132, 'lanterna', d=.2)),
          CUT('vela', 1260, 650, 260, wt(132, 'vela')), XX(1260, 650, 160, wt(132, 'vela', d=.2))]
S[133] = [T('SÓ AO AR LIVRE'), CUT('gerador', 760, 660, 320, st(133, .05)), ARROW(960, 640, 1240, 640, wt(133, 'livre'), bend=0, color=GREEN),
          CUT('casa', 1440, 660, 300, wt(133, 'janelas'))]
S[134] = [T('GELADEIRA FECHADA · TOMADAS FORA', px=92), CUT('geladeira', 620, 650, 300, wt(134, 'geladeira')), CUT('plugue', 1000, 650, 260, wt(134, 'tomadas')),
          CUT('lampada', 1360, 620, 260, wt(134, 'lampada'))]
S[135] = [T('AR LIVRE + 192'), CUT('janela_aberta', 760, 640, 360, st(135, .05)), CUT('celular_192', 1260, 640, 320, wt(135, 'samu'), beat=True)]
S[136] = [T('ISOPOR · KIT'), CUT('isopor', 760, 660, 340, wt(136, 'remedio')), CUT('caixa_kit', 1260, 660, 380, wt(136, 'antes'))]
S[137] = [T('NA DÚVIDA, JOGUE FORA', px=104), ROWS([('lanterna', 'LANTERNA, NÃO VELA'), ('gerador', 'FOGO SÓ AO AR LIVRE'), ('geladeira', 'GELADEIRA FECHADA'),
                                                  ('plugue', 'TOMADAS DESLIGADAS'), ('celular_192', 'PASSOU MAL? AR LIVRE + 192'),
                                                  ('caixa_kit', 'KIT PRONTO ANTES'), ('lixeira', 'NA DÚVIDA, JOGUE FORA')], st(137, .1), en(137))]

# ---------------------------------------------------------------- bloco 11: fechamento
S[138] = [T('QUAL ERRO?'), CUT('ze_pensa', 960, 650, 320, st(138, .1))]
S[139] = [T('3 ERROS')] + [CARD(t, x, 640, 300, wt(139, k)) for t, x, k in [('1', 560, 'acender'), ('2', 960, 'ligar'), ('3', 1360, 'abrir')]] + \
         [TAG(t, x, 880, 46, wt(139, k, d=.2)) for t, x, k in [('VELAS', 560, 'acender'), ('CARRO', 960, 'ligar'), ('GELADEIRA', 1360, 'abrir')]]
S[140] = [T('COMENTE'), CUT('balao', 760, 640, 360, st(140, .1), wiggle=True), CUT('balao', 1240, 600, 300, st(140, .5), flip=True)]
S[141] = [T('SE CUIDA'), CF(141)]
S[142] = [T('INSCREVA-SE'), CUT('ze_acena', 700, 650, 320, st(142, .1)), BTN('INSCREVA-SE', 1300, 640, wt(142, 'inscreva'))]
S[143] = [T('O INSTINTO: ACENDER'), CUT('fosforo', 960, 660, 340, st(143, .1)), NO(960, 640, 260, wt(143, 'fogo'))]
S[144] = [T('CHOQUE? NÃO ENCOSTE', px=104, color=RED), P(144, 'red')]
S[145] = [T('ASSISTA AQUI'), CUT('ze_aponta', 700, 650, 320, st(145, .1)), ARROW(900, 600, 1500, 600, wt(145, 'video'), bend=0)]
S[146] = [T('SE CUIDA!'), CUT('ze_acena', 960, 650, 340, st(146, .1), wiggle=True)]

# ---------------------------------------------------------------- palco nunca vazio
def _t(e): return e.get('at') if e.get('at') is not None else e.get('t0')
for _sid, _els in S.items():
    if any(e['k'] == 'FRAME' for e in _els):
        continue
    _vis = [e for e in _els if e['k'] != 'T' and _t(e) is not None]
    if not _vis:
        continue
    _first = min(_vis, key=_t)
    if _t(_first) > st(_sid, .7):
        if _first.get('at') is not None: _first['at'] = st(_sid, .1)
        else: _first['t0'] = st(_sid, .1)

CLIPS = [1, 3, 5, 11, 15, 20, 29, 32, 42, 45, 48, 57, 59, 62, 65, 69, 76, 78, 85, 94, 98, 99, 100, 112, 118, 119, 122, 125, 129, 141]
