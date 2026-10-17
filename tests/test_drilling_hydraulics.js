const {load,near,summary}=require('./harness');
const c=load('drilling hydraulics calculator.html');
if(c.__loadError)console.log('load:',c.__loadError);
// Bourgoyne et al. (1986) Example 4.20-type check, recomputed independently:
// 5 in DP (ID 4.276 in), q 335 gpm, 10 ppg, PV 15 cP, YP 10: turbulent, dp/dL = rho^.75 v^1.75 PV^.25/(1800 d^1.25)
const v=335/(2.448*4.276**2);
near('pipe velocity ft/s',c.psaBPpipeField(335,4.276,1,15,10,10).v,v,1e-9);
near('pipe turbulent psi/ft',c.psaBPpipeField(335,4.276,1,15,10,10).dP,10**0.75*v**1.75*15**0.25/(1800*4.276**1.25),1e-9);
// Laminar annulus: 8.5 x 5 in, 100 gpm, 9 ppg, PV 20, YP 15
const va=100/(2.448*(8.5**2-5**2)),r=c.psaBPannField(100,8.5,5,1000,20,15,9);
console.log('annulus laminar:',r.lam);
near('annulus laminar psi/1000 ft',r.dP,1000*(20*va/(1000*3.5**2)+15/(200*3.5)),1e-9);
// Bit: 3 x 12/32 nozzles, 400 gpm, 12 ppg -> dP = 8.311e-5*12*400^2/(0.95^2*At^2)
const At=3*Math.PI/4*(12/32)**2;
near('bit dP psi',c.psaBit(400,At,12).dP,8.311e-5*12*160000/(0.9025*At*At),1e-9);
near('bit HHP',c.psaBit(400,At,12).HHP,c.psaBit(400,At,12).dP*400/1714,1e-9);
// ECD unit check: 1.30 g/cm3 at 3500 m with 120 psi APL -> 1.30 + 120/(1.42233*3500)
c.calcECD();
const m=c.__els.r3.innerHTML.match(/ECD \(circulating\)<\/div><div[^>]*>([\d.]+)/);
near('ECD g/cm3',parseFloat(m?m[1]:'NaN'),1.30+120/(1.42233*3500),1e-3);
// Static BHP 1.30 g/cm3 x 3500 m = 446.2 bar = 6471 psi
near('static BHP psi',1.30*1.42233*3500,6471.6,1e-3);
c.calcDS();c.calcAnn();c.calcBit();c.calcPump();
console.log('renders:',['r1','r2','r4','r5'].every(k=>c.__els[k].innerHTML.length>100));
summary();
