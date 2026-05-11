import re

def classify_with_regex(log_message):
    regex_patterns = {
        # User Actions
    r"User User\d+ logged (in|out)": "User Action",
    r"Account with ID \d+ created by .*": "User Action",
    r"Password reset requested by user .*": "User Action",

    # System Notifications
    r"Backup (started|ended) at .*": "System Notification",
    r"Backup completed successfully": "System Notification",
    r"Scheduled task completed at .*": "System Notification",

    # System Updates / Deprecation
    r"System updated to version .*": "System Update",
    r"Deprecated API .* detected": "Deprecation Warning",
    r"Legacy module .* is no longer supported": "Deprecation Warning",

    # File Operations
    r"File .* uploaded successfully by user": "File Operation",
    r"File .* deleted successfully": "File Operation",
    r"Document .* downloaded by user .*": "File Operation",

    # System Maintenance
    r"Disk cleanup completed successfully": "System Maintenance",
    r"Cache memory cleared successfully": "System Maintenance",
    r"Temporary files removed from system": "System Maintenance",

    # System Reboot
    r"System reboot initiated by user .*": "System Reboot",
    r"Server restarted successfully": "System Reboot",

    # Workflow Errors
    r"Email service failed to send notification to user .*": "Workflow Error",
    r"Payment workflow execution failed .*": "Workflow Error",
    r"Data synchronization job failed during execution": "Workflow Error",

    # Authentication Errors
    r"Invalid user credentials provided": "Authentication Error",
    r"Unauthorized access attempt detected": "Authentication Error",

    # Unrecognized
    r"Unrecognized log message format": "Unrecognized",
    r"Unknown status received from external service": "Unrecognized"
    }
    for pattern, label in regex_patterns.items():
        if re.search(pattern, log_message, re.IGNORECASE):
            return label
    return None

if __name__ == "__main__":
    print(classify_with_regex("User User123 logged in"))
    print(classify_with_regex("Backup started at 2024-06-01 10:00:00"))
    print(classify_with_regex("System updated to version 2.1.0"))       
    print(classify_with_regex("File report.pdf uploaded successfully by user"))
    print(classify_with_regex("Disk cleanup completed successfully"))
    print(classify_with_regex("System reboot initiated by user AdminUser"))
    print(classify_with_regex("Account with ID 456 created by AdminUser"))
    print(classify_with_regex("Unrecognized log message format"))
    