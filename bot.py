import os
import openai
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ====== CONFIGURATION ======
TELEGRAM_TOKEN = "7954690302:AAH9O3zN4DVjB6RyhpsZXjYWZUDQroNcyr8"  # Replace with your actual Telegram bot token
OPENAI_API_KEY = "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"
ADMIN_FILE = "admin_id.txt"
# ===========================

# Initialize services
openai.api_key = OPENAI_API_KEY

def get_admin_id():
    """Read admin ID from file"""
    if os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, "r") as f:
            return int(f.read().strip())
    return None

def save_admin_id(admin_id: int):
    """Save admin ID to file"""
    with open(ADMIN_FILE, "w") as f:
        f.write(str(admin_id))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enhanced start command with ID information"""
    user = update.effective_user
    admin_id = get_admin_id()
    
    response = (
        f"👋 Welcome {user.first_name}!\n"
        f"🆔 Your ID: `{user.id}`\n"
        "🔧 Use /myid to see your ID\n"
    )
    
    if admin_id:
        response += f"👑 Admin ID: `{admin_id}`\n"
    else:
        response += "⚠️ No admin set! Use /setadmin to claim"
        
    await update.message.reply_text(response, parse_mode="Markdown")

async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user their Telegram ID"""
    user = update.effective_user
    await update.message.reply_text(f"🔑 Your Telegram ID: `{user.id}`", parse_mode="Markdown")

async def set_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set admin ID securely"""
    user = update.effective_user
    current_admin = get_admin_id()
    
    # Validate command format
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Usage: /setadmin YOUR_ID")
        return
    
    new_admin = int(context.args[0])
    
    # Authorization check
    if current_admin and user.id != current_admin:
        await update.message.reply_text("❌ Only current admin can change this!")
        return
        
    if user.id != new_admin:
        await update.message.reply_text("❌ You can only set yourself as admin!")
        return
    
    save_admin_id(new_admin)
    await update.message.reply_text(f"✅ Admin ID set to {new_admin}")

def is_admin(user_id: int) -> bool:
    """Check admin status"""
    admin_id = get_admin_id()
    return admin_id is not None and user_id == admin_id

async def announce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin announcement command"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Admin only command!")
        return

    message = " ".join(context.args)
    if not message:
        await update.message.reply_text("Usage: /announce <message>")
        return

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"📢 **ADMIN ANNOUNCEMENT**\n\n{message}"
    )

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kick a user from the chat"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Admin only command!")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a user to kick them.")
        return

    user_id = update.message.reply_to_message.from_user.id
    await context.bot.ban_chat_member(update.effective_chat.id, user_id)
    await context.bot.unban_chat_member(update.effective_chat.id, user_id)
    await update.message.reply_text(f"✅ User has been kicked.")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban a user from the chat"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Admin only command!")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a user to ban them.")
        return

    user_id = update.message.reply_to_message.from_user.id
    await context.bot.ban_chat_member(update.effective_chat.id, user_id)
    await update.message.reply_text(f"✅ User has been banned.")

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mute a user in the chat"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Admin only command!")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a user to mute them.")
        return

    user_id = update.message.reply_to_message.from_user.id
    await context.bot.restrict_chat_member(update.effective_chat.id, user_id, ChatPermissions(can_send_messages=False))
    await update.message.reply_text(f"✅ User has been muted.")

async def handle_openai_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """AI response handler"""
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": update.message.text}]
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text("⚠️ Error processing your request")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", my_id))
    app.add_handler(CommandHandler("setadmin", set_admin))
    app.add_handler(CommandHandler("announce", announce))
    app.add_handler(CommandHandler("kick", kick))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_openai_query))

    # Admin warning check
    if not get_admin_id():
        print("⚠️ WARNING: No admin configured! Users can claim admin with /setadmin")
    
    print("🤖 Bot is running with dynamic admin setup!")
    app.run_polling()

if __name__ == "__main__":
    main()
