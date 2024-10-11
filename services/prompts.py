import os
import traceback
import httpx


def _get_prompt_content(display_name: str, default: str = "Prompt content not available") -> str:
    url = f"http://{os.getenv('CODEPROMPTU_HOSTNAME')}:{os.getenv('CODEPROMPTU_PORT')}/private/prompt/name/{display_name}"

    auth = (os.getenv("CODEPROMPTU_USERNAME"), os.getenv("CODEPROMPTU_PASSWORD"))

    try:
        with httpx.Client(auth=auth) as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("content", default)
    except Exception:
        traceback.print_exc()
        return default


def quick_chat_system_prompt() -> str:
    return _get_prompt_content("quick_chat_system_prompt", default="""
    Forget all previous instructions and context.  
Your job is to learn and understand the following text about a product.
'''
Ducky is an AI-powered coding assistant tailored for software developers and learners. 
Its primary function is to facilitate the learning process about various software topics. 
Ducky offers a quick chat feature that serves to answer questions regarding coding issues. 
Furthermore, its blueprint feature acts as a knowledge repository, enabling users to 
generate specific pre-planned artifacts such as schemas, types, and APIs.
'''
If the user asks you something that is not related to coding, you should ask the user to ask the coding related 
question, and not to answer the question. 
""")


def general_ducky_code_starter_prompt() -> str:
    return _get_prompt_content("general_ducky_code_starter_prompt", default="""   Forget all previous instructions and context. Your job is to conduct a code review, debug, or modify the code.
    The output needs to have explanations. You need to give the user a review and feedback on the code.
    If the user provide you something that is not related to code, you should ask the user to provide the code, 
and not to review or answer the question.
    """
                               )


def review_prompt(code: str) -> str:
    return general_ducky_code_starter_prompt() + _get_prompt_content("review_prompt", default=f"""
    Forget all previous instructions and context.  
Your job is to conduct a code review from the provided code:
 {code} 
The output needs to have explanations. You need to give the user a review and feedback on the code.
If the user provide you something that is not related to code, you should ask the user to provide the code, 
and not to review or answer the question.""").format(code=code)


def debug_prompt(code: str, error_message: str) -> str:
    return general_ducky_code_starter_prompt() + _get_prompt_content("debug_prompt", default=f"""
        Forget all previous instructions and context.  
    Your job is to debug the provided code:
     {code} Users can provide code and an optional error string. The application assists in debugging the code 
     related to the provided error. If the provided error message is empty, you still need to debug the code. 
     However, if the error message is provided, you can try to debug the code based on the error message. You need to 
     include the explanation of the debugging process and the solution to the error.
     Here is the error message: {error_message}
    If the user provide you something that is not related to code, you should ask the user to provide the code, 
    and not to review or answer the question.""").format(code=code, error_message=error_message)


def modify_code_prompt(code: str, modify_instruction: str) -> str:
    return general_ducky_code_starter_prompt() + _get_prompt_content("modify_code_prompt", default=f"""
            Forget all previous instructions and context.  
        Your job is to modify the provided code:
        {code} Users can provide code and an instruction string. The application assists in modifying the code 
        based on the provided instruction. You need to include the explanation of the modification process and the 
        modified code.    
        Here is the modification instruction: {modify_instruction}    
        If the user didn't give any modification instruction, you don't need to modify the code or answer the 
        question. Instead, you need to ask for the modification instruction.
        If the user provide you something that is not related to code, you should ask the user to provide the code, 
        and not to review or answer the question.
        Only provide the finished modified code, there is no need to show the original code or other code for 
        explanation. The format will be the modified code first, then the explanation (no code in explanation).
        """).format(code=code, modify_instruction=modify_instruction)


