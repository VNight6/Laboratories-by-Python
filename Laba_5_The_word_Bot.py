from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import random

# Слова і підказки
categories = {
    "Тварини": {
        "Лисиця": ["Я хитрий і рудий, часто живу в лісі.", "Моє хутро яскраво-руде, а хвіст пухнастий."],
        "Вовк": ["Я сірий, дикий і полюю в зграї.", "Мене часто бояться, але я захищаю свою територію."],
        "Бобер": ["Я будую хатки на воді та маю плаский хвіст.", "Я гризун, що вміє гризти дерева."],
        "Хорьок": ["Я маленький, гнучкий і полюю на мишей.", "Моє хутро буває темним."],
    },
    "Фрукти і овочі": {
        "Тиква": ["Мене часто використовують на Хелловін.", "Я великий, круглий і оранжевого кольору."],
        "Яблуко": ["Я круглий фрукт, червоний або зелений.", "Я падаю недалеко від дерева."],
        "Помідор": ["Я червоний і круглий, але я не фрукт.", "Мене додають до салатів і соусів."],
        "Огірок": ["Я зелений, довгий і росту на городі.", "Я хрумкий і додаюсь до салатів."],
    },
    "Псевдонім розробника": {
        "Блепіка": ["Це слово починається на букву 'Б'", "Це слово пов’язане з ім’ям в телеграмі"],
    }
}

current_word = {}
current_category = {}
current_difficulty = {}
guess_count = {}

difficulty_levels = {
    "1": "легкий",
    "2": "середній",
    "3": "важкий",
    "легкий": "легкий",
    "середній": "середній",
    "важкий": "важкий"
}

def get_hints(word, category, difficulty):
    hints = categories[category][word]
    if difficulty == "легкий":
        return hints[:2]  # Перші дві підказки
    elif difficulty == "середній":
        return random.sample(hints, 1)  # Одна випадкова підказка
    else:
        return [hints[-1]]  # Остання, найскладніша підказка

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    guess_count[chat_id] = 0
    await update.message.reply_text(
        "Привіт! Давай зіграємо у 'Вгадай слово'! Обери категорію:\n"
        "1. Тварини\n"
        "2. Фрукти і овочі\n"
        "3. Псевдонім розробника\n"
        "Напиши номер категорії або її назву."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    chat_id = update.message.chat_id

    if user_text in ["1", "Тварини", "2", "Фрукти і овочі", "3", "Псевдонім розробника"]:
        if user_text in ["1", "Тварини"]:
            current_category[chat_id] = "Тварини"
            await update.message.reply_text("Виберіть рівень складності:\n1. Легкий\n2. Середній\n3. Важкий")
        elif user_text in ["2", "Фрукти і овочі"]:
            current_category[chat_id] = "Фрукти і овочі"
            await update.message.reply_text("Виберіть рівень складності:\n1. Легкий\n2. Середній\n3. Важкий")
        elif user_text in ["3", "Псевдонім розробника"]:
            current_category[chat_id] = "Псевдонім розробника"
            await select_word(update, context)
        return

    if current_category.get(chat_id):
        if current_category[chat_id] != "Псевдонім розробника" and not current_difficulty.get(chat_id):
            if user_text in ["1", "2", "3", "легкий", "середній", "важкий"]:
                current_difficulty[chat_id] = difficulty_levels[user_text.lower()]
                await select_word(update, context)
            else:
                await update.message.reply_text("Невірний ввід. Спробуйте ще раз. Виберіть рівень складності:\n1. Легкий\n2. Середній\n3. Важкий")
            return

        if current_word.get(chat_id):
            word = current_word[chat_id]
            if user_text.lower() == word.lower():
                await update.message.reply_text(f"Вітаю! 🎉 Ви вгадали слово '{word}'!")
                guess_count[chat_id] += 1
                if current_category[chat_id] == "Псевдонім розробника" or guess_count[chat_id] >= 3:
                    await update.message.reply_text("Гра завершена. Дякую за гру! 👋")
                    del current_word[chat_id]
                    del current_category[chat_id]
                    if chat_id in current_difficulty:
                        del current_difficulty[chat_id]
                    del guess_count[chat_id]
                else:
                    await select_word(update, context)
            else:
                await update.message.reply_text("Ні, це не те слово. Спробуйте ще раз! 🧐")
            return

async def select_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    category = current_category[chat_id]
    if category == "Псевдонім розробника":
        word, hints = random.choice(list(categories[category].items()))
    else:
        difficulty = current_difficulty[chat_id]
        word, hints = random.choice(list(categories[category].items()))
    current_word[chat_id] = word
    hint = random.choice(hints) if category == "Псевдонім розробника" else random.choice(get_hints(word, category, difficulty))
    await update.message.reply_text(f"🔍 Підказка: {hint}")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    if chat_id in current_word:
        del current_word[chat_id]
    if chat_id in current_category:
        del current_category[chat_id]
    if chat_id in current_difficulty:
        del current_difficulty[chat_id]
    if chat_id in guess_count:
        del guess_count[chat_id]
    await update.message.reply_text("Гра завершена. Дякую за гру! 👋")

def main():
    app = ApplicationBuilder().token("7801316447:AAHTsN8c7pP-C8ZZ2jCZgb2sk2BFQLHb1Zo").build()

    # Додаємо обробники команд і повідомлень
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("stop", stop))

    # Запускаємо бота
    app.run_polling()
if __name__ == '__main__':
    main()
