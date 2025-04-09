import json
from typing import List
from lib import get_formatted_filelist_str, resolve_relative_path


def guess_files_in_message(cwd: str, user_message: str) -> List[str]:
    try:
        value = extract(
            {"includedFiles": ["relative path format", "relative path format", "..."]},
            'Please find the files mentioned in the text. If none, return {"includedFiles": []}:\n'
            + user_message,
        )
        return [resolve_relative_path(cwd, p) for p in value["includedFiles"]]
    except:
        print("Failed to guess files in message")
        return []


def generate_user_task_prompt(conversation_history, cwd, user_input: str, bot_setting_file:str):
    # 需要重新读取openedFiles和activeFile
    with open(bot_setting_file, encoding="utf-8") as f: 
        bot_setting = json.load(f)
    folder_context = bot_setting["folderContext"]
    opened_files = bot_setting["openedFiles"]
    active_file = bot_setting["activeFile"]

    if folder_context:
        potential_paths = guess_files_in_message(cwd, user_input)

        existing_files = get_formatted_filelist_str(cwd, True, 200)

        active_file_str = f"Currently viewing: {active_file}" if active_file else ""
        
        opened_files_str = '\n'.join(opened_files)
        opened_files_str =  f"Open tabs:\n{opened_files_str}" if opened_files else ""
        
        existing_files_str = f"Files in directory:\n{existing_files}" if existing_files else ""
        return f"""<task>
{user_input}
</task>

<environment_details>
Current working directory: {cwd}

{active_file_str}

{opened_files_str}

{existing_files_str}

{format_content(cwd, potential_paths, conversation_history)}

</environment_details>
    """

    else:
        return f"""<task>
{user_input}
</task>
"""
