# Task 4 Report: Interactive Chat Interface

## 1. Overview
The goal of Task 4 was to build a user-friendly, modern web interface for the Intelligent Complaint Analysis system. We utilized **Streamlit** to create a responsive chat application that allows analysts to interact with the RAG pipeline intuitively.

## 2. Key Features
- **Conversational Interface**: A chat-like experience using `st.chat_message` to maintain context visually.
- **RAG Integration**: Seamlessly connects to the pre-built RAG pipeline to retrieve and generate answers.
- **Source Verification**: Every answer is accompanied by an **expandable "📚 Source Documents" section**, displaying the exact complaint IDs and text chunks used by the model. This ensures transparency and trust.
- **Modern UI/UX**:
    - **Dark Theme**: Optimized for long working hours with a professional dark color scheme.
    - **Custom Styling**: Enhanced with custom CSS for rounded chat bubbles, gradient headers, and polished inputs.
    - **Streaming Simulation**: Answers appear token-by-token to improve perceived latency and user engagement.
- **Session Management**: Includes a "Clear Chat History" button to easily reset the analysis session.

## 3. Implementation Details
The interface is implemented in `src/app.py` and run via Streamlit.

### Core Components
- **`load_rag_pipeline()`**: Cached function to load the heavy RAG model only once, ensuring fast re-runs.
- **`st.session_state`**: Manages the chat history so previous Q&A pairs remain visible during interaction.
- **Css Injection**: Reads a rigorous set of CSS rules to override default Streamlit styles for a "premium" feel.

## 4. User Guide
1. **Launch**: Run `streamlit run src/app.py` in the terminal.
2. **Access**: Open the provided local URL (e.g., `http://localhost:8501`).
3. **Ask**: Type a question like *"What are the main complaints about credit card rewards?"* in the bottom input box.
4. **Verify**: Click "📚 View Source Documents" below the answer to see the evidence.
5. **Reset**: Use the sidebar "Clear Chat History" button to start fresh.

## 5. Conclusion
Task 4 is successfully completed. The interface meets all functional requirements (input, display, sources, clear button) and exceeds usability expectations with its modern design and streaming capabilities. The system is now ready for end-user testing.
