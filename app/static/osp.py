class BindSendMessage:
    SUCCESS = "Telegram connection successful."
    FAILED = "Telegram connection failed."
    OSP_CONNECTED_ANOTHER_TG = "The OSP profile has already connected another Telegram account."
    TG_CONNECTED = "This Telegram account has already been connected."
    CODE_EXPIRED = "This verification code is invalid, Please return to the quest page and click 'Go' again."


class BanChatMemberSendMessage:
    Membership_Expiration = "{user} left the Space Group Chat—now it’s just us fabulous folks! 💁‍♀️"


class JoinDifferentGroupSendMessage:
    Join_Public_Group = ("Oops! 😅 It looks like your group chat isn’t set to private yet. Please make it private "
                         "so we can get you up and running!")
    Join_Private_Group = ("Welcome, superstar! 🌟 Your Space Group Chat is about to go live soon! 👀\n"
                          "Copy and paste the link below to your Space so your Group Chat can be set up: "
                          "{invite_link} \nCan’t wait to see you in action! 🩵")
