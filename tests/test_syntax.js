// Every inline script of every page must parse.
const fs=require('fs'),path=require('path'),vm=require('vm');
let bad=0;
for(const f of fs.readdirSync(path.join(__dirname,'..')).filter(f=>f.endsWith('.html'))){
  const s=fs.readFileSync(path.join(__dirname,'..',f),'utf8');
  [...s.matchAll(/<script>([\s\S]*?)<\/script>/g)].forEach((m,i)=>{try{new vm.Script(m[1])}catch(e){bad++;console.log('FAIL',f,'script',i,e.message)}});
}
console.log(bad?bad+' syntax errors':'all scripts parse');process.exitCode=bad?1:0;
