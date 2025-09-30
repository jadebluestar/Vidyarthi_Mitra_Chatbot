import hashlib
import logging
import os
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext

# ==============================
# Logging Setup
# ==============================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ==============================
# Mock Student Data (embedded)
# ==============================
STUDENTS = {
    "101": {
        "name": "Aarav Sharma",
        "fees": {"total": 100000, "paid": 75000, "due": 25000},
        "attendance": {"classes_held": 120, "attended": 110, "percentage": 91.6},
        "hostel": {"block": "A", "room": "105", "mess": "Veg"},
        "library": {"books_issued": ["DBMS", "Operating Systems"], "fine": 0},
        "placements": {"company": "Infosys", "role": "SDE Intern", "package": 6.5},
        "certificates": [
            {"id": "CERT-2024-001", "name": "Blockchain Workshop"},
            {"id": "CERT-2024-002", "name": "Hackathon Winner"}
        ]
    },
    "102": {
        "name": "Meera Nair",
        "fees": {"total": 100000, "paid": 100000, "due": 0},
        "attendance": {"classes_held": 120, "attended": 100, "percentage": 83.3},
        "hostel": {"block": "B", "room": "210", "mess": "Non-Veg"},
        "library": {"books_issued": ["C++ Programming", "AI Basics"], "fine": 50},
        "placements": {"company": "Wipro", "role": "Data Analyst Intern", "package": 5.0},
        "certificates": [
            {"id": "CERT-2024-003", "name": "AI ML Bootcamp"}
        ]
    }
}

# ==============================
# Mock Blockchain (dict)
# ==============================
MOCK_BLOCKCHAIN = {}

def generate_certificate_hash(cert_id: str) -> str:
    """Generate SHA256 hash for a certificate ID."""
    return hashlib.sha256(cert_id.encode()).hexdigest()

# Pre-store certificates in blockchain
for sid, details in STUDENTS.items():
    for cert in details.get("certificates", []):
        cert_id = cert["id"]
        cert_hash = generate_certificate_hash(cert_id)
        MOCK_BLOCKCHAIN[cert_id] = {
            "hash": cert_hash,
            "transaction": f"0x{cert_hash[:16]}"  # fake tx id
        }

# ==============================
# Command Handlers
# ==============================
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Hello! I’m your College Student Info Bot.\n\n"
        "Available commands:\n"
        "/fees <student_id>\n"
        "/attendance <student_id>\n"
        "/hostel <student_id>\n"
        "/library <student_id>\n"
        "/placements <student_id>\n"
        "/certificates <student_id>\n"
        "/verify <certificate_id>\n"
    )

def get_student(student_id: str):
    return STUDENTS.get(student_id)

def fees(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Usage: /fees <student_id>")
        return
    sid = context.args[0]
    student = get_student(sid)
    if student:
        f = student["fees"]
        update.message.reply_text(
            f"💰 *Fees Info for {student['name']}*:\n"
            f"Total: ₹{f['total']}\nPaid: ₹{f['paid']}\nDue: ₹{f['due']}",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        update.message.reply_text("❌ Student not found.")

def attendance(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Usage: /attendance <student_id>")
        return
    sid = context.args[0]
    student = get_student(sid)
    if student:
        a = student["attendance"]
        update.message.reply_text(
            f"📊 *Attendance for {student['name']}*:\n"
            f"Classes Held: {a['classes_held']}\n"
            f"Attended: {a['attended']}\n"
            f"Percentage: {a['percentage']}%",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        update.message.reply_text("❌ Student not found.")

def hostel(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Usage: /hostel <student_id>")
        return
    sid = context.args[0]
    student = get_student(sid)
    if student:
        h = student["hostel"]
        update.message.reply_text(
            f"🏠 *Hostel Info for {student['name']}*:\n"
            f"Block: {h['block']}\nRoom: {h['room']}\nMess: {h['mess']}",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        update.message.reply_text("❌ Student not found.")

def library(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Usage: /library <student_id>")
        return
    sid = context.args[0]
    student = get_student(sid)
    if student:
        l = student["library"]
        books = "\n".join(l["books_issued"])
        update.message.reply_text(
            f"📚 *Library Info for {student['name']}*:\n"
            f"Books Issued:\n{books}\nFine: ₹{l['fine']}",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        update.message.reply_text("❌ Student not found.")

def placements(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Usage: /placements <student_id>")
        return
    sid = context.args[0]
    student = get_student(sid)
    if student:
        p = student["placements"]
        update.message.reply_text(
            f"💼 *Placement Info for {student['name']}*:\n"
            f"Company: {p['company']}\n"
            f"Role: {p['role']}\n"
            f"Package: {p['package']} LPA",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        update.message.reply_text("❌ Student not found.")

def certificates(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Usage: /certificates <student_id>")
        return
    sid = context.args[0]
    student = get_student(sid)
    if student:
        certs = student["certificates"]
        msg = f"📜 *Certificates for {student['name']}*:\n"
        for c in certs:
            msg += f"- {c['id']} ({c['name']})\n"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("❌ Student not found.")

def verify(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Usage: /verify <certificate_id>")
        return
    cert_id = context.args[0]
    if cert_id in MOCK_BLOCKCHAIN:
        data = MOCK_BLOCKCHAIN[cert_id]
        update.message.reply_text(
            f"✅ Certificate *{cert_id}* is VALID.\n"
            f"Hash: `{data['hash']}`\n"
            f"Tx: `{data['transaction']}`",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        update.message.reply_text("❌ Certificate not found or invalid.")

# ==============================
# Main Function
# ==============================
def main():
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        print("❌ TELEGRAM_TOKEN not found in environment.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("fees", fees))
    dp.add_handler(CommandHandler("attendance", attendance))
    dp.add_handler(CommandHandler("hostel", hostel))
    dp.add_handler(CommandHandler("library", library))
    dp.add_handler(CommandHandler("placements", placements))
    dp.add_handler(CommandHandler("certificates", certificates))
    dp.add_handler(CommandHandler("verify", verify))

    # Start bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
