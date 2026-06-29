package archive.authz

default allow = false

# Reglerar åtkomst baserat på clearance_level
allow {
    input.method == "GET"
    input.user.clearance_level == "Secret" # Exempel: Secret har tillgång till allt
}

allow {
    input.method == "GET"
    input.user.clearance_level == "Normal"
    input.resource.security_class == "Normal" # Normal får bara läsa Normal
}