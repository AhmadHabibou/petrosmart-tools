const {load,near,summary}=require('./harness');
const c=load('cementing calculator.html');
if(c.__loadError)console.log('load:',c.__loadError);
// API 10A Class G, 44% water, SG 3.15: 15.8 ppg (1.89 g/cm3), yield 1.15 ft3/sack = 32.6 L
const g=c.psaSlurry(3.15,0.44,2.65,0,94);
near('Class G density g/cm3 (15.8 ppg rounded)',g.rho,1.893,0.01);
near('Class G yield L/sack (1.15 ft3)',g.yieldSack,1.15*28.317,0.01);
// Class H 38%: 16.4 ppg = 1.97 g/cm3, 1.06 ft3/sack
const h=c.psaSlurry(3.15,0.38,2.65,0,94);
near('Class H density',h.rho,1.97,0.005);
near('Class H yield',h.yieldSack,1.06*28.317,0.01);
// Shoe pressure: 700 m of 1.89 slurry under 1,800 m of 1.25 mud
c.calcECD();
const m=c.__els.r3.innerHTML.match(/BHP at shoe \(end of job\)<\/div><div[^>]*>([\d.]+)/);
near('static pressure at shoe bar',parseFloat(m?m[1]:'NaN'),0.0980665*(parseFloat(c.__els['ecd-cem'].value)*700+1.25*1800),0.002);
// Volume: no previous casing, 311.2 mm hole, 244.5 mm casing, 700 m, excess 1.35, shoe track 40 m of 220.5 mm ID
c.calcVol();
const vann=Math.PI/4*(311.2**2-244.5**2)/1e6*1.35*700, vst=Math.PI/4*0.2205**2*40;
const mv=c.__els.r2.innerHTML.match(/Cement volume \(annulus \+ shoe track\)<\/div><div[^>]*>([\d.]+)/);
near('cement volume m3',parseFloat(mv?mv[1]:'NaN'),vann+vst,0.005);
summary();
