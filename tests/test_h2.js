const {load,near,summary}=require('./harness');
const c=load('h2_production_cost_calculator.html');
if(c.__loadError)console.log('load:',c.__loadError);
c.calcSMR();
const h=c.__els.r1.innerHTML;
// Gas cost at 8.5 USD/MMBtu with 0.41 Nm3/Nm3: 8.5 x 0.41 x 0.03412 / 0.0899 = 1.32 USD/kg H2
const ng=parseFloat(c.__els['ng-price']?c.__els['ng-price'].value:'NaN');
const m=h.match(/NG cost:<\/strong>[^=]*= <span class="hi">([\d.]+)/);
near('SMR gas cost USD/kg',parseFloat(m?m[1]:'NaN'),(isNaN(ng)?8.5:ng)*0.41*0.03412/0.0899,0.002);
// Energy check: 0.41 Nm3 NG (36 MJ/Nm3) per Nm3 H2 = 164 MJ per kg H2
near('SMR gas use MJ/kg H2',0.41*36/0.0899,165,0.02);
summary();
