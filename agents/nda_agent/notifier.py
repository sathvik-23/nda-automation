"""
Notification module for NDA Agent
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class Notifier:
    """Notification handler for NDA Agent"""
    
    def __init__(self, config: Dict[str, Any]):
        self.email = config.get("email")
        self.smtp_server = config.get("smtp_server", "smtp.gmail.com")
        self.smtp_port = config.get("smtp_port", 587)
        self.smtp_username = config.get("smtp_username")
        self.smtp_password = config.get("smtp_password")
        
        self.enabled = all([
            self.email,
            self.smtp_username,
            self.smtp_password
        ])
        
        if not self.enabled:
            logger.warning("Email notifications not fully configured")
    
    def send_email(self, subject: str, body: str, to_email: Optional[str] = None) -> bool:
        """
        Send an email notification.
        
        Args:
            subject: Email subject
            body: Email body content
            to_email: Recipient email (defaults to configured notification email)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            logger.warning("Email notifications not configured")
            return False
        
        recipient = to_email or self.email
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = recipient
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent successfully to {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def send_html_email(self, subject: str, html_body: str, to_email: Optional[str] = None) -> bool:
        """
        Send an HTML email notification.
        
        Args:
            subject: Email subject
            html_body: HTML email body content
            to_email: Recipient email (defaults to configured notification email)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            logger.warning("Email notifications not configured")
            return False
        
        recipient = to_email or self.email
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.smtp_username
            msg['To'] = recipient
            msg['Subject'] = subject
            
            # Add HTML body
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"HTML email sent successfully to {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send HTML email: {e}")
            return False
    
    def notify_document_created(self, document_id: str, template_name: str, recipient: str) -> bool:
        """
        Send notification when a new document is created.
        
        Args:
            document_id: PandaDoc document ID
            template_name: Name of the template used
            recipient: Document recipient
            
        Returns:
            True if successful, False otherwise
        """
        subject = f"NDA Document Created: {template_name}"
        body = f"""
A new NDA document has been created:

Document ID: {document_id}
Template: {template_name}
Recipient: {recipient}
Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Please review and send the document when ready.
        """
        
        return self.send_email(subject, body.strip())
    
    def notify_document_sent(self, document_id: str, template_name: str, recipient: str) -> bool:
        """
        Send notification when a document is sent for signature.
        
        Args:
            document_id: PandaDoc document ID
            template_name: Name of the template used
            recipient: Document recipient
            
        Returns:
            True if successful, False otherwise
        """
        subject = f"NDA Document Sent: {template_name}"
        body = f"""
An NDA document has been sent for signature:

Document ID: {document_id}
Template: {template_name}
Recipient: {recipient}
Sent: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

The recipient will receive an email with signing instructions.
        """
        
        return self.send_email(subject, body.strip())
    
    def notify_document_signed(self, document_id: str, template_name: str, recipient: str) -> bool:
        """
        Send notification when a document is signed.
        
        Args:
            document_id: PandaDoc document ID
            template_name: Name of the template used
            recipient: Document recipient
            
        Returns:
            True if successful, False otherwise
        """
        subject = f"NDA Document Signed: {template_name}"
        body = f"""
An NDA document has been signed:

Document ID: {document_id}
Template: {template_name}
Recipient: {recipient}
Signed: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

The document is now complete and legally binding.
        """
        
        return self.send_email(subject, body.strip())
    
    def notify_document_error(self, document_id: str, error_message: str) -> bool:
        """
        Send notification when there's an error with a document.
        
        Args:
            document_id: PandaDoc document ID
            error_message: Description of the error
            
        Returns:
            True if successful, False otherwise
        """
        subject = f"NDA Document Error: {document_id}"
        body = f"""
An error occurred with an NDA document:

Document ID: {document_id}
Error: {error_message}
Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Please check the document status and take appropriate action.
        """
        
        return self.send_email(subject, body.strip())
    
    def send_daily_summary(self, statistics: Dict[str, Any]) -> bool:
        """
        Send daily summary of NDA activities.
        
        Args:
            statistics: Dictionary containing NDA statistics
            
        Returns:
            True if successful, False otherwise
        """
        subject = f"NDA Daily Summary - {datetime.now().strftime('%Y-%m-%d')}"
        
        html_body = f"""
        <html>
        <body>
            <h2>NDA Daily Summary</h2>
            <p>Date: {datetime.now().strftime('%Y-%m-%d')}</p>
            
            <h3>Statistics</h3>
            <ul>
                <li>Total Documents: {statistics.get('total_documents', 0)}</li>
                <li>Documents Sent: {statistics.get('documents_sent', 0)}</li>
                <li>Documents Signed: {statistics.get('documents_signed', 0)}</li>
                <li>Pending Signatures: {statistics.get('pending_signatures', 0)}</li>
            </ul>
            
            <h3>Recent Activity</h3>
            <ul>
        """
        
        for activity in statistics.get('recent_activity', []):
            html_body += f"""
                <li>
                    <strong>{activity.get('timestamp', 'N/A')}</strong>: 
                    {activity.get('action', 'N/A').title()} - 
                    {activity.get('template_name', 'N/A')} 
                    ({activity.get('recipient', 'N/A')})
                </li>
            """
        
        html_body += """
            </ul>
        </body>
        </html>
        """
        
        return self.send_html_email(subject, html_body)
    
    def log_notification(self, notification_type: str, success: bool, details: str = "") -> None:
        """
        Log notification attempts.
        
        Args:
            notification_type: Type of notification
            success: Whether the notification was successful
            details: Additional details
        """
        status = "SUCCESS" if success else "FAILED"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_message = f"{timestamp} - {notification_type} - {status}"
        if details:
            log_message += f" - {details}"
        
        if success:
            logger.info(log_message)
        else:
            logger.error(log_message)
