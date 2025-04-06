from typing import Any

import markdown
import pprint

from .custom_payload import Payload, new_custom_payload

def new_dump_payload(value: Any) -> Payload:
    raw_dump = pprint.pformat(value)

    md = f"```\n{raw_dump}\n```"

    html_output = markdown.markdown(md)

    styled_output = html_output.replace(
        "<pre><code>",
        '<pre class="relative overflow-x-auto w-full p-5 h-auto bg-gray-100 dark:bg-gray-800">'
        '<code class="h-auto">',
        1
    )

    return new_custom_payload(styled_output, "")
