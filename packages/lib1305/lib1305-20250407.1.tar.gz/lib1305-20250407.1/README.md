Python wrapper around implementation of the Poly1305 one-time authenticator

### Poly1305

Import library:

    from lib1305 import poly1305

Authenticating a message:

    a = poly1305.auth(m, k)

Verifying an authenticator:

    poly1305.verify(a, m, k)
