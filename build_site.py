#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Eva Casino SEO pages."""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
AFF = "https://lkga.cc/0b02c9ea"
DOMAIN = "https://evacasino1.vercel.app"
OG_IMAGE = f"{DOMAIN}/assets/img/eva-banner.png"
LOGO_URL = f"{DOMAIN}/assets/img/logo.png"
DATE = "2026-05-17"

NAV = [
    ("/official-site/", "Официальный сайт"),
    ("/casino/", "Казино"),
    ("/bonus/", "Бонусы"),
    ("/registration/", "Регистрация"),
    ("/zerkalo/", "Зеркало"),
    ("/bets/", "Ставки"),
    ("/download/", "Скачать"),
    ("/login/", "Вход"),
    ("/reviews/", "Отзывы"),
]

RELATED = [
    ("/official-site/", "Официальный сайт"),
    ("/login/", "Вход"),
    ("/registration/", "Регистрация"),
    ("/zerkalo/", "Зеркало"),
    ("/bonus/", "Бонусы"),
    ("/casino/", "Казино"),
    ("/download/", "Скачать"),
    ("/bets/", "Ставки"),
    ("/reviews/", "Отзывы"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def faq_html(faq):
    items = []
    for q, a in faq:
        items.append(f'<div class="faq-item"><h3>{esc(q)}</h3><p>{a}</p></div>')
    return "\n".join(items)


def faq_schema(faq):
    def strip_html(s):
        return re.sub(r"<[^>]+>", "", s).strip()

    return [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": strip_html(a)},
        }
        for q, a in faq
    ]


def sections_html(sections):
    blocks = []
    for h2, paragraphs in sections:
        ps = "".join(f"<p>{p}</p>" for p in paragraphs)
        blocks.append(
            f'<section class="section-block"><div class="container"><div class="text-wrap">'
            f"<h2>{esc(h2)}</h2>{ps}</div></div></section>"
        )
    return "\n".join(blocks)


def related_html(current_path):
    links = [f'<a href="{href}">{label}</a>' for href, label in RELATED if href != current_path]
    return (
        '<section class="section-block section-related">'
        '<div class="container"><div class="text-wrap">'
        "<h2>Полезные разделы ева казино</h2>"
        f'<nav class="related-links" aria-label="Связанные разделы">{"".join(links)}</nav>'
        "</div></div></section>"
    )


def schema_graph(page):
    url = page["canonical"]
    graph = [
        {
            "@type": "WebSite",
            "@id": f"{DOMAIN}/#website",
            "url": f"{DOMAIN}/",
            "name": "Eva Casino",
            "inLanguage": "ru-RU",
        },
        {
            "@type": "Organization",
            "@id": f"{DOMAIN}/#organization",
            "name": "Eva Casino",
            "url": f"{DOMAIN}/",
            "logo": {"@type": "ImageObject", "url": LOGO_URL},
        },
        {
            "@type": "WebPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": page["title"],
            "description": page["description"],
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "inLanguage": "ru-RU",
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{DOMAIN}/"},
            ]
            + (
                [{"@type": "ListItem", "position": 2, "name": page["bc_name"], "item": url}]
                if page.get("bc_name") != "Главная"
                else []
            ),
        },
    ]
    if page.get("faq"):
        graph.append({"@type": "FAQPage", "mainEntity": faq_schema(page["faq"])})
    if page.get("article"):
        graph.append(
            {
                "@type": "Article",
                "headline": page["h1"],
                "description": page["description"],
                "author": {"@type": "Organization", "name": "Eva Casino"},
                "publisher": {"@type": "Organization", "name": "Eva Casino", "logo": {"@type": "ImageObject", "url": LOGO_URL}},
                "datePublished": DATE,
                "dateModified": DATE,
                "inLanguage": "ru-RU",
                "mainEntityOfPage": {"@id": f"{url}#webpage"},
            }
        )
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)


