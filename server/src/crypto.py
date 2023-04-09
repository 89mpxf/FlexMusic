############################################################
# FlexMusic Cryptography Library                           #
# Revision: 2023M3R1-SX                                    #
# Written by: cooper@mpxf.men                              #
# Designed specifically for the official FlexMusic server. #
############################################################

# Import dependencies
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from time import time

# Import local dependencies
from .util import log

def generate_parameters(ksize: int, debug: bool = False) -> tuple[dh.DHParameters, bytes, dh.DHPrivateKey, dh.DHPublicKey, bytes]:
    """Diffie-Hellman parameter generation called by the bootstrapper. Should not be called manually."""
    st = time()
    if debug:
        log("bootstrap/crypto", f"Generating Diffie Hellman parameters (key size: {ksize})...")
    parameters = dh.generate_parameters(generator=2, key_size=ksize, backend=default_backend())
    if debug:
        log("bootstrap/crypto", "Serializing Diffie Hellman parameters...")
    parameter_bytes = parameters.parameter_bytes(encoding=serialization.Encoding.PEM, format=serialization.ParameterFormat.PKCS3)
    if debug:
        log("bootstrap/crypto", "Generating server private key...")
    private_key = parameters.generate_private_key()
    if debug:
        log("bootstrap/crypto", "Generating server public key...")
    public_key = private_key.public_key()
    if debug:
        log("bootstrap/crypto", "Serializing server public key...")
    public_key_bytes = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    et = time()
    if debug:
        log("bootstrap/crypto", f"Successfully generated and serialized server keyring in {et-st:.2}s.")
    return tuple([parameters, parameter_bytes, private_key, public_key, public_key_bytes])

@staticmethod
def process_client_key(client_key_bytes: bytes, session_id: int, server_keyring: tuple[dh.DHParameters, bytes, dh.DHPrivateKey, dh.DHPublicKey, bytes], debug: bool = False) -> Fernet | None:
    """Processes the Diffie-Hellman key exchange between the server and the client and generates the encryption/decryption cipher.\n
    This function is called by the handshake handler for the session and should not be called manually."""
    try:
        if debug:
            log(f"session-{session_id}/handshake/crypto", "Deserializing client public key...")
        client_key = serialization.load_pem_public_key(client_key_bytes, backend=default_backend())
        if debug:
            log(f"session-{session_id}/handshake/crypto", "Generating shared key...")
        shared_key = server_keyring[2].exchange(client_key)
        if debug:
            log(f"session-{session_id}/handshake/crypto", "Deriving shared key...")
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=None,
            backend=default_backend()
        ).derive(shared_key)
        if debug:
            log(f"session-{session_id}/handshake/crypto", "Key exchange complete. Generating Fernet encryption/decryption cipher...")
        cipher = Fernet(urlsafe_b64encode(derived_key))
        if debug:
            log(f"session-{session_id}/handshake/crypto", "Successfully generated Fernet encryption/decryption cipher.")
        return cipher
    except:
        if debug:
            log(f"session-{session_id}/handshake/crypto", "Failed to process client key.")
        return None