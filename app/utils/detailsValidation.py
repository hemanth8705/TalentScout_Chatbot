import re
from datetime import datetime

# Predefined departments list
DEPARTMENTS = ["Full Stack", "Frontend", "Backend", "UI/UX", "Data Scientist"]

def validate_name(name: str) -> bool:
    """
    Validate Full Name:
    - Must be alphabetic (spaces allowed)
    - At least 2 characters long
    """
    if not name or len(name.strip()) < 2:
        return False
    return all(char.isalpha() or char.isspace() for char in name.strip())

def validate_email(email: str) -> bool:
    """
    Validate Email Address:
    - Must match a standard email regex
    """
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(email_pattern, email))

def validate_phone(phone: str) -> bool:
    """
    Validate Phone Number:
    - Digits only
    - Length between 10 to 15 characters
    """
    return phone.isdigit() and 10 <= len(phone) <= 15

def validate_dob(dob: str) -> bool:
    """
    Validate Date of Birth (optional):
    - Format should be YYYY-MM-DD
    - Applicant must be older than 18
    """
    try:
        dob_date = datetime.strptime(dob, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
        return age > 18
    except Exception:
        return False

def validate_experience(exp: int) -> bool:
    """
    Validate Years of Experience:
    - Must be a number greater than or equal to 0
    """
    return isinstance(exp, (int, float)) and exp >= 0

def validate_department(department: str) -> bool:
    """
    Validate Department Applied:
    - Must be one of the predefined options
    """
    return department in DEPARTMENTS

def validate_programming_languages(languages: list) -> bool:
    """
    Validate Programming Languages:
    - Should not be empty
    - Each language should be a non-empty string
    """
    return bool(languages) and all(isinstance(lang, str) and lang.strip() for lang in languages)

def validate_frameworks(frameworks) -> bool:
    """
    Validate Frameworks Known:
    - Optional field but if provided, every entry should be a non-empty string
    """
    if frameworks is None:
        return True
    if isinstance(frameworks, list):
        return all(isinstance(framework, str) and framework.strip() for framework in frameworks)
    return False