from django.conf import settings


class SecurityHeadersMiddleware:
    """Add common security headers to responses.

    - Content-Security-Policy (minimal)
    - X-Content-Type-Options
    - Referrer-Policy
    - Permissions-Policy
    - Strict-Transport-Security (when SSL enforced)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Prevent MIME type sniffing
        response.setdefault('X-Content-Type-Options', 'nosniff')
        # Basic Referrer Policy
        response.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
        # Minimal permission policy (disable features by default)
        response.setdefault('Permissions-Policy', "geolocation=(), microphone=(), camera=()")
        # Content Security Policy: keep conservative default, adjust for your frontend
        csp = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; img-src 'self' data:; style-src 'self' 'unsafe-inline';"
        response.setdefault('Content-Security-Policy', csp)
        # HSTS when SSL redirect is enabled
        if getattr(settings, 'SECURE_SSL_REDIRECT', False) and getattr(settings, 'SECURE_HSTS_SECONDS', 0) > 0:
            response.setdefault('Strict-Transport-Security', f"max-age={settings.SECURE_HSTS_SECONDS}; includeSubDomains={str(settings.SECURE_HSTS_INCLUDE_SUBDOMAINS).lower()}; preload={str(settings.SECURE_HSTS_PRELOAD).lower()}")
        return response
