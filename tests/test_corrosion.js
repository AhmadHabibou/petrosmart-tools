const {load,near,summary}=require('./harness');
const c=load('corrosion rate calculator.html');
if(c.__loadError)console.log('load:',c.__loadError);
// de Waard-Milliams nomogram equation at 60 C, 1 bar CO2: log V = 5.8 - 1710/333.15 = 0.667 -> 4.65 mm/yr
const r=c.psaDWM(1e-9,1,60,0);
near('base rate 60 C, 1 bar',r.V,Math.pow(10,5.8-1710/333.15),1e-6);
// scale factor equals 1 below the scaling temperature: log Fs = 2400/T - 6.7 at fCO2 = 1 -> T_scale = 358 K (85 C)
near('Fs at 60 C, 1 bar',r.Fs,1,1e-9);
near('Fs at 100 C, 1 bar',c.psaDWM(1e-9,1,100,0).Fs,Math.pow(10,2400/373.15-6.7),1e-6);
// glycol: 50 % glycol -> W = 50 -> Fg = 10^(1.6 (log 50 - 2)) = 0.330
near('glycol factor 50 %',c.psaDWM(1e-9,1,60,50).Fg,Math.pow(10,1.6*(Math.log10(50)-2)),1e-6);
// API RP 14E: C = 100, rho = 1000 kg/m3 (62.43 lb/ft3): Ve = 100/sqrt(62.43) = 12.66 ft/s = 3.86 m/s
near('erosional velocity m/s',c.psaVe(100,1000),100/Math.sqrt(62.428)*0.3048,1e-3);
// ASTM E140: 22 HRC ~ 248 HV
near('22 HRC to HV',c.psaHRCtoHV(22),248,0.01);
// Barlow pressure limit, 168.3 mm, 6.0 mm, SMYS 241 MPa, F 0.72: 2*241*0.72*6/168.3 = 12.37 MPa = 123.7 bar
c.__els['t_meas']={value:'6.0'};c.__els['yrs_since']={value:'0'};
c.calcLife();
const m=c.__els.r3.innerHTML.match(/Pressure limit with current t<\/div><div[^>]*>([\d.]+)/);
near('pressure limit bar',parseFloat(m?m[1]:'NaN'),2*241*0.72*6/168.3*10,0.01);
summary();
