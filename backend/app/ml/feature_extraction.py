from urllib.parse import urlparse
import re


def extract_features(url):
    parsed = urlparse(url)

    hostname = parsed.netloc.lower()

    # Remove port number from hostname
    hostname_without_port = hostname.split(":")[0]

    path = parsed.path
    query = parsed.query

    # Suspicious words commonly found in phishing URLs
    suspicious_words = [
        "login",
        "signin",
        "verify",
        "verification",
        "account",
        "update",
        "secure",
        "security",
        "password",
        "confirm",
        "bank",
        "payment",
        "wallet",
        "recover",
    ]

    suspicious_word_count = sum(
        1 for word in suspicious_words
        if word in url.lower()
    )

    features = {
        # Basic URL features
        "url_length": len(url),

        "has_https": 1 if parsed.scheme == "https" else 0,

        "dot_count": url.count("."),

        "hyphen_count": url.count("-"),

        "at_symbol": 1 if "@" in url else 0,

        "question_mark": 1 if "?" in url else 0,

        "equal_symbol": 1 if "=" in url else 0,

        "slash_count": url.count("/"),

        "digit_count": sum(char.isdigit() for char in url),

        # IP address detection
        "has_ip": 1 if re.search(
            r"https?://(?:\d{1,3}\.){3}\d{1,3}",
            url
        ) else 0,

        # Additional URL features
        "hostname_length": len(hostname_without_port),

        "path_length": len(path),

        "query_length": len(query),

        "subdomain_count": max(
            0,
            len(hostname_without_port.split(".")) - 2
        ),

        "has_port": 1 if parsed.port else 0,

        "double_slash": 1 if "//" in path else 0,

        "percent_encoding": 1 if "%" in url else 0,

        "has_punycode": 1 if "xn--" in hostname_without_port else 0,

        "suspicious_word_count": suspicious_word_count,
    }

    return features