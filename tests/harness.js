// Loads the inline scripts of a calculator page into a sandbox with a minimal DOM stub.
const fs=require('fs'),vm=require('vm'),path=require('path');
function load(file,overrides){
  const html=fs.readFileSync(path.join(__dirname,'..',file),'utf8');
  const vals={};
  for(const m of html.matchAll(/<input[^>]*id="([^"]+)"[^>]*value="([^"]*)"/g))vals[m[1]]=m[2];
  for(const m of html.matchAll(/<input[^>]*value="([^"]*)"[^>]*id="([^"]+)"/g))if(!(m[2] in vals))vals[m[2]]=m[1];
  for(const m of html.matchAll(/<select[^>]*id="([^"]+)"[^>]*>([\s\S]*?)<\/select>/g)){
    const sel=m[2].match(/<option[^>]*value="([^"]*)"[^>]*selected/)||m[2].match(/<option[^>]*value="([^"]*)"/);
    if(sel)vals[m[1]]=sel[1];}
  Object.assign(vals,overrides||{});
  const els={};
  const el=id=>els[id]||(els[id]={id,value:vals[id]!==undefined?vals[id]:'',innerHTML:'',textContent:'',style:{},checked:false,
    classList:{add(){},remove(){},toggle(){},contains(){return false}},setAttribute(){},getContext(){return{}},
    appendChild(){},querySelectorAll(){return[]},querySelector(){return null},addEventListener(){},options:[],selectedIndex:0});
  const document={getElementById:el,querySelectorAll:()=>[],querySelector:()=>null,addEventListener(){},createElement:()=>el('_tmp'+Math.random()),body:el('body')};
  const ctx={document,window:{},console,Math,Chart:function(){return{destroy(){},update(){}}},setTimeout:()=>0,
    navigator:{},localStorage:{getItem(){return null},setItem(){}},alert(){},parseFloat,parseInt,isNaN,Number,String,Array,Object,JSON};
  ctx.window=ctx;vm.createContext(ctx);
  const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
  for(const s of scripts){try{vm.runInContext(s,ctx)}catch(e){ctx.__loadError=(ctx.__loadError||'')+e.message+'\n'}}
  ctx.__els=els;return ctx;
}
let fails=0,passes=0;
function near(name,got,exp,tol){const ok=Math.abs(got-exp)<=Math.abs(exp)*tol+1e-12;
  console.log((ok?'PASS ':'FAIL ')+name+': got '+(+got).toPrecision(6)+', expected '+exp+' (tol '+(tol*100)+'%)');ok?passes++:fails++;}
function summary(){console.log(`\n${passes} pass, ${fails} fail`);process.exitCode=fails?1:0;}
module.exports={load,near,summary};
