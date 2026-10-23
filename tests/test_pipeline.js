const {load,near,summary}=require('./harness');
const c=load('pipeline pressure drop calculator.html');
if(c.__loadError)console.log('load:',c.__loadError);
// Default case: 500 mm, 100 km, 5 million Sm3/d, 70 bar(a), 15 C, gas gravity 0.65
const o={Q:5e6,P1:70,D:0.5,L:1e5,T:288.15,g:0.65,eps:0.046e-3,dz:0,E:0.92};
const g=c.psaGasLine(o,'gfe');
// Independent recomputation of the isothermal equation with the same Z, f
const R=8314.46,M=28.97*0.65,rho_sc=1.01325e5*M/(R*288.15),G=5e6/86400*rho_sc/(Math.PI/4*0.25);
const P2=Math.sqrt((7e6)**2-g.f*1e5*g.Z*R*288.15*G*G/(0.5*M))/1e5;
near('general flow equation P2',g.P2,P2,1e-3);
// Weymouth and Panhandle A bracket the general flow equation within about 5 %
near('Weymouth vs GFE',c.psaGasLine(o,'wey').P2,g.P2,0.05);
near('Panhandle A vs GFE',c.psaGasLine(o,'pa').P2,g.P2,0.06);
// Colebrook: Re 1e5, smooth -> f = 0.0180 (Moody chart)
near('Colebrook smooth Re 1e5',c.frictionFactor(1e5,0),0.0180,0.01);
// Elevation: uphill must lower P2
console.log('uphill lowers P2:',c.psaGasLine(Object.assign({},o,{dz:500}),'gfe').P2<g.P2);
summary();
