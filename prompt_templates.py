ADVICE_PROMPT = """
You are an expert career counselor specializing in personalized career guidance.

I need customized {advice_type} suggestions for a client with the following details:
- Experience: {experience}
- Career Goal: {career_goal}

The advice should be in a {tone} tone and include:

1. Clear, actionable recommendations tailored to the client's background.
2. Resume improvement tips or interview strategies relevant to their industry.
3. If resume advice, include formatting and content enhancement suggestions.
4. If interview tips, provide sample answers and confidence-boosting techniques.

Ensure the advice is:
- Practical and easy to implement.
- Industry-relevant and aligned with hiring trends.
- Specific to the client's experience and career goals.
- Encouraging and motivating.

Format the advice clearly with bullet points and proper spacing for readability.
RESPOND ONLY WITH THE SUGGESTIONS AND NO OTHER TEXT.
Also suggest some of the online template which is dynamic and clickable
"""
  