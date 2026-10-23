const {load,near,summary}=require('./harness');
const c=load('compressor power calculator.html');
if(c.__loadError)console.log('load:',c.__loadError);
c.calcComp();
const h=c.__els.r1.innerHTML;
// Defaults: methane, k 1.307, Z 0.98, 5 -> 25 bar(a), 35 C, 10 kg/s, eta_p 82 %
const R=8314/16.04,T1=308.15,r=5,k=1.307,ep=0.82,m=k/(k-1)*ep,n=m/(m-1);
const Hp=0.98*R*T1*(n/(n-1))*(Math.pow(r,(n-1)/n)-1);
const wp=parseFloat(h.match(/Polytropic shaft power<\/div><div[^>]*>([\d.]+)/)[1]);
near('polytropic gas power kW = m Hp / eta_p',wp,10*Hp/ep/1000,0.001);
// Inlet actual flow: rho = P M /(Z R T) = 5e5 x 16.04 /(0.98 x 8314 x 308.15) = 3.194 kg/m3 -> 11,271 m3/h
const q=parseFloat(h.match(/Actual inlet flow<\/div><div[^>]*>([\d.]+)/)[1]);
near('inlet actual flow m3/h',q,10/(5e5*16.04/(0.98*8314*308.15))*3600,0.001);
summary();
