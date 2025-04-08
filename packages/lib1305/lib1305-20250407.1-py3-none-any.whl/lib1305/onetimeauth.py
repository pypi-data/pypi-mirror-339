from typing import Tuple as _Tuple
import ctypes as _ct
from ._lib import _lib, _check_input


class poly1305:
    KEYBYTES = 32
    BYTES = 16

    def __init__(self) -> None:
        '''
        '''
        self._c_auth = getattr(_lib, 'lib1305_onetimeauth_poly1305')
        self._c_auth.argtypes = [_ct.c_char_p,
                                 _ct.c_char_p, _ct.c_longlong, _ct.c_char_p]
        self._c_auth.restype = None
        self._c_verify = getattr(_lib, 'lib1305_onetimeauth_poly1305_verify')
        self._c_verify.argtypes = [_ct.c_char_p,
                                   _ct.c_char_p, _ct.c_longlong, _ct.c_char_p]
        self._c_auth.restype = None

    def auth(self, m, k):
        '''
        Auth - generates an authenticator 'a' given a message 'm' and a secret key 'k'.
        Parameters:
            m (bytes): message
            k (bytes): secret key
        '''
        _check_input(m, -1, 'm')
        _check_input(k, self.KEYBYTES, 'k')
        mlen = _ct.c_longlong(len(m))
        m = _ct.create_string_buffer(m)
        k = _ct.create_string_buffer(k)
        a = _ct.create_string_buffer(self.BYTES)
        self._c_auth(a, m, mlen, k)
        return a.raw

    def verify(self, a, m, k):
        '''
        Verify - verifies an authenticator 'a' given a message 'm' and a secret key 'k'.
        Parameters:
            a (bytes): authenticator
            m (bytes): message
            k (bytes): secret key
        '''
        _check_input(a, self.BYTES, 'a')
        _check_input(m, -1, 'm')
        _check_input(k, self.KEYBYTES, 'k')
        mlen = _ct.c_longlong(len(m))
        m = _ct.create_string_buffer(m)
        k = _ct.create_string_buffer(k)
        a = _ct.create_string_buffer(a)
        if self._c_verify(a, m, mlen, k):
            raise Exception('verify failed')


poly1305 = poly1305()