def render(page):
    nav = "".join(f'<a href="{h}">{l}</a>' for h, l in NAV)
    footer_nav = "".join(f'<a href="{h}">{l}</a>' for h, l in NAV)
    mid_cta = ""
    if page.get("mid_cta"):
        mid_cta = (
            '<section class="section-block section-cta">'
            '<div class="container"><div class="text-wrap text-center">'
            f'<a class="btn btn--primary" href="{AFF}" target="_blank" rel="nofollow sponsored noopener">{esc(page["mid_cta"])}</a>'
            "</div></div></section>"
        )
    trust = (
        '<section class="trust-block"><div class="container">'
        '<p class="trust-line"><span>18+</span><span>Ответственная игра</span><span>Актуальная информация</span></p>'
        "</div></section>"
    )
    faq_sec = ""
    if page.get("faq"):
        faq_sec = (
            f'<section class="section-block"><div class="container"><div class="text-wrap">'
            f'<h2>{esc(page.get("faq_h2", "Частые вопросы о ева казино"))}</h2>'
            f'<div class="faq">{faq_html(page["faq"])}</div></div></div></section>'
        )
    intro = "".join(f'<p class="lead">{p}</p>' for p in page.get("intro", []))
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <title>{esc(page["title"])}</title>
  <meta name="description" content="{esc(page["description"])}">
  <link rel="canonical" href="{page["canonical"]}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{page["canonical"]}">
  <meta property="og:title" content="{esc(page["title"])}">
  <meta property="og:description" content="{esc(page["description"])}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:locale" content="ru_RU">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(page["title"])}">
  <meta name="twitter:description" content="{esc(page["description"])}">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <meta name="theme-color" content="#1f2937">
  <link rel="icon" href="/favicon.ico?v=2" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png?v=2">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png?v=2">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png?v=2">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="stylesheet" href="/style.css">
  <script type="application/ld+json">{schema_graph(page)}</script>
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <div class="header-left">
        <a class="site-logo" href="/" aria-label="Eva Casino — главная">
          <img src="/assets/img/logo.png" alt="Eva Casino — логотип бренда" width="160" height="48" decoding="async">
        </a>
        <a class="header-bonus-btn" href="{AFF}" target="_blank" rel="nofollow sponsored noopener">Бонус</a>
      </div>
      <button class="menu-toggle" type="button" aria-label="Открыть меню" aria-expanded="false"></button>
      <nav class="site-nav" aria-label="Основное меню">{nav}</nav>
    </div>
  </header>
  <main class="site-main">
    <section class="hero">
      <div class="container">
        <div class="text-wrap">
          <h1>{esc(page["h1"])}</h1>
          {intro}
          <div class="hero-cta">
            <a class="btn btn--primary" href="{AFF}" target="_blank" rel="nofollow sponsored noopener">{esc(page["cta"])}</a>
          </div>
        </div>
        <a class="hero-banner" href="{AFF}" target="_blank" rel="nofollow sponsored noopener">
          <img src="/assets/img/eva-banner.png" alt="{esc(page["banner_alt"])}" width="920" height="400" loading="eager" fetchpriority="high" decoding="async">
        </a>
      </div>
    </section>
    {trust}
    {sections_html(page["sections"])}
    {mid_cta}
    {related_html(page["path"])}
    {faq_sec}
  </main>
  <footer class="site-footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <a class="site-logo" href="/" aria-label="Eva Casino — главная">
          <img src="/assets/img/logo.png" alt="Eva Casino — логотип бренда" width="160" height="48" loading="lazy" decoding="async">
        </a>
      </div>
      <nav class="footer-links" aria-label="Нижнее меню">{footer_nav}</nav>
      <nav class="footer-trust" aria-label="Правовая информация">
        <a href="/responsible-gaming/">Ответственная игра</a>
        <a href="/privacy-policy/">Политика конфиденциальности</a>
        <a href="/terms/">Условия использования</a>
        <a href="/contacts/">Контакты</a>
      </nav>
      <p class="footer-age">18+ · Играйте ответственно</p>
      <p class="footer-copy">© Eva Casino · Updated: May 2026</p>
    </div>
  </footer>
  <script src="/script.js" defer></script>
