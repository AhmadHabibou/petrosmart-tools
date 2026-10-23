const {load,near,summary}=require('./harness');
const c=load('hydrostatic_pressure_calculator.html');
if(c.__loadError)console.log('load:',c.__loadError);
// Gradient of fresh water: 1000 kg/m3 -> 0.0981 bar/m, 0.4335 psi/ft
near('water gradient bar/m',c.rhoToGrad(1000),0.0981,1e-3);
near('water gradient psi/ft',c.rhoToGradPsi(1000),0.4335,1e-3);
// Barite: 1200 -> 1500 kg/m3 with barite 4200 kg/m3: 4200 x 300 / 2700 = 466.7 kg per m3 of initial mud
near('barite kg/m3',4200*(1500-1200)/(4200-1500),466.7,1e-3);
summary();
