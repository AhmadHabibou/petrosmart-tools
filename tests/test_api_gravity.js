const {load,near,summary}=require('./harness');
const c=load('api_gravity_calculator.html');
if(c.__loadError)console.log('load:',c.__loadError);
near('water SG 1.000 -> 10 API',c.toAPI(1.0),10,1e-9);
near('35 API -> SG',c.toSG(35),0.8498,1e-4);
console.log('30 API is Medium:',c.cls(30).l==='Medium','| 32 API is Light:',c.cls(32).l==='Light','| 20 API is Heavy:',c.cls(20).l==='Heavy');
summary();
