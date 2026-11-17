"""Monta o vídeo atual no DaVinci Resolve (versão gratuita).

Como usar: abra o DaVinci Resolve e clique em Workspace > Scripts > Canal - Montar video.
O script lê o manifesto (~/.canal-por-referencia/manifest_atual.json), cria o projeto, importa a mídia,
monta a timeline e exporta o projeto (.drp) para a pasta do vídeo.

Timeline:  V1 fundo (imagens e clipes) · V2 motion graphics em HTML (PNG com transparência, um clipe por bloco)
           A1 narração · A2 música (já abaixada sob a voz; opcional: sem 'musica' no manifesto, não entra)
No Resolve gratuito, scripts só rodam por dentro do programa (menu Workspace > Scripts).
"""
import json, os

MANIFEST = os.path.join(os.path.expanduser('~'), '.canal-por-referencia', 'manifest_atual.json')

def log(*a):
    print('[Canal]', *a)

def main():
    m = json.load(open(MANIFEST, encoding='utf-8'))
    fps = int(m['fps'])
    pm = resolve.GetProjectManager()  # noqa: F821 (variável global do Resolve)
    name = m['project']
    proj = pm.LoadProject(name)
    if proj:
        name = name + '_novo'
        log('projeto já existia; criando', name)
    proj = pm.CreateProject(name)
    if not proj:
        log('não consegui criar o projeto', name)
        return
    proj.SetSettings({'timelineFrameRate': str(fps), 'timelinePlaybackFrameRate': str(fps),
                      'timelineResolutionWidth': '1920', 'timelineResolutionHeight': '1080'})
    mp = proj.GetMediaPool()
    root = mp.GetRootFolder()

    mp.SetCurrentFolder(mp.AddSubFolder(root, 'V1 fundo'))
    base = mp.ImportMedia([{'FilePath': m['base']}])[0]
    mp.SetCurrentFolder(mp.AddSubFolder(root, 'V2 motion graphics'))
    ovs = []
    for b in m['overlays']:
        items = mp.ImportMedia([{'FilePath': b['pattern'], 'StartIndex': 1, 'EndIndex': b['frames']}])
        ovs.append((b, items[0] if items else None))
    mp.SetCurrentFolder(mp.AddSubFolder(root, 'Audio'))
    voz = mp.ImportMedia([{'FilePath': m['voz']}])[0]
    mus = mp.ImportMedia([{'FilePath': m['musica']}])[0] if m.get('musica') else None

    tl = mp.CreateEmptyTimeline(m['timeline'])
    proj.SetCurrentTimeline(tl)
    while tl.GetTrackCount('video') < 2:
        tl.AddTrack('video')
    while tl.GetTrackCount('audio') < (2 if mus else 1):
        tl.AddTrack('audio', 'stereo')
    tl.SetTrackName('video', 1, 'Fundo')
    tl.SetTrackName('video', 2, 'Motion graphics')
    tl.SetTrackName('audio', 1, 'Narracao')
    if mus:
        tl.SetTrackName('audio', 2, 'Musica')
    t0 = tl.GetStartFrame()

    mp.AppendToTimeline([{'mediaPoolItem': base, 'trackIndex': 1, 'recordFrame': t0, 'mediaType': 1}])
    for b, item in ovs:
        if item is None:
            log('falhou ao importar', b['pattern'])
            continue
        mp.AppendToTimeline([{'mediaPoolItem': item, 'trackIndex': 2, 'recordFrame': t0 + int(round(b['start'] * fps)), 'mediaType': 1}])
    mp.AppendToTimeline([{'mediaPoolItem': voz, 'trackIndex': 1, 'recordFrame': t0, 'mediaType': 2}])
    if mus:
        mp.AppendToTimeline([{'mediaPoolItem': mus, 'trackIndex': 2, 'recordFrame': t0, 'mediaType': 2}])

    pm.SaveProject()
    os.makedirs(os.path.dirname(m['drp']), exist_ok=True)
    ok = pm.ExportProject(name, m['drp'])
    log('timeline montada:', m['timeline'], '| projeto exportado:' if ok else '| falha ao exportar:', m['drp'])

main()
