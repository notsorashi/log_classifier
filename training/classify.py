import pandas as pd

from regex_exp import classify_with_regex
from processorbert import classify_with_bert
from processor_llm import classify_with_llm

def classify(logs):
    labels = []
    for source, log_msg in logs:
        label = classify_log(source, log_msg)
        labels.append((source, log_msg, label))
    return labels


def classify_log(source,log_message):
    if source == "LegacyCRM":
        label = classify_with_llm(log_message)
    else:
        label = classify_with_regex(log_message)
        if label is None:
            label = classify_with_bert(log_message)   
        return label

def classify_csv(input_file):
    df = pd.read_csv(input_file)
    
    df["target_label"] = classify(list(zip(df["source"], df["log_message"])))
    
    output_file = "output.csv"
    df.to_csv(output_file, index=False)



if __name__ == "__main__":
    classify_csv("resources/test.csv")
    """logs = [
    ("Billing System", "User User123 logged in"),
    ("Modern CRM", "Account with ID 456 created by AdminUser"),
    ("LegacyCRM", "Password reset requested by user User789"),
    ("LegacyCRM", "Backup started at 2024-06-01 10:00:00"),
    ("Billing System", "Scheduled task completed at 2024-06-01 12:00:00"),
    ("Modern CRM", "System updated to version 2.1.0"),
    ("LegacyCRM", "Deprecated API v1 detected"),
    ("Billing System", "Legacy module payment_gateway is no longer supported"),
    ("Modern CRM", "Deprecated API authentication_v1 detected"),
    ("LegacyCRM", "File report.pdf uploaded successfully by user"),
    ("Billing System", "File invoice.xlsx deleted successfully"),
    ("Modern CRM", "Document summary.docx downloaded by user User123"),
    ("LegacyCRM", "Disk cleanup completed successfully"),
    ("Modern CRM", "Cache memory cleared successfully"),
    ("Billing System", "Temporary files removed from system"),
    ("Modern CRM", "System reboot initiated by user AdminUser"),
    ("LegacyCRM", "Server restarted successfully"),
    ("LegacyCRM", "Email service failed to send notification to user User123"),
    ("Billing System", "Payment workflow execution failed due to timeout"),
    ("Modern CRM", "Data synchronization job failed during execution"),
    ("LegacyCRM", "Invalid user credentials provided"),
    ("Billing System", "Unauthorized access attempt detected"),
    ("LegacyCRM", "Unrecognized log message format"),
    ("Modern CRM", "Unknown status received from external service")
    ]

classified_logs = classify(logs)
print(classified_logs)"""