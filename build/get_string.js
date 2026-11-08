const fs=require('fs');const [tool,lang,key]=process.argv.slice(2);
if(key.startsWith('faq[')){const d=JSON.parse(fs.readFileSync(`tools/${tool}/faq.json`,'utf8'));const m=key.match(/faq\[(\d+)\]\.(q|a)/);console.log(JSON.stringify(d.items[+m[1]][lang][m[2]]));process.exit(0);}
const src=fs.readFileSync(`tools/${tool}/index.html`,'utf8');let js=src.split('<script>')[1].split('\nlet lang')[0].replace(/\/\*@include [\w.-]+\.js\*\//g,'');
const T=(new Function(js+';return T'))();let v=T[lang];for(const p of key.split(/[.\[\]]+/).filter(Boolean))v=v[p];console.log(JSON.stringify(v));
