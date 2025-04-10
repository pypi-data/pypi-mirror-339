import extra_streamlit_components as stx
from typing import Optional, Dict, Any
import time
import streamlit as st
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import base64
import json
import os

class SessionManager:
    """
    A simple session management library for Streamlit applications that allows 
    easy access to user session data from digitally signed URL parameters.
    """
    def __init__(self):
        """
        Initialize the session manager with RSA public key from environment variable
        """
        public_key_pem = os.getenv('STREAMLIT_SESSION_PUBLIC_KEY')
        if not public_key_pem:
            raise ValueError("Environment variable 'STREAMLIT_SESSION_PUBLIC_KEY' not set")
        
        try:
            self._public_key = serialization.load_pem_public_key(
                public_key_pem.encode()
            )
        except Exception as e:
            raise ValueError(f"Invalid public key format: {str(e)}")
            
        # Initialize session state if not already done
        if 'user_data' not in st.session_state:
            st.session_state.user_data = None
            
        self._load_user_data()

    def _load_user_data(self) -> None:
        """
        Load and verify signed user data from URL parameters and store in session state
        """
        try:
            # Get signed data from URL parameters
            signed_data = st.query_params.get("user_data", None)
            if not signed_data:
                return
                
            # Decode from URL-safe base64
            signed_bytes = base64.urlsafe_b64decode(signed_data)
            
            # Split the signature and the data
            signature = signed_bytes[:256]  # RSA signature is 256 bytes
            data = signed_bytes[256:]
            
            # Verify the signature
            self._public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            # Parse the JSON data and store in session state
            st.session_state.user_data = json.loads(data.decode())
        except Exception as e:
            print(f"Error loading user data: {str(e)}")
            st.session_state.user_data = None

    def get_user(self) -> Optional[Dict[str, Any]]:
        """
        Get user details from verified signed data stored in session state
        Returns: Dict with user details or None if not found
        """
        return st.session_state.user_data

    def get_email(self) -> Optional[str]:
        """
        Get user email from verified data stored in session state
        Returns: Email string or None if not found
        """
        return st.session_state.user_data.get('email') if st.session_state.user_data else None

    def get_full_name(self) -> Optional[str]:
        """
        Get user's full name from verified data stored in session state
        Returns: Full name string or None if not found
        """
        if not st.session_state.user_data:
            return None
            
        first_name = st.session_state.user_data.get('first_name')
        last_name = st.session_state.user_data.get('last_name')
        
        if first_name or last_name:
            return ' '.join(filter(None, [first_name, last_name]))
        return None

    def get_session_value(self, session_key: str) -> Optional[Any]:
        """
        Get value for a specific session key from verified data stored in session state
        Args:
            session_key: The key to lookup in the session
        Returns:
            The value associated with the key or None if not found
        """
        return st.session_state.user_data.get(session_key) if st.session_state.user_data else None    