# -*- coding: utf-8 -*-
"""Fifth pass — reach 1000+ words on all internal pages."""
import os, re, collections

ROOT = os.path.dirname(os.path.abspath(__file__))

NEW_BLOCKS = {
"registration.html": '''<section class="section-block"><div class="container"><div class="text-wrap"><h2>Регистрация Eva Casino на разных устройствах</h2><p>На смартфоне форма регистрации занимает весь экран — удобно заполнять по одному полю. На десктопе видны все поля сразу, проще проверить опечатки в email.</p><p>Если регистрируетесь с планшета, поверните экран горизонтально — клавиатура не перекроет кнопку подтверждения.</p><p>Один аккаунт Eva Casino работает на всех устройствах — не создавайте отдельный профиль «для телефона».</p></div></div></section>''',
"zerkalo.html": '''<section class="section-block"><div class="container"><div class="text-wrap"><h2>Обновление адреса зеркала Eva Casino</h2><p>Когда оператор публикует новое зеркало, старое может перестать работать через несколько дней. Не полагайтесь на закладку годовой давности.</p><p>Актуальную ссылку ищите через официальные каналы или кнопку на этой странице — не через рекламные посты с обещанием «100% бонус за переход».</p><p>После смены зеркала вход выполняется теми же данными; баланс и история сохраняются в аккаунте ева казино.</p><p>Если новое зеркало не открывается, вернитесь к основному домену — возможно, блокировка уже снята.</p></div></div></section>''',
"bets.html": '''<section class="section-block"><div class="container"><div class="text-wrap"><h2>Статистика и аналитика ставок в ева казино</h2><p>В карточке матча Eva Casino часто показывает форму команд, очные встречи и травмы — используйте как справку, не как гарантию.</p><p>Раздел «Мои ставки» хранит архив — удобно анализировать, на каких рынках вы чаще ошибаетесь.</p><p>Не ставьте на матчи, правила расчёта которых не понимаете — например, азиатский тотал или форы с возвратом.</p><p>Live-график momentum показывает давление, но коэффициент уже учитывает часть этой информации.</p></div></div></section>''',
"bonus.html": '''<section class="section-block"><div class="container"><div class="text-wrap"><h2>VIP и лояльность бонусов Eva Casino</h2><p>Программа лояльности начисляет баллы за ставки в слотах и иногда за депозиты. Баллы обмениваются на бонусы или фриспины по курсу в профиле.</p><p>VIP-уровни открывают персонального менеджера, ускоренный вывод и эксклюзивные акции — условия роста указаны в разделе лояльности ева казино.</p><p>Не гонитесь за уровнем ценой превышения бюджета — VIP-выгода должна оправдывать объём игры.</p><p>Кэшбэк по VIP часто начисляется еженедельно с отдельным вейджером — читайте правило каждого начисления.</p></div></div></section>''',
"casino.html": '''<section class="section-block"><div class="container"><div class="text-wrap"><h2>Провайдеры игр в ева казино</h2><p>Каталог Eva Casino объединяет десятки студий: Pragmatic Play, Evolution для live, NetEnt, Play'n GO и другие. Фильтр по провайдеру ускоряет поиск.</p><p>У каждого провайдера свой стиль — Pragmatic часто даёт buy bonus, NetEnt — классические механики с высоким RTP.</p><p>Новые релизы помечаются в разделе «Новинки» — там же указана дата добавления в ева казино.</p><p>Лицензия провайдера указана в футере игры — это подтверждение аудита RNG, а не гарантия выигрыша игроку.</p></div></div></section>''',
"download.html": '''<section class="section-block"><div class="container"><div class="text-wrap"><h2>Безопасность мобильного доступа к Eva Casino</h2><p>Установите блокировку экрана на телефоне — приложение Eva Casino не должен быть доступен без PIN или биометрии.</p><p>Не root-ите Android и не jailbreak-ите iPhone для «обхода ограничений» — это снижает безопасность платёжных данных.</p><p>Обновляйте ОС: патчи безопасности закрывают уязвимости, через которые могут перехватить сессию.</p><p>Публичный Wi‑Fi без VPN рискован для входа в кабинет — используйте мобильный интернет или домашнюю сеть.</p><p>После сессии выходите из аккаунта, если телефон может попасть в чужие руки.</p></div></div></section>''',
"reviews.html": '''<section class="section-block"><div class="container"><div class="text-wrap"><h2>Сравнение Eva Casino с ожиданиями игроков</h2><p>Новички ожидают мгновенный вывод без документов — в реальности KYC стандартен для лицензированных операторов, включая ева казино.</p><p>Опытные игроки ценят широкую линию ставок и live-казино в одном кабинете — в отзывах это частый аргумент «за».</p><p>Критика касается вейджера на бонусы — это не уникальная черта Eva Casino, но важно читать условия до активации.</p><p>Мобильное приложение в отзывах 2025–2026 года чаще хвалят за стабильность, чем ранние версии.</p></div></div></section>''',
}

