import re
import pyperclip


def sort_api_errors(file_content):
    # Find the start of the ApiError class definition
    class_start = file_content.find("class ApiErrorIdentifier(str, Enum):")
    if class_start == -1:
        return "Could not find ApiErrorIdentifier class"

    # Find all enum definitions
    enum_pattern = r'    ([A-Z_]+)\s*=\s*"([a-z_]+)"'
    enum_matches = re.finditer(enum_pattern, file_content)

    # Extract all enum entries
    enum_entries = []
    for match in enum_matches:
        full_match = match.group(0)
        enum_name = match.group(1)
        enum_entries.append((enum_name, full_match.strip()))

    # Sort entries by enum name
    sorted_entries = sorted(enum_entries, key=lambda x: x[0])

    # Reconstruct the class content
    class_header = "class ApiErrorIdentifier(str, Enum):\n\n"
    sorted_content = class_header + "\n    ".join(entry[1] for entry in sorted_entries)

    return sorted_content


# Example usage:
if __name__ == "__main__":
    with open("python/crypticorn/common/errors.py", "r") as f:
        content = f.read()

    sorted_content = sort_api_errors(content)
    pyperclip.copy(sorted_content)
