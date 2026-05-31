# -*- coding: utf-8 -*-
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

BLOCKS = {
"bonus.html": (
    "Промокоды ева казино: где и когда вводить",
    "Промокод на регистрации срабатывает один раз — проверьте поле до отправки формы.",
    "Промокод в кассе активирует reload-бонус — введите до подтверждения депозита.",
    "Просроченные коды из старых рассылок не работают — ищите актуальные акции на сайте Eva Casino.",
),
"casino.html": (
    "Сессия в слотах Eva Casino: практические советы",
    "Задайте лимит спинов или времени в голове до запуска — autoplay без лимита быстро расходует баланс.",
    "Перерыв каждые 20–30 минут снижает импульсивные решения о повышении ставки.",
    "Не меняйте слот после каждого проигрыша — дисперсия может развернуться на той же игре.",
),
"download.html": (
    "Экономия трафика в мобильном Eva Casino",
    "Live-игры потребляют больше данных, чем слоты — на лимитном тарифе предпочтите RNG-версии.",
    "Отключите автозагрузку тяжёлых баннеров в настройках браузера, если играете через мобильную версию.",
    "Скачивайте APK только по Wi‑Fi — повторная загрузка при обрыве связи тратит пакет трафика.",
),
"reviews.html": (
    "Когда отзывы о ева казино устаревают",
    "Интерфейс и платёжные методы обновляются — отзыв трёхлетней давности может не отражать текущий Eva Casino.",
    "Жалобы на «долгий вывод» иногда связаны с праздничными днями банка, а не с оператором.",
    "Сверяйте дату отзыва с датой вашего визита — свежий опыт важнее архивных историй.",
),
}

def sec(h2, *ps):
    return '<section class="section-block"><div class="container"><div class="text-wrap"><h2>' + h2 + '</h2>' + ''.join(f'<p>{p}</p>' for p in ps) + '</div></div></section>'

for fname, (h2, *ps) in BLOCKS.items():
    path = os.path.join(ROOT, fname)
    html = open(path, encoding='utf-8').read()
    m = re.search(r'(<main class="site-main">.*?</main>)', html, re.S)
    main = m.group(1)
    if h2 not in main:
        main = main.replace('<section class="section-block section-cta">', sec(h2, *ps) + '\n    <section class="section-block section-cta">', 1)
    open(path, 'w', encoding='utf-8').write(html[:m.start(1)] + main + html[m.end(1):])
    w = len(re.findall(r'[\w\u0400-\u04FF]+', re.sub(r'<[^>]+>', ' ', main)))
    print(fname, w)
