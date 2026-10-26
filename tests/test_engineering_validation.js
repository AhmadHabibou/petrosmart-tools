const assert=require('assert');
const {load,near,summary}=require('./harness');
function cards(c,fn){const out={};c.rc=(cls,label,value,unit,sub)=>{out[label]={value,unit,sub};return '';};c[fn]();return out;}
let c=load('hydrostatic_pressure_calculator.html',{rho1:1000,h1:100,p01:0,g1:1.62});
let r=cards(c,'calc1');near('entered gravity used in pressure',+r['Hydrostatic pressure'].value,1.62,1e-6);near('entered gravity used in gradient',+r['Pressure gradient'].value,.0162,1e-6);
c=load('hydrostatic_pressure_calculator.html',{h1:-100});r=cards(c,'calc1');assert(!r['Hydrostatic pressure']);assert(/No result/.test(c.__els.r1.innerHTML));
c=load('hydrostatic_pressure_calculator.html',{rho1:''});r=cards(c,'calc1');assert(!r['Hydrostatic pressure']);
c=load('pipe_wall_thickness_calculator.html',{P:80,OD:219.1,S:138,E:1,W:.5,Y:.4,c1:3,mill:12.5});r=cards(c,'calc1');near('W included in inverse pressure equation',+r['Formula pressure capacity'].value,85.80453051485739,.001);
c=load('pipe_wall_thickness_calculator.html',{P:80,OD:219.1,S:138,E:1,W:1,Y:.4,c1:3,mill:12.5});r=cards(c,'calc1');near('flow area cm2',+r['Flow area'].value,Math.PI*(219.1-2*12.7)**2/400,.0001);
assert.strictEqual(c.findNextSch(8,100),null);assert.strictEqual(c.findNextSch(null,10),null);
for(const overrides of [{P:''},{S:0},{W:0},{mill:100},{OD:-1},{P:5000}]){c=load('pipe_wall_thickness_calculator.html',overrides);r=cards(c,'calc1');assert(!r['Required t (calc)']);assert(/No result/.test(c.__els.r1.innerHTML));}
c=load('pipe_wall_thickness_calculator.html',{p2_W:.5});r=cards(c,'calc2');const half=+r['Formula pressure capacity'].value;c=load('pipe_wall_thickness_calculator.html',{p2_W:1});r=cards(c,'calc2');near('pressure panel respects W',half,+r['Formula pressure capacity'].value/2,.002);
c=load('pipe_wall_thickness_calculator.html',{h_OD:200,h_t:20,h_P:100,h_SMYS:241,h_df:.72,h_F:0});r=cards(c,'calc3');const sh=10*(80**2+100**2)/(100**2-80**2),sl=10*80**2/(100**2-80**2),sr=-10,vm=Math.sqrt(((sh-sl)**2+(sl-sr)**2+(sr-sh)**2)/2);near('three-principal-stress von Mises',+r['Inner-wall von Mises stress'].value,vm,.0001);
console.log('PASS invalid input, missing schedule and blank input rejection assertions');summary();
