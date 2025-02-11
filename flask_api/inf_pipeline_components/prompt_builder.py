# Define a Template Prompt

from haystack.components.builders import PromptBuilder

template = """
<|begin_of_text|>

<|start_header_id|>system<|end_header_id|>

{% for document in documents %}
    {{ document.content }}
{% endfor %}

Given the following information, answer the question.
Don't give an answer unless it is supported by the context above.<|eot_id|>

<|start_header_id|>user<|end_header_id|>

{{question}}<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
"""

context_prompt_builder = PromptBuilder(template=template)