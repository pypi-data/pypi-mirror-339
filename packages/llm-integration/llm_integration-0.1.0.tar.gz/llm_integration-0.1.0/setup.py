from setuptools import setup, find_packages

setup(
    name='llm_integration',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pydantic',
        'backoff',
        'ollama',   # or mark these as optional if some users won't need both
        'openai',
    ],
    python_requires='>=3.10',
)