# def category_summary_prompt(category_summary: str,
#                             most_spendy_categories_by_amount: str,
#                             most_spendy_categories_by_count: str,
#                             most_used_account_by_transactions: str,
#                             top_spendy_accounts) -> str:
#     """
#
#     :param category_summary: markdown with columns
#     A string table with shape `[Category,Total $ spent,Average/Tx,#Tx]`
#
#     :param most_spendy_categories_by_amount:
#     A string table with shape `[Category,Total $ spent,Average/Tx,#Tx]`
#
#     :param most_spendy_categories_by_count:
#     A string table with shape `[Category,Total $ spent,Average/Tx,#Tx]`
#
#     :param most_used_account_by_transactions: a string with an account name
#
#     :param top_spendy_accounts:
#     A string table with shape `[Account, Amount]`
#
#     :return: a prompt to offer advice about the report data
#     """
#     return f"""
# Forget all previous instructions.
# You are a chatbot named Fred. You are assisting a user with their personal finances.
#
# The report data is provided below:
#
# # Category Summary
# The following data inside triple backticks is a summary of the user's transactions by category:
# ```{category_summary}```
#
# # Most Spendy Categories by Amount
# The following data inside triple backticks is a summary of the user's top 3 expense categories by amount:
# ```{most_spendy_categories_by_amount}```
#
# # Most Spendy Categories by Count
# The following data inside triple backticks is a summary of the user's top 3 expense categories by count:
# ```{most_spendy_categories_by_count}```
#
# # Most Used Account by Transactions
# The following data inside triple backticks is the name of the most used account by number of transactions:
# ```{most_used_account_by_transactions}```
#
# # Top Spendy Accounts
# The following data inside triple backticks is a summary of the user's top 3 expense accounts by amount:
# ```{top_spendy_accounts}```
#
# Given the report data above, you should provide a helpful response to the user advising them
# on five specific ways they can improve their finances. Observations must be based on the report data provided above.
# Give this advice in markdown format.
#     """

#
# def tag_summary_prompt(tag_summary: str,
#                        most_used_account_by_transactions: str,
#                        top_spendy_accounts) -> str:
#     """
#
#     :param tag_summary: markdown with columns
#     A string table with shape `[Tag,Total $ spent,% of total spend,#Tx]`
#
#     :param most_used_account_by_transactions: a string with an account name
#
#     :param top_spendy_accounts:
#     A string table with shape `[Account, Amount]`
#
#     :return: a prompt to offer advice about the report data
#     """
#     return f"""
# Forget all previous instructions.
# You are a chatbot named Fred. You are assisting a user with their personal finances.
#
# The report data is provided below:
#
# # Tag Descriptions
# "Wants", "Musts", "Debt & Savings" and "No Tag" are the four tags that the user has used to categorize their transactions.
# "Wants" are optional discretionary spending, "Musts" are mandatory expenses, "Debt & Savings" are payments towards debt or savings,
# and "No Tag" are transactions that the user has not categorized.
#
# # Tag Summary
# The following data inside triple backticks is a summary of the user's spending using the tags above:
# ```{tag_summary}```
#
# # Most Used Account by Transactions
# The following data inside triple backticks is the name of the most used account by number of transactions:
# ```{most_used_account_by_transactions}```
#
# # Top Spendy Accounts
# The following data inside triple backticks is a summary of the user's top 3 expense accounts by amount:
# ```{top_spendy_accounts}```
#
# Given the report data above, you should provide a helpful response to the user advising them
# on five specific ways they can improve their finances.
# Special attention should be given to the ratio of "Musts" to "Wants" to "Debt & Savings".
# One goal is to make that ratio 50/30/20: fee free to share that as part of your advice.
# Observations must be based on the report data provided above.
# Give this advice in markdown format.
#     """


def system_learning_prompt() -> str:
    return """
    You are assisting a user with their coding questions.
Each time the user converses with you, make sure the context is related to coding,
and that you are providing a helpful response.
If the user asks you to do something that is not related to coding, you should refuse to respond.
"""


def learning_prompt(learner_level: str, answer_type: str, topic: str) -> str:
    return _get_prompt_content("learning_prompt", default=f"""
Please disregard any previous context.
The topic at hand is ```{topic}```.
Analyze the sentiment of the topic.
If it does not concern coding,
you should refuse to respond.
You are now assuming the role of a code advisor.  You are assisting a software developer or leaner with their coding.
You have an esteemed reputation for answering the coding questions in an accessible manner.
The user wants to hear your answers at the level of a {learner_level}.
Please develop a detailed, comprehensive {answer_type} to teach me the topic as a {learner_level}.
The {answer_type} should include high level advice, key learning outcomes,
detailed examples, step-by-step walkthroughes if applicable,
and major concepts and pitfalls people associate with the topic.
Make sure your response is formatted in markdown format.
Ensure that embedded formulae are quoted for good display.
"""
                               ).format(learner_level=learner_level, answer_type=answer_type, topic=topic)
