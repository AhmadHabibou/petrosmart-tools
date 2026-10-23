const {load,near,summary}=require('./harness');
const fs=require('fs'),path=require('path');
const c=load('cetane_index_calculator.html');
if(c.__loadError)console.log('load:',c.__loadError);
// ASTM D976: CI = 454.74 - 1641.416 D + 774.74 D^2 - 0.554 B + 97.803 (log B)^2, D g/mL at 15 C, B mid-boiling point C
const D=0.835,B=265, ci976=454.74-1641.416*D+774.74*D*D-0.554*B+97.803*Math.pow(Math.log10(B),2);
const src=fs.readFileSync(path.join(__dirname,'..','cetane_index_calculator.html'),'utf8');
console.log('D976 constants present:',/454\.74/.test(src)&&/1641\.416/.test(src)&&/97\.803/.test(src),'| reference CI =',ci976.toFixed(2));
console.log('no generic improver curve:',!/addDose\*35/.test(src));
summary();
