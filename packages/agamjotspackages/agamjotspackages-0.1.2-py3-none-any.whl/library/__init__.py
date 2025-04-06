def askai(question, model):
    import cohere
    co = cohere.Client('LMrLYbBsVoOLIAPghzjPcKomJr5mXzjWsnmmFPGZ')
    response = co.generate(
        model=model,
        prompt=question
    )
    return response.generations[0].text