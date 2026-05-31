# -*- coding: utf-8 -*-
"""Sixth pass: final sections to 1000+ words + remove duplicate paragraphs."""
import os, re, collections

ROOT = os.path.dirname(os.path.abspath(__file__))

FINAL_BLOCKS = {
"registration.html": (
    "Первый депозит после регистрации в Eva Casino",
    "После подтверждения аккаунта откройте кассу и изучите доступные методы — карты, кошельки, криптовалюта зависят от региона.",
    "Минимальный депозит указан в форме пополнения. Не вносите больше, чем готовы потратить на знакомство с платформой.",
    "Если планируете бонус, активируйте его до перевода средств — иначе начисление может не сработать.",
),
"zerkalo.html": (
    "Сохранение рабочего адреса ева казино",
    "Добавьте проверенное зеркало в закладки браузера с понятным названием — «Eva Casino зеркало», а не набор символов.",
    "Не храните десятки ссылок из форумов: половина из них устареет или окажется фишингом.",
    "При смене адреса удалите старую закладку, чтобы случайно не войти на неактивный домен.",
),
"bets.html": (
    "Популярные виды спорта в ставках Eva Casino",
    "Футбол даёт широкую линию: исход, тотал, форы, статистика игроков. Хоккей и теннис — отдельные вкладки с live-трансляциями где доступно.",
    "Киберспорт растёт в линии: CS2, Dota 2, League of Legends с prematch и live-коэффициентами.",
    "Спецставки на статистику матча требуют понимания правил расчёта — откройте справку «?» у исхода перед подтверждением.",
),
"bonus.html": (
    "Фриспины и турниры в ева казино",
    "Фриспины начисляются на конкретный слот с фиксированной ставкой — изменить её нельзя до отыгрыша.",
    "Турнирные призы делятся между топ-N игроков по таблице лидеров; минимальная ставка для участия указана в правилах.",
    "Комбинировать турнир и активный депозитный бонус можно не всегда — проверьте совместимость в карточках акций Eva Casino.",
),
"casino.html": (
    "Настольные игры RNG в Eva Casino",
    "Рулетка, блэкджек и баккара в цифровой версии работают быстрее live — подходят для коротких сессий.",
    "У RNG-блэкджека можно включить подсказку по базовой стратегии — это обучает, но не гарантирует выигрыш.",
    "Европейская рулетка с одним зеро даёт меньшее преимущество казино, чем американская с двойным зеро — смотрите тип стола в описании.",
),
"download.html": (
    "Обновление приложения Eva Casino",
    "Android: при выходе новой версии сайт показывает уведомление — скачайте APK поверх старой или удалите и установите заново.",
    "iOS PWA обновляется автоматически при открытии сайта — принудительное обновление через очистку кэша Safari.",
    "После обновления выполните вход заново, если сессия сбросилась — это нормально после смены версии.",
),
"reviews.html": (
    "Итоговая оценка Eva Casino для новых игроков",
    "Eva Casino подходит тем, кто хочет казино и ставки в одном аккаунте с русскоязычным интерфейсом.",
    "Перед депозитом прочитайте правила бонусов и подготовьтесь к KYC — это снимает большую часть негатива из отзывов.",
    "Используйте лимиты и демо-слоты для спокойного старта без завышенных ожиданий.",
),
}


def make_section(h2, *paras):
    ps = "".join(f"<p>{p}</p>" for p in paras)
    return f'<section class="section-block"><div class="container"><div class="text-wrap"><h2>{h2}</h2>{ps}</div></div></section>'


def dedup_paragraphs(main):
    seen = set()
    def repl(m):
        inner = m.group(1)
        text = re.sub(r"<[^>]+>", "", inner).strip()
        text = re.sub(r"\s+", " ", text)
        if text in seen:
            return ""
        seen.add(text)
        return m.group(0)
    return re.sub(r"<p>(.*?)</p>", repl, main, flags=re.DOTALL)


for fname, (h2, *paras) in FINAL_BLOCKS.items():
    path = os.path.join(ROOT, fname)
    with open(path, encoding="utf-8") as f:
        html = f.read()
    m = re.search(r"(<main class=\"site-main\">.*?</main>)", html, re.DOTALL)
    main = m.group(1)
    block = make_section(h2, *paras)
    if h2 not in main:
        main = main.replace(
            '<section class="section-block section-cta">',
            block + '\n    <section class="section-block section-cta">',
            1,
        )
    main = dedup_paragraphs(main)
    html = html[: m.start(1)] + main + html[m.end(1) :]
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

for fn in ["official-site.html", "login.html"]:
    path = os.path.join(ROOT, fn)
    with open(path, encoding="utf-8") as f:
        html = f.read()
    m = re.search(r"(<main class=\"site-main\">.*?</main>)", html, re.DOTALL)
    main = dedup_paragraphs(m.group(1))
    html = html[: m.start(1)] + main + html[m.end(1) :]
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

ALL = [
    "official-site.html", "login.html", "registration.html", "zerkalo.html",
    "bets.html", "bonus.html", "casino.html", "download.html", "reviews.html",
]
FORBIDDEN = [
    "Если вы новичок в ева казино", "Так вы избежите сюрпризов при выводе",
    "Площадка имеет понятную структуру", "онлайн-площадка", "рабочий кабинет",
    "маркетинговый лендинг", "корпоративный прокси",
]
print("--- final check ---")
for fn in ALL:
    t = open(os.path.join(ROOT, fn), encoding="utf-8").read()
    m = re.search(r"<main.*?</main>", t, re.S)
    main = m.group(0)
    body = re.sub(r"<[^>]+>", " ", main)
    words = len(re.findall(r"[\w\u0400-\u04FF]+", body))
    bad = [f for f in FORBIDDEN if f.lower() in main.lower()]
    print(f"{fn}: {words}w forbidden={bad}")
