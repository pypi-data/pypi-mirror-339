from sentence_transformers import CrossEncoder
from forcolate import search_outlook_emails, search_folder, convert_folders_to_markdown    

import os

DEFAULT_TOOLS = [
    (
        "Search in Folders",
        "Search in Local Folders and Documents: This tool allows you to search for files and documents within your local directories. You can find items by their names, content, or metadata across various file types, including text documents, spreadsheets, and presentations.",
        search_folder
    ),
    (
        "Search in Outlook",
        "Search in Outlook Email: This tool enables you to search through your Outlook emails. You can filter emails based on criteria such as sender, recipient, subject, date, and content. It can search across different email folders, including the inbox and sent items.",
        search_outlook_emails
    ),
    (
        "Convert to text",
        "Convert Documents to Text: This tool converts documents from various formats into plain text. It supports formats like PDF and Word documents, extracting the textual content while removing formatting elements.",
        convert_folders_to_markdown
    )
]


def select_tool(message, available_tools=DEFAULT_TOOLS):

    # Load the pre-trained model
    model_path = os.path.join(os.path.dirname(__file__), 'vendors', 'ms-marco-MiniLM-L6-v2')
    model = CrossEncoder(model_path)

    # Prepare the input pairs for the model
    input_pairs = [[message, tool] for name,tool, fun in available_tools]

    # Compute similarity scores
    similarity_scores = model.predict(input_pairs)

    # Find the tool with the highest similarity score
    best_tool_index = similarity_scores.argmax()
    best_tool = available_tools[best_tool_index]

    return best_tool

