**Short Answer:**  
You should instruct the developer to make changes in multiple files:

- **chroma_utils.py:** Add `return_source_documents=True` when creating the QA chain.
- **chat_routes.py:** After receiving the QA chain’s output, extract the page references from `response["source_documents"]` and include them in the JSON response to the frontend.
- **chat.js:** Modify the code that appends AI messages to include references and add event listeners for clicking on these references.
- **(Optional) PDF viewer integration file:** If you use a PDF.js viewer or another method, you may need to handle messages or URL changes to jump to a specific page in the PDF.

**Detailed Explanation:**

1. **chroma_utils.py:**
   - In the `get_qa_chain` function, add `return_source_documents=True` to the `RetrievalQA.from_chain_type` call. This ensures the QA chain returns both the answer and the documents that were used to produce it.
   
   For example:
   ```python
   qa = RetrievalQA.from_chain_type(
       llm=llm,
       chain_type="refine",
       retriever=retriever,
       chain_type_kwargs={
           "question_prompt": PROMPT,
           "refine_prompt": REFINE_PROMPT,
           "document_variable_name": "context"
       },
       return_source_documents=True
   )
   ```

2. **chat_routes.py:**
   - After calling `qa_chain.invoke({"query": query})`, you’ll have access to `response["source_documents"]`.
   - Extract page references from these documents’ metadata.
   - Include the pages in the JSON response to the frontend:
   ```python
   result = qa_chain.invoke({"query": query})
   answer = result["result"]
   sources = result.get("source_documents", [])
   pages = [doc.metadata.get("page") for doc in sources if doc.metadata.get("page")]

   return jsonify({'response': answer, 'pages': pages})
   ```

3. **chat.js:**
   - Modify the `appendMessage` or equivalent function that displays AI messages. After parsing and displaying the AI message, also display references as clickable links. For example:
   ```javascript
   function appendMessage(message, isUser, pages = []) {
       const messageDiv = document.createElement('div');
       messageDiv.classList.add('message', isUser ? 'user-message' : 'ai-message');

       if (isUser) {
           messageDiv.textContent = message;
       } else {
           const html = marked.parse(message);
           messageDiv.innerHTML = html;

           if (pages && pages.length > 0) {
               const refsDiv = document.createElement('div');
               refsDiv.classList.add('references');
               refsDiv.innerHTML = "<strong>References:</strong> " + pages.map(page => `<a href="#" class="ref-link" data-page="${page}">Page ${page}</a>`).join(", ");
               messageDiv.appendChild(refsDiv);
           }
       }

       messages.appendChild(messageDiv);
       messages.scrollTop = messages.scrollHeight;
   }
   ```

   - Add event listeners for `.ref-link` clicks to jump to the corresponding page in the PDF viewer.

4. **PDF Viewer Integration (if needed):**
   - Depending on how you integrate the PDF viewer, you may need a separate file or code snippet to handle `jumpToPageInPDF(pageNumber)` calls. This might mean listening for `postMessage` in the iframe or adjusting the `src` attribute of the iframe to load a specific page.

**Summary:**
- Add `return_source_documents=True` in `chroma_utils.py` to get source documents.
- Extract and return `pages` to frontend in `chat_routes.py`.
- Update `chat.js` to display references and handle clicks.
- Possibly integrate page-jumping logic in your PDF viewer code.

By implementing changes across these files, the developer can enable the display of references and allow users to click on them to navigate the PDF viewer accordingly.