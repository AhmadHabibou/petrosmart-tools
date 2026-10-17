const {load,near,summary}=require('./harness');
const c=load('separator sizing calculator.html');
if(c.__loadError)console.log('load:',c.__loadError);
// Standard conditions: Sm3 at 15 C and 1.01325 bar (ISO 13443); actual flow = Q x Z x T/288.15 x 1.01325/P
const s=require('fs').readFileSync(require('path').join(__dirname,'..','separator sizing calculator.html'),'utf8');
console.log('uses 288.15 K:',(s.match(/T_K\/288\.15\*\(1\.01325\/P_abs\)/g)||[]).length===4,'| no 273.15 basis:',!/T_K\/273\.15/.test(s));
summary();
