from transformers import AutoTokenizer, TextIteratorStreamer
from optimum.intel.openvino import OVModelForCausalLM
from threading import Thread

DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\
"""


def build_inputs(history: list[tuple[str, str]],
                 query: str,
                 system_prompt=DEFAULT_SYSTEM_PROMPT) -> str:
    texts = [f'{system_prompt}<|end_of_turn|>\n']
    for user_input, response in history:
        texts.append(
            f'GPT4 Correct User: {user_input.strip()} \nGPT4 Correct Assistant: {response.strip()}\n')
    texts.append(f'GPT4 Correct User: {query.strip()} <|end_of_turn|> GPT4 Correct Assistant: ')
    return ''.join(texts)


class LlamaModel():
    def __init__(self,
                 model_path,
                 device='CPU') -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(model_path,
                                                        trust_remote_code=True)
        self.ov_model = OVModelForCausalLM.from_pretrained(model_path,
                                                           compile=False,
                                                           device=device)
        self.ov_model.compile()
    def generate_iterate(self, prompt: str, max_generated_tokens, top_k, top_p,
                         temperature):
        # Tokenize the user text.
        model_inputs = self.tokenizer(prompt, return_tensors="pt")

        # Start generation on a separate thread, so that we don't block the UI. The text is pulled from the streamer
        # in the main thread. Adds timeout to the streamer to handle exceptions in the generation thread.
        streamer = TextIteratorStreamer(self.tokenizer,
                                        skip_prompt=True,
                                        skip_special_tokens=True)
        generate_kwargs = dict(model_inputs,
                               streamer=streamer,
                               max_new_tokens=max_generated_tokens,
                               do_sample=True,
                               top_p=top_p,
                               temperature=float(temperature),
                               top_k=top_k,
                               eos_token_id=self.tokenizer.eos_token_id)
        t = Thread(target=self.ov_model.generate, kwargs=generate_kwargs)
        t.start()

        # Pull the generated text from the streamer, and update the model output.
        model_output = ""
        for new_text in streamer:
            model_output += new_text
            yield model_output
        return model_output