</body>
</html>"""


def p(*parts):
    return list(parts)


# --- PAGE CONTENT ---
PAGES = []

# INDEX
PAGES.append({
    "file": "index.html",
    "path": "/",
    "canonical": f"{DOMAIN}/",
    "bc_name": "Главная",
    "title": "Ева казино — официальный сайт, вход и зеркало",
    "description": "Ева казино: официальный сайт, вход, регистрация, бонусы, зеркало, ставки, казино и скачать приложение.",
    "h1": "Ева казино — официальный сайт, вход, зеркало и бонусы",
    "cta": "Получить бонус",
    "mid_cta": "Перейти на Eva Casino",
    "banner_alt": "Ева казино официальный сайт, вход и бонусы",
    "article": False,
    "intro": p(
        "Eva Casino — бренд онлайн-площадки, где собраны казино, бонусы, ставки и мобильный доступ. Эта страница помогает быстро понять структуру сервиса и выбрать нужный раздел без лишних переходов.",
        "Если вы ищете ева казино официальный сайт, вход или рабочее зеркало, начните с обзора ниже. Мы описываем только то, что важно игроку: как зарегистрироваться, где смотреть акции и как безопасно открыть платформу.",
        "Для перехода к актуальным предложениям используйте кнопку «Получить бонус» — она ведёт на официальный раздел Eva Casino.",
    ),
    "sections": [
        ("Что такое ева казино", p(
            "Ева казино — это онлайн-бренд с разделами казино, live-игр, бонусов и спортивных ставок. Платформа ориентирована на пользователей, которым нужен единый кабинет: один аккаунт, один баланс и понятная навигация между играми и линией событий.",
            "Бренд Eva Casino часто ищут по запросам «ева казино официальный сайт» и «eva casino online». Смысл один: найти рабочий вход, пройти регистрацию и открыть нужный раздел — слоты, live или купон ставок.",
            "Важно помнить: азартные игры связаны с риском. Ева казино — формат досуга, а не способ заработка. Задавайте лимиты по времени и бюджету до первого депозита.",
            "На сайте собраны материалы по каждому направлению: официальный доступ, зеркало, вход, регистрация, бонусы, игры, ставки, приложение и отзывы игроков.",
        )),
        ("Как пользоваться Eva Casino", p(
            "Начните с выбора сценария. Новичкам подойдёт <a href=\"/registration/\">регистрация</a>, действующим пользователям — <a href=\"/login/\">вход</a>. Если основной адрес недоступен, откройте раздел <a href=\"/zerkalo/\">зеркала</a>.",
            "После авторизации изучите <a href=\"/bonus/\">бонусы</a> и условия отыгрыша. Затем перейдите в <a href=\"/casino/\">игры</a> или <a href=\"/bets/\">ставки</a> — в зависимости от вашего интереса.",
            "Для смартфона есть <a href=\"/download/\">мобильная версия и приложение</a>. Интерфейс адаптирован под вертикальный экран, сохраняя те же функции кабинета.",
            "Перед пополнением баланса прочитайте <a href=\"/reviews/\">отзывы</a> и страницу <a href=\"/responsible-gaming/\">ответственной игры</a> — это помогает принять взвешенное решение.",
        )),
        ("Официальный сайт и зеркало ева казино", p(
            "Официальный сайт Eva Casino — основная точка входа с актуальными правилами, поддержкой и платёжными методами. Подробнее — на странице <a href=\"/official-site/\">официального сайта</a>.",
            "Зеркало ева казино используют, когда основной домен временно недоступен. Альтернативный адрес должен вести к той же экосистеме. Проверяйте источник ссылки и не вводите данные на подозрительных копиях.",
            "После входа через зеркало сохраните рабочий адрес в закладки и сверьте баланс с ожидаемым. Любые расхождения — повод обратиться в поддержку через проверенный канал.",
            "Не путайте информационные обзоры с платёжными формами оператора. Платежи и игра выполняются только на официальной площадке Eva Casino.",
        )),
        ("Бонусы и акции Eva Casino", p(
            "В ева казино доступны приветственные пакеты, фриспины, кэшбэк и сезонные акции. У каждого предложения есть срок, вейджер и список игр с полным или частичным зачётом.",
            "Активируйте бонус только после прочтения условий. Если отыгрыш кажется слишком жёстким, можно играть на чистый депозит без ограничений по ставке.",
            "Промокоды вводятся при регистрации или в кассе. Используйте коды из надёжных источников — устаревшие комбинации не сработают.",
            "Полный обзор — в разделе <a href=\"/bonus/\">бонусы ева казино</a>.",
        )),
        ("Казино, ставки и мобильная версия ева казино", p(
            "Казино-раздел Eva Casino включает слоты, настольные игры и live-столы. Ставки покрывают prematch и live-события с купоном и быстрыми исходами.",
            "Мобильная версия повторяет функции десктопа: вход, касса, бонусы и история. Приложение удобно, если нужен ярлык на экране и стабильная сессия на слабом интернете.",
            "Выбирайте формат под задачу: слоты для коротких сессий, live — для медленного темпа, ставки — если следите за спортом. Комбинируйте разделы, но не повышайте ставки импульсивно.",
            "Подробности: <a href=\"/casino/\">игры</a>, <a href=\"/bets/\">ставки</a>, <a href=\"/download/\">скачать</a>.",
        )),
        ("Почему игроки выбирают Eva Casino", p(
            "Игроки отмечают понятное меню, быстрый вход и разнообразие слотов. Отдельно хвалят фильтры по провайдерам и наличие live-раздела.",
            "Плюсом считают единый кошелёк для казино и ставок — не нужно переводить средства между разными продуктами внутри бренда.",
            "Среди минусов в отзывах встречаются задержки верификации и строгие условия бонусов. Это типично для индустрии, но важно учитывать заранее.",
            "Сравните впечатления в <a href=\"/reviews/\">отзывах о ева казино</a> и проверьте платформу лично через кнопку перехода.",
        )),
    ],
    "faq_h2": "Частые вопросы о ева казино",
    "faq": [
        ("Как открыть официальный сайт ева казино?", "Используйте кнопку «Получить бонус» или раздел «Официальный сайт» в меню. Переход ведёт на актуальную страницу Eva Casino с регистрацией и входом."),
        ("Нужна ли регистрация для игры?", "Для игры на деньги нужен аккаунт. Пройдите регистрацию, подтвердите контакты и выполните вход. Демо-режим в отдельных слотах может быть доступен без депозита."),
        ("Что делать, если сайт не открывается?", "Проверьте интернет и DNS. Если проблема сохраняется, откройте раздел зеркала и используйте только проверенные ссылки."),
        ("Есть ли мобильное приложение Eva Casino?", "Да, доступны мобильная версия и приложение для Android и iOS. Инструкции — на странице «Скачать»."),
        ("Как получить бонус в ева казино?", "Зарегистрируйтесь, откройте раздел акций и активируйте предложение. Прочитайте вейджер и срок до начала отыгрыша."),
        ("Безопасно ли играть в Eva Casino?", "Используйте только официальный вход, уникальный пароль и лимиты депозита. Играйте ответственно и только если это допустимо в вашем регионе."),
        ("Можно ли делать ставки и играть в казино с одного счёта?", "Да, ева казино объединяет казино и ставки в одном кабинете. Баланс общий, а все операции отображаются в профиле после авторизации."),
        ("Где читать отзывы игроков?", "На странице «Отзывы» собран обзор плюсов, минусов и типичных впечатлений пользователей."),
    ],
})

# Load content from external module to keep file manageable - continue inline for other pages
exec(open(os.path.join(ROOT, "_pages_data.py"), encoding="utf-8").read())
from _expand_content import enrich, bulk_enrich, trust_bulk

TRUST_FILES = {"privacy-policy.html", "terms.html", "contacts.html", "responsible-gaming.html"}
BULK_N = {
    "index.html": 22,
    "reviews.html": 50,
    "official-site.html": 36,
    "login.html": 40,
    "registration.html": 42,
    "zerkalo.html": 42,
    "bets.html": 42,
    "bonus.html": 42,
    "casino.html": 42,
    "download.html": 42,
}

for page in PAGES:
    page = enrich(page)
    if page["file"] in TRUST_FILES:
        page = trust_bulk(page, 38)
    else:
        page = bulk_enrich(page, BULK_N.get(page["file"], 14))
    out = os.path.join(ROOT, page["file"])
    with open(out, "w", encoding="utf-8") as f:
        f.write(render(page))
    print("Wrote", page["file"])

print("Done:", len(PAGES), "pages")
