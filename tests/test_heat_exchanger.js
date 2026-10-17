const {load,near,summary}=require('./harness');
const c=load('heat exchanger calculator.html');
if(c.__loadError)console.log('load:',c.__loadError);
// Default temperatures 180 -> 100 C hot, 30 -> 90 C cold: P = 0.4, R = 1.333
near('F 1-2 shell (Bowman)',c.psaFshell(0.4,4/3,1),0.857,0.003);
// Two shell passes raise F above one shell for the same duty
console.log('2 shells > 1 shell:',c.psaFshell(0.4,4/3,2)>c.psaFshell(0.4,4/3,1));
// R = 1 limit continuity
near('R = 1 continuity',c.psaFshell(0.4,1,1),c.psaFshell(0.4,1.0001,1),1e-3);
summary();
