from datetime import time
from zoneinfo import ZoneInfo

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
)

from app.bot.api import (
    complete_task,
    get_today_progress,
    get_today_tasks,
)
from app.config import settings


JAKARTA = ZoneInfo("Asia/Jakarta")


def format_task_message(tasks: list[dict]) -> str:
    if not tasks:
        return (
            "☀️ Good morning!\n\n"
            "Tidak ada task yang dijadwalkan hari ini.\n\n"
            "Enjoy your day."
        )

    lines = [
        "☀️ GOOD MORNING",
        "",
        "Today's Tasks",
        "",
    ]

    for index, task in enumerate(tasks, start=1):
        priority = task.get("priority", 1)
        estimated = task.get("estimated_minutes")

        priority_icon = {
            5: "🔥",
            4: "🔴",
            3: "🟡",
            2: "🟢",
            1: "⚪",
        }.get(priority, "⚪")

        duration = (
            f"{estimated} min"
            if estimated
            else "time unspecified"
        )

        lines.append(
            f"{index}. {priority_icon} "
            f"{task['title']}"
        )

        lines.append(
            f"   ⏱ {duration}"
        )

        if task.get("why"):
            lines.append(
                f"   Why: {task['why']}"
            )

        lines.append("")

    lines.append(
        "Tap ✅ when you finish a task."
    )

    return "\n".join(lines)


def build_task_keyboard(tasks: list[dict]):
    keyboard = []

    for index, task in enumerate(tasks, start=1):
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"✅ Done {index}",
                    callback_data=f"done:{task['id']}",
                )
            ]
        )

    return InlineKeyboardMarkup(keyboard)


async def today_command(
    update: Update,
    context: CallbackContext,
):
    tasks = await get_today_tasks()

    text = format_task_message(tasks)

    keyboard = None

    if tasks:
        keyboard = build_task_keyboard(tasks)

    await update.message.reply_text(
        text,
        reply_markup=keyboard,
    )


async def progress_command(
    update: Update,
    context: CallbackContext,
):
    progress = await get_today_progress()

    text = (
        "📊 TODAY'S PROGRESS\n\n"
        f"Completed: {progress['completed']}/{progress['total']}\n"
        f"Remaining: {progress['remaining']}\n"
        f"Progress: {progress['completion_rate']}%"
    )

    await update.message.reply_text(text)


async def start_command(
    update: Update,
    context: CallbackContext,
):
    telegram_user_id = update.effective_user.id

    await update.message.reply_text(
        "Orbit is online 🚀\n\n"
        f"Telegram User ID:\n"
        f"`{telegram_user_id}`\n\n"
        "Commands:\n"
        "/today - lihat task hari ini\n"
        "/progress - lihat progress hari ini",
        parse_mode="Markdown",
    )


async def done_callback(
    update: Update,
    context: CallbackContext,
):
    query = update.callback_query

    await query.answer()

    data = query.data

    if not data.startswith("done:"):
        return

    task_id = data.split(":", 1)[1]

    try:
        task = await complete_task(task_id)

        await query.edit_message_text(
            text=(
                "✅ Task completed!\n\n"
                f"{task['title']}"
            )
        )

    except Exception as exc:
        await query.message.reply_text(
            f"Failed to complete task: {exc}"
        )


async def daily_task_job(
    context: CallbackContext,
):
    try:
        tasks = await get_today_tasks()

        text = format_task_message(tasks)

        keyboard = None

        if tasks:
            keyboard = build_task_keyboard(tasks)

        await context.bot.send_message(
            chat_id=settings.telegram_user_id,
            text=text,
            reply_markup=keyboard,
        )

    except Exception as exc:
        await context.bot.send_message(
            chat_id=settings.telegram_user_id,
            text=(
                "⚠️ Orbit mengalami error "
                "saat mengambil daily task.\n\n"
                f"{exc}"
            ),
        )


async def journal_reminder_job(
    context: CallbackContext,
):
    await context.bot.send_message(
        chat_id=settings.telegram_user_id,
        text=(
            "🌙 NIGHT CHECK-IN\n\n"
            "It's 11 PM.\n\n"
            "Time to reflect on your day.\n\n"
            "Buka ChatGPT dan ceritakan bagaimana "
            "hari kamu berjalan."
        ),
    )


async def test_morning_command(
    update: Update,
    context: CallbackContext,
):
    tasks = await get_today_tasks()

    text = format_task_message(tasks)

    keyboard = None

    if tasks:
        keyboard = build_task_keyboard(tasks)

    await update.message.reply_text(
        text,
        reply_markup=keyboard,
    )


async def test_journal_command(
    update: Update,
    context: CallbackContext,
):
    await update.message.reply_text(
        "🌙 NIGHT CHECK-IN\n\n"
        "It's 11 PM.\n\n"
        "Time to reflect on your day.\n\n"
        "Buka ChatGPT dan ceritakan bagaimana "
        "hari kamu berjalan."
    )

def main():
    app: Application = (
        ApplicationBuilder()
        .token(settings.telegram_bot_token)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start_command)
    )

    app.add_handler(
        CommandHandler("today", today_command)
    )

    app.add_handler(
        CommandHandler("progress", progress_command)
    )

    app.add_handler(
        CommandHandler(
            "test_morning",
            test_morning_command,
        )
    )

    app.add_handler(
        CommandHandler(
            "test_journal",
            test_journal_command,
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            done_callback,
            pattern=r"^done:",
        )
    )

    # 07:00 Asia/Jakarta
    app.job_queue.run_daily(
        daily_task_job,
        time=time(
            hour=7,
            minute=0,
            tzinfo=JAKARTA,
        ),
        name="daily-task",
    )

    # 23:00 Asia/Jakarta
    app.job_queue.run_daily(
        journal_reminder_job,
        time=time(
            hour=23,
            minute=0,
            tzinfo=JAKARTA,
        ),
        name="journal-reminder",
    )

    print("Orbit Telegram Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
