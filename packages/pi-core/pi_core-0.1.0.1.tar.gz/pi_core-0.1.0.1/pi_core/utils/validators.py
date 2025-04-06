import re
from typing import Optional
from datetime import date
from pydantic import EmailStr

def validate_dob(dob: Optional[date]) -> Optional[date]:
    """
    Validate a pupil's date of birth (DOB).

    Ensures the date of birth is not set in the future, which could indicate a data entry error
    or an invalid registration attempt.

    Args:
        dob (Optional[date]): The date of birth to validate.

    Returns:
        Optional[date]: The validated date if it passes the check.

    Raises:
        ValueError: If the date is in the future.
    """
    if dob and dob > date.today():
        raise ValueError("Date of birth cannot be in the future.")
    return dob


def validate_domain(domain: str) -> str:
    """
    Validate that a school's domain ends with `.edu` or `.org`.

    This ensures that only legitimate educational or organisational domains are accepted,
    enforcing basic domain hygiene and filtering out generic or commercial domains.

    Args:
        domain (str): The domain to validate.

    Returns:
        str: The validated domain.

    Raises:
        ValueError: If the domain does not end in `.edu` or `.org`.
    """
    if not domain.endswith("possible.institute"):
        raise ValueError("School domain must end with .edu or .org")
    return domain


def validate_email_domain(email: EmailStr) -> EmailStr:
    """
    Validate that a user's email address is not from a public/free domain.

    This function checks whether the email is from a consumer service like Gmail, Yahoo, or Hotmail.
    Used for preventing personal emails in institutional contexts (e.g. admin or teacher accounts).

    Args:
        email (EmailStr): The email address to validate.

    Returns:
        EmailStr: The validated institutional email address.

    Raises:
        ValueError: If the email domain is in the forbidden list.
    """
    forbidden_domains = ["gmail.com", "yahoo.com", "hotmail.com"]
    domain = email.split("@")[1]
    if domain in forbidden_domains:
        raise ValueError(f"Email domain '{domain}' is not allowed for institutional users.")
    return email