EXTRA5 = {
"registration.html": {
"Как пройти регистрацию в ева казино": [
    "Согласие на рассылку можно отключить — рекламные письма не обязательны для работы аккаунта Eva Casino.",
],
},
"zerkalo.html": {
"Проверка зеркала Eva Casino перед входом": [
    "Убедитесь, что в футере сайта есть ссылки на правила и поддержку — их отсутствие характерно для подделок.",
],
},
"bets.html": {
"Как оформить первую ставку в Eva Casino": [
    "Начните с ординара на знакомый вид спорта — экспресс оставьте на потом, когда поймёте интерфейс купона.",
],
},
"bonus.html": {
"Активация бонуса Eva Casino без ошибок": [
    "Сделайте скриншот условий акции при активации — при споре с поддержкой пригодится фиксация текста на момент депозита.",
],
},
"casino.html": {
"Старт в казино Eva Casino": [
    "Первую сессию ограничьте 30–60 минутами — так проще оценить интерфейс без импульсивного увеличения ставок.",
],
},
"download.html": {
"Установка Eva Casino на телефон": [
    "После установки откройте настройки уведомлений и оставьте только важные — выплаты и безопасность.",
],
},
"reviews.html": {
"Как проверить Eva Casino самостоятельно": [
    "Запишите время ответа поддержки на тестовый вопрос — это объективнее, чем чужой отзыв о «молчаливой службе».",
],
},
}


def expand_main(html, extras):
    for h2, paras in extras.items():
        insert = "".join(f"<p>{p}</p>" for p in paras)
        pattern = rf'(<h2>{re.escape(h2)}</h2>)(.*?)(</div></div></section>)'
        html, _ = re.subn(
            pattern, lambda m: m.group(1) + m.group(2) + insert + m.group(3),
            html, count=1, flags=re.DOTALL,
        )
    return html


for fname, block in {**NEW_BLOCKS}.items():
    path = os.path.join(ROOT, fname)
    with open(path, encoding="utf-8") as f:
        html = f.read()
    m = re.search(r"(<main class=\"site-main\">.*?</main>)", html, re.DOTALL)
    main = m.group(1)
    if fname in EXTRA5:
        main = expand_main(main, EXTRA5[fname])
    if block not in main:
        main = main.replace(
            '<section class="section-block section-cta">',
            block + '\n    <section class="section-block section-cta">',
            1,
        )
    html = html[: m.start(1)] + main + html[m.end(1) :]
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    body = re.sub(r"<[^>]+>", " ", main)
    words = len(re.findall(r"[\w\u0400-\u04FF]+", body))
    print(f"{fname}: {words}")

# verify official-site and login too
for fn in ["official-site.html", "login.html"] + list(NEW_BLOCKS.keys()):
    path = os.path.join(ROOT, fn)
    if not os.path.exists(path):
        continue
    t = open(path, encoding="utf-8").read()
    m = re.search(r"<main.*?</main>", t, re.S)
    body = re.sub(r"<[^>]+>", " ", m.group(0))
    words = len(re.findall(r"[\w\u0400-\u04FF]+", body))
    print(f"check {fn}: {words}")
