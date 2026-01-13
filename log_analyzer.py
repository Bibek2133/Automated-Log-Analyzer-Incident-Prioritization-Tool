import re
from collections import Counter
from datetime import datetime
import os

# Read Log File
def read_logs(file_path):
    if not os.path.exists(file_path):
        print("Log file not found.")
        return []

    with open(file_path, "r") as file:
        return file.readlines()

# Detect Issues Using Regex
def detect_issues(log_lines):
    issues = []

    pattern = re.compile(r"(CRITICAL|ERROR|WARNING)\s+(.*)", re.IGNORECASE)

    for line in log_lines:
        match = pattern.search(line)
        if match:
            level = match.group(1).upper()
            message = match.group(2).strip()
            issues.append((level, message))

    return issues

# Count Repeated Issues
def count_issues(issues):
    messages = [msg for _, msg in issues]
    return Counter(messages)

# Assign Incident Priority
def assign_priority(issues, issue_counts):
    priorities = {}

    for message, count in issue_counts.items():
        if any(level == "CRITICAL" for level, msg in issues if msg == message):
            priorities[message] = "P1 - Critical"
        elif count >= 3:
            priorities[message] = "P2 - High"
        elif count == 2:
            priorities[message] = "P3 - Medium"
        else:
            priorities[message] = "P4 - Low"

    return priorities

# Generate Incident Report
def generate_report(issue_counts, priorities):
    with open("incident_report.txt", "w") as report:
        report.write("INCIDENT SUMMARY REPORT\n")
        report.write("=" * 40 + "\n")
        report.write(f"Generated on: {datetime.now()}\n\n")

        for issue, count in issue_counts.items():
            report.write(f"Issue: {issue}\n")
            report.write(f"Occurrences: {count}\n")
            report.write(f"Priority: {priorities[issue]}\n")
            report.write("Suggested Action: Investigate service, check logs, escalate if needed\n")
            report.write("-" * 40 + "\n")

def main():
    log_file = "sample_logs.log"
    log_lines = read_logs(log_file)

    if not log_lines:
        return

    issues = detect_issues(log_lines)
    issue_counts = count_issues(issues)
    priorities = assign_priority(issues, issue_counts)

    generate_report(issue_counts, priorities)

    print("Log analysis completed. Incident report generated.")

if __name__ == "__main__":
    main()
