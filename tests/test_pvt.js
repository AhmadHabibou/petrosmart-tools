const {load,near,summary}=require('./harness');
const c=load('reservoir fluid pvt calculator.html');
if(c.__loadError)console.log('load:',c.__loadError);
const T=93.33, API=35, gg=0.75, TF=200, TR=659.67, go=141.5/(API+131.5), Rs=600;
// Inversion checks against the published bubble-point forms (Rs at p = pb must return Rs)
const pbStanding=18.2*(Math.pow(Rs/gg,0.83)*Math.pow(10,0.00091*TF-0.0125*API)-1.4);
near('Standing Rs(pb)',c.Rs_standing(pbStanding/14.5038,T,API,gg),Rs,0.002);
const pbVB=Math.pow(Rs/(0.0178*gg*Math.exp(23.931*API/TR)),1/1.1870);
near('Vasquez-Beggs Rs(pb)',c.Rs_vasquez(pbVB/14.5038,T,API,gg),Rs,0.002);
const pbAM=5.38088e-3*Math.pow(Rs,0.715082)*Math.pow(gg,-1.87784)*Math.pow(go,3.1437)*Math.pow(TR,1.32657);
near('Al-Marhoun Rs(pb)',c.Rs_almarhoun(pbAM/14.5038,T,API,gg),Rs,0.002);
const x=Math.pow(Rs/gg,0.816)*Math.pow(TF,0.172)/Math.pow(API,0.989),lx=Math.log10(x);
const pbG=Math.pow(10,1.7669+1.7447*lx-0.30218*lx*lx);
near('Glaso Rs(pb)',c.Rs_glaso(pbG/14.5038,T,API,gg),Rs,0.002);
// Bo values must agree within about 5 % across correlations for an ordinary black oil
const bs=c.Bo_standing(Rs,T,API,gg);
['Bo_vasquez','Bo_almarhoun','Bo_glaso'].forEach(k=>near(k+' vs Standing',c[k](Rs,T,API,gg),bs,0.05));
// Vasquez-Beggs co sign: positive for ordinary oil
console.log('co positive:',c.co_vasquez(Rs,T,API,gg,300)>0);
// Z-factor: Standing-Katz chart Tpr 1.5, Ppr 2.0 ~ 0.825 (gas with gg 0.7)
const Tpc=168+325*0.7-12.5*0.49,Ppc=677+15*0.7-37.5*0.49;
const Tc=(1.5*Tpc)/1.8-273.15,Pb=2*Ppc/14.5038;
['hy','papay','bk'].forEach(m=>near('Z '+m+' (SK chart 0.825)',c.calcZ(Pb,Tc,0.7,0,0,0,m),0.825,0.03));
// McCain water: Bw 200 F, 5000 psia ~ 1.028 (recomputed); viscosity pure water 200 F ~ 0.29 cP (McCain), steam tables 0.305
c.__els['fp_P']={value:String(5000/14.5038)};c.__els['fp_T']={value:'93.333'};c.__els['fp_sal']={value:'0'};
c.calcFluid();
const h=c.__els.r4?c.__els.r4.innerHTML:'';
const bw=(h.match(/Water Bw \(McCain\)<\/div><div[^>]*>([\d.]+)/)||[])[1];
near('Bw McCain',parseFloat(bw),1.0281,0.001);
summary();
