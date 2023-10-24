from llama_cpp import Llama

llm = Llama(
    model_path="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    n_gpu_layers=-1, main_gpu=1
)

output = llm(
    "Q: Name the planets in the solar system and invent a new one. A: ",
    max_tokens=258,
    stop=["Q:", "\n"],
    echo=True,
)

print(output)
