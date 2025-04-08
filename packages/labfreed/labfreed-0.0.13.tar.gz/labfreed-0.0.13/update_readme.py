# update_readme.py
start_marker = "<!-- BEGIN EXAMPLES -->"
end_marker = "<!-- END EXAMPLES -->"

with open("examples.py", encoding='utf-8') as ex_file:
    example_code = ex_file.read()

# Optional: Format as Markdown code block
example_code_md = f"```python\n{example_code}\n```"

with open("README.md", encoding='utf-8') as readme_file:
    readme = readme_file.read()

if not readme:
    raise ValueError('README.md is empty')

# Replace the section between markers
new_readme = (
    readme.split(start_marker)[0]
    + start_marker + "\n"
    + example_code_md + "\n"
    + end_marker
    + readme.split(end_marker)[1]
)

with open("README.md", "w", encoding='utf-8') as readme_file:
    readme_file.write(new_readme)
