import resend
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_password_reset_email(email: str, token: str):
        """Send password reset email"""
        try:
            resend.api_key = settings.resend_api_key
            reset_link = f"{settings.frontend_url}/reset-password?token={token}"
            
            params = {
                "from": settings.email_from,
                "to": [email],
                "subject": "Reset Your Resumade Password",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #059669;">Reset Your Password</h2>
                    <p>You requested to reset your password for your Resumade account.</p>
                    <p>Click the button below to reset your password:</p>
                    <a href="{reset_link}" style="display: inline-block; background: linear-gradient(to right, #059669, #0d9488); color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; margin: 20px 0;">Reset Password</a>
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="color: #666; word-break: break-all;">{reset_link}</p>
                    <p style="color: #666; font-size: 14px; margin-top: 30px;">This link will expire in 1 hour.</p>
                    <p style="color: #666; font-size: 14px;">If you didn't request this, please ignore this email.</p>
                </div>
                """
            }
            
            resend.Emails.send(params)
            logger.info(f"Password reset email sent to: {email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send password reset email to {email}: {str(e)}")
            return False
