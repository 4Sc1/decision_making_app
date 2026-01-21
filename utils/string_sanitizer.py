class StringSanitizer:
    @staticmethod
    def sanitize(text, semicolon_replacement=',', newline_replacement=' ', quote_replacement="'"):
        sanitized = text.replace(';', semicolon_replacement)
        sanitized = sanitized.replace('\n', newline_replacement).replace('\r', newline_replacement)
        sanitized = sanitized.replace('"', quote_replacement)
        return sanitized
