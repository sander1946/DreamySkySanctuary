# Import the following module 
from email.mime.text import MIMEText 
from email.mime.image import MIMEImage 
from email.mime.application import MIMEApplication 
from email.mime.multipart import MIMEMultipart 
import smtplib 
import os

from fastapi import Request
import yagmail

from src.config import config
from src.schemas.Login import UserDB 

defualt_subject = "Password Reset"

default_html = """
Hello {},

Greetings from the Dreamy Sky Team,
We received a request to reset the password for the account associated with this e-mail address. Click the link below to reset your password for your account:

{}

If clicking the link doesn't work, you can copy and paste the link into your web browser's address bar. You will be able to create a new password for your account after clicking the link above.
If you did not request to have your password reset, you can safely ignore this email. Or contact us via email at: contact@dreamyskysanctuary.com
Thank you for using the Dreamy Sky Sanctuary website!

Sincerely,
Dreamy Sky Team

<table class="table__StyledTable-sc-1avdl6r-0 bztkJx" style="font-size: medium; font-family: Trebuchet MS;" border="0" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td>
<table class="table__StyledTable-sc-1avdl6r-0 bztkJx" style="font-size: medium; font-family: Trebuchet MS;" border="0" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td style="vertical-align: middle;" width="150"><span class="template3__ImageContainer-sc-vj949k-0 gQAWto" style="margin-right: 20px; display: block;"><img class="image__StyledImage-sc-hupvqm-0 ctEjzA" style="max-width: 130px;" src="https://dreamyskysanctuary.com/public/imgs/icon.png" width="130" /></span></td>
<td style="vertical-align: middle;">
<h2 class="name__NameContainer-sc-1m457h3-0 iegFqm" style="margin: 0px; font-size: 18px; color: #000000; font-weight: 600;"><span>Dreamy</span><span>&nbsp;</span><span>Sky Team</span></h2>
<p class="company-details__CompanyContainer-sc-j5pyy8-0 jyMkYn" style="margin: 0px; font-weight: 500; color: #000000; font-size: 14px; line-height: 22px;"><span>Contact</span><span>&nbsp;|&nbsp;</span><span>Dreamy Sky Sanctuary</span></p>
</td>
<td width="30">
<div style="width: 30px;">&nbsp;</div>
</td>
<td class="color-divider__Divider-sc-1h38qjv-0 iqkkET" style="width: 1px; border-bottom: medium; border-left: 1px solid #396ed7;" width="1" height="auto">&nbsp;</td>
<td width="30">
<div style="width: 30px;">&nbsp;</div>
</td>
<td style="vertical-align: middle;">
<table class="table__StyledTable-sc-1avdl6r-0 bztkJx" style="font-size: medium; font-family: Trebuchet MS;" border="0" cellspacing="0" cellpadding="0">
<tbody>
<tr style="vertical-align: middle;">
<td style="vertical-align: middle;" width="30">
<table class="table__StyledTable-sc-1avdl6r-0 bztkJx" style="font-size: medium; font-family: Trebuchet MS;" border="0" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td style="vertical-align: bottom;"><span class="contact-info__IconWrapper-sc-mmkjr6-1 dmdaIT" style="display: inline-block; background-color: #396ed7;"><img class="contact-info__ContactLabelIcon-sc-mmkjr6-0 cuMGNv" style="display: block; background-color: #396ed7;" src="https://cdn2.hubspot.net/hubfs/53/tools/email-signature-generator/icons/phone-icon-2x.png" alt="mobilePhone" width="13" /></span></td>
</tr>
</tbody>
</table>
</td>
<td style="padding: 0px; color: #000000;"><a class="contact-info__ExternalLink-sc-mmkjr6-2 ixYHUl" style="text-decoration: none; color: #000000; font-size: 14px;" href="tel:+31 6 20636924"><span>+31 6 20636924</span></a></td>
</tr>
<tr style="vertical-align: middle;">
<td style="vertical-align: middle;" width="30">
<table class="table__StyledTable-sc-1avdl6r-0 bztkJx" style="font-size: medium; font-family: Trebuchet MS;" border="0" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td style="vertical-align: bottom;"><span class="contact-info__IconWrapper-sc-mmkjr6-1 dmdaIT" style="display: inline-block; background-color: #396ed7;"><img class="contact-info__ContactLabelIcon-sc-mmkjr6-0 cuMGNv" style="display: block; background-color: #396ed7;" src="https://cdn2.hubspot.net/hubfs/53/tools/email-signature-generator/icons/email-icon-2x.png" alt="emailAddress" width="13" /></span></td>
</tr>
</tbody>
</table>
</td>
<td style="padding: 0px;"><a class="contact-info__ExternalLink-sc-mmkjr6-2 ixYHUl" style="text-decoration: none; color: #000000; font-size: 14px;" href="mailto:contact@dreamyskysanctuary.com"><span>contact@dreamyskysanctuary.com</span></a></td>
</tr>
<tr style="vertical-align: middle;">
<td style="vertical-align: middle;" width="30">
<table class="table__StyledTable-sc-1avdl6r-0 bztkJx" style="font-size: medium; font-family: Trebuchet MS;" border="0" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td style="vertical-align: bottom;"><span class="contact-info__IconWrapper-sc-mmkjr6-1 dmdaIT" style="display: inline-block; background-color: #396ed7;"><img class="contact-info__ContactLabelIcon-sc-mmkjr6-0 cuMGNv" style="display: block; background-color: #396ed7;" src="https://cdn2.hubspot.net/hubfs/53/tools/email-signature-generator/icons/link-icon-2x.png" alt="website" width="13" /></span></td>
</tr>
</tbody>
</table>
</td>
<td style="padding: 0px;"><a class="contact-info__ExternalLink-sc-mmkjr6-2 ixYHUl" style="text-decoration: none; color: #000000; font-size: 14px;" href="//DreamySkySanctuary.com"><span>DreamySkySanctuary.com</span></a></td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
<tr>
<td>
<table class="table__StyledTable-sc-1avdl6r-0 bztkJx" style="width: 100%; font-size: medium; font-family: Trebuchet MS;" border="0" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td class="color-divider__Divider-sc-1h38qjv-0 iqkkET" style="width: 100%; border-bottom: 1px solid #396ed7; border-left: medium; display: block;" width="auto" height="1">&nbsp;</td>
</tr>
<tr>
<td height="10">&nbsp;</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
"""

async def send_password_reset_mail(request: Request, user: UserDB, token: str) -> None: 
    print(f"Sending password reset email to {user.email}")

    if request:
        host = request.headers.get("host")
    else:
        host = "localhost"
    
    content = f"Hello {user.username},\n\nGreetings from the Dreamy Sky Team,\nWe received a request to reset the password for the account associated with this e-mail address. Click the link below to reset your password for your account:\n\nhttp://{host}/reset-password/{token}\n\nIf clicking the link doesn't work, you can copy and paste the link into your web browser's address bar. You will be able to create a new password for your account after clicking the link above.\nIf you did not request to have your password reset, you can safely ignore this email. Or contact us via email at: contact@dreamyskysanctuary.com\nThank you for using the Dreamy Sky Sanctuary website!\n\nSincerely,\nThe Dreamy Sky Team"
    
    yag = yagmail.SMTP(user=config.SMTP_USERNAME, password=config.SMTP_PASSWORD, host=config.SMTP_SERVER, port=config.SMTP_PORT)
    yag.send(
        to="sanderkleine2@gmail.com", 
        subject=defualt_subject, 
        contents=content
    )
    print("Email sent")