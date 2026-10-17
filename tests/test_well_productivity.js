const {load,near,summary}=require('./harness');
const c=load('well productivity calculator.html');
if(c.__loadError)console.log('load:',c.__loadError);
// Standing-Katz chart readings (Standing and Katz, 1942) via DAK
const pc=c.psaPseudoCrit(0.65);
near('Z Tpr 1.5 Ppr 2.0',c.psaZ(1.5*pc.Tpc,2*pc.Ppc,0.65),0.825,0.01);
near('Z Tpr 1.2 Ppr 1.0',c.psaZ(1.2*pc.Tpc,1*pc.Ppc,0.65),0.780,0.01);
// Lee-Gonzalez-Eakin worked example (Ahmed, Reservoir Engineering Handbook): 0.0173 cP
near('mu_g LGE 600 R 2000 psia g 0.72 Z 0.78',c.psaMuGas(600,2000,0.72,0.78),0.0173,0.01);
// Low-pressure check: pseudo-pressure tends to p^2/(mu Z) when Z~1, mu~const
const T=(60*1.8+491.67),m=c.psaPseudoP(100,T,0.6),Z=c.psaZ(T,50,0.6),mu=c.psaMuGas(T,50,0.6,Z);
near('m(p) ~ p^2/(mu Z) at 100 psia',m,100*100/(mu*Z),0.01);
// Default case: independent pressure-squared estimate at average pressure must be within ~10%
const r=c.psaGasRate({Pr:300,Pwf:100,T_C:120,g:0.65,k:20,h:25,re:600,rw:0.108,S:3});
near('net pay ft',r.h_ft,82.021,0.001);
const pa=(r.Pr+r.Pwf)/2,Za=c.psaZ(r.T_R,pa,0.65),mua=c.psaMuGas(r.T_R,pa,0.65,Za);
near('q vs p^2 at average pressure',r.q,20*r.h_ft*(r.Pr**2-r.Pwf**2)/(1422*r.T_R*mua*Za*(Math.log(600/0.108)-0.75+3)),0.10);
c.calcGas();
console.log('render ok:',/Mscf\/d/.test(c.__els.r3.innerHTML));
summary();
