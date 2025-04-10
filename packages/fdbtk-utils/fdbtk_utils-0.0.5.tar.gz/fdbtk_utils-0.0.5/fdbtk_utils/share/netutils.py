import socket


def setup_uri(prefix, step, identifier, base_domain):
    return f"{prefix}.{step}.{identifier}.{base_domain}"


def check_dms(fqdn):
    try:
        # Attempt to resolve the FQDN to an IP address
        socket.gethostbyname(fqdn)
    except Exception:
        # Silently handle any exceptions during resolution
        pass
