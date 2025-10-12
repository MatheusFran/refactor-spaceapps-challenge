GRADE_PROMPT = (
    "You are a grader assessing relevance of a retrieved document to a user question.\n"
    "Here is the retrieved document:\n\n{context}\n\n"
    "Here is the user question: {question}\n"
    "If the document contains keyword(s) or semantic meaning related to the user question, "
    "grade it as relevant. Give a binary score 'yes' or 'no'."
)

REWRITE_PROMPT = (
    "Look at the input and try to reason about the underlying semantic intent / meaning.\n"
    "Here is the initial question:\n-------\n{question}\n-------\n"
    "Formulate an improved question:"
)

GENERATE_PROMPT = (
    "You are a NASA BioScience assistant. Answer the user's question using the context from NASA experiments. "
    "Your output must be a JSON object with the following fields:\n"
    "1. abstract: a concise summary (max 3 sentences) of the main findings related to the question.\n"
    "2. graph_datas: a dictionary with data for charts, including:\n"
    "   - experiments_timeline: {year: number of experiments}\n"
    "   - subject_distribution: {research area: count}\n"
    "   - relevance_scores: [{title: ..., score: ...}]\n"
    "3. documents: a list of relevant publications, each with:\n"
    "   - title\n"
    "   - authors\n"
    "   - date\n"
    "   - summary\n"
    "   - url\n"
    "   - keywords\n"
    "   - relevance\n\n"
    "Include links and titles for each publication, and generate data suitable for pie and bar charts. "
    "If information is missing, leave fields empty or null, but always return valid JSON.\n\n"
    "Question: {question}\n"
    "Context: {context}"
)
