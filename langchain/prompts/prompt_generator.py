from langchain_core.prompts import PromptTemplate

# template
template = PromptTemplate(
    template="Greet this person in 5 languages. The name of the person is {name}",
input_variables=['name'],
validate_template=True
)

template.save('template.json')