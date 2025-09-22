async function callAPI(endpoint, payload){
const res = await fetch(endpoint, {
method: 'POST',
headers: {'Content-Type':'application/json'},
body: JSON.stringify(payload)
});
return res.json();
}


document.querySelectorAll('.run-btn').forEach(btn => {
btn.addEventListener('click', async e => {
const task = btn.dataset.task;
if(task === 'summarize'){
const text = document.getElementById('input-summarize').value;
const max_length = document.getElementById('sum-max').value;
const min_length = document.getElementById('sum-min').value;
document.getElementById('out-summarize').textContent = 'Processing...';
const data = await callAPI('/api/summarize', {text, max_length, min_length});
document.getElementById('out-summarize').textContent = data.error || data.result || JSON.stringify(data);
} else if(task === 'paraphrase'){
const text = document.getElementById('input-paraphrase').value;
const num = document.getElementById('par-num').value;
document.getElementById('out-paraphrase').textContent = 'Processing...';
const data = await callAPI('/api/paraphrase', {text, num_return_sequences: num});
if(data.result){
if(Array.isArray(data.result)){
document.getElementById('out-paraphrase').textContent = data.result.join('\n\n---\n\n');
} else document.getElementById('out-paraphrase').textContent = data.result;
}