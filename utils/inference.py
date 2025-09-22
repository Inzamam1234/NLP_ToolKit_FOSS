import torch
from transformers import T5ForConditionalGeneration, T5TokenizerFast
import threading


class T5Inference:
def __init__(self, model_dir_or_id: str):
self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
self.lock = threading.Lock()
self.tokenizer = T5TokenizerFast.from_pretrained(model_dir_or_id)
self.model = T5ForConditionalGeneration.from_pretrained(model_dir_or_id).to(self.device)
self.model.eval()


def _generate(self, input_text, max_length=150, min_length=5, num_return_sequences=1, **gen_kwargs):
# Keep model calls thread-safe
with self.lock:
inputs = self.tokenizer(input_text, return_tensors='pt', truncation=True, padding='longest').to(self.device)
out = self.model.generate(
**inputs,
max_length=max_length,
min_length=min_length,
num_return_sequences=num_return_sequences,
early_stopping=True,
do_sample=False,
**gen_kwargs
)
outputs = [self.tokenizer.decode(ids, skip_special_tokens=True, clean_up_tokenization_spaces=True) for ids in out]
return outputs if num_return_sequences > 1 else outputs[0]


def run_task(self, text: str, task: str = 'summarize', **kwargs):
# You can adjust prefixes based on how you fine-tuned the model.
# Example prefixes: "summarize:", "paraphrase:", "grammar:"
prefix_map = {
'summarize': 'summarize: ',
'paraphrase': 'paraphrase: ',
'grammar': 'grammar: '
}
prefix = prefix_map.get(task, '')
input_text = prefix + text.strip()


# sensible defaults
if task == 'summarize':
max_length = kwargs.get('max_length', 150)
min_length = kwargs.get('min_length', 20)
return self._generate(input_text, max_length=max_length, min_length=min_length, **kwargs)
elif task == 'paraphrase':
n = kwargs.get('num_return_sequences', 1)
return self._generate(input_text, max_length=256, min_length=5, num_return_sequences=n, num_beams=4)
elif task == 'grammar':
return self._generate(input_text, max_length=256, min_length=1, num_return_sequences=1)
else:
return self._generate(input_text, **kwargs)