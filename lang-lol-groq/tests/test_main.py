import pytest
from unittest.mock import patch, MagicMock
import psycopg2
import streamlit as st
from main import save_conversation_to_db, initialize_session_state

@pytest.fixture
def mock_db_connection():
    # Mock database connection
    with patch("main.get_db_connection") as mock_conn:
        mock_conn.return_value = MagicMock(psycopg2.extensions.connection)
        yield mock_conn

def test_initialize_session_state():
    # Test to verify that the session state is initialized correctly
    st.session_state = {}
    initialize_session_state()
    
    assert 'responses' in st.session_state
    assert st.session_state['responses'] == ["Please elaborate your question related to the game League of Legends"]
    
    assert 'requests' in st.session_state
    assert st.session_state['requests'] == ["Ex: What is the main role of Garen in League of Legends?"]
    
    assert 'buffer_memory' in st.session_state
    assert isinstance(st.session_state.buffer_memory, ConversationBufferWindowMemory)

def test_save_conversation_to_db(mock_db_connection):
    # Test to verify that conversations are saved to the database
    mock_cursor = MagicMock()
    mock_db_connection.return_value.cursor.return_value = mock_cursor
    
    question = "What is the role of Garen?"
    response = "Garen is a top lane champion."
    
    save_conversation_to_db(question, response)
    
    # Verify that the cursor.execute method was called with the correct parameters
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO conversation_history (question, response) VALUES (%s, %s)",
        (question, response)
    )
    
    # Verify that the transaction was committed
    mock_db_connection.return_value.commit.assert_called_once()

if __name__ == "__main__":
    pytest.main()