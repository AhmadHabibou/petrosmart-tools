const {load,near,summary}=require('./harness');
const c=load('pipe_wall_thickness_calculator.html');
if(c.__loadError)console.log('load:',c.__loadError);
// ASME B31.3 eq. (3a): t = P D / (2 (S E W + P Y)); A106 B S = 138 MPa (20 ksi) at ambient
c.calc1();
const h=c.__els.r1.innerHTML;
const t=parseFloat(h.match(/Required t \(calc\)<\/div><div[^>]*>([\d.]+)/)[1]);
near('t_calc 6 in, 100 bar, A106 B',t,10*168.3/(2*(138+10*0.4)),0.001);
console.log('schedule:',h.match(/Recommended schedule<\/div><div[^>]*>([^<]+)/)[1].trim(),'(expected Sch 80, 10.97 mm)');
// ASME B36.10M spot checks
const s20=c.npsData[20].schs.find(x=>x.n==='Sch 40').t, s12=c.npsData[12].schs.find(x=>x.n==='Sch 80').t;
near('20 in Sch 40 wall mm',s20,15.09,1e-6);near('12 in Sch 80 wall mm',s12,17.48,1e-6);
const a106=c.materials[0];near('A106 B allowable = min(SMTS/3, 2/3 SMYS)',a106.S,Math.min(a106.smts/3,2*a106.smys/3),0.01);
summary();